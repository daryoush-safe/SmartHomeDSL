from antlr4 import *
import argparse


from CustomListener import CustomListener #make customListner -> class customListener(<grammar Name>Listener) -> automatically overrides
from gen.SmartHomeStateMachineLexer import SmartHomeStateMachineLexer #////
from gen.SmartHomeStateMachineParser import SmartHomeStateMachineParser #////
from required_code_collection.ast_to_networkx_graph import show_ast



def main(args):
    stream = FileStream(args.input, encoding='utf8')
    lexer = SmartHomeStateMachineLexer(stream)
    token_stream = CommonTokenStream(lexer)
    parser = SmartHomeStateMachineParser(token_stream)
    parse_tree = parser.program()
    ast_builder_listener = CustomListener()
    ast_builder_listener.rule_names = parser.ruleNames
    walker = ParseTreeWalker()
    walker.walk(t=parse_tree, listener=ast_builder_listener)
    ast = ast_builder_listener.ast
    traversal = ast.traverse_ast(ast.root)
    # print(traversal)
    show_ast(ast.root)






if __name__ == '__main__':
	argparser = argparse.ArgumentParser()
	argparser.add_argument('-i', '--input', help='Input source', default=f'test2.txt')
	argparser.add_argument('-o', '--output', help='Output path', default=f'out.txt')
	args = argparser.parse_args()
	main(args)
