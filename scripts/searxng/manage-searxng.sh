#!/bin/bash
# SearXNG Management Script for LUXOR AI CUA

COMPOSE_FILE="docker/searxng/docker-compose.searxng.yml"
SEARXNG_URL="http://localhost:8080"

case "$1" in
    "start")
        echo "🚀 Starting SearXNG services..."
        docker-compose -f $COMPOSE_FILE up -d
        echo "✅ SearXNG started at: $SEARXNG_URL"
        ;;
    "stop")
        echo "⏹️  Stopping SearXNG services..."
        docker-compose -f $COMPOSE_FILE down
        echo "✅ SearXNG stopped"
        ;;
    "restart")
        echo "🔄 Restarting SearXNG services..."
        docker-compose -f $COMPOSE_FILE restart
        echo "✅ SearXNG restarted"
        ;;
    "status")
        echo "📊 SearXNG Service Status:"
        docker-compose -f $COMPOSE_FILE ps
        ;;
    "logs")
        echo "📋 SearXNG Logs:"
        docker-compose -f $COMPOSE_FILE logs -f searxng
        ;;
    "test")
        echo "🧪 Testing SearXNG API..."
        curl -s "$SEARXNG_URL/search?q=test&format=json" | head -20
        ;;
    "health")
        echo "🏥 SearXNG Health Check:"
        if curl -s -f "$SEARXNG_URL" > /dev/null; then
            echo "✅ SearXNG is healthy"
        else
            echo "❌ SearXNG is not responding"
        fi
        ;;
    *)
        echo "🔍 SearXNG Management Script"
        echo "============================"
        echo "Usage: $0 {start|stop|restart|status|logs|test|health}"
        echo ""
        echo "Commands:"
        echo "  start    - Start SearXNG services"
        echo "  stop     - Stop SearXNG services"
        echo "  restart  - Restart SearXNG services"
        echo "  status   - Show service status"
        echo "  logs     - Show service logs"
        echo "  test     - Test SearXNG API"
        echo "  health   - Check service health"
        ;;
esac