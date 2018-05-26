'''a collection of all grg_pssedata exception classes'''


class PSSEDataException(Exception):
    '''root class for all PSSEData Exceptions'''
    pass


class PSSEDataParsingError(PSSEDataException):
    '''for errors that occur while attempting to parse a pss/e data file'''
    pass


class PSSEDataValidationError(PSSEDataException):
    '''for errors that occur while attempting to validate the correctness of
        a parsed pss/e data file
    '''
    pass


class PSSEDataWarning(Warning):
    '''root class for all PSSEData Warnings'''
    pass
