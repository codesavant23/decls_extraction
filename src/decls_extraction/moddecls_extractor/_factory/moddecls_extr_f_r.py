from .i_moddecls_extr_f import IModuleDeclsExtractorFactory
from .e_moddeclsextr_chars import EModuleDeclsExtractorChars

from .mutable_moddeclsextr_f import MutableModuleDeclsExtractorFactory



class ModuleDeclsExtractorFactoryResolver:
	"""
		Represents a factory for each `IModuleDeclsExtractorFactory`
	"""
	
	
	@classmethod
	def create(
			cls,
			chars: EModuleDeclsExtractorChars,
	) -> IModuleDeclsExtractorFactory:
		"""
			Instantiates a new module focal code extractor with the specified
            abstract characteristics provided
            
            Parameters
            ----------
				chars: EModuleDeclsExtractorChars
                    An `EModuleDeclsExtractorChars` value representing the set of
                    abstract characteristics that the `IModuleDeclsExtractor` object
                    must have
                    
            Returns
            -------
				IModuleDeclsExtractorFactory
                    An `IModuleDeclsExtractorFactory` object that allows you to instantiate
                    extractors of the focal code with the specified abstract characteristics
		"""
		obj_f: IModuleDeclsExtractorFactory
		match chars:
			case EModuleDeclsExtractorChars.MUTABLE:
				obj_f = MutableModuleDeclsExtractorFactory()
		
		return obj_f
		
		
	##	============================================================
	##						PRIVATE METHODS
	##	============================================================