# Define the package name
$PACKAGE_NAME = "montecarlocsv"

# Uninstall the previous version of the package if it exists
Write-Host "Uninstalling any previous version of $PACKAGE_NAME..."
python -m pip uninstall -y $PACKAGE_NAME

# Check if the uninstallation was successful
if ($LastExitCode -ne 0) {
    Write-Host "Failed to uninstall the previous version of $PACKAGE_NAME."
    exit $LastExitCode
}

# Install the latest version of the package from PyPi
Write-Host "Installing the latest version of $PACKAGE_NAME from PyPi..."
python -m pip install $PACKAGE_NAME

# Check if the installation was successful
if ($LastExitCode -ne 0) {
    Write-Host "Failed to install the latest version of $PACKAGE_NAME from PyPi."
    exit $LastExitCode
}

Write-Host "Installation of $PACKAGE_NAME from PyPi was successful."