$ErrorActionPreference = "Stop"
$FunctionName = "create-invoice-kfc"
$Region = "ap-southeast-2"
$BuildDir = "build"
$ZipFile = "function.zip"

Write-Host "Cleaning up previous build..."
if (Test-Path $BuildDir) { Remove-Item -Recurse -Force $BuildDir }
if (Test-Path $ZipFile) { Remove-Item $ZipFile }

Write-Host "Installing dependencies..."
New-Item -ItemType Directory -Path $BuildDir | Out-Null
pip install reportlab -t $BuildDir --quiet

Write-Host "Packaging $FunctionName..."
Copy-Item "kfc.py" "$BuildDir\"
Compress-Archive -Path "$BuildDir\*" -DestinationPath $ZipFile

Write-Host "Deploying to Lambda..."
aws lambda update-function-code `
    --function-name $FunctionName `
    --zip-file "fileb://$ZipFile" `
    --region $Region

Write-Host "Cleaning up build folder..."
Remove-Item -Recurse -Force $BuildDir

Write-Host "Done. $FunctionName deployed successfully."
