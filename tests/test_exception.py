import pytest

import grg_pssedata

from test_common import incorrect_files

@pytest.mark.parametrize('input_data', incorrect_files)
def test_001(input_data):
    #with pytest.raises(grg_pssedata.exception.PSSEDataException):
    with pytest.raises(BaseException):
        case = grg_pssedata.io.parse_psse_case_file(input_data)
