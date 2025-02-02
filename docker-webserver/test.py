import unittest
from compiler import Parser, Compiler, Node

class TestCompiler(unittest.TestCase):
    def setUp(self):
        self.translation = {
            'p': 'p',
            'd': 'div'
        }
        self.styles = {
            'bold': 'font-weight: bold',
            'color': 'color: {}',
            'size': 'font-size: {}'
        }

    def test_simple_text(self):
        input_text = """[
            p{Test text}
        ]"""
        
        parser = Parser(input_text)
        tokens = parser.tokenize()
        compiler = Compiler(tokens)
        root = compiler.compile()
        
        html = Compiler.compile_to_html(root, self.translation, self.styles)
        expected = '<p>Test text</p>'
        self.assertEqual(html.strip(), expected)

    def test_nested_text(self):
        input_text = """[
            d[
                p{Test text}
            ]
        ]"""
        
        parser = Parser(input_text)
        tokens = parser.tokenize()
        compiler = Compiler(tokens)
        root = compiler.compile()
        
        html = Compiler.compile_to_html(root, self.translation, self.styles)
        expected = '<div><p>Test text</p></div>'
        self.assertEqual(html.strip(), expected)

    def test_style_application(self):
        input_text = """[
            s-text(style="bold color(red)")
            p{Test text}(class="text")
        ]"""
        
        parser = Parser(input_text)
        tokens = parser.tokenize()
        compiler = Compiler(tokens)
        root = compiler.compile()
        
        html = Compiler.compile_to_html(root, self.translation, self.styles)
        expected = '<p class="text" style="font-weight: bold; color: red">Test text</p>'
        self.assertEqual(html.strip(), expected)

    def test_multiple_styles(self):
        input_text = """[
            s-header(style="color(blue) size(24px)")
            p{Header}(class="header")
        ]"""
        
        parser = Parser(input_text)
        tokens = parser.tokenize()
        compiler = Compiler(tokens)
        root = compiler.compile()
        
        html = Compiler.compile_to_html(root, self.translation, self.styles)
        expected = '<p class="header" style="color: blue; font-size: 24px">Header</p>'
        self.assertEqual(html.strip(), expected)

if __name__ == '__main__':
    unittest.main()