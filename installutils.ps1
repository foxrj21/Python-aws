# -------------------------------------------------
# PowerShell script to install:
# - Visual Studio Code
# - Python
# - VSCode Python extension
# - Useful Python packages
# -------------------------------------------------

Write-Host "Starting installation of VSCode and Python..."

# Check if winget is available
if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
    Write-Error "winget is not installed. Please install App Installer from Microsoft Store."
    exit 1
}

# Install Python via winget
Write-Host "Installing Python..."
winget install -e --id Python.Python.3 -h

# Install Visual Studio Code via winget
Write-Host "Installing Visual Studio Code..."
winget install -e --id Microsoft.VisualStudioCode -h

# Wait a bit for installation to complete
Start-Sleep -Seconds 5

# Ensure python and pip are on PATH
Write-Host "Checking Python installation..."
$pythonVersion = python --version
$pipVersion = pip --version
Write-Host "Python version: $pythonVersion"
Write-Host "pip version: $pipVersion"

# Upgrade pip
Write-Host "Upgrading pip..."
python -m pip install --upgrade pip

# Install useful Python packages
Write-Host "Installing virtualenv..."
pip install virtualenv

Write-Host "Installing pylint (code linter)..."
pip install pylint



# Install VSCode Python extension via command line
Write-Host "Installing VSCode Python extension..."
code --install-extension ms-python.python

Write-Host "Installation complete!"
