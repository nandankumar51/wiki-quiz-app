import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
import re


class WikipediaScraper:
    """
    Scrapes Wikipedia articles and extracts structured information.
    """
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape_article(self, url: str) -> Optional[Dict]:
        """
        Scrape a Wikipedia article and extract key information.
        
        Args:
            url: Wikipedia article URL
            
        Returns:
            Dictionary containing extracted article data
        """
        try:
            # Validate URL
            if not self._is_valid_wikipedia_url(url):
                raise ValueError("Invalid Wikipedia URL")
            
            # Fetch the page
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title = self._extract_title(soup)
            
            # Extract summary (first paragraph)
            summary = self._extract_summary(soup)
            
            # Extract sections
            sections = self._extract_sections(soup)
            
            # Extract full text content
            full_text = self._extract_full_text(soup)
            
            # Extract key entities
            key_entities = self._extract_entities(soup)
            
            return {
                'url': url,
                'title': title,
                'summary': summary,
                'sections': sections,
                'full_text': full_text,
                'key_entities': key_entities,
                'raw_html': str(soup)[:50000]  # Store first 50KB of HTML
            }
            
        except Exception as e:
            print(f"Error scraping Wikipedia article: {e}")
            return None
    
    def _is_valid_wikipedia_url(self, url: str) -> bool:
        """Validate that the URL is a Wikipedia article."""
        pattern = r'^https?://(en\.)?wikipedia\.org/wiki/.+'
        return bool(re.match(pattern, url))
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract article title."""
        title_elem = soup.find('h1', {'id': 'firstHeading'})
        if title_elem:
            return title_elem.get_text().strip()
        return "Unknown Title"
    
    def _extract_summary(self, soup: BeautifulSoup) -> str:
        """Extract the first paragraph as summary."""
        content = soup.find('div', {'id': 'mw-content-text'})
        if content:
            # Find first paragraph that's not empty
            paragraphs = content.find_all('p', recursive=False)
            for p in paragraphs:
                text = p.get_text().strip()
                if len(text) > 50:  # Skip very short paragraphs
                    return text
        return "No summary available."
    
    def _extract_sections(self, soup: BeautifulSoup) -> List[str]:
        """Extract section headings."""
        sections = []
        for heading in soup.find_all(['h2', 'h3']):
            headline = heading.find('span', {'class': 'mw-headline'})
            if headline:
                section_text = headline.get_text().strip()
                # Skip common non-content sections
                if section_text not in ['Contents', 'References', 'External links', 
                                       'See also', 'Notes', 'Further reading']:
                    sections.append(section_text)
        return sections[:10]  # Limit to first 10 sections
    
    def _extract_full_text(self, soup: BeautifulSoup) -> str:
        """Extract the full article text content."""
        content = soup.find('div', {'id': 'mw-content-text'})
        if not content:
            return ""
        
        # Remove unwanted elements
        for element in content.find_all(['table', 'style', 'script', 'sup', 'span']):
            element.decompose()
        
        # Get all paragraphs
        paragraphs = content.find_all('p')
        text_parts = []
        
        for p in paragraphs:
            text = p.get_text().strip()
            if len(text) > 20:  # Skip very short paragraphs
                text_parts.append(text)
        
        full_text = '\n\n'.join(text_parts)
        
        # Limit to ~8000 characters to avoid token limits
        return full_text[:8000]
    
    def _extract_entities(self, soup: BeautifulSoup) -> Dict[str, List[str]]:
        """
        Extract key entities (people, organizations, locations).
        This is a simple extraction based on links and formatting.
        """
        entities = {
            'people': [],
            'organizations': [],
            'locations': []
        }
        
        # Extract from infobox if available
        infobox = soup.find('table', {'class': 'infobox'})
        if infobox:
            # Extract linked entities from infobox
            links = infobox.find_all('a')
            for link in links[:15]:  # Limit to avoid overwhelming
                text = link.get_text().strip()
                if len(text) > 2 and not text.startswith('['):
                    # Simple heuristic classification
                    if 'University' in text or 'College' in text or 'Institute' in text:
                        entities['organizations'].append(text)
                    elif any(word in text for word in ['Kingdom', 'States', 'City', 'County']):
                        entities['locations'].append(text)
                    else:
                        # Assume it's a person if it's a proper noun
                        if text[0].isupper():
                            entities['people'].append(text)
        
        # Remove duplicates
        for key in entities:
            entities[key] = list(set(entities[key]))[:10]  # Limit to 10 each
        
        return entities
