import argparse
import os
import compiler
import logging

def main():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    parser = argparse.ArgumentParser(description='Process some arguments.')
    parser.add_argument('-d', '--directory', type=str, help='Directory to process')
    parser.add_argument('-o', '--output', type=str, help='Output directory')
    args = parser.parse_args()
    
    if args.directory:
        if not args.output:
            raise NameError("No output directory specified")
        logger.info(f"Directory specified: {args.directory}")
        logger.info(f"Output directory specified: {args.output}")

        items = os.walk(args.directory)

        for root, dirs, files in items:
            for file in files:
                if file.endswith((".minihtml", ".mhtml")):
                    with open(os.path.join(root, file), "r") as f:
                        text = f.read()
                        logger.info(f"File: {file}")
                        logger.info(f"Text: {text}")
                        parser = compiler.Parser(text)
                        tokens = parser.tokenize()
                        logger.info("Tokens: %s", tokens)
                        compiler_instance = compiler.Compiler(tokens)
                        root_node = compiler_instance.compile()
                        html = compiler.Compiler.compile_to_html(root_node, compiler.translation, compiler.styles)
                        logger.info("Generated HTML: %s", html)

                        output_file_path = os.path.join(args.output, file.replace(".minihtml", ".html").replace(".mhtml", ".html"))
                        with open(output_file_path, "w") as f:
                            f.write(html)
                        
    else:
        raise NameError("No directory specified")

if __name__ == "__main__":
    main()