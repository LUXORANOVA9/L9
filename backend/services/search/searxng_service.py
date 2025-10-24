"""
SearXNG Privacy Search Integration Service
Provides search capabilities for LUXOR AI CUA platform
"""

import asyncio
import aiohttp
import json
from typing import List, Dict, Optional, Any
from urllib.parse import urlencode
import logging

logger = logging.getLogger(__name__)

class SearXNGService:
    """SearXNG Privacy-focused Search Service"""
    
    def __init__(self, base_url: str = "http://localhost:8080"):
        self.base_url = base_url.rstrip('/')
        self.session = None
        
    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create HTTP session"""
        if self.session is None or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=30)
            self.session = aiohttp.ClientSession(
                timeout=timeout,
                headers={'User-Agent': 'LUXOR-AI-CUA/1.0'}
            )
        return self.session
    
    async def search(
        self, 
        query: str, 
        category: str = "general",
        language: str = "auto",
        format: str = "json",
        engines: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Perform privacy-focused search using SearXNG
        
        Args:
            query: Search query string
            category: Search category (general, images, videos, etc.)
            language: Search language preference
            format: Response format (json, html)
            engines: Specific engines to use
            
        Returns:
            Dictionary containing search results
        """
        try:
            session = await self._get_session()
            
            # Prepare search parameters
            params = {
                'q': query,
                'category': category,
                'language': language,
                'format': format
            }
            
            if engines:
                params['engines'] = ','.join(engines)
            
            # Make search request
            search_url = f"{self.base_url}/search"
            
            async with session.get(search_url, params=params) as response:
                if response.status == 200:
                    if format == 'json':
                        return await response.json()
                    else:
                        return {'html': await response.text()}
                else:
                    logger.error(f"SearXNG search failed: {response.status}")
                    return {'error': f'Search failed with status {response.status}'}
                    
        except Exception as e:
            logger.error(f"SearXNG search error: {str(e)}")
            return {'error': str(e)}
    
    async def ai_focused_search(self, query: str) -> Dict[str, Any]:
        """Perform AI and development focused search"""
        ai_engines = ['google', 'github', 'stackoverflow', 'arxiv']
        
        results = await self.search(
            query=f"{query} AI machine learning",
            engines=ai_engines,
            category="general"
        )
        
        # Filter results for AI relevance
        if 'results' in results:
            filtered_results = []
            ai_keywords = [
                'ai', 'machine learning', 'neural network', 'deep learning',
                'python', 'tensorflow', 'pytorch', 'github', 'api'
            ]
            
            for result in results['results']:
                title = result.get('title', '').lower()
                content = result.get('content', '').lower()
                
                # Score based on AI relevance
                relevance_score = sum(
                    1 for keyword in ai_keywords 
                    if keyword in title or keyword in content
                )
                
                if relevance_score > 0:
                    result['ai_relevance_score'] = relevance_score
                    filtered_results.append(result)
            
            # Sort by relevance
            filtered_results.sort(
                key=lambda x: x.get('ai_relevance_score', 0), 
                reverse=True
            )
            
            results['results'] = filtered_results[:10]
            results['total_ai_filtered'] = len(filtered_results)
        
        return results
    
    async def code_search(self, query: str, language: str = "python") -> Dict[str, Any]:
        """Search for code examples and documentation"""
        code_query = f"{query} {language} example code github"
        
        return await self.search(
            query=code_query,
            engines=['github', 'stackoverflow', 'google'],
            category="general"
        )
    
    async def chinese_search(self, query: str) -> Dict[str, Any]:
        """Perform Chinese language search"""
        return await self.search(
            query=query,
            engines=['baidu', 'google'],
            language="zh_CN",
            category="general"
        )
    
    async def health_check(self) -> bool:
        """Check if SearXNG service is available"""
        try:
            session = await self._get_session()
            async with session.get(f"{self.base_url}/") as response:
                return response.status == 200
        except Exception as e:
            logger.error(f"SearXNG health check failed: {str(e)}")
            return False
    
    async def close(self):
        """Close the HTTP session"""
        if self.session and not self.session.closed:
            await self.session.close()
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

# Example usage
async def main():
    """Example usage of SearXNG service"""
    async with SearXNGService() as search:
        # Check service health
        if not await search.health_check():
            print("SearXNG service is not available")
            return
        
        # Perform AI-focused search
        results = await search.ai_focused_search("machine learning algorithms")
        print(f"Found {len(results.get('results', []))} AI-relevant results")
        
        # Perform code search
        code_results = await search.code_search("fastapi authentication", "python")
        print(f"Found {len(code_results.get('results', []))} code examples")

if __name__ == "__main__":
    asyncio.run(main())