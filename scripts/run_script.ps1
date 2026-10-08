#!/usr/bin/env pwsh
# ============================================================
# OrbisERP Script Runner
# Usage: .\run_script.ps1 <step_number>
# Example: .\run_script.ps1 1
# ============================================================

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("1","2","3","4","5","6","7","8","9","10","all")]
    [string]$Step
)

$CONTAINER = "frappe_docker-backend-1"
$SITE      = "frontend"

# Folder where this script lives (e:\erpnext\scripts)
$LOCAL_SCRIPTS = Split-Path -Parent $MyInvocation.MyCommand.Path

function Run-Step {
    param([string]$num)

    $found = Get-ChildItem -Path $LOCAL_SCRIPTS -Filter "step${num}_*.py" | Select-Object -First 1
    if (-not $found) {
        Write-Host "ERROR: Could not find step${num}_*.py in $LOCAL_SCRIPTS" -ForegroundColor Red
        return
    }

    $localFile = $found.FullName
    $filename  = $found.Name

    Write-Host "`n>>> Copying $filename into container ..." -ForegroundColor Cyan
    docker cp $localFile "${CONTAINER}:/tmp/${filename}"

    Write-Host ">>> Running $filename inside ERPNext ..." -ForegroundColor Cyan

    $pyCode = @"
import sys
sys.path.insert(0, '/home/frappe/frappe-bench/apps/frappe')
sys.path.insert(0, '/home/frappe/frappe-bench/apps/erpnext')
import frappe
frappe.init(site='$SITE', sites_path='/home/frappe/frappe-bench/sites')
frappe.connect()
import importlib.util
spec = importlib.util.spec_from_file_location('step_script', '/tmp/$filename')
mod  = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
if hasattr(mod, 'run'):
    result = mod.run()
elif hasattr(mod, 'run_branding_setup'):
    result = mod.run_branding_setup()
elif hasattr(mod, 'setup_login_ui'):
    result = mod.setup_login_ui()
elif hasattr(mod, 'main'):
    result = mod.main()
else:
    result = 'Done'
frappe.db.commit()
print('RESULT:', result)
frappe.destroy()
"@

    docker exec $CONTAINER /home/frappe/frappe-bench/env/bin/python -c $pyCode

    Write-Host "`n>>> $filename execution finished." -ForegroundColor Green
}

if ($Step -eq "all") {
    foreach ($n in @("1","2","3","4","5","6","7","8","9","10")) {
        Run-Step $n
    }
} else {
    Run-Step $Step
}
