from .._private.i_classdecls_extractor import IClassDeclsExtractor
from ..._private.e_parser_tool import ECodeParserTool

from .._private.treesitter_clsdeclsextr import TreeSitterClassDeclsExtractor



class ClassDeclsExtractorFactory:
	"""
		Represents a factory for each `IClassDeclsExtractor`
	"""
	
	
	@classmethod
	def create(
			cls,
			tool: ECodeParserTool,
	        class_code: str
	) -> IClassDeclsExtractor:
		"""
			Instantiates a new class focal code extractor that uses the specified parsing tool.
            
            Parameters
            ----------
                tool: ECodeParserTool
					An `ECodeParserTool` value representing the parsing tool that
                    the requested `IModuleDeclsExtractor` object must use
                    
                class_code: str
                    A string containing the Python class code to be associated
                    with the extractor
					
			Returns
            -------
                IClassDeclsExtractor
                    An `IClassDeclsExtractor` object that allows you to extract the core code
                    of the associated class using the specified tool
                    
            Raises
            ------
				ValueError
                    Occurs if:
                        
                        - The `class_code` parameter is `None`
                        - The `class_code` parameter is an empty string
		"""
		obj: IClassDeclsExtractor
		match tool:
			case ECodeParserTool.TREE_SITTER:
				obj = TreeSitterClassDeclsExtractor(class_code)
		
		return obj
		
		
	##	============================================================
	##						PRIVATE METHODS
	##	============================================================