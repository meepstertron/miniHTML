from enum import Enum
import logging
from typing import List, Dict

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class TokenType(Enum):
    OPEN_BRACKET = '['
    CLOSE_BRACKET = ']'
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
        self.tag: str = ""
        self.attributes: Dict[str, str] = {}
        self.content: str = ""
        self.children: List[Node] = []

class Parser:
    def __init__(self, text: str):
        self.text = text

    def tokenize(self) -> List[Token]:
        tokens = []
        i = 0
        while i < len(self.text):
            char = self.text[i]
            if char.isspace():
                i += 1
                continue
            if char == '{':
                i += 1
                text_content = []
                while i < len(self.text) and self.text[i] != '}':
                    text_content.append(self.text[i])
                    i += 1
                i += 1
                tokens.append(Token(TokenType.TEXT, ''.join(text_content)))
                continue
            if char == '(':
                i += 1
                attr_content = []
                in_quotes = False
                while i < len(self.text):
                    current_char = self.text[i]
                    if current_char == '"':
                        in_quotes = not in_quotes
                    elif current_char == ')' and not in_quotes:
                        break
                    attr_content.append(current_char)
                    i += 1
                tokens.append(Token(TokenType.ATTRIBUTE, ''.join(attr_content)))
                i += 1  # Skip the closing ')'
                continue
            if char in '[]':
                token_type = TokenType.OPEN_BRACKET if char == '[' else TokenType.CLOSE_BRACKET
                tokens.append(Token(token_type, char))
                i += 1
                continue
            if self.is_tag_char(char):
                start = i
                while i < len(self.text) and self.is_tag_char(self.text[i]):
                    i += 1
                tag = self.text[start:i]
                tokens.append(Token(TokenType.TAG, tag))
                continue
            i += 1
        return tokens

    def is_tag_char(self, c: str) -> bool:
        return c.isalnum() or c in '-_.'

    def parse_node(self, node: Node):
        if self.pos >= len(self.tokens):
            return

        # Process TAG (mandatory for non-root nodes)
        if self.tokens[self.pos].type == TokenType.TAG:
            node.tag = self.tokens[self.pos].value
            self.pos += 1
        else:
            return  # Invalid structure if there's no TAG

        # Process ATTRIBUTE(s) immediately after TAG
        while self.pos < len(self.tokens) and self.tokens[self.pos].type == TokenType.ATTRIBUTE:
            attrs = self.parse_attributes(self.tokens[self.pos].value)
            node.attributes.update(attrs)
            self.pos += 1

        # Process TEXT
        if self.pos < len(self.tokens) and self.tokens[self.pos].type == TokenType.TEXT:
            node.content = self.tokens[self.pos].value
            self.pos += 1

        # Process ATTRIBUTE(s) after TEXT
        while self.pos < len(self.tokens) and self.tokens[self.pos].type == TokenType.ATTRIBUTE:
            attrs = self.parse_attributes(self.tokens[self.pos].value)
            node.attributes.update(attrs)
            self.pos += 1

        # Process children if there's an OPEN_BRACKET
        if self.pos < len(self.tokens) and self.tokens[self.pos].type == TokenType.OPEN_BRACKET:
            self.pos += 1
            while self.pos < len(self.tokens) and self.tokens[self.pos].type != TokenType.CLOSE_BRACKET:
                if self.tokens[self.pos].type == TokenType.TAG:
                    child = Node()
                    self.parse_node(child)
                    node.children.append(child)
                else:
                    # Skip unexpected tokens within child brackets
                    self.pos += 1
            if self.pos < len(self.tokens) and self.tokens[self.pos].type == TokenType.CLOSE_BRACKET:
                self.pos += 1  # Skip CLOSE_BRACKET

class Compiler:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def compile(self) -> Node:
        root = Node()
        if self.pos < len(self.tokens) and self.tokens[self.pos].type == TokenType.OPEN_BRACKET:
            self.pos += 1  # Skip root OPEN_BRACKET
            # Parse root children (nodes inside the outermost brackets)
            while self.pos < len(self.tokens) and self.tokens[self.pos].type != TokenType.CLOSE_BRACKET:
                if self.tokens[self.pos].type == TokenType.TAG:
                    child = Node()
                    self.parse_node(child)
                    root.children.append(child)
                else:
                    # Skip unexpected tokens to avoid infinite loops
                    self.pos += 1
            self.pos += 1  # Skip root CLOSE_BRACKET
        return root

    def parse_node(self, node: Node):
        if self.pos >= len(self.tokens):
            return

        # Process TAG (mandatory for non-root nodes)
        if self.tokens[self.pos].type == TokenType.TAG:
            node.tag = self.tokens[self.pos].value
            self.pos += 1
        else:
            return  # Invalid structure if there's no TAG

        # Process ATTRIBUTE(s) immediately after TAG
        while self.pos < len(self.tokens) and self.tokens[self.pos].type == TokenType.ATTRIBUTE:
            attrs = self.parse_attributes(self.tokens[self.pos].value)
            node.attributes.update(attrs)  # Merge attributes
            self.pos += 1

        # Process TEXT
        if self.pos < len(self.tokens) and self.tokens[self.pos].type == TokenType.TEXT:
            node.content = self.tokens[self.pos].value
            self.pos += 1

        # Process ATTRIBUTE(s) after TEXT
        while self.pos < len(self.tokens) and self.tokens[self.pos].type == TokenType.ATTRIBUTE:
            attrs = self.parse_attributes(self.tokens[self.pos].value)
            node.attributes.update(attrs)  # Merge attributes
            self.pos += 1

        # Process children if there's an OPEN_BRACKET
        if self.pos < len(self.tokens) and self.tokens[self.pos].type == TokenType.OPEN_BRACKET:
            self.pos += 1
            while self.pos < len(self.tokens) and self.tokens[self.pos].type != TokenType.CLOSE_BRACKET:
                if self.tokens[self.pos].type == TokenType.TAG:
                    child = Node()
                    self.parse_node(child)
                    node.children.append(child)
                else:
                    # Skip unexpected tokens within child brackets
                    self.pos += 1
            if self.pos < len(self.tokens) and self.tokens[self.pos].type == TokenType.CLOSE_BRACKET:
                self.pos += 1  # Skip CLOSE_BRACKET

    def parse_attributes(self, attr_str: str) -> Dict[str, str]:
        pairs = {}
        current_key = []
        current_value = []
        parsing_key = True
        in_quotes = False

        i = 0
        while i < len(attr_str):
            c = attr_str[i]
            if c == '"' and not in_quotes:
                in_quotes = True
                i += 1
                continue
            elif c == '"' and in_quotes:
                in_quotes = False
                i += 1
                continue

            if in_quotes:
                current_value.append(c)
                i += 1
            else:
                if c == '=' and parsing_key:
                    parsing_key = False
                    i += 1
                elif c in ', ' and not parsing_key and not in_quotes:
                    key = ''.join(current_key).strip()
                    value = ''.join(current_value).strip()
                    if key:
                        pairs[key] = value
                    current_key = []
                    current_value = []
                    parsing_key = True
                    i += 1
                else:
                    if parsing_key:
                        current_key.append(c)
                    else:
                        current_value.append(c)
                    i += 1

        if current_key and current_value:
            key = ''.join(current_key).strip()
            value = ''.join(current_value).strip()
            pairs[key] = value

        return pairs
    
    @staticmethod
    def compile_to_html(element: Node, translation: dict, styles: dict) -> str:
        globalstyles = {}  # Class-based styles storage

        def parse_style(style_str):
            styles_list = []
            current_style = ''
            paren_count = 0
            
            for char in style_str:
                if char == '(' and paren_count == 0:
                    paren_count += 1
                elif char == ')' and paren_count > 0:
                    paren_count -= 1
                elif char == ' ' and paren_count == 0:
                    if current_style:
                        styles_list.append(current_style)
                        current_style = ''
                    continue
                current_style += char
            
            if current_style:
                styles_list.append(current_style)
            
            return styles_list

        def process_style(style_directive):
            if '(' in style_directive:
                name, value = style_directive.split('(', 1)
                value = value.rstrip(')')
                if name in styles:
                    return styles[name].format(value)
            elif style_directive in styles:
                return styles[style_directive]
            return style_directive

        def process_node(node: Node) -> str:
            if not node.tag:
                return ""
            
            # Handle style definition nodes (s- tags)
            if node.tag.startswith('s-'):
                # Remove s- prefix when storing the style
                class_name = node.tag[2:]  # 'text' from 's-text'
                globalstyles[class_name] = node.attributes.copy()
                return ""  # No output for style definitions

            translated_tag = translation.get(node.tag, node.tag)
            combined_styles = []
            attributes = node.attributes.copy()

            # Apply styles from classes
            if 'class' in attributes:
                classes = attributes['class'].split()  # Split multiple classes
                for class_name in classes:
                    if class_name in globalstyles:
                        style_def = globalstyles[class_name].get('style', '')
                        directives = style_def.split()
                        for directive in directives:
                            if '(' in directive:
                                style_name, params_part = directive.split('(', 1)
                                params = params_part.rstrip(')').split(',')
                                if style_name in styles:
                                    css = styles[style_name].format(*[p.strip() for p in params])
                                    combined_styles.append(css)
                            else:
                                if directive in styles:
                                    combined_styles.append(styles[directive])

            # Handle inline styles
            if 'style' in attributes:
                style_value = attributes.pop('style')
                style_directives = parse_style(style_value)
                processed_styles = [process_style(directive) for directive in style_directives]
                combined_styles.extend(processed_styles)

            # Build final HTML
            html_attrs = []
            for k, v in attributes.items():
                html_attrs.append(f'{k}="{v}"')
            if combined_styles:
                html_attrs.append(f'style="{"; ".join(combined_styles)}"')

            # Construct HTML element
            html = [f"<{translated_tag}"]
            if html_attrs:
                html.append(" " + " ".join(html_attrs))
            html.append(">")
            
            if node.content:
                html.append(node.content)
                
            for child in node.children:
                html.append(process_node(child))
                
            html.append(f"</{translated_tag}>")
            return "".join(html)
        
        return "".join(process_node(child) for child in element.children)

translation = {
    "d": "div",
    "p": "p",
    "br": "br",
    "i": "img",
    "l": "a",
    "hl": "h1",
    "hm": "h2",
    "hs": "h3",
    "hss": "h4",
    "hsss": "h5",
    "hline": "hr",
}

# Add near the bottom of the file where other dictionaries are defined
styles = {
    'bold': 'font-weight: bold',
    'italic': 'font-style: italic',
    'underline': 'text-decoration: underline',
    'strike': 'text-decoration: line-through',
    'text-center': 'text-align: center',
    'text-right': 'text-align: right',
    'card': 'border: 1px solid #ddd; border-radius: 8px; padding: 15px; margin: 10px 0',
    'color': 'color: {}',
    'size': 'font-size: {}',
    'font': 'font-family: {}',
    'background': 'background-color: {}',
    'padding': 'padding: {}',
    'margin': 'margin: {}',
    'm': 'margin: {}',
    'p': 'padding: {}',
    'codeblock': 'background-color: #f4f4f4; padding: 10px; border-left: 3px solid #ccc',
    'width': 'width: {}',
    'height': 'height: {}',
    'width-height': 'width: {}; height: {}',
}
