import re
from typing import Dict, List, Any, Set


class FontAnalyzer:
    
    def __init__(self):
        self.font_cache = {}
    
    def analyze_font_distribution(self, text_dict: Dict) -> Dict[str, Any]:

        font_sizes = []
        font_names = []
        font_flags = []
        
        if 'blocks' not in text_dict:
            return {'sizes': [], 'names': [], 'flags': []}
        
        for block in text_dict['blocks']:
            if 'lines' not in block:
                continue
                
            for line in block['lines']:
                if 'spans' not in line:
                    continue
                    
                for span in line['spans']:
                    font_sizes.append(span.get('size', 12))
                    font_names.append(span.get('font', 'default'))
                    font_flags.append(span.get('flags', 0))
        
        return {
            'sizes': font_sizes,
            'names': font_names,
            'flags': font_flags,
            'avg_size': sum(font_sizes) / len(font_sizes) if font_sizes else 12,
            'max_size': max(font_sizes) if font_sizes else 12,
            'min_size': min(font_sizes) if font_sizes else 12
        }
    
    def is_heading_font(self, font_size: float, font_flags: int, 
                       avg_size: float, threshold: float = 1.2) -> bool:

        size_ratio = font_size / avg_size if avg_size > 0 else 1
        is_large = size_ratio >= threshold
        
        is_bold = bool(font_flags & 2**4)
        
        return is_large or is_bold
    
    def get_font_hierarchy(self, font_sizes: List[float]) -> Dict[float, int]:

        unique_sizes = sorted(set(font_sizes), reverse=True)
        hierarchy = {}
        
        for i, size in enumerate(unique_sizes[:3]):  # Only top 3 levels
            hierarchy[size] = i + 1
        
        return hierarchy


class TextProcessor:
    
    def __init__(self):
        self.stop_words = {
            'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 
            'with', 'by', 'from', 'about', 'into', 'through', 'during', 
            'before', 'after', 'above', 'below', 'up', 'down', 'out', 'off',
            'over', 'under', 'again', 'further', 'then', 'once'
        }
    
    def clean_text(self, text: str) -> str:

        if not text:
            return ""
        
        text = re.sub(r'\s+', ' ', text.strip())
        
        text = re.sub(r'[\x00-\x1f\x7f-\x9f]', '', text)
        
        text = text.replace('"', '"').replace('"', '"')
        text = text.replace(''', "'").replace(''', "'")
        text = text.replace('–', '-').replace('—', '-')
        
        return text
    
    def is_likely_heading(self, text: str) -> bool:

        if not text or len(text.strip()) < 3:
            return False
        
        text = text.strip()
        
        heading_patterns = [
            r'^\d+\.',                  
            r'^[A-Z][A-Z\s]*$',      
            r'^[A-Z][a-z]+(\s[A-Z][a-z]+)*$', 
            r'^(Chapter|Section|Part)\s+\d+',  
        ]
        
        for pattern in heading_patterns:
            if re.match(pattern, text):
                return True
        
        words = text.split()
        
        if not (2 <= len(words) <= 12):
            return False
        
        if text.endswith(('.', '!', '?')):
            return False
        
        non_stop_words = [w for w in words if w.lower() not in self.stop_words]
        if len(non_stop_words) < len(words) * 0.5:
            return False
        
        return True
    
    def extract_numbering(self, text: str) -> tuple:

        match = re.match(r'^(\d+(?:\.\d+)*)\.\s*(.+)$', text)
        if match:
            numbering = match.group(1)
            clean_text = match.group(2)
            level = len(numbering.split('.'))
            return (level, clean_text)
        
        match = re.match(r'^(\d+)\.\s*(.+)$', text)
        if match:
            clean_text = match.group(2)
            return (1, clean_text)
        
        match = re.match(r'^([A-Z])\.\s*(.+)$', text)
        if match:
            clean_text = match.group(2)
            return (2, clean_text)
        
        match = re.match(r'^([IVX]+)\.\s*(.+)$', text)
        if match:
            clean_text = match.group(2)
            return (1, clean_text)
        
        return (None, text)
    
    def calculate_text_complexity(self, text: str) -> float:

        if not text:
            return 0.0
        
        words = text.split()
        if not words:
            return 0.0
        
        avg_word_length = sum(len(word) for word in words) / len(words)
        
        sentences = len(re.split(r'[.!?]+', text))
        
        words_per_sentence = len(words) / max(sentences, 1)
        
        complexity = (avg_word_length * 0.5) + (words_per_sentence * 0.3)
        
        return complexity
    
    def split_into_sentences(self, text: str) -> List[str]:

        if not text:
            return []
        
        sentences = re.split(r'[.!?]+', text)
        
        cleaned_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence and len(sentence) > 3:
                cleaned_sentences.append(sentence)
        
        return cleaned_sentences
    
    def extract_keywords(self, text: str, top_k: int = 10) -> List[str]:

        if not text:
            return []
        
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        
        words = [word for word in words if word not in self.stop_words]
        
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        
        return [word for word, freq in sorted_words[:top_k]]
