from typing import List
from abc import ABC, abstractmethod



class IClassDeclsExtractor(ABC):
	"""
		Represents an object capable of extracting and separating the code of an associated Python class
        by breaking it down into the method declarations it contains.
        
        The code parser used is specified by the subclasses of this interface.
	"""
	
	
	@abstractmethod
	def decorators(self) -> List[str]:
		"""
			Retrieves the associated class decorators
            
            Returns
            -------
                List[str]
                    A list of strings containing the decorator names without the
                    preceding character `@`
		"""
		pass
	
	
	@abstractmethod
	def class_name(self) -> str:
		"""
			Returns the name of the class associated with this IClassDeclsExtractor
            
            Returns
            -------
                str
                    A string containing the name of the class associated with this object
		"""
		pass
	
	
	@abstractmethod
	def method_names(self) -> List[str]:
		"""
			Retrieves the names of the methods defined within the associated class
            
            Returns
            -------
                List[str]
                    A list of strings containing the names of the methods defined within
                    the associated class
		"""
		pass
	
	
	@abstractmethod
	def methods(self) -> List[str]:
		"""
			Retrieves the method definitions contained within the associated class
            
            Returns
            -------
                List[str]
                    A list of strings containing the method definitions
                    contained within the associated class
		"""
		pass