import re
from typing import Dict, List, Any, Optional, Tuple
from utils import FontAnalyzer, TextProcessor


class OutlineExtractor:
    
    def __init__(self):
        self.font_analyzer = FontAnalyzer()
        self.text_processor = TextProcessor()
        
        # Heading detection patterns
        self.heading_patterns = [
            r'^\d+\.\s+(.+)$',                    
            r'^\d+\.\d+\s+(.+)$',                 
            r'^\d+\.\d+\.\d+\s+(.+)$',           
            r'^[A-Z][A-Z\s]+$',                
            r'^[IVX]+\.\s+(.+)$',               
            r'^[A-Z]\.\s+(.+)$',                  
            r'^\([a-z]\)\s+(.+)$',             
            r'^•\s+(.+)$',                     
            r'^-\s+(.+)$',                     
        ]
    
    def extract_title(self, metadata: Dict, pages_content: List[Dict]) -> str:

        if metadata and metadata.get('title'):
            title = metadata['title'].strip()
            if title and len(title) > 3:
                print(f"  Title from metadata: {title}")
                return title
        
        if pages_content:
            first_page = pages_content[0]
            title = self._extract_title_from_page(first_page)
            if title:
                print(f"  Title from first page: {title}")
                return title
        
        print("  Using filename as title fallback")
        return "Document Title"
    
    def _extract_title_from_page(self, page_content: Dict) -> Optional[str]:
        text_dict = page_content.get('text_dict', {})
        
        if not text_dict or 'blocks' not in text_dict:
            return None
        
        candidates = []
        
        for block in text_dict['blocks']:
            if 'lines' not in block:
                continue
                
            for line in block['lines']:
                if 'spans' not in line:
                    continue
                    
                for span in line['spans']:
                    text = span.get('text', '').strip()
                    font_size = span.get('size', 0)
                    font_flags = span.get('flags', 0)
                    
                    if not text or len(text) < 5:
                        continue
                    
                    if any(pattern in text.lower() for pattern in 
                          ['page', 'abstract', 'introduction', 'contents', 'index']):
                        continue
                    
                    score = self._calculate_title_score(text, font_size, font_flags)
                    
                    if score > 0:
                        candidates.append((text, score, font_size))
        
        if candidates:
            candidates.sort(key=lambda x: x[1], reverse=True)
            return candidates[0][0]
        
        return None
    
    def _calculate_title_score(self, text: str, font_size: float, font_flags: int) -> float:
        score = 0.0
        
        if font_size > 16:
            score += 3.0
        elif font_size > 12:
            score += 2.0
        elif font_size > 10:
            score += 1.0
        
        if font_flags & 2**4:  # Bold flag
            score += 2.0
        
        word_count = len(text.split())
        if 3 <= word_count <= 10:  
            score += 1.0
        elif word_count > 15:  
            score -= 1.0
        
        if text.isupper():
            score += 1.0
        elif text.istitle():
            score += 0.5
        
        common_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        text_words = set(text.lower().split())
        if len(text_words.intersection(common_words)) > len(text_words) * 0.5:
            score -= 0.5
        
        return score
    
    def extract_headings(self, pages_content: List[Dict]) -> List[Dict[str, Any]]:

        headings = []
        
        for page_content in pages_content:
            page_num = page_content['page_num']
            page_headings = self._extract_headings_from_page(page_content)
            
            # Add page number to each heading
            for heading in page_headings:
                heading['page'] = page_num
                headings.append(heading)
        
        processed_headings = self._process_heading_hierarchy(headings)
        
        print(f"  Extracted {len(processed_headings)} headings")
        return processed_headings
    
    def _extract_headings_from_page(self, page_content: Dict) -> List[Dict[str, Any]]:
        """Extract potential headings from a single page."""
        text_dict = page_content.get('text_dict', {})
        plain_text = page_content.get('plain_text', '')
        
        candidates = []
        
        font_candidates = self._extract_by_font_analysis(text_dict)
        candidates.extend(font_candidates)
        
        pattern_candidates = self._extract_by_patterns(plain_text)
        candidates.extend(pattern_candidates)
        
        unique_candidates = self._deduplicate_candidates(candidates)
        
        return unique_candidates
    
    def _extract_by_font_analysis(self, text_dict: Dict) -> List[Dict[str, Any]]:
        """Extract headings based on font characteristics."""
        candidates = []
        
        if not text_dict or 'blocks' not in text_dict:
            return candidates
        
        font_sizes = []
        for block in text_dict['blocks']:
            if 'lines' not in block:
                continue
            for line in block['lines']:
                if 'spans' not in line:
                    continue
                for span in line['spans']:
                    size = span.get('size', 0)
                    if size > 0:
                        font_sizes.append(size)
        
        if not font_sizes:
            return candidates
        
        avg_size = sum(font_sizes) / len(font_sizes)
        max_size = max(font_sizes)
        
        for block in text_dict['blocks']:
            if 'lines' not in block:
                continue
                
            for line in block['lines']:
                if 'spans' not in line:
                    continue
                
                line_text = ''
                line_size = 0
                line_flags = 0
                
                for span in line['spans']:
                    line_text += span.get('text', '')
                    line_size = max(line_size, span.get('size', 0))
                    line_flags |= span.get('flags', 0)
                
                line_text = line_text.strip()
                
                if not line_text or len(line_text) < 3:
                    continue
                
                size_ratio = line_size / avg_size if avg_size > 0 else 1
                
                if size_ratio >= 1.2 or line_size >= avg_size + 2:
                    confidence = min(size_ratio, 3.0)
                    
                    if line_flags & 2**4:  # Bold
                        confidence += 0.5
                    
                    candidates.append({
                        'text': line_text,
                        'confidence': confidence,
                        'font_size': line_size,
                        'method': 'font_analysis'
                    })
        
        return candidates
    
    def _extract_by_patterns(self, plain_text: str) -> List[Dict[str, Any]]:
        """Extract headings based on text patterns."""
        candidates = []
        
        lines = plain_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or len(line) < 3:
                continue
            
            for pattern in self.heading_patterns:
                match = re.match(pattern, line)
                if match:
                    if match.groups():
                        heading_text = match.group(1).strip()
                    else:
                        heading_text = line.strip()
                    
                    if heading_text and len(heading_text) >= 3:
                        confidence = 1.0
                        
                        if any(char.isdigit() for char in line[:10]):
                            confidence += 0.5
                        
                        candidates.append({
                            'text': heading_text,
                            'confidence': confidence,
                            'pattern': pattern,
                            'method': 'pattern_matching'
                        })
                    break
        
        return candidates
    
    def _deduplicate_candidates(self, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        seen_texts = set()
        unique_candidates = []
        
        candidates.sort(key=lambda x: x.get('confidence', 0), reverse=True)
        
        for candidate in candidates:
            text = candidate['text'].lower().strip()
            
            if text in seen_texts:
                continue
            
            if len(text) < 3:
                continue
            
            if len(text) > 200:
                continue
            
            seen_texts.add(text)
            unique_candidates.append(candidate)
        
        return unique_candidates
    
    def _process_heading_hierarchy(self, headings: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not headings:
            return []
        
        sorted_headings = sorted(headings, key=lambda x: (
            x.get('confidence', 0),
            x.get('font_size', 0)
        ), reverse=True)
        
        processed = []
        font_size_to_level = {}
        
        for heading in sorted_headings:
            text = heading['text']
            font_size = heading.get('font_size', 12)
            page = heading['page']
            
            level = self._determine_heading_level(text, font_size, font_size_to_level)
            
            processed.append({
                'level': level,
                'text': text,
                'page': page
            })
        
        processed.sort(key=lambda x: x['page'])
        
        return processed
    
    def _determine_heading_level(self, text: str, font_size: float, 
                               font_size_to_level: Dict[float, str]) -> str:
        """Determine the hierarchy level (H1, H2, H3) for a heading."""
        
        if re.match(r'^\d+\.\s+', text):
            return 'H1'
        elif re.match(r'^\d+\.\d+\s+', text):
            return 'H2'
        elif re.match(r'^\d+\.\d+\.\d+\s+', text):
            return 'H3'
        
        if font_size in font_size_to_level:
            return font_size_to_level[font_size]
        
        existing_sizes = sorted(font_size_to_level.keys(), reverse=True)
        
        if not existing_sizes:
            font_size_to_level[font_size] = 'H1'
            return 'H1'
        
        if font_size > existing_sizes[0]:
            new_mapping = {font_size: 'H1'}
            for size in existing_sizes:
                current_level = font_size_to_level[size]
                if current_level == 'H1':
                    new_mapping[size] = 'H2'
                elif current_level == 'H2':
                    new_mapping[size] = 'H3'
                else:
                    new_mapping[size] = 'H3'
            font_size_to_level.update(new_mapping)
            return 'H1'
        
        elif font_size >= existing_sizes[0]:
            font_size_to_level[font_size] = 'H1'
            return 'H1'
        
        elif len(existing_sizes) == 1:
            font_size_to_level[font_size] = 'H2'
            return 'H2'
        
        else:
            font_size_to_level[font_size] = 'H3'
            return 'H3'
