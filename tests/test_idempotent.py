import os, pytest

import grg_pssedata

import warnings

from test_common import correct_files
from test_common import warning_files

@pytest.mark.parametrize('input_data', correct_files)
def test_001(input_data):
    case = grg_pssedata.io.parse_psse_case_file(input_data)
    psse_data = case.to_psse()
    case_2 = grg_pssedata.io.parse_psse_case_str(psse_data)
    diff_count = grg_pssedata.cmd.diff(case, case_2)

    assert diff_count <= 0 # checks full data structure
    assert not case != case_2
    assert str(case) == str(case_2) # checks string representation of data structure


@pytest.mark.parametrize('input_data', warning_files)
def test_002(input_data):
    case = grg_pssedata.io.parse_psse_case_file(input_data)
    psse_data = case.to_psse()
    case_2 = grg_pssedata.io.parse_psse_case_str(psse_data)
    diff_count = grg_pssedata.cmd.diff(case, case_2)

    assert diff_count <= 0 # checks full data structure
    assert not case != case_2
    assert str(case) == str(case_2) # checks string representation of data structure

