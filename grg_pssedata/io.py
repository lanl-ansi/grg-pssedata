from __future__ import print_function

import argparse
import functools
import re
import warnings
import sys
import collections

from grg_pssedata.struct import Bus
from grg_pssedata.struct import Load
from grg_pssedata.struct import FixedShunt
from grg_pssedata.struct import Generator
from grg_pssedata.struct import Branch
from grg_pssedata.struct import TwoWindingTransformer
from grg_pssedata.struct import ThreeWindingTransformer
from grg_pssedata.struct import TransformerParametersFirstLine
from grg_pssedata.struct import TransformerParametersSecondLine
from grg_pssedata.struct import TransformerParametersSecondLineShort
from grg_pssedata.struct import TransformerWinding
from grg_pssedata.struct import TransformerWindingShort
from grg_pssedata.struct import Area
from grg_pssedata.struct import Zone
from grg_pssedata.struct import Owner
from grg_pssedata.struct import SwitchedShunt
from grg_pssedata.struct import Case
from grg_pssedata.struct import TwoTerminalDCLine
from grg_pssedata.struct import TwoTerminalDCLineParameters
from grg_pssedata.struct import TwoTerminalDCLineRectifier
from grg_pssedata.struct import TwoTerminalDCLineInverter
from grg_pssedata.struct import VSCDCLine
from grg_pssedata.struct import VSCDCLineParameters
from grg_pssedata.struct import VSCDCLineConverter
from grg_pssedata.struct import TransformerImpedanceCorrection
from grg_pssedata.struct import MultiTerminalDCLine
from grg_pssedata.struct import MultiTerminalDCLineParameters
from grg_pssedata.struct import MultiTerminalDCLineConverter
from grg_pssedata.struct import MultiTerminalDCLineDCBus
from grg_pssedata.struct import MultiTerminalDCLineDCLink
from grg_pssedata.struct import MultiSectionLineGrouping
from grg_pssedata.struct import InterareaTransfer
from grg_pssedata.struct import FACTSDevice
from grg_pssedata.struct import InductionMachine

from grg_pssedata.exception import PSSEDataParsingError
from grg_pssedata.exception import PSSEDataWarning

LineRequirements = collections.namedtuple('LineRequirements',['line_index','min_values','max_values','section'])

print_err = functools.partial(print, file=sys.stderr)

psse_table_terminus = '0'
psse_record_terminus = 'Q'
psse_terminuses = [psse_table_terminus, psse_record_terminus]

def expand_commas(list):
    expanded_list = []
    for item in list:
        if not ',' in item:
            expanded_list.append(item)
        else:
            for i in range(0, item.count(',')-1):
                expanded_list.append(None)
    return expanded_list


def parse_psse_case_file(psse_file_name):
    '''opens the given path and parses it as pss/e data

    Args:
        psse_file_name(str): path to the a psse data file
    Returns:
        Case: a grg_pssedata case
    '''

    with open(psse_file_name, 'r') as psse_file:
        lines = psse_file.readlines()

    #try:
    psse_data = parse_psse_case_lines(lines)
    #except BaseException as e:
    #    raise PSSEDataParsingError('{}'.format(str(e)))

    return psse_data


def parse_psse_case_str(psse_string):
    '''parses a given string as matpower data

    Args:
        mpString(str): a matpower data file as a string
    Returns:
        Case: a grg_pssedata case
    '''

    lines = psse_string.split('\n')

    #try:
    psse_data = parse_psse_case_lines(lines)
    #except BaseException as e:
    #    raise PSSEDataParsingError('{}'.format(str(e)))

    return psse_data



def parse_line(line, line_reqs=None):
    line = line.strip()
    comment = None

    l = re.split(r"(?!\B[\"\'][^\"\']*)[\/](?![^\"\']*[\"\']\B)", line, maxsplit=1)
    if len(l) > 1:
        line, comment = l
    else:
        line = l[0]

    line_parts = re.split(r",(?=(?:[^']*'[^']*')*[^']*$)", line)

    if line_reqs is not None:
        if len(line_parts) < line_reqs.min_values:
            raise PSSEDataParsingError('on psse data line {} in the "{}" section, at least {} values were expected but only {} where found.\nparsed: {}'.format(line_reqs.line_index, line_reqs.section, line_reqs.min_values, len(line_parts), line_parts))
        if len(line_parts) > line_reqs.max_values:
            warnings.warn('on psse data line {} in the "{}" section, at most {} values were expected but {} where found, extra values will be ignored.\nparsed: {}'.format(line_reqs.line_index, line_reqs.section, line_reqs.max_values, len(line_parts), line_parts), PSSEDataWarning)
            line_parts = line_parts[:line_reqs.max_values]

    return line_parts, comment


def parse_psse_case_lines(lines):
    if len(lines) < 3: # need at base values and record
        raise PSSEDataParsingError('psse case has {} lines and at least 3 are required'.format(len(lines)))

    (ic, sbase, rev, xfrrat, nxfrat, basefrq), comment = parse_line(lines[0], LineRequirements(0, 6, 6, "header"))
    print_err('case data: {} {} {} {} {} {}'.format(ic, sbase, rev, xfrrat, nxfrat, basefrq))

    if len(ic.strip()) > 0 and not (ic.strip() == "0"): # note validity checks may fail on "change data"
        raise PSSEDataParsingError('ic value of {} given, only a value of 0 is supported'.format(ic))

    version_id = 33
    if len(rev.strip()) > 0:
        try:
            version_id = int(float(rev))
        except ValueError:
             warnings.warn('assuming PSSE version 33, given version value "{}".'.format(rev.strip()), PSSEDataWarning)

    if version_id != 33:
        warnings.warn('PSSE version {} given but only version 33 is supported, parser may not function correctly.'.format(rev.strip()), PSSEDataWarning)

    record1 = lines[1].strip('\n')
    record2 = lines[2].strip('\n')
    print_err('record 1: {}'.format(record1))
    print_err('record 2: {}'.format(record2))

    buses = []
    loads = []
    fixed_shunts = []
    generators = []
    branches = []
    transformers = []
    areas = []
    tt_dc_lines = []
    vsc_dc_lines = []
    transformer_corrections = []
    mt_dc_lines = []
    line_groupings = []
    zones = []
    transfers = []
    owners = []
    facts = []
    switched_shunts = []
    gnes = []
    induction_machines = []


    line_index = 3
    while parse_line(lines[line_index])[0][0].strip() not in psse_terminuses:
        line_parts, comment = parse_line(lines[line_index], LineRequirements(line_index, 13, 13, "bus"))
        buses.append(Bus(*line_parts))
        line_index += 1
    print_err('parsed {} buses'.format(len(buses)))
    if parse_line(lines[line_index])[0][0].strip() != psse_record_terminus:
        line_index += 1

    load_index_offset = line_index
    while parse_line(lines[line_index])[0][0].strip() not in psse_terminuses:
        line_parts, comment = parse_line(lines[line_index], LineRequirements(line_index, 13, 14, "load"))
        loads.append(Load(line_index - load_index_offset, *line_parts))
        line_index += 1
    print_err('parsed {} loads'.format(len(loads)))

    if parse_line(lines[line_index])[0][0].strip() != psse_record_terminus:
        line_index += 1

    fixed_shunt_index_offset = line_index
    while parse_line(lines[line_index])[0][0].strip() not in psse_terminuses:
        line_parts, comment = parse_line(lines[line_index], LineRequirements(line_index, 5, 5, "fixed shunt"))
        fixed_shunts.append(FixedShunt(line_index - fixed_shunt_index_offset, *line_parts))
        line_index += 1
    print_err('parsed {} fixed shunts'.format(len(fixed_shunts)))

    if parse_line(lines[line_index])[0][0].strip() != psse_record_terminus:
        line_index += 1

    gen_index_offset = line_index
    while parse_line(lines[line_index])[0][0].strip() not in psse_terminuses:
        line_parts, comment = parse_line(lines[line_index], LineRequirements(line_index, 28, 28, "generator"))
        generators.append(Generator(line_index - gen_index_offset, *line_parts))
        line_index += 1
    print_err('parsed {} generators'.format(len(generators)))

    if parse_line(lines[line_index])[0][0].strip() != psse_record_terminus:
        line_index += 1

    branch_index_offset = line_index
    while parse_line(lines[line_index])[0][0].strip() not in psse_terminuses:
        #line = shlex.split(lines[line_index].strip())
        #line = expand_commas(line)
        line_parts, comment = parse_line(lines[line_index], LineRequirements(line_index, 24, 24, "branch"))
        #print(line_parts)
        branches.append(Branch(line_index - branch_index_offset, *line_parts))
        line_index += 1
    print_err('parsed {} branches'.format(len(branches)))

    if parse_line(lines[line_index])[0][0].strip() != psse_record_terminus:
        line_index += 1

    transformer_index = 0
    while parse_line(lines[line_index])[0][0].strip() not in psse_terminuses:
        line_parts_1, comment_1 = parse_line(lines[line_index], LineRequirements(line_index, 21, 21, "transformer"))
        parameters_1 = TransformerParametersFirstLine(*line_parts_1)
        #print(parameters_1)

        if parameters_1.k == 0: # two winding case
            line_parts_2, comment_2 = parse_line(lines[line_index+1], LineRequirements(line_index+1, 3, 3, "transformer"))
            line_parts_3, comment_3 = parse_line(lines[line_index+2], LineRequirements(line_index+1, 17, 17, "transformer"))
            line_parts_4, comment_4 = parse_line(lines[line_index+3], LineRequirements(line_index+1, 2, 2, "transformer"))

            parameters_2 = TransformerParametersSecondLineShort(*line_parts_2)
            winding_1 = TransformerWinding(1, *line_parts_3)
            winding_2 = TransformerWindingShort(2, *line_parts_4)

            t = TwoWindingTransformer(transformer_index, parameters_1, parameters_2, winding_1, winding_2)

            line_index += 4
        else: # three winding case
            line_parts_2, comment_2 = parse_line(lines[line_index+1], LineRequirements(line_index+1, 11, 11, "transformer"))
            line_parts_3, comment_3 = parse_line(lines[line_index+2], LineRequirements(line_index+2, 17, 17, "transformer"))
            line_parts_4, comment_4 = parse_line(lines[line_index+3], LineRequirements(line_index+3, 17, 17, "transformer"))
            line_parts_5, comment_5 = parse_line(lines[line_index+4], LineRequirements(line_index+4, 17, 17, "transformer"))

            parameters_2 = TransformerParametersSecondLine(*line_parts_2)
            winding_1 = TransformerWinding(1, *line_parts_3)
            winding_2 = TransformerWinding(2, *line_parts_4)
            winding_3 = TransformerWinding(3, *line_parts_5)

            t = ThreeWindingTransformer(transformer_index, parameters_1, parameters_2, winding_1, winding_2, winding_3)

            line_index += 5

        transformers.append(t)
        transformer_index += 1
    print_err('parsed {} transformers'.format(len(transformers)))

    if parse_line(lines[line_index])[0][0].strip() != psse_record_terminus:
        line_index += 1

    while parse_line(lines[line_index])[0][0].strip() not in psse_terminuses:
        line_parts, comment = parse_line(lines[line_index], LineRequirements(line_index, 1, 5, "areas"))
        areas.append(Area(*line_parts))
        line_index += 1
    print_err('parsed {} areas'.format(len(areas)))

    if parse_line(lines[line_index])[0][0].strip() != psse_record_terminus:
        line_index += 1

    #two terminal dc line data
    ttdc_index = 0
    while parse_line(lines[line_index])[0][0].strip() not in psse_terminuses:
        line_parts_1, comment_1 = parse_line(lines[line_index], LineRequirements(line_index, 12, 12, "two terminal dc line"))
        line_parts_2, comment_2 = parse_line(lines[line_index+1], LineRequirements(line_index+1, 17, 17, "two terminal dc line"))
        line_parts_3, comment_3 = parse_line(lines[line_index+2], LineRequirements(line_index+2, 17, 17, "two terminal dc line"))

        parameters = TwoTerminalDCLineParameters(*line_parts_1)
        rectifier = TwoTerminalDCLineRectifier(*line_parts_2)
        inverter = TwoTerminalDCLineInverter(*line_parts_3)

        tt_dc_lines.append(TwoTerminalDCLine(ttdc_index, parameters, rectifier, inverter))

        ttdc_index += 1
        line_index += 3
    print_err('parsed {} two terminal dc lines'.format(len(tt_dc_lines)))

    if parse_line(lines[line_index])[0][0].strip() != psse_record_terminus:
        line_index += 1

    #vsc dc line data
    vscdc_index = 0
    while parse_line(lines[line_index])[0][0].strip() not in psse_terminuses:
        line_parts_1, comment_1 = parse_line(lines[line_index], LineRequirements(line_index, 3, 11, "vsc dc line"))
        line_parts_2, comment_2 = parse_line(lines[line_index+1], LineRequirements(line_index+1, 13, 15, "vsc dc line"))
        line_parts_3, comment_3 = parse_line(lines[line_index+2], LineRequirements(line_index+2, 13, 15, "vsc dc line"))

        parameters = VSCDCLineParameters(*line_parts_1)
        converter_1 = VSCDCLineConverter(*line_parts_2)
        converter_2 = VSCDCLineConverter(*line_parts_3)

        vsc_dc_lines.append(VSCDCLine(vscdc_index, parameters, converter_1, converter_2))

        line_index += 3
        vscdc_index += 1
    print_err('parsed {} vsc dc lines'.format(len(vsc_dc_lines)))

    if parse_line(lines[line_index])[0][0].strip() != psse_record_terminus:
        line_index += 1

    #transformer impedence correction tables data
    trans_offset_index = line_index
    while parse_line(lines[line_index])[0][0].strip() not in psse_terminuses:
        line_parts, comment = parse_line(lines[line_index], LineRequirements(line_index, 1, 23, "transformer correction"))
        transformer_corrections.append(TransformerImpedanceCorrection(line_index - trans_offset_index, *line_parts))
        line_index += 1
    print_err('parsed {} transformer corrections'.format(len(transformer_corrections)))

    if parse_line(lines[line_index])[0][0].strip() != psse_record_terminus:
        line_index += 1

    #multi-terminal dc line data
    mtdc_count = 0
    while parse_line(lines[line_index])[0][0].strip() not in psse_terminuses:
        line_parts, comment = parse_line(lines[line_index], LineRequirements(line_index, 8, 8, "multi-terminal dc line"))
        parameters = MultiTerminalDCLineParameters(*line_parts)

        nconv, ndcbs, ndcln = [], [], []
        for i in range(0, parameters.nconv):
            line_parts, comment = parse_line(lines[line_index + i + 1], LineRequirements(line_index + i + 1, 16, 16, "multi-terminal dc line"))
            nconv.append(MultiTerminalDCLineConverter(*line_parts))

        for i in range(parameters.nconv, parameters.ndcbs+parameters.nconv):
            line_parts, comment = parse_line(lines[line_index + i + 1], LineRequirements(line_index + i + 1, 8, 8, "multi-terminal dc line"))
            ndcbs.append(MultiTerminalDCLineDCBus(*line_parts))

        for i in range(parameters.nconv + parameters.ndcbs, parameters.ndcln+parameters.nconv+parameters.ndcbs):
            line_parts, comment = parse_line(lines[line_index + i + 1], LineRequirements(line_index + i + 1, 6, 6, "multi-terminal dc line"))
            ndcln.append(MultiTerminalDCLineDCLink(*line_parts))

        mt_dc_lines.append(MultiTerminalDCLine(mtdc_count, parameters, nconv, ndcbs, ndcln))
        mtdc_count += 1
        line_index += 1 + parameters.nconv + parameters.ndcbs + parameters.ndcln
    print_err('parsed {} multi-terminal dc lines'.format(len(mt_dc_lines)))

    if parse_line(lines[line_index])[0][0].strip() != psse_record_terminus:
        line_index += 1

    #multi-section line grouping data
    msline_index_offset = line_index
    while parse_line(lines[line_index])[0][0].strip() not in psse_terminuses:
        line_parts, comment = parse_line(lines[line_index], LineRequirements(line_index, 5, 5, "multi-section line"))
        line_groupings.append(MultiSectionLineGrouping(line_index - msline_index_offset, *line_parts))
        line_index += 1
    print_err('parsed {} multi-section lines'.format(len(line_groupings)))

    if parse_line(lines[line_index])[0][0].strip() != psse_record_terminus:
        line_index += 1

    while parse_line(lines[line_index])[0][0].strip() not in psse_terminuses:
        line_parts, comment = parse_line(lines[line_index], LineRequirements(line_index, 2, 2, "zone"))
        zones.append(Zone(*line_parts))
        line_index += 1
    print_err('parsed {} zones'.format(len(zones)))

    if parse_line(lines[line_index])[0][0].strip() != psse_record_terminus:
        line_index += 1

    # inter area transfer data
    intarea_index_offset = line_index
    while parse_line(lines[line_index])[0][0].strip() not in psse_terminuses:
        line_parts, comment = parse_line(lines[line_index], LineRequirements(line_index, 4, 4, "inter-area transfer"))
        transfers.append(InterareaTransfer(line_index - intarea_index_offset, *line_parts))
        line_index += 1
    print_err('parsed {} inter-area transfers'.format(len(transfers)))

    if parse_line(lines[line_index])[0][0].strip() != psse_record_terminus:
        line_index += 1

    while parse_line(lines[line_index])[0][0].strip() not in psse_terminuses:
        line_parts, comment = parse_line(lines[line_index], LineRequirements(line_index, 2, 2, "owner"))
        owners.append(Owner(*line_parts))
        line_index += 1
    print_err('parsed {} owners'.format(len(owners)))

    if parse_line(lines[line_index])[0][0].strip() != psse_record_terminus:
        line_index += 1

    # facts device data block
    facts_index = 0
    while parse_line(lines[line_index])[0][0].strip() not in psse_terminuses:
        line_parts, comment = parse_line(lines[line_index], LineRequirements(line_index, 19, 21, "facts device"))
        facts.append(FACTSDevice(facts_index, *line_parts))
        facts_index += 1
        line_index += 1
    print_err('parsed {} facts devices'.format(len(facts)))

    if parse_line(lines[line_index])[0][0].strip() != psse_record_terminus:
        line_index += 1

    # switched shunt data block
    swithced_shunt_index_offset = line_index
    while parse_line(lines[line_index])[0][0].strip() not in psse_terminuses:
        line_parts, comment = parse_line(lines[line_index], LineRequirements(line_index, 12, 26, "swticthed shunt"))
        switched_shunts.append(SwitchedShunt(line_index - swithced_shunt_index_offset, *line_parts))
        line_index += 1
    print_err('parsed {} switched shunts'.format(len(switched_shunts)))

    if parse_line(lines[line_index])[0][0].strip() != psse_record_terminus:
        line_index += 1

    # GNE device data
    gne_count = 0
    while parse_line(lines[line_index])[0][0].strip() not in psse_terminuses:
        gne_count += 1
        line_index += 1
    if gne_count > 0:
        warnings.warn('skipped {} lines of GNE data'.format(gne_count), PSSEDataWarning)
        #print_err('parsed {} generic network elements'.format(len(gnes)))

    if parse_line(lines[line_index])[0][0].strip() != psse_record_terminus:
        line_index += 1

    # induction machine data
    indm_index_offset = line_index
    while parse_line(lines[line_index])[0][0].strip() not in psse_terminuses:
        line_parts, comment = parse_line(lines[line_index], LineRequirements(line_index, 34, 34, "induction machine"))
        induction_machines.append(InductionMachine(line_index - indm_index_offset, *line_parts))
        line_index += 1
    print_err('parsed {} induction machines'.format(len(induction_machines)))

    if parse_line(lines[line_index])[0][0].strip() != psse_record_terminus:
        line_index += 1

    print_err('un-parsed lines:')
    while line_index < len(lines):
        #print(parse_line(lines[line_index]))
        print_err('  '+lines[line_index])
        line_index += 1

    case = Case(ic, sbase, rev, xfrrat, nxfrat, basefrq, record1, record2,
        buses, loads, fixed_shunts, generators, branches, transformers, areas,
        tt_dc_lines, vsc_dc_lines, transformer_corrections, mt_dc_lines,
        line_groupings, zones, transfers, owners, facts, switched_shunts,
        gnes, induction_machines)

    #print(case)
    #print(case.to_psse())
    return case


def main(args):
    case = parse_psse_case_file(args.file)
    print(case)
    print(case.to_psse())


def build_cli_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('file', help='the pss/e data file to operate on (.raw)')

    return parser


if __name__ == '__main__':
    parser = build_cli_parser()
    main(parser.parse_args())