from typing import List
from abc import abstractmethod
from .. import IModuleDeclsExtractor

# ============== OS Utilities ============== #
from os import remove as os_remove
from tempfile import gettempdir as os_tempdir
# ========================================== #
# ============ Path Utilities ============ #
from pathlib import Path as SystemPath
# ======================================== #
from datetime import datetime as DateTime
from py_compile import (
	compile as py_compile,
	PycInvalidationMode as Pyc_InvMode,
	PyCompileError
)

from ...classdecls_extractor import IClassDeclsExtractor

from ..exceptions import IncorrectModuleCodeError



class AMutableModuleDeclsExtractor(IModuleDeclsExtractor):
	"""
		Represents an ʻIModuleDeclsExtractor` whose associated module file code can be changed.
		
		The extraction implementation technology is specified by descendants of this interface.
	"""
	
	def __init__(
			self,
			module_code: str
	):
		"""
			Creates a new AMutableModuleDeclsExtractor by providing the first module file
            from which to extract function and class declarations
            
            Parameters
            ----------
				module_code: str
                    A string containing the code of the module file from which to extract
                    the declarations
                    
            Raises
            ------
                ValueError
                    Occurs if the `module_code` parameter is `None` or an empty string
		"""
		if (module_code is None) or (module_code == ""):
			raise ValueError()
		
		self._module_code: str = module_code


	def set_module_code(
			self,
	        module_code: str
	):
		"""
            Set the code of the next module file from which to extract any
            functions and/or classes

            Parameters
            ----------
				module_code: str
                    A string containing the code of the module file from which to extract, and
                    separate, any functions and/or classes
                    
            Raises
            ------
                ValueError
                    Occurs if:
					
						- The provided string is empty
						- The `module_code` parameter is `None`
                        
                IncorrectModuleCodeError
                    Occurs if the module code contains syntax errors
		"""
		if (module_code is None) or (module_code == ""):
			raise ValueError()
		
		self._assert_synt_correctness(module_code)
		
		self._module_code = module_code
		
	
	#	============================================================
	#						ABSTRACT METHODS
	#	============================================================


	@abstractmethod
	def extract_funcnames(self) -> List[str]:
		pass
	
	
	@abstractmethod
	def extract_funcs(self) -> List[str]:
		pass
	
	
	@abstractmethod
	def extract_classes(self) -> List[IClassDeclsExtractor]:
		pass
	
	
	#	============================================================
	#						PRIVATE METHODS
	#	============================================================
	
	
	def _pf_get_module_code(self) -> str:
		"""
			Returns the code of the last Python module file set
            
            Returns
            -------
                str
                    A string containing the code of the last Python
                    module file set
		"""
		return self._module_code
	
	
	@classmethod
	def _assert_synt_correctness(
			cls,
			module_code: str
	):
		"""
			Checks whether the code in the given module file is syntactically correct
            
            Parameters
            ----------
				module_code: str
                    A string containing the code of the module file to be checked
                    for syntactic correctness
                    
            Raises
            ------
                IncorrectModuleCodeError
                    Occurs if the module code contains syntactic errors
		"""
		now: DateTime = DateTime.now()
		tmpfile_name: str = (
				"tmp_" +
				f"{int(now.timestamp()*100)}" +
				".py"
		)
		tmpfile_path: SystemPath = SystemPath(os_tempdir(), tmpfile_name)
		
		with tmpfile_path.open("w") as ftemp:
			ftemp.write(module_code)
			ftemp.flush()
			
		try:
			py_compile(
				str(tmpfile_path),
				doraise=True,
				invalidation_mode=Pyc_InvMode.TIMESTAMP
			)
		except PyCompileError:
			os_remove(str(tmpfile_path))
			raise IncorrectModuleCodeError()
		
		os_remove(str(tmpfile_path))