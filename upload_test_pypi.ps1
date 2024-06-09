# Call the rebuild script
./rebuild.ps1

# Check if the rebuild script was successful
if ($LastExitCode -ne 0) {
    Write-Host "Rebuild failed. Exiting."
    exit $LastExitCode
}

# Define the dist folder path
$DIST_FOLDER = "dist"

# Check if the TWINE_TESTPYPI_PASSWORD environment variable is set
if (-not $env:TWINE_TESTPYPI_PASSWORD) {
    Write-Host "TWINE_TESTPYPI_PASSWORD environment variable is not set."
    exit 1
}

# Upload to TestPyPi using twine
Write-Host "Uploading to TestPyPi using twine..."
twine upload --repository-url https://test.pypi.org/legacy/ -u __token__ -p $env:TWINE_TESTPYPI_PASSWORD "$DIST_FOLDER/*"

# Check if the twine command was successful
if ($LastExitCode -ne 0) {
    Write-Host "Failed to upload to TestPyPi."
    exit $LastExitCode
}

Write-Host "Upload to TestPyPi successful."