from typing import List, FrozenSet
from .. import AMutableModuleDeclsExtractor

from tree_sitter import (
	Language, Parser,
	Node as TreeNode
)
from tree_sitter_python import language as py_grammar
from textwrap import dedent as tw_dedent
# ============= RegEx Utilities ============ #
from regex import (
	sub as reg_replace,
	RegexFlag as RegexFlags,
)
# ========================================== #

from ..._private.e_parser_tool import ECodeParserTool
from ...classdecls_extractor import (
	ClassDeclsExtractorFactory,
	IClassDeclsExtractor
)



class TreeSitterModuleDeclsExtractor(AMutableModuleDeclsExtractor):
	"""
		Represents an `AMutableModuleDeclsExtractor` that is implemented using
        the Python `tree-sitter` library
	"""
	
	_4WHSPACES_PATT: str = r"(?m)(?: {4})+?"
	_FUNCS_TIPOLOGY: FrozenSet[str] = {"function_definition", "async_function_definition"}
	
	def __init__(
			self,
			module_code: str
	):
		"""
			Creates a new TreeSitterModuleDeclsExtractor by providing the first module file
            from which to extract function and class declarations
            
            Parameters
            ----------
				module_code: str
                    A string containing the code of the module file from which to extract
                    the declarations
                    
            Raises
            ------
				ValueError
                    Occurs if:
                    
						- The provided string is empty
						- The `module_code` parameter is `None`
                        
                IncorrectModuleCodeError
                    Occurs if the module code contains syntax errors
		"""
		super().__init__(module_code)
		
		self._py_parser: Parser = Parser(Language(py_grammar()))
		
		self._module_source: bytes = module_code.encode("utf-8")
		self._module: TreeNode = self._py_parser.parse(self._module_source).root_node
	
	
	def set_module_code(self, module_code: str):
		super().set_module_code(module_code)
		
		self._module = self._py_parser.parse(module_code.encode()).root_node
	
	
	def extract_funcnames(self) -> List[str]:
		mod_funcsnames: List[str] = self._extract_functions(with_code=False)
				
		return mod_funcsnames
	
	
	def extract_funcs(self) -> List[str]:
		mod_funcs: List[str] = self._extract_functions(with_code=True)
		for i, funct in enumerate(mod_funcs):
			mod_funcs[i] = tw_dedent(reg_replace(
				self._4WHSPACES_PATT, "\t",
				funct,
				flags=RegexFlags.MULTILINE
			))
		
		return mod_funcs
	
	
	def extract_classes(self) -> List[IClassDeclsExtractor]:
		mod_classes: List[IClassDeclsExtractor] = []
		class_node: TreeNode
		class_code: str
		
		for mod_stmt in self._module.named_children:
			if mod_stmt.type == "class_definition":
				self._add_class_tolist(
					mod_stmt, mod_classes
				)
			elif mod_stmt.type == "decorated_definition":
				class_node = mod_stmt.child_by_field_name("definition")
				if (class_node is not None) and (class_node.type == "class_definition"):
					self._add_class_tolist(
						mod_stmt, mod_classes
					)
		
		return mod_classes


	##	============================================================
	##						PRIVATE METHODS
	##	============================================================


	def _extract_functions(self, with_code: bool) -> List[str]:
		"""
			Extracts the definitions of functions that are part of the specified module file.
            It's possible to choose whether to extract the body of the definition or just the name
            of each function found
            
            Parameters
            ----------
				with_code: bool
                    A boolean indicating whether to extract the code from the definition
                    of each function
		"""
		name_only: bool = (not with_code)
		mod_funcs: List[str] = []
		inner_node: TreeNode
		
		for mod_stmt in self._module.named_children:
			if mod_stmt.type == "decorated_definition":
				inner_node = mod_stmt.child_by_field_name("definition")
				if inner_node is not None:
					self._add_iffunc_tolist(
						inner_node, mod_funcs,
						name_only=name_only
					)
			else:
				self._add_iffunc_tolist(
					mod_stmt, mod_funcs,
					name_only=name_only
				)
				
		return mod_funcs


	def _add_iffunc_tolist(
			self,
			node: TreeNode,
			list_: List[str],
			name_only: bool = True
	):
		"""
			Adds the "name" attribute, or the "block" attribute, of the provided node to the given list,
            if and only if the provided node is a function.
            
            Parameters
            ----------
				node: TreeNode
                    A `TreeNode` object representing the potential Python function whose
                    name is to be added to the given list
                
                list_: List[str]
                    A list of strings indicating the list to which the definition
                    of the node should be added if it represents a Python function
					
				name_only: bool
                    Optional. Default = `True`. A boolean indicating whether only
                    the function name should be extracted. If this parameter is `False`,
                    the entire function code will be added to the list
		"""
		needed: str
		if node.type in self._FUNCS_TIPOLOGY:
			if name_only:
				needed = node.child_by_field_name("name").text.decode("utf-8")
			else:
				needed = self._module_source[node.start_byte:node.end_byte].decode("utf-8")
			list_.append(needed)
			
			
	@classmethod
	def _add_class_tolist(
			cls,
			node: TreeNode,
			list_: List[IClassDeclsExtractor]
	):
		"""
			Creates a code extractor for the provided class and adds it to the given list
            
            Parameters
            ----------
				node: TreeNode
                    A `TreeNode` object representing the Python class for which to create and add
                    the code extractor to the given list
                
                list_: List[str]
                    A list of `IClassDeclsExtractor` objects representing the list of
                    class code extractors
		"""
		class_code: str = node.text.decode("utf-8")
		list_.append(
			ClassDeclsExtractorFactory.create(
				ECodeParserTool.TREE_SITTER,
				class_code
			)
		)