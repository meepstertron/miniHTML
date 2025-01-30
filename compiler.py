from enum import Enum
from typing import List, Dict, Any, Union

class TokenType(Enum):
    OPEN_BRACKET = '['
    CLOSE_BRACKET = ']'
    OPEN_CURLY = '{'
    CLOSE_CURLY = '}'
    OPEN_PAREN = '('
    CLOSE_PAREN = ')'
    TEXT = 'TEXT'
    TAG = 'TAG'
    ATTRIBUTE = 'ATTRIBUTE'
    
class Token:
    def __init__(self, type: TokenType, value: str):
        self.type = type
        self.value = value
    def __repr__(self) -> str:
        return f"Token({self.type}, '{self.value}')"
        

class Node:
    def __init__(self):
        self.tag: str
        self.attributes: Dict[str, str]
        self.content: str
        self.children: List[Node]
    

class Parser:
    def __init__(self, text: str):
        self.text = text
        self.tokens: List[Token] = []
        self.pos = 0
        
    def tokenize(self, text: str) -> List[Token]:
        tokens = []
        i = 0
        while i < len(text):
            char = text[i]
            
            # Skip whitespace
            if char.isspace():
                i += 1
                continue
                
            # Handle special characters
            if char in '[]{}()':
                token_type = {
                    '[': TokenType.OPEN_BRACKET,
                    ']': TokenType.CLOSE_BRACKET,
                    '{': TokenType.OPEN_CURLY,
                    '}': TokenType.CLOSE_CURLY,
                    '(': TokenType.OPEN_PAREN,
                    ')': TokenType.CLOSE_PAREN
                }[char]
                tokens.append(Token(token_type, char))
                i += 1
                continue
                
            # Handle text content
            if char == '{':
                i += 1  # Skip opening brace
                text_content = ""
                while i < len(text) and text[i] != '}':
                    text_content += text[i]
                    i += 1
                if text_content:  
                    tokens.append(Token(TokenType.TEXT, text_content))
                i += 1  
                continue
                
            # Handle attributes
            if char == '(':
                i += 1  
                attr_content = ""
                while i < len(text) and text[i] != ')':
                    attr_content += text[i]
                    i += 1
                if attr_content:  
                    tokens.append(Token(TokenType.ATTRIBUTE, attr_content))
                i += 1  
                continue
                
            # Handle tags
            if self.is_tag_char(char):
                start = i
                while i < len(text) and self.is_tag_char(text[i]):
                    i += 1
                tag = text[start:i]
                if tag:  
                    tokens.append(Token(TokenType.TAG, tag))
                continue
                
            i += 1
        return tokens
    
    def is_tag_char(self, c: str) -> bool:
        return c.isalnum() or c in '-_.'  
    
    def extract_until(text: str, end_char: str, start: int) -> tuple[str, int]:
        """Extract string until end_char"""
        result = []
        i = start
        while i < len(text) and text[i] != end_char:
            result.append(text[i])
            i += 1
        return ''.join(result), i
    
    def parse_attributes(self, attr_str: str) -> Dict[str, str]:
        pairs = {}
        current_key = ""
        current_value = ""
        i = 0
        
        while i < len(attr_str):
            char = attr_str[i]
            
            # Skip whitespace and commas
            if char in ' ,':
                i += 1
                continue
                
            # Parse key
            if not current_key:
                while i < len(attr_str) and attr_str[i] not in '=':
                    current_key += attr_str[i]
                    i += 1
                current_key = current_key.strip()
                i += 1  
                continue
                
            # Parse value
            if char == '"':
                i += 1  
                while i < len(attr_str) and attr_str[i] != '"':
                    current_value += attr_str[i]
                    i += 1
                i += 1  
            else:
                while i < len(attr_str) and attr_str[i] not in ', ':
                    current_value += attr_str[i]
                    i += 1
                    
            if current_key and current_value:
                pairs[current_key] = current_value
                current_key = ""
                current_value = ""
                
            i += 1
                
        return pairs

text = """[
    d[
        p{Hello!}
        i(src="example.com",alt="example")
    ]
]"""

print(Parser(text.replace('\n', '').replace(' ', '')).tokenize(text.replace('\n', '').replace(' ', '')))