# Call the rebuild script
./rebuild.ps1

# Check if the rebuild script was successful
if ($LastExitCode -ne 0) {
    Write-Host "Rebuild failed. Exiting."
    exit $LastExitCode
}

# Define the dist folder path
$DIST_FOLDER = "dist"

# Check if the TWINE_PYPI_PASSWORD environment variable is set
if (-not $env:TWINE_PYPI_PASSWORD) {
    Write-Host "TWINE_PYPI_PASSWORD environment variable is not set."
    exit 1
}

# Upload to PyPi using twine
Write-Host "Uploading to PyPi using twine..."
twine upload -u __token__ -p $env:TWINE_PYPI_PASSWORD "$DIST_FOLDER/*"

# Check if the twine command was successful
if ($LastExitCode -ne 0) {
    Write-Host "Failed to upload to PyPi."
    exit $LastExitCode
}

Write-Host "Upload to PyPi successful."