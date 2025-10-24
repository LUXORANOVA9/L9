# SearXNG Management Script for LUXOR AI CUA (PowerShell)
param(
    [Parameter(Mandatory=$true, Position=0)]
    [ValidateSet("start", "stop", "restart", "status", "logs", "test", "health")]
    [string]$Action
)

$ComposeFile = "docker\searxng\docker-compose.searxng.yml"
$SearXNGUrl = "http://localhost:8080"

function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

switch ($Action) {
    "start" {
        Write-ColorOutput Green "🚀 Starting SearXNG services..."
        docker-compose -f $ComposeFile up -d
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput Green "✅ SearXNG started successfully!"
            Write-ColorOutput Cyan "🌐 Access SearXNG at: $SearXNGUrl"
        } else {
            Write-ColorOutput Red "❌ Failed to start SearXNG services"
        }
    }
    
    "stop" {
        Write-ColorOutput Yellow "⏹️  Stopping SearXNG services..."
        docker-compose -f $ComposeFile down
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput Green "✅ SearXNG stopped successfully"
        } else {
            Write-ColorOutput Red "❌ Failed to stop SearXNG services"
        }
    }
    
    "restart" {
        Write-ColorOutput Yellow "🔄 Restarting SearXNG services..."
        docker-compose -f $ComposeFile restart
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput Green "✅ SearXNG restarted successfully"
        } else {
            Write-ColorOutput Red "❌ Failed to restart SearXNG services"
        }
    }
    
    "status" {
        Write-ColorOutput Cyan "📊 SearXNG Service Status:"
        docker-compose -f $ComposeFile ps
    }
    
    "logs" {
        Write-ColorOutput Cyan "📋 SearXNG Logs (Press Ctrl+C to exit):"
        docker-compose -f $ComposeFile logs -f searxng
    }
    
    "test" {
        Write-ColorOutput Cyan "🧪 Testing SearXNG API..."
        try {
            $response = Invoke-RestMethod -Uri "$SearXNGUrl/search?q=test&format=json" -TimeoutSec 10
            Write-ColorOutput Green "✅ SearXNG API is responding"
            Write-Output "Results found: $($response.results.Count)"
        } catch {
            Write-ColorOutput Red "❌ SearXNG API test failed: $($_.Exception.Message)"
        }
    }
    
    "health" {
        Write-ColorOutput Cyan "🏥 SearXNG Health Check..."
        try {
            $response = Invoke-WebRequest -Uri $SearXNGUrl -TimeoutSec 5 -UseBasicParsing
            if ($response.StatusCode -eq 200) {
                Write-ColorOutput Green "✅ SearXNG is healthy (Status: $($response.StatusCode))"
            } else {
                Write-ColorOutput Yellow "⚠️  SearXNG responded with status: $($response.StatusCode)"
            }
        } catch {
            Write-ColorOutput Red "❌ SearXNG is not responding: $($_.Exception.Message)"
        }
    }
}

Write-Output ""
Write-ColorOutput Cyan "💡 Available commands:"
Write-Output "  start    - Start SearXNG services"
Write-Output "  stop     - Stop SearXNG services"  
Write-Output "  restart  - Restart SearXNG services"
Write-Output "  status   - Show service status"
Write-Output "  logs     - Show service logs"
Write-Output "  test     - Test SearXNG API"
Write-Output "  health   - Check service health"