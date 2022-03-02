if (($PSVersionTable.PSVersion.Major) -lt 5) {
    Write-Warning "PowerShell 5 or later is required to run this install script."
    Write-Warning "Please upgrade: https://docs.microsoft.com/en-us/powershell/scripting/setup/installing-windows-powershell"
    break
}

# show notification to change execution policy
$allowedExecutionPolicy = @('Unrestricted', 'RemoteSigned', 'Bypass')
if ((Get-ExecutionPolicy).ToString() -notin $allowedExecutionPolicy) {
    Write-Warning "PowerShell requires an execution policy in [$($allowedExecutionPolicy -join ", ")] to run this install script."
    Write-Warning "For example, to set the execution policy to 'RemoteSigned' please run :"
    Write-Warning "'Set-ExecutionPolicy RemoteSigned -scope CurrentUser'"
    break
}

$tempdir = (Join-Path ([IO.Path]::GetTempPath()) ([IO.Path]::GetRandomFileName()))

Write-Host "created tempdir: $tempdir"

$baseUrl = "https://github.com/go-task/task/releases"

try {
    if ($PSVersionTable.PSEdition -eq "Core") {
        $response = Invoke-WebRequest -Uri "$baseUrl/latest" -MaximumRedirection 0 -ErrorAction:SilentlyContinue -SkipHttpErrorCheck
    } else {
        $response = Invoke-WebRequest -Uri "$baseUrl/latest" -UseBasicParsing -MaximumRedirection 0 -ErrorAction:SilentlyContinue
    }

    $version = Split-Path -Leaf $response.Headers.Location

    if (-not $version) {
        Write-Error "failed to get version"
    }

    Write-Host "found version: $version" -ForegroundColor Green

    $asset = "$baseUrl/download/$version/task_windows_amd64.zip"

    Write-Host "downloading: $asset"

    New-Item -Type Directory -Path $tempdir | Out-Null

    $tmp_zip = (Join-Path $tempdir "task.zip")

    $cl = New-Object Net.WebClient
    $cl.Headers['User-Agent'] = 'System.Net.WebClient'
    $cl.DownloadFile($asset, $tmp_zip)

    Expand-Archive -LiteralPath $tmp_zip -DestinationPath $tempdir

    $binDir = Join-Path $HOME ".local\bin"
    if (-not (Test-Path $binDir)) {
        Write-Host "creating '$binDir'" -ForegroundColor Yellow
        New-Item -Type Directory -Path $binDir | Out-Null
    }

    Move-Item (Join-Path $tempdir "task.exe") $binDir

    $userEnv = [Environment]::GetEnvironmentVariable("Path", [EnvironmentVariableTarget]::User)
    if (-not $userEnv.Contains($binDir)) {
        Write-Host "adding '$binDir' to system path" -ForegroundColor Yellow
        $env:Path = "$binDir;$env:Path"
        [Environment]::SetEnvironmentVariable(
            "Path",
            "$binDir;" + [Environment]::GetEnvironmentVariable("Path", [EnvironmentVariableTarget]::User),
            [EnvironmentVariableTarget]::User
        )
    }

    Write-Host "done!" -ForegroundColor Green
} catch {
    Write-Host "An error occurred while installing: $_"
} finally {
    if (Test-Path $tempdir) {
        Remove-Item -LiteralPath $tempdir -Recurse -Force
    }
}
