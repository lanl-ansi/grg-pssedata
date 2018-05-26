import pytest, warnings

import grg_pssedata

from test_common import warning_files

@pytest.mark.parametrize('input_data', warning_files)
def test_001(input_data):
    with pytest.warns(grg_pssedata.exception.PSSEDataWarning):
        case = grg_pssedata.io.parse_psse_case_file(input_data)
