import os, pytest

import grg_pssedata

class TestDiff:
    def setup_method(self, _):
        """Parse a real network file"""
        test_path = os.path.dirname(os.path.realpath(__file__))
        self.case_1 = grg_pssedata.io.parse_psse_case_file(test_path+'/data/correct/powermodels/case5.raw')
        self.case_2 = grg_pssedata.io.parse_psse_case_file(test_path+'/data/correct/powermodels/frankenstein_20.raw')
        self.case_3 = grg_pssedata.io.parse_psse_case_file(test_path+'/data/correct/powermodels/three_winding_test.raw')
        self.case_4 = grg_pssedata.io.parse_psse_case_file(test_path+'/data/correct/pglib_opf_case73_ieee_rts.raw')
        self.case_5 = grg_pssedata.io.parse_psse_case_file(test_path+'/data/correct/WECC240_M21_psse33_v01b.raw')

    def test_001(self):
        count = grg_pssedata.cmd.diff(self.case_1, self.case_2)
        assert(count == 17)

    def test_002(self):
        count = grg_pssedata.cmd.diff(self.case_2, self.case_3)
        assert(count == 17)

    def test_003(self):
        count = grg_pssedata.cmd.diff(self.case_3, self.case_4)
        assert(count == 349)

    def test_004(self):
        count = grg_pssedata.cmd.diff(self.case_4, self.case_5)
        assert(count == 678)

    def test_005(self):
        count = grg_pssedata.cmd.diff(self.case_2, self.case_5)
        assert(count == 1011)


class TestEq:
    def setup_method(self, _):
        """Parse a real network file"""
        test_path = os.path.dirname(os.path.realpath(__file__))
        self.case_1 = grg_pssedata.io.parse_psse_case_file(test_path+'/data/correct/powermodels/case5.raw')
        self.case_2 = grg_pssedata.io.parse_psse_case_file(test_path+'/data/correct/powermodels/case5.raw')
        self.case_3 = grg_pssedata.io.parse_psse_case_file(test_path+'/data/correct/powermodels/case14.raw')

    def test_001(self):
        equiv = grg_pssedata.cmd.eq(self.case_1, self.case_2)
        assert(equiv)

    def test_002(self):
        equiv = grg_pssedata.cmd.eq(self.case_2, self.case_3)
        assert(not equiv)


class TestCLI:
    def setup_method(self, _):
        """Parse a real network file"""
        self.parser = grg_pssedata.cmd.build_cmd_parser()

        test_path = os.path.dirname(os.path.realpath(__file__))
        self.case_1_file = test_path+'/data/correct/powermodels/case5.raw'
        self.case_2_file = test_path+'/data/correct/powermodels/case5.raw'
        self.case_3_file = test_path+'/data/correct/powermodels/case14.raw'

    def test_diff_001(self):
        args = self.parser.parse_args(['diff', self.case_1_file, self.case_2_file])
        count = grg_pssedata.cmd.main(args)
        assert(count == 0)

    def test_diff_001(self):
        args = self.parser.parse_args(['diff', self.case_2_file, self.case_3_file])
        count = grg_pssedata.cmd.main(args)
        assert(count == 37)

    def test_eq_001(self):
        args = self.parser.parse_args(['eq', self.case_1_file, self.case_2_file])
        equiv = grg_pssedata.cmd.main(args)
        assert(equiv)

    def test_eq_002(self):
        args = self.parser.parse_args(['eq', self.case_2_file, self.case_3_file])
        equiv = grg_pssedata.cmd.main(args)
        assert(not equiv)


class TestParsing:
    def setup_method(self, _):
        """Parse a network file"""
        test_path = os.path.dirname(os.path.realpath(__file__))
        self.case_1 = grg_pssedata.io.parse_psse_case_file(test_path+'/data/correct/powermodels/parser_test_a.raw')

    def test_001(self):
        assert(len(self.case_1.buses) == 2)
