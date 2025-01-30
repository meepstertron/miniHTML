from enum import Enum
from typing import List, Dict

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
                while i < len(self.text) and self.text[i] != ')':
                    attr_content.append(self.text[i])
                    i += 1
                i += 1
                tokens.append(Token(TokenType.ATTRIBUTE, ''.join(attr_content)))
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

        # Process ATTRIBUTE(s)
        while self.pos < len(self.tokens) and self.tokens[self.pos].type == TokenType.ATTRIBUTE:
            node.attributes = self.parse_attributes(self.tokens[self.pos].value)
            self.pos += 1

        # Process TEXT
        if self.pos < len(self.tokens) and self.tokens[self.pos].type == TokenType.TEXT:
            node.content = self.tokens[self.pos].value
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
    def compile_to_html(element: Node, translation: dict) -> str:
        def process_node(node: Node) -> str:
            if not node.tag:
                return ""

            # Convert s- tags to divs with class
            if node.tag.startswith('s-'):
                class_name = node.tag[2:]  # Get class after s- prefix
                node.tag = 'div'
                node.attributes['class'] = class_name

            # Translate tag name
            translated_tag = translation.get(node.tag, node.tag)
            
            # Build HTML
            html = [f"<{translated_tag}"]
            for k, v in node.attributes.items():
                html.append(f' {k}="{v}"')
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
}

# Test the corrected parser
text = """[
    s-container(style="background-color: red;")
    s-join-text(style="color: green;")
    d[
        br()
        p{Hack Club!}
        i(src="hack.club",alt="Hackclub")
    ]
    d[
        br()
        p{Join NOW!}(class="join-text")
        l(href="hack.club"){Join Hackclub.}
    ](class="container")
]"""
# Remove newlines but KEEP SPACES and other formatting
cleaned_text = text.replace('\n', '')  # Only remove newlines, not spaces
parser = Parser(cleaned_text)
tokens = parser.tokenize()
print("Tokens:", tokens)

compiler = Compiler(tokens)
root = compiler.compile()

print("Root children:", [child.tag for child in root.children])  # Should output ['d', 'd']

def print_tree(node: Node, indent: int = 0):
    print(' ' * indent + f"Tag: {node.tag}, Attributes: {node.attributes}, Content: {node.content}")
    for child in node.children:
        print_tree(child, indent + 2)

print_tree(root)

html = Compiler.compile_to_html(root, translation)
print("\nGenerated HTML:")
print(html)