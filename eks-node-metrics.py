import time
from kubernetes import client, config
from rich.live import Live
from rich.table import Table
from rich.text import Text
from rich import box
import re

CPU_RE = re.compile(r"^(\d+)(n|u|m)?$")
MEM_RE = re.compile(r"^(\d+)(Ki|Mi|Gi)?$")

def parse_cpu_to_cores(cpu: str) -> float:
    m = CPU_RE.match(cpu.strip())
    if not m:
        return 0.0
    val = int(m.group(1))
    unit = m.group(2)
    if unit == "n":
        return val / 1_000_000_000
    if unit == "u":
        return val / 1_000_000
    if unit == "m":
        return val / 1000
    return float(val)

def parse_mem_to_bytes(mem: str) -> float:
    m = MEM_RE.match(mem.strip())
    if not m:
        return 0.0
    val = int(m.group(1))
    unit = m.group(2)
    if unit == "Ki":
        return val * 1024
    if unit == "Mi":
        return val * 1024**2
    if unit == "Gi":
        return val * 1024**3
    return float(val)

def bytes_fmt(b: float) -> str:
    # simples e suficiente
    for unit in ["B","KiB","MiB","GiB","TiB"]:
        if b < 1024:
            return f"{b:.1f}{unit}"
        b /= 1024
    return f"{b:.1f}PiB"

def bar(pct: float, width: int = 18) -> Text:
    pct = max(0.0, min(100.0, pct))
    filled = int((pct / 100.0) * width)
    empty = width - filled

    color = "green"
    if pct >= 85:
        color = "red"
    elif pct >= 60:
        color = "yellow"

    t = Text()
    t.append("█" * filled, style=color)
    t.append("░" * empty, style="grey50")
    t.append(f" {pct:5.1f}%")
    return t

def make_table(rows, title: str) -> Table:
    table = Table(title=title, box=box.SIMPLE_HEAVY)
    table.add_column("Node", no_wrap=True)
    table.add_column("CPU (used/alloc)", justify="right")
    table.add_column("CPU %", justify="left")
    table.add_column("Mem (used/alloc)", justify="right")
    table.add_column("Mem %", justify="left")
    table.add_column("Pods", justify="right")

    for r in rows:
        table.add_row(
            r["node"],
            f'{r["cpu_used"]:.2f} / {r["cpu_alloc"]:.2f}',
            bar(r["cpu_pct"]),
            f'{bytes_fmt(r["mem_used"])} / {bytes_fmt(r["mem_alloc"])}',
            bar(r["mem_pct"]),
            str(r["pods"]),
        )
    return table

def main(refresh_s: float = 2.0):
    # usa kubeconfig local (ou in-cluster se rodar como pod)
    try:
        config.load_kube_config()
    except Exception:
        config.load_incluster_config()

    core = client.CoreV1Api()
    custom = client.CustomObjectsApi()

    # Cache: capacidade alocável do node (mudam pouco)
    def get_allocatable():
        alloc = {}
        nodes = core.list_node().items
        for n in nodes:
            name = n.metadata.name
            cpu_alloc = parse_cpu_to_cores(n.status.allocatable.get("cpu", "0"))
            mem_alloc = parse_mem_to_bytes(n.status.allocatable.get("memory", "0Ki"))
            alloc[name] = (cpu_alloc, mem_alloc)
        return alloc

    alloc = get_allocatable()

    def render():
        nonlocal alloc
        # se entrar node novo, atualiza alloc
        live_nodes = {n.metadata.name for n in core.list_node().items}
        if set(alloc.keys()) != live_nodes:
            alloc = get_allocatable()

        # métricas por node (metrics-server)
        nm = custom.list_cluster_custom_object(
            group="metrics.k8s.io", version="v1beta1", plural="nodes"
        )

        # contagem de pods por node
        pods = core.list_pod_for_all_namespaces(watch=False).items
        pod_count = {}
        for p in pods:
            if p.spec.node_name:
                pod_count[p.spec.node_name] = pod_count.get(p.spec.node_name, 0) + 1

        rows = []
        for item in nm.get("items", []):
            node = item["metadata"]["name"]
            usage = item["usage"]
            cpu_used = parse_cpu_to_cores(usage.get("cpu", "0"))
            mem_used = parse_mem_to_bytes(usage.get("memory", "0Ki"))
            cpu_alloc, mem_alloc = alloc.get(node, (0.0, 0.0))
            cpu_pct = (cpu_used / cpu_alloc * 100.0) if cpu_alloc > 0 else 0.0
            mem_pct = (mem_used / mem_alloc * 100.0) if mem_alloc > 0 else 0.0

            rows.append({
                "node": node,
                "cpu_used": cpu_used,
                "cpu_alloc": cpu_alloc,
                "cpu_pct": cpu_pct,
                "mem_used": mem_used,
                "mem_alloc": mem_alloc,
                "mem_pct": mem_pct,
                "pods": pod_count.get(node, 0),
            })

        rows.sort(key=lambda r: r["cpu_pct"], reverse=True)
        return make_table(rows, title=f"Node Top (refresh {refresh_s}s)")

    with Live(render(), refresh_per_second=max(1, int(1/refresh_s)), screen=True) as live:
        while True:
            live.update(render())
            time.sleep(refresh_s)

if __name__ == "__main__":
    main(refresh_s=2.0)
