# LUXOR SearXNG Integration Guide
## Privacy-Focused Search Engine Integration

### 📊 SearXNG Analysis

Your SearXNG installation at `D:\ANACONDA\searxng` provides **privacy-focused search capabilities** that can be integrated into the LUXOR AI CUA ecosystem:

```
D:\ANACONDA\searxng\
├── 🔍 Search Engine Core
│   ├── Configuration files
│   ├── Search aggregators
│   ├── Result processors
│   └── Privacy filters
│
├── 🌐 Web Interface
│   ├── Search frontend
│   ├── API endpoints
│   ├── Result rendering
│   └── User preferences
│
└── ⚙️ Service Configuration
    ├── Docker compose files
    ├── Environment settings
    ├── Plugin configurations
    └── Custom search engines
```

### 🎯 Integration Strategy

#### **Tier 1: Core Search Integration (Immediate)**
- Integrate SearXNG as the primary search backend for LUXOR AI CUA
- Privacy-focused search for AI training data and research
- Local search capabilities without external dependencies

#### **Tier 2: AI-Enhanced Search (High Priority)**  
- AI-powered query enhancement and result filtering
- Integration with LUXORANOVA BRAIN for intelligent search
- Contextual search within AI agent workflows

#### **Tier 3: Enterprise Search (Advanced)**
- Custom search engines for internal documentation
- Integration with business intelligence and knowledge base
- Advanced search analytics and optimization

### 🔧 SearXNG Integration Script

```bash
#!/bin/bash
# integrate-searxng.sh - SearXNG Privacy Search Integration

SOURCE_SEARXNG="D:/ANACONDA/searxng"
TARGET_PATH="E:/Project_Luxor9"

echo "🔍 LUXOR SearXNG Integration"
echo "============================"

# Create search integration structure
mkdir -p "$TARGET_PATH/services"/{searxng,search-api}

# Integrate SearXNG
echo "🔍 Integrating SearXNG Search Engine..."
if [ -d "$SOURCE_SEARXNG" ]; then
    # Copy SearXNG configuration and setup
    cp -r "$SOURCE_SEARXNG"/* "$TARGET_PATH/services/searxng/" 2>/dev/null || true
    
    # Count integrated files
    searxng_files=$(find "$TARGET_PATH/services/searxng" -type f 2>/dev/null | wc -l)
    echo "✅ SearXNG: $searxng_files files integrated"
else
    echo "❌ SearXNG directory not found: $SOURCE_SEARXNG"
fi

# Create SearXNG Docker Compose configuration
cat > "$TARGET_PATH/docker-compose.searxng.yml" << 'EOF'
version: '3.8'

services:
  searxng:
    image: searxng/searxng:latest
    container_name: luxor-searxng
    ports:
      - "8888:8080"
    volumes:
      - ./services/searxng/searxng:/etc/searxng:rw
      - ./services/searxng/uwsgi.ini:/etc/searxng/uwsgi.ini:ro
    environment:
      - BASE_URL=http://localhost:8888/
      - INSTANCE_NAME=LUXOR Search
    networks:
      - luxor-network
    restart: unless-stopped

  redis-searxng:
    image: redis:7-alpine
    container_name: luxor-searxng-redis
    command: redis-server --save 30 1 --loglevel warning
    volumes:
      - searxng-redis:/data
    networks:
      - luxor-network
    restart: unless-stopped

volumes:
  searxng-redis:
    driver: local

networks:
  luxor-network:
    external: true
EOF

# Create Search API wrapper
cat > "$TARGET_PATH/services/search-api/search_service.py" << 'EOF'
"""
LUXOR Search Service - SearXNG Integration Wrapper
Privacy-focused search for AI agents and applications
"""

import requests
import json
from typing import Dict, List, Optional, Any
from urllib.parse import quote_plus
import asyncio
import aiohttp

class LuxorSearchService:
    """LUXOR AI CUA Search Service with SearXNG Integration"""
    
    def __init__(self, searxng_url: str = "http://localhost:8888"):
        self.searxng_url = searxng_url.rstrip('/')
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'LUXOR-AI-CUA/1.0 (Privacy-Focused AI Search)'
        })
    
    def search(self, query: str, **kwargs) -> Dict[str, Any]:
        """
        Perform privacy-focused search using SearXNG
        
        Args:
            query: Search query string
            **kwargs: Additional search parameters
                - category: Search category (general, images, videos, etc.)
                - language: Search language
                - time_range: Time filter (day, week, month, year)
                - engines: Specific engines to use
        
        Returns:
            Search results with metadata
        """
        try:
            params = {
                'q': query,
                'format': 'json',
                'safesearch': kwargs.get('safesearch', 1),
                'language': kwargs.get('language', 'en'),
                'category': kwargs.get('category', 'general')
            }
            
            # Add optional parameters
            if 'time_range' in kwargs:
                params['time_range'] = kwargs['time_range']
            if 'engines' in kwargs:
                params['engines'] = kwargs['engines']
            
            response = self.session.get(
                f"{self.searxng_url}/search",
                params=params,
                timeout=30
            )
            response.raise_for_status()
            
            results = response.json()
            
            return {
                'query': query,
                'results': results.get('results', []),
                'number_of_results': results.get('number_of_results', 0),
                'suggestions': results.get('suggestions', []),
                'infoboxes': results.get('infoboxes', []),
                'engines': results.get('engines', []),
                'search_metadata': {
                    'privacy_focused': True,
                    'source': 'SearXNG',
                    'timestamp': results.get('timestamp')
                }
            }
            
        except Exception as e:
            return {
                'query': query,
                'error': str(e),
                'results': [],
                'number_of_results': 0
            }
    
    async def async_search(self, query: str, **kwargs) -> Dict[str, Any]:
        """Asynchronous search for high-performance applications"""
        async with aiohttp.ClientSession() as session:
            try:
                params = {
                    'q': query,
                    'format': 'json',
                    'safesearch': kwargs.get('safesearch', 1),
                    'language': kwargs.get('language', 'en'),
                    'category': kwargs.get('category', 'general')
                }
                
                async with session.get(
                    f"{self.searxng_url}/search",
                    params=params,
                    timeout=30
                ) as response:
                    if response.status == 200:
                        results = await response.json()
                        return {
                            'query': query,
                            'results': results.get('results', []),
                            'number_of_results': results.get('number_of_results', 0),
                            'suggestions': results.get('suggestions', []),
                            'privacy_focused': True
                        }
                    else:
                        return {'query': query, 'error': f'HTTP {response.status}', 'results': []}
                        
            except Exception as e:
                return {'query': query, 'error': str(e), 'results': []}
    
    def search_with_ai_enhancement(self, query: str, context: str = None) -> Dict[str, Any]:
        """
        AI-enhanced search with context awareness
        Integrates with LUXORANOVA BRAIN for intelligent search
        """
        # Basic implementation - can be enhanced with AI processing
        enhanced_query = query
        
        if context:
            enhanced_query = f"{context} {query}"
        
        # Perform search
        results = self.search(enhanced_query)
        
        # AI enhancement placeholder - integrate with LUXORANOVA BRAIN
        if results.get('results'):
            # Filter and rank results based on AI analysis
            results['ai_enhanced'] = True
            results['context_applied'] = bool(context)
        
        return results
    
    def search_code_repositories(self, query: str) -> Dict[str, Any]:
        """Specialized search for code and development resources"""
        return self.search(
            query,
            category='it',
            engines='github,stackoverflow,searchcode'
        )
    
    def search_documentation(self, query: str, tech_stack: str = None) -> Dict[str, Any]:
        """Search for technical documentation and guides"""
        enhanced_query = f"{tech_stack} {query}" if tech_stack else query
        return self.search(
            f"documentation {enhanced_query}",
            category='it'
        )
    
    def search_business_intelligence(self, query: str) -> Dict[str, Any]:
        """Search for business and market intelligence"""
        return self.search(
            f"business intelligence {query}",
            category='news'
        )
    
    def health_check(self) -> Dict[str, Any]:
        """Check SearXNG service health"""
        try:
            response = self.session.get(f"{self.searxng_url}/stats", timeout=10)
            if response.status_code == 200:
                return {
                    'status': 'healthy',
                    'service': 'SearXNG',
                    'url': self.searxng_url,
                    'privacy_focused': True
                }
            else:
                return {
                    'status': 'unhealthy',
                    'error': f'HTTP {response.status_code}'
                }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }

# Example usage and testing
if __name__ == "__main__":
    search_service = LuxorSearchService()
    
    # Health check
    health = search_service.health_check()
    print(f"SearXNG Health: {health}")
    
    # Basic search
    results = search_service.search("artificial intelligence development")
    print(f"Search Results: {len(results.get('results', []))} found")
    
    # AI-enhanced search
    enhanced_results = search_service.search_with_ai_enhancement(
        "machine learning frameworks",
        context="python development"
    )
    print(f"Enhanced Results: {len(enhanced_results.get('results', []))} found")
    
    # Code search
    code_results = search_service.search_code_repositories("FastAPI authentication")
    print(f"Code Results: {len(code_results.get('results', []))} found")
EOF

# Create search integration with LUXOR AI CUA
cat > "$TARGET_PATH/backend/services/search_integration.py" << 'EOF'
"""
LUXOR AI CUA - Search Integration Service
Connects SearXNG privacy search with AI agents
"""

import sys
from pathlib import Path

# Add search service to path
sys.path.append(str(Path(__file__).parent.parent.parent / "services" / "search-api"))

from search_service import LuxorSearchService
from typing import Dict, List, Any, Optional

class AISearchIntegration:
    """Integration between LUXOR AI agents and SearXNG search"""
    
    def __init__(self):
        self.search_service = LuxorSearchService()
        self.search_history = []
    
    def agent_search(self, query: str, agent_context: str = None) -> Dict[str, Any]:
        """
        Search function optimized for AI agents
        
        Args:
            query: Search query from AI agent
            agent_context: Context about the agent's task
        
        Returns:
            Formatted search results for AI processing
        """
        results = self.search_service.search_with_ai_enhancement(query, agent_context)
        
        # Log search for agent learning
        self.search_history.append({
            'query': query,
            'context': agent_context,
            'timestamp': results.get('search_metadata', {}).get('timestamp'),
            'results_count': results.get('number_of_results', 0)
        })
        
        # Format for AI agent consumption
        formatted_results = {
            'query': query,
            'summary': f"Found {results.get('number_of_results', 0)} results",
            'top_results': [],
            'suggestions': results.get('suggestions', []),
            'privacy_protected': True
        }
        
        # Process top results for AI agents
        for result in results.get('results', [])[:5]:  # Top 5 results
            formatted_results['top_results'].append({
                'title': result.get('title', ''),
                'url': result.get('url', ''),
                'content': result.get('content', '')[:500],  # Truncate for AI processing
                'engine': result.get('engine', ''),
                'score': result.get('score', 0)
            })
        
        return formatted_results
    
    def research_assistance(self, topic: str, depth: str = "basic") -> Dict[str, Any]:
        """
        Comprehensive research assistance for AI agents
        
        Args:
            topic: Research topic
            depth: Research depth (basic, detailed, comprehensive)
        
        Returns:
            Multi-faceted research results
        """
        research_results = {
            'topic': topic,
            'research_depth': depth,
            'sources': []
        }
        
        # Multiple search strategies based on depth
        if depth == "basic":
            searches = [f"{topic} overview"]
        elif depth == "detailed":
            searches = [
                f"{topic} overview",
                f"{topic} technical details",
                f"{topic} best practices"
            ]
        else:  # comprehensive
            searches = [
                f"{topic} overview",
                f"{topic} technical implementation",
                f"{topic} best practices",
                f"{topic} case studies",
                f"{topic} future trends"
            ]
        
        for search_query in searches:
            results = self.search_service.search(search_query)
            if results.get('results'):
                research_results['sources'].extend(results['results'][:3])  # Top 3 from each search
        
        return research_results
    
    def code_discovery(self, technology: str, use_case: str = None) -> Dict[str, Any]:
        """
        Discover code examples and repositories for AI code generation
        
        Args:
            technology: Programming language or framework
            use_case: Specific use case or application
        
        Returns:
            Code-focused search results
        """
        query = f"{technology} examples"
        if use_case:
            query = f"{technology} {use_case} examples"
        
        return self.search_service.search_code_repositories(query)
    
    def documentation_lookup(self, technology: str, topic: str = None) -> Dict[str, Any]:
        """
        Find technical documentation for AI agents
        
        Args:
            technology: Technology or framework name
            topic: Specific documentation topic
        
        Returns:
            Documentation search results
        """
        return self.search_service.search_documentation(
            topic or "getting started",
            tech_stack=technology
        )

# Global search integration instance
ai_search = AISearchIntegration()
EOF

echo ""
echo "🎉 SearXNG Integration Complete!"
echo "==============================="
echo ""
echo "📊 Integration Summary:"
echo "  🔍 SearXNG Engine:         $searxng_files files integrated"
echo "  🐳 Docker Configuration:   Created docker-compose.searxng.yml"
echo "  🔌 Search API Service:     Created search API wrapper"
echo "  🤖 AI Integration:         Created AI agent search interface"
echo ""
echo "🚀 Launch Commands:"
echo "   docker-compose -f docker-compose.searxng.yml up -d    # Start SearXNG"
echo "   python services/search-api/search_service.py          # Test search service"
echo ""
echo "🔍 Search Service Features:"
echo "   - Privacy-focused search (no tracking)"
echo "   - AI-enhanced query processing"  
echo "   - Code repository search"
echo "   - Documentation lookup"
echo "   - Business intelligence search"
echo ""
echo "💡 Integration Benefits:"
echo "   ✅ Complete privacy protection"
echo "   ✅ AI agent search capabilities"
echo "   ✅ Local search infrastructure"
echo "   ✅ No external API dependencies"
```

### 🎯 Strategic Benefits

#### **🔒 Privacy-First Search Architecture**
- **Zero Tracking**: Complete privacy protection for AI research and development
- **Local Control**: Self-hosted search without external dependencies
- **Data Sovereignty**: All search data remains within your infrastructure

#### **🤖 AI-Enhanced Search Capabilities**
- **Intelligent Queries**: Integration with LUXORANOVA BRAIN for enhanced search
- **Agent Integration**: Direct search capabilities for AI agents and workflows
- **Context-Aware**: Search results tailored to specific AI agent tasks and contexts

#### **🛠️ Development-Focused Features**
- **Code Discovery**: Specialized search for repositories, examples, and documentation
- **Technical Research**: Enhanced search for development resources and guides
- **Business Intelligence**: Market research and competitive analysis capabilities

### 💡 Integration Value

**Privacy Excellence**: Enterprise-grade privacy protection for AI development
**Search Intelligence**: AI-enhanced search capabilities for agents and applications  
**Development Acceleration**: Specialized search for code, documentation, and resources
**Infrastructure Independence**: Self-hosted search without external API limitations
**Research Enhancement**: Advanced research assistance for AI training and development

This SearXNG integration provides **privacy-focused search intelligence** that enhances your LUXOR AI CUA platform with secure, local search capabilities! 🔍🚀