# Define the dist folder path
$DIST_FOLDER = "dist"

# Check if the dist folder exists
if (Test-Path $DIST_FOLDER) {
    # Remove everything inside the dist folder
    Write-Host "Removing all contents from $DIST_FOLDER..."
    Remove-Item -Path $DIST_FOLDER -Recurse -Force
}

# Create a new empty dist folder
New-Item -Path $DIST_FOLDER -ItemType Directory -Force | Out-Null

# Run the setup.py commands
Write-Host "Running python setup.py sdist bdist_wheel..."
python setup.py sdist bdist_wheel

# Check if the setup.py command was successful
if ($LastExitCode -ne 0) {
    Write-Host "Failed to create distribution packages."
    exit $LastExitCode
}

Write-Host "Build successful."
