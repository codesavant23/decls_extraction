from typing import List, FrozenSet
from .. import IClassDeclsExtractor

from tree_sitter import (
	Language, Parser, Tree,
	Node as TreeNode
)
from tree_sitter_python import language as py_grammar



class TreeSitterClassDeclsExtractor(IClassDeclsExtractor):
	"""
		Represents an `IClassDeclsExtractor` that is implemented using
        the Python `tree-sitter` library
	"""
	
	_METHS_TIPOLOGY: FrozenSet[str] = { "function_definition", "async_function_definition" }
	
	def __init__(
			self,
			class_code: str
	):
		"""
			Creates a new TreeSitterClassDeclsExtractor
            
            Parameters
            ----------
                class_code: str
                    A string containing the code of the Python class from which
                    to extract method declarations
			
			Raises
            ------
                ValueError
                    Occurs if:
                        
                        - The `class_code` parameter is `None`
                        - The `class_code` parameter is an empty string
                        - The provided code is not a Python class definition
		"""
		if (class_code is None) or (class_code == ""):
			raise ValueError()
		
		py_parser: Parser = Parser(Language(py_grammar()))
		
		self._module_source: bytes = class_code.encode("utf-8")
		module_cst: Tree = py_parser.parse(self._module_source)
		
		class_node: TreeNode = module_cst.root_node.named_child(0)
		
		self._assert_classcode_valid(class_node)
		
		self._class: TreeNode = class_node
	
	
	def class_name(self) -> str:
		class_node: TreeNode = self._get_classdef_node()
		
		return class_node.child_by_field_name("name").text.decode("utf-8")
	
	
	def method_names(self) -> List[str]:
		class_node: TreeNode = self._get_classdef_node()
		
		classbody_node: TreeNode = class_node.child_by_field_name("body")
		
		if classbody_node is None:
			return []
		
		class_methods: List[str] = self._extract_methods(classbody_node, with_code=False)
		return class_methods
	
	
	def methods(self) -> List[str]:
		class_node: TreeNode = self._get_classdef_node()
		
		classbody_node: TreeNode = class_node.child_by_field_name("body")
		
		if classbody_node is None:
			return []
		
		class_methods: List[str] = self._extract_methods(classbody_node, with_code=True)
		return class_methods
	
	
	##	============================================================
	##						PRIVATE METHODS
	##	============================================================
	
	
	@classmethod
	def _assert_classcode_valid(
			cls,
			class_node: TreeNode
	):
		"""
			Checks whether the provided node represents a Python class.
            
            If the check succeeds, this operation is equivalent to a no-op
            
            Parameters
            ----------
				class_node: TreeNode
                    A `tree_sitter.Node` object representing the node, which should be
                    a Python class
            
            Raises
            ------
                ValueError
                    Occurs if `class_node` is not a Python class
		"""
		if (class_node is None):
			raise ValueError()
		if (class_node.type == "decorated_definition"):
			if (class_node.child_by_field_name("definition").type != "class_definition"):
				raise ValueError()
		elif (class_node.type != "class_definition"):
			raise ValueError()
	
	
	def _extract_methods(
			self,
			classbody_node: TreeNode,
			with_code: bool
	) -> List[str]:
		"""
			Extracts the definitions of functions that are part of the specified module file.
            It's possible to choose whether to extract the body of the definition or just
            the name of each method found
            
            Parameters
            ----------
				with_code: bool
                    A boolean indicating whether to extract the code from the definition
                    of each method
		"""
		name_only: bool = (not with_code)
		class_methods: List[str] = []
		poss_method: TreeNode
		meth_name: str
		for stmt in classbody_node.named_children:
			poss_method = None
			
			if stmt.type == "decorated_definition":
				# Estrazione metodo decorato
				poss_method = stmt.child_by_field_name("definition")
			else:
				# Estrazione metodo classico
				poss_method = stmt
				
			if poss_method is not None:
				self._add_ifmeth_tolist(stmt, class_methods, name_only)
		
		return class_methods
	
	
	def _add_ifmeth_tolist(
			self,
			node: TreeNode,
			list_: List[str],
			name_only: bool = True
	):
		"""
			Adds the "name" attribute, or the "block" attribute, of the provided node to the given list,
            if and only if the provided node is a method.
            
            Parameters
            ----------
				node: TreeNode
                    A `TreeNode` object representing the potential Python method whose
                    name is to be added to the given list
                
                list_: List[str]
                    A list of strings indicating the list to which the definition
                    of the node should be added if it represents a Python method
					
				name_only: bool
                    Optional. Default = `True`. A boolean indicating whether only
                    the method name should be extracted. If this parameter is `False`,
                    the entire method code will be added to the list
		"""
		needed: str
		if node.type in self._METHS_TIPOLOGY:
			if name_only:
				needed = node.child_by_field_name("name").text.decode("utf-8")
			else:
				needed = self._module_source[node.start_byte:node.end_byte].decode("utf-8")
			list_.append(needed)
		
		
	def _get_classdef_node(self) -> TreeNode:
		"""
			Returns the node containing the class definition without
			any decorators
            
            Returns
            -------
				TreeNode
                    A `tree_sitter.Node` object representing the node with the definition
                    of the Python class set as the node at the `self._class` attribute
		"""
		class_node: TreeNode
		if self._class.type == "class_definition":
			class_node = self._class
		else:
			class_node = self._class.child_by_field_name("definition")
			
		return class_node