from antlr4 import *
import argparse

from CustomListener import CustomListener
from gen.SmartHomeStateMachineLexer import SmartHomeStateMachineLexer
from gen.SmartHomeStateMachineParser import SmartHomeStateMachineParser

from required_code_collection.ast_to_networkx_graph import show_ast
from code_generator import CodeGenerator


def main(args):
    # --- Parse input file ---
    stream = FileStream(args.input, encoding='utf8')
    lexer = SmartHomeStateMachineLexer(stream)
    token_stream = CommonTokenStream(lexer)
    parser = SmartHomeStateMachineParser(token_stream)
    parse_tree = parser.program()

    # --- Build AST with CustomListener ---
    ast_builder_listener = CustomListener()
    ast_builder_listener.rule_names = parser.ruleNames
    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=ast_builder_listener)
    ast = ast_builder_listener.ast

    # --- Debug / visualization (optional) ---
    # traversal = ast.traverse_ast(ast.root)
    # print(traversal)
    # show_ast(ast.root)

    # --- Generate Arduino C++ code ---
    show_ast(ast.root)

    generator = CodeGenerator(ast.root)
    code = generator.generate()

    # --- Write to output file ---
    with open(args.output, "w") as f:
        f.write(code)

    print(f"Arduino code generated at {args.output}")

    # show_ast(ast.root)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-i', '--input', help='Input DSL source', default='./test/test5.txt')
    argparser.add_argument('-o', '--output', help='Output Arduino file', default='SmartHome.ino')
    args = argparser.parse_args()
    main(args)
