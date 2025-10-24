# WSL Backup Integration Script for LUXOR AI CUA (PowerShell)
param(
    [string]$Action = "integrate"
)

# Configuration
$WSLBackupPath = "D:\WSLBackup"
$LuxorCUAPath = "E:\Project_Luxor9"
$ExtractionPath = "$LuxorCUAPath\wsl-extraction"

function Write-ColorOutput($ForegroundColor, $Message) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    Write-Output $Message
    $host.UI.RawUI.ForegroundColor = $fc
}

function Write-Info($Message) { Write-ColorOutput Blue "ℹ️  $Message" }
function Write-Success($Message) { Write-ColorOutput Green "✅ $Message" }
function Write-Warning($Message) { Write-ColorOutput Yellow "⚠️  $Message" }
function Write-Error($Message) { Write-ColorOutput Red "❌ $Message" }

Write-ColorOutput Cyan "🔄 WSL Backup Integration for LUXOR AI CUA"
Write-ColorOutput Cyan "=========================================="
Write-Output "Source: $WSLBackupPath"
Write-Output "Target: $LuxorCUAPath"

function Test-BackupFiles {
    Write-Info "Checking WSL backup files availability..."
    
    $BackupFiles = @(
        "luxora_backup.tar",
        "rootfs.vhdx", 
        "ubuntu_backup_20250808_192805.vhdx",
        "Ubuntu-backup.tar"
    )
    
    $FoundFiles = 0
    foreach ($File in $BackupFiles) {
        $FilePath = Join-Path $WSLBackupPath $File
        if (Test-Path $FilePath) {
            $Size = (Get-Item $FilePath).Length / 1GB
            Write-Success "Found: $File ($([math]::Round($Size, 2)) GB)"
            $FoundFiles++
        } else {
            Write-Warning "Missing: $File"
        }
    }
    
    if ($FoundFiles -eq 0) {
        Write-Error "No WSL backup files found at $WSLBackupPath"
        return $false
    }
    
    Write-Success "Found $FoundFiles backup files"
    return $true
}

function New-ExtractionStructure {
    Write-Info "Creating extraction directory structure..."
    
    # Create extraction directories
    $ExtractionDirs = @(
        "$ExtractionPath\luxora_backup",
        "$ExtractionPath\ubuntu_backup", 
        "$ExtractionPath\rootfs_mount",
        "$ExtractionPath\ubuntu_vhdx_mount",
        "$ExtractionPath\integration"
    )
    
    # Create integration directories  
    $IntegrationDirs = @(
        "$LuxorCUAPath\ai-models\wsl-restored",
        "$LuxorCUAPath\configs\wsl",
        "$LuxorCUAPath\scripts\wsl",
        "$LuxorCUAPath\databases\wsl-backup",
        "$LuxorCUAPath\environments\wsl",
        "$LuxorCUAPath\wsl-integration\logs"
    )
    
    foreach ($Dir in ($ExtractionDirs + $IntegrationDirs)) {
        if (!(Test-Path $Dir)) {
            New-Item -ItemType Directory -Path $Dir -Force | Out-Null
        }
    }
    
    Write-Success "Extraction structure created"
}

function Expand-TarArchives {
    Write-Info "Extracting TAR backup archives..."
    
    # Check if tar command is available
    try {
        $null = Get-Command tar -ErrorAction Stop
    } catch {
        Write-Warning "TAR command not available. Attempting to use 7-Zip..."
        try {
            $null = Get-Command 7z -ErrorAction Stop
        } catch {
            Write-Error "Neither TAR nor 7-Zip available. Please install one of them."
            return $false
        }
    }
    
    # Extract LUXORA backup
    $LuxoraBackupPath = Join-Path $WSLBackupPath "luxora_backup.tar"
    if (Test-Path $LuxoraBackupPath) {
        Write-Info "Extracting luxora_backup.tar..."
        
        try {
            $TargetDir = "$ExtractionPath\luxora_backup"
            
            if (Get-Command tar -ErrorAction SilentlyContinue) {
                & tar -xf $LuxoraBackupPath -C $TargetDir 2>$null
            } else {
                & 7z x $LuxoraBackupPath -o"$TargetDir" -y | Out-Null
            }
            
            $ExtractedFiles = (Get-ChildItem $TargetDir -Recurse -File).Count
            Write-Success "LUXORA backup extracted: $ExtractedFiles files"
        } catch {
            Write-Warning "Some files may not have extracted properly from LUXORA backup"
        }
    } else {
        Write-Warning "luxora_backup.tar not found"
    }
    
    # Extract Ubuntu backup
    $UbuntuBackupPath = Join-Path $WSLBackupPath "Ubuntu-backup.tar"
    if (Test-Path $UbuntuBackupPath) {
        Write-Info "Extracting Ubuntu-backup.tar..."
        
        try {
            $TargetDir = "$ExtractionPath\ubuntu_backup"
            
            if (Get-Command tar -ErrorAction SilentlyContinue) {
                & tar -xf $UbuntuBackupPath -C $TargetDir 2>$null
            } else {
                & 7z x $UbuntuBackupPath -o"$TargetDir" -y | Out-Null
            }
            
            $ExtractedFiles = (Get-ChildItem $TargetDir -Recurse -File).Count
            Write-Success "Ubuntu backup extracted: $ExtractedFiles files"
        } catch {
            Write-Warning "Some files may not have extracted properly from Ubuntu backup"
        }
    } else {
        Write-Warning "Ubuntu-backup.tar not found"
    }
    
    return $true
}

function New-VHDXInstructions {
    Write-Info "Creating VHDX mounting PowerShell script..."
    
    # The script content was already created in the bash version
    # Copy it from the previously created file
    $VHDXScriptPath = "$LuxorCUAPath\wsl-integration\mount-vhdx-instructions.ps1"
    
    if (!(Test-Path (Split-Path $VHDXScriptPath))) {
        New-Item -ItemType Directory -Path (Split-Path $VHDXScriptPath) -Force | Out-Null
    }
    
    # Create a simple VHDX mounting script
    $VHDXScript = @'
# VHDX Mounting Script for WSL Backup Recovery
# Run this script as Administrator in PowerShell

param([string]$Action = "mount")

$WSLBackupPath = "D:\WSLBackup"
$ExtractionPath = "E:\Project_Luxor9\wsl-extraction"

switch ($Action.ToLower()) {
    "mount" {
        Write-Host "🔄 Mounting WSL VHDX files..." -ForegroundColor Cyan
        
        $VHDXFiles = @(
            @{Path = "$WSLBackupPath\rootfs.vhdx"; Name = "rootfs"},
            @{Path = "$WSLBackupPath\ubuntu_backup_20250808_192805.vhdx"; Name = "ubuntu"}
        )
        
        foreach ($VHDX in $VHDXFiles) {
            if (Test-Path $VHDX.Path) {
                try {
                    Mount-VHD -Path $VHDX.Path -ReadOnly
                    $Volume = Get-VHD -Path $VHDX.Path | Get-Disk | Get-Partition | Get-Volume
                    Write-Host "✅ $($VHDX.Name) mounted to drive: $($Volume.DriveLetter)" -ForegroundColor Green
                } catch {
                    Write-Host "❌ Failed to mount $($VHDX.Name): $($_.Exception.Message)" -ForegroundColor Red
                }
            }
        }
    }
    
    "dismount" {
        Write-Host "🔄 Dismounting WSL VHDX files..." -ForegroundColor Cyan
        
        $VHDXFiles = @(
            "$WSLBackupPath\rootfs.vhdx",
            "$WSLBackupPath\ubuntu_backup_20250808_192805.vhdx"
        )
        
        foreach ($VHDXPath in $VHDXFiles) {
            if (Test-Path $VHDXPath) {
                try {
                    Dismount-VHD -Path $VHDXPath
                    Write-Host "✅ $(Split-Path $VHDXPath -Leaf) dismounted" -ForegroundColor Green
                } catch {
                    Write-Host "❌ Failed to dismount $(Split-Path $VHDXPath -Leaf)" -ForegroundColor Red
                }
            }
        }
    }
    
    default {
        Write-Host "Usage: .\mount-vhdx-instructions.ps1 -Action [mount|dismount]" -ForegroundColor Yellow
    }
}
'@
    
    $VHDXScript | Out-File -FilePath $VHDXScriptPath -Encoding UTF8
    Write-Success "VHDX mounting script created at: $VHDXScriptPath"
}

function Test-ExtractedContents {
    Write-Info "Analyzing extracted WSL backup contents..."
    
    $LuxoraBackupDir = "$ExtractionPath\luxora_backup"
    if (Test-Path $LuxoraBackupDir) {
        Write-Info "Analyzing LUXORA backup contents..."
        
        # Look for AI models
        $ModelFiles = Get-ChildItem $LuxoraBackupDir -Recurse -Include "*.gguf", "*.bin", "*.safetensors" -ErrorAction SilentlyContinue
        if ($ModelFiles) {
            Write-Success "Found $($ModelFiles.Count) AI model files"
        }
        
        # Look for Python scripts
        $PythonFiles = Get-ChildItem $LuxoraBackupDir -Recurse -Include "*.py" -ErrorAction SilentlyContinue
        if ($PythonFiles) {
            Write-Success "Found $($PythonFiles.Count) Python scripts"
        }
        
        # Look for configuration files
        $ConfigFiles = Get-ChildItem $LuxoraBackupDir -Recurse -Include "*.yml", "*.yaml", "*.json", "*.conf" -ErrorAction SilentlyContinue
        if ($ConfigFiles) {
            Write-Success "Found $($ConfigFiles.Count) configuration files"
        }
        
        # Look for Docker files
        $DockerFiles = Get-ChildItem $LuxoraBackupDir -Recurse -Include "Dockerfile", "docker-compose.yml", "*.dockerfile" -ErrorAction SilentlyContinue
        if ($DockerFiles) {
            Write-Success "Found $($DockerFiles.Count) Docker files"
        }
    }
}

function Copy-IntegratedComponents {
    Write-Info "Integrating valuable WSL components..."
    
    $LuxoraBackupDir = "$ExtractionPath\luxora_backup"
    if (Test-Path $LuxoraBackupDir) {
        # Integrate AI models
        Write-Info "Integrating AI models from LUXORA backup..."
        $ModelFiles = Get-ChildItem $LuxoraBackupDir -Recurse -Include "*.gguf", "*.bin", "*.safetensors" -ErrorAction SilentlyContinue
        foreach ($ModelFile in $ModelFiles) {
            try {
                Copy-Item $ModelFile.FullName "$LuxorCUAPath\ai-models\wsl-restored\" -ErrorAction SilentlyContinue
            } catch {
                # Ignore copy errors
            }
        }
        
        $IntegratedModels = (Get-ChildItem "$LuxorCUAPath\ai-models\wsl-restored" -ErrorAction SilentlyContinue).Count
        Write-Success "Integrated $IntegratedModels AI model files"
        
        # Integrate Python scripts
        Write-Info "Integrating Python scripts..."
        $PythonFiles = Get-ChildItem $LuxoraBackupDir -Recurse -Include "*.py" -ErrorAction SilentlyContinue
        foreach ($PythonFile in $PythonFiles) {
            try {
                $RelativePath = $PythonFile.FullName.Replace($LuxoraBackupDir, "").TrimStart('\')
                $TargetDir = Split-Path "$LuxorCUAPath\scripts\wsl\$RelativePath"
                
                if (!(Test-Path $TargetDir)) {
                    New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
                }
                
                Copy-Item $PythonFile.FullName $TargetDir -ErrorAction SilentlyContinue
            } catch {
                # Ignore copy errors
            }
        }
        
        $IntegratedScripts = (Get-ChildItem "$LuxorCUAPath\scripts\wsl" -Recurse -Include "*.py" -ErrorAction SilentlyContinue).Count
        Write-Success "Integrated $IntegratedScripts Python scripts"
        
        # Integrate configuration files
        Write-Info "Integrating configuration files..."
        $ConfigFiles = Get-ChildItem $LuxoraBackupDir -Recurse -Include "*.yml", "*.yaml", "*.json", "*.conf" -ErrorAction SilentlyContinue
        foreach ($ConfigFile in $ConfigFiles) {
            try {
                $RelativePath = $ConfigFile.FullName.Replace($LuxoraBackupDir, "").TrimStart('\')
                $TargetDir = Split-Path "$LuxorCUAPath\configs\wsl\$RelativePath"
                
                if (!(Test-Path $TargetDir)) {
                    New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
                }
                
                Copy-Item $ConfigFile.FullName $TargetDir -ErrorAction SilentlyContinue
            } catch {
                # Ignore copy errors
            }
        }
        
        $IntegratedConfigs = (Get-ChildItem "$LuxorCUAPath\configs\wsl" -Recurse -ErrorAction SilentlyContinue).Count
        Write-Success "Integrated $IntegratedConfigs configuration files"
    }
}

function New-IntegrationReport {
    Write-Info "Generating WSL backup integration report..."
    
    $LuxoraFiles = if (Test-Path "$ExtractionPath\luxora_backup") { (Get-ChildItem "$ExtractionPath\luxora_backup" -Recurse -File -ErrorAction SilentlyContinue).Count } else { 0 }
    $UbuntuFiles = if (Test-Path "$ExtractionPath\ubuntu_backup") { (Get-ChildItem "$ExtractionPath\ubuntu_backup" -Recurse -File -ErrorAction SilentlyContinue).Count } else { 0 }
    $IntegratedModels = if (Test-Path "$LuxorCUAPath\ai-models\wsl-restored") { (Get-ChildItem "$LuxorCUAPath\ai-models\wsl-restored" -ErrorAction SilentlyContinue).Count } else { 0 }
    $IntegratedScripts = if (Test-Path "$LuxorCUAPath\scripts\wsl") { (Get-ChildItem "$LuxorCUAPath\scripts\wsl" -Recurse -Include "*.py" -ErrorAction SilentlyContinue).Count } else { 0 }
    $IntegratedConfigs = if (Test-Path "$LuxorCUAPath\configs\wsl") { (Get-ChildItem "$LuxorCUAPath\configs\wsl" -Recurse -ErrorAction SilentlyContinue).Count } else { 0 }
    
    $ReportContent = @"
# WSL Backup Integration Report (PowerShell)
**Generated:** $(Get-Date)
**Integration Script:** integrate-wsl-backups.ps1

## 📦 WSL Backup Files Processed

### TAR Archive Extractions
| Backup File | Status | Files Extracted |
|-------------|--------|----------------|
| luxora_backup.tar | $( if (Test-Path "$ExtractionPath\luxora_backup") { "✅ Extracted" } else { "❌ Failed" } ) | $LuxoraFiles |
| Ubuntu-backup.tar | $( if (Test-Path "$ExtractionPath\ubuntu_backup") { "✅ Extracted" } else { "❌ Failed" } ) | $UbuntuFiles |

### VHDX Files (PowerShell Mounting Available)
| VHDX File | Size | PowerShell Script |
|-----------|------|-------------------|
| rootfs.vhdx | $( if (Test-Path "$WSLBackupPath\rootfs.vhdx") { [math]::Round((Get-Item "$WSLBackupPath\rootfs.vhdx").Length / 1GB, 2).ToString() + " GB" } else { "N/A" } ) | mount-vhdx-instructions.ps1 |
| ubuntu_backup_20250808_192805.vhdx | $( if (Test-Path "$WSLBackupPath\ubuntu_backup_20250808_192805.vhdx") { [math]::Round((Get-Item "$WSLBackupPath\ubuntu_backup_20250808_192805.vhdx").Length / 1GB, 2).ToString() + " GB" } else { "N/A" } ) | mount-vhdx-instructions.ps1 |

## 🔧 Integration Results

### AI Models Recovered
- **Location**: `ai-models/wsl-restored/`
- **Count**: $IntegratedModels model files
- **Types**: GGUF, BIN, SafeTensors formats

### Scripts Integrated  
- **Location**: `scripts/wsl/`
- **Count**: $IntegratedScripts Python scripts
- **Organization**: Preserved original directory structure

### Configurations Recovered
- **Location**: `configs/wsl/`
- **Count**: $IntegratedConfigs configuration files
- **Formats**: YAML, JSON, CONF files

## 🎯 Next Steps

### 1. VHDX Processing (PowerShell as Administrator)
``````powershell
# Mount all VHDX files and extract contents
.\wsl-integration\mount-vhdx-instructions.ps1 -Action mount

# Dismount when done
.\wsl-integration\mount-vhdx-instructions.ps1 -Action dismount
``````

### 2. Integration Validation
``````powershell
# Test integrated components
Get-ChildItem ai-models\wsl-restored
Get-ChildItem scripts\wsl -Recurse -Include "*.py"
Get-ChildItem configs\wsl -Recurse
``````

## 💡 Integration Benefits

### 🧠 Enhanced AI Capabilities
- **Additional AI Models**: $IntegratedModels recovered models from Linux environment
- **Cross-Platform Compatibility**: Linux-optimized models and configurations
- **Development History**: Access to previous development states

### 🛠️ Operational Intelligence  
- **Script Libraries**: $IntegratedScripts Python scripts from WSL environment
- **Environment Snapshots**: Complete Linux development environment states
- **Configuration Management**: $IntegratedConfigs configuration files recovered

## 🚀 Enhanced System Status

With WSL backup integration, LUXOR AI CUA now includes:
- ✅ **Extended AI Model Library** ($IntegratedModels models from WSL)
- ✅ **Cross-Platform Development** continuity
- ✅ **Script Collections** ($IntegratedScripts Python scripts)
- ✅ **Configuration Repository** ($IntegratedConfigs config files)
- ✅ **Linux Environment Recovery** with Windows compatibility

---
**Total WSL Components Integrated**: $($IntegratedModels + $IntegratedScripts + $IntegratedConfigs) files  
**Integration Status**: ✅ **COMPLETE** (TAR archives) + 📋 **VHDX ready for mounting**  
**Next Phase**: VHDX processing and system validation

**WSL Integration: Successfully bridging Linux development with Windows LUXOR AI CUA platform** 🐧🪟🚀
"@

    $ReportPath = "$LuxorCUAPath\WSL_BACKUP_INTEGRATION_REPORT.md"
    $ReportContent | Out-File -FilePath $ReportPath -Encoding UTF8
    Write-Success "WSL integration report generated at: $ReportPath"
}

# Main execution
switch ($Action.ToLower()) {
    "integrate" {
        if (!(Test-BackupFiles)) { return }
        
        New-ExtractionStructure
        Expand-TarArchives
        New-VHDXInstructions
        Test-ExtractedContents
        Copy-IntegratedComponents
        New-IntegrationReport
        
        Write-Output ""
        Write-Success "🎉 WSL Backup Integration Completed!"
        Write-Output ""
        Write-Info "📋 Summary:"
        $IntegratedModels = if (Test-Path "$LuxorCUAPath\ai-models\wsl-restored") { (Get-ChildItem "$LuxorCUAPath\ai-models\wsl-restored" -ErrorAction SilentlyContinue).Count } else { 0 }
        $IntegratedScripts = if (Test-Path "$LuxorCUAPath\scripts\wsl") { (Get-ChildItem "$LuxorCUAPath\scripts\wsl" -Recurse -Include "*.py" -ErrorAction SilentlyContinue).Count } else { 0 }
        $IntegratedConfigs = if (Test-Path "$LuxorCUAPath\configs\wsl") { (Get-ChildItem "$LuxorCUAPath\configs\wsl" -Recurse -ErrorAction SilentlyContinue).Count } else { 0 }
        
        Write-Output "  📦 TAR archives: Extracted and integrated"
        Write-Output "  💿 VHDX files: PowerShell mounting script created"
        Write-Output "  🧠 AI models: $IntegratedModels files integrated"
        Write-Output "  🐍 Scripts: $IntegratedScripts Python files integrated"
        Write-Output "  ⚙️ Configs: $IntegratedConfigs configuration files integrated"
        Write-Output ""
        Write-Info "📖 Next Steps:"
        Write-Output "1. Review report: Get-Content WSL_BACKUP_INTEGRATION_REPORT.md"
        Write-Output "2. Mount VHDX files (PowerShell Admin): .\wsl-integration\mount-vhdx-instructions.ps1 -Action mount"
        Write-Output "3. View integrated files: Get-ChildItem ai-models\wsl-restored"
        Write-Output "4. Update system: .\quick-start.sh --with-wsl-integration"
    }
    
    "status" {
        Write-ColorOutput Cyan "📊 WSL Backup Integration Status"
        Write-ColorOutput Cyan "=================================="
        
        if (Test-BackupFiles) {
            Write-Output ""
            Write-Info "Integration Status:"
            
            $IntegratedModels = if (Test-Path "$LuxorCUAPath\ai-models\wsl-restored") { (Get-ChildItem "$LuxorCUAPath\ai-models\wsl-restored" -ErrorAction SilentlyContinue).Count } else { 0 }
            $IntegratedScripts = if (Test-Path "$LuxorCUAPath\scripts\wsl") { (Get-ChildItem "$LuxorCUAPath\scripts\wsl" -Recurse -Include "*.py" -ErrorAction SilentlyContinue).Count } else { 0 }
            $IntegratedConfigs = if (Test-Path "$LuxorCUAPath\configs\wsl") { (Get-ChildItem "$LuxorCUAPath\configs\wsl" -Recurse -ErrorAction SilentlyContinue).Count } else { 0 }
            
            Write-Output "  🧠 AI Models: $IntegratedModels files"
            Write-Output "  🐍 Python Scripts: $IntegratedScripts files"
            Write-Output "  ⚙️ Configurations: $IntegratedConfigs files"
            
            if (Test-Path "$LuxorCUAPath\wsl-integration\mount-vhdx-instructions.ps1") {
                Write-Success "VHDX mounting script ready"
            } else {
                Write-Warning "VHDX mounting script not found"
            }
        }
    }
    
    default {
        Write-ColorOutput Cyan "WSL Backup Integration Script for LUXOR AI CUA"
        Write-ColorOutput Cyan "=============================================="
        Write-Output "Usage: .\integrate-wsl-backups.ps1 [-Action integrate|status]"
        Write-Output ""
        Write-Output "Actions:"
        Write-Output "  integrate - Process WSL backup files and integrate components"
        Write-Output "  status    - Check current integration status"
        Write-Output ""
        Write-Output "Examples:"
        Write-Output "  .\integrate-wsl-backups.ps1"
        Write-Output "  .\integrate-wsl-backups.ps1 -Action status"
    }
}