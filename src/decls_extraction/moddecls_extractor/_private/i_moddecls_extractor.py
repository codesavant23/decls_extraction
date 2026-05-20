from typing import List
from abc import ABC, abstractmethod

from ...classdecls_extractor import IClassDeclsExtractor



class IModuleDeclsExtractor(ABC):
	"""
		It represents an object capable of extracting the declarations of an associated Python
		module file, separating its functions from the classes within it.
		
		The code parser used is specified by descendants of this interface.
	"""


	@abstractmethod
	def extract_funcnames(self) -> List[str]:
		"""
			Extracts the names of functions defined within the associated module file.
			
			Returns
			-------
				List[str]
					A list of strings containing the names of functions defined
					in the associated module file's namespace.
		"""
		pass
	
	
	@abstractmethod
	def extract_funcs(self) -> List[str]:
		"""
			Extracts function definitions from the associated module file.

			Returns
			-------
				List[str]
					A list of strings containing the function definitions found in the associated
					module file's namespace.
		"""
		pass
	
	
	@abstractmethod
	def extract_classes(self) -> List[IClassDeclsExtractor]:
		"""
			Extracts the classes defined in its namespace from the given module file.
			
			Returns
			-------
				List[IClassDeclsExtractor]
					A list of `IClassDeclsExtractor` objects, one for each class defined
					in the module file.
		"""
		pass