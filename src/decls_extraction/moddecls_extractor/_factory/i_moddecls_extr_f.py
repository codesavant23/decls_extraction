from abc import ABC, abstractmethod
from .._private.i_moddecls_extractor import IModuleDeclsExtractor

from ..._private.e_parser_tool import ECodeParserTool



class IModuleDeclsExtractorFactory(ABC):
	"""
		Represents a factory for each `IModuleDeclsExtractor`.
        
        The abstract properties, characteristic of the instantiated specific implementations, are
        described by the subclasses of this interface.
	"""
	
	
	@abstractmethod
	def create(
			self,
			tool: ECodeParserTool,
	        module_code: str
	) -> IModuleDeclsExtractor:
		"""
			Instantiates a new module focal code extractor that uses the specified
            parsing tool
            
            Parameters
            ----------
                tool: ECodeParserTool
					An `ECodeParserTool` value representing the parsing tool that
                    the requested `IModuleDeclsExtractor` object must use
                    
                module_code: str
                    A string containing the Python module code to be associated
                    with the extractor
					
			Returns
            -------
                IModuleDeclsExtractor
                    An `IModuleDeclsExtractor` object that allows you to extract the core code
                    of the associated module using the specified tool
                    
            Raises
            ------
				ValueError
                    Occurs if:
                        
                        - The `module_code` parameter is `None`
                        - The `module_code` parameter is an empty string
						
				NotImplementedError
                    Occurs if the requested module extractor is not implemented in the component,
                    for the abstract properties characteristic of the instantiated `IModuleDeclsExtractor`s
                    specified by the descendants of this interface
		"""
		pass
		
		
	##	============================================================
	##						PRIVATE METHODS
	##	============================================================