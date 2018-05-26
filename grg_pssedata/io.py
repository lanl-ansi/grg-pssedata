from __future__ import print_function

import argparse
import functools
import warnings
import sys

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

from grg_pssedata.exception import PSSEDataParsingError
from grg_pssedata.exception import PSSEDataWarning

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



def parse_line(line):
    slash_count = line.count('/')
    if slash_count > 1:
        raise PSSEDataParsingError('line has {} occurences of "/" and the parser only supports at most 1'.format(slash_count))

    line = line.strip()
    comment = None

    if slash_count > 0:
        line, comment = line.strip().split('/')

    #TODO this should be robust to strings
    line_parts = line.strip().split(',')

    return line_parts, comment


def parse_psse_case_lines(lines):
    if len(lines) < 3: # need at base values and record
        raise PSSEDataParsingError('psse case has {} lines and at least 3 are required'.format(len(lines)))

    (ic, sbase, rev, xfrrat, nxfrat, basefrq), comment = parse_line(lines[0])
    print_err('case data: {} {} {} {} {} {}'.format(ic, sbase, rev, xfrrat, nxfrat, basefrq))

    if int(ic) != 0: # validity checks may fail on "change data"
        raise PSSEDataParsingError('ic value of {} given, only a value of 0 is supported'.format(ic))

    if int(float(rev)) != 33:
        warnings.warn('PSEE version {} given but only version 33 is supported, parser may not function correctly.'.format(rev.strip()), PSSEDataWarning)

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
        line_parts, comment = parse_line(lines[line_index])
        buses.append(Bus(*line_parts))
        line_index += 1
    print_err('parsed {} buses'.format(len(buses)))

    if parse_line(lines[line_index])[0][0].strip() != psse_record_terminus:
        line_index += 1

    load_index_offset = line_index
    while parse_line(lines[line_index])[0][0].strip() not in psse_terminuses:
        line_parts, comment = parse_line(lines[line_index])
        loads.append(Load(line_index - load_index_offset, *line_parts))
        line_index += 1
    print_err('parsed {} loads'.format(len(loads)))

    if parse_line(lines[line_index])[0][0].strip() != psse_record_terminus:
        line_index += 1

    fixed_shunt_index_offset = line_index
    while parse_line(lines[line_index])[0][0].strip() not in psse_terminuses:
        line_parts, comment = parse_line(lines[line_index])
        fixed_shunts.append(FixedShunt(line_index - fixed_shunt_index_offset, *line_parts))
        line_index += 1
    print_err('parsed {} fixed shunts'.format(len(fixed_shunts)))

    if parse_line(lines[line_index])[0][0].strip() != psse_record_terminus:
        line_index += 1

    gen_index_offset = line_index
    while parse_line(lines[line_index])[0][0].strip() not in psse_terminuses:
        line_parts, comment = parse_line(lines[line_index])
        generators.append(Generator(line_index - gen_index_offset, *line_parts))
        line_index += 1
    print_err('parsed {} generators'.format(len(generators)))

    if parse_line(lines[line_index])[0][0].strip() != psse_record_terminus:
        line_index += 1

    branch_index_offset = line_index
    while parse_line(lines[line_index])[0][0].strip() not in psse_terminuses:
        #line = shlex.split(lines[line_index].strip())
        #line = expand_commas(line)
        line_parts, comment = parse_line(lines[line_index])
        #print(line_parts)
        branches.append(Branch(line_index - branch_index_offset, *line_parts))
        line_index += 1
    print_err('parsed {} branches'.format(len(branches)))

    if parse_line(lines[line_index])[0][0].strip() != psse_record_terminus:
        line_index += 1

    transformer_index = 0
    while parse_line(lines[line_index])[0][0].strip() not in psse_terminuses:
        line_parts_1, comment_1 = parse_line(lines[line_index])
        parameters_1 = TransformerParametersFirstLine(*line_parts_1)
        #print(parameters_1)

        if parameters_1.k == 0: # two winding case
            line_parts_2, comment_2 = parse_line(lines[line_index+1])
            line_parts_3, comment_3 = parse_line(lines[line_index+2])
            line_parts_4, comment_4 = parse_line(lines[line_index+3])

            parameters_2 = TransformerParametersSecondLineShort(*line_parts_2)
            winding_1 = TransformerWinding(1, *line_parts_3)
            winding_2 = TransformerWindingShort(2, *line_parts_4)

            t = TwoWindingTransformer(transformer_index, parameters_1, parameters_2, winding_1, winding_2)

            line_index += 4
        else: # three winding case
            line_parts_2, comment_2 = parse_line(lines[line_index+1])
            line_parts_3, comment_3 = parse_line(lines[line_index+2])
            line_parts_4, comment_4 = parse_line(lines[line_index+3])
            line_parts_5, comment_5 = parse_line(lines[line_index+4])

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
        line_parts, comment = parse_line(lines[line_index])
        areas.append(Area(*line_parts))
        line_index += 1
    print_err('parsed {} areas'.format(len(areas)))

    if parse_line(lines[line_index])[0][0].strip() != psse_record_terminus:
        line_index += 1

    #two terminal dc line data
    ttdc_count = 0
    while parse_line(lines[line_index])[0][0].strip() not in psse_terminuses:
        ttdc_count += 1
        line_index += 1
    if ttdc_count > 0:
        warnings.warn('skipped {} lines of two terminal dc line data'.format(ttdc_count), PSSEDataWarning)
        #print_err('parsed {} two terminal dc lines'.format(len(vsc_dc_lines)))

    if parse_line(lines[line_index])[0][0].strip() != psse_record_terminus:
        line_index += 1

    #vsc dc line data
    vscdc_count = 0
    while parse_line(lines[line_index])[0][0].strip() not in psse_terminuses:
        vscdc_count += 1
        line_index += 1
    if vscdc_count > 0:
        warnings.warn('skipped {} lines of vsc dc line data'.format(vscdc_count), PSSEDataWarning)
        #print_err('parsed {} vsc dc lines'.format(len(vsc_dc_lines)))

    if parse_line(lines[line_index])[0][0].strip() != psse_record_terminus:
        line_index += 1

    trans_index_offset = line_index
    trans_count = 0
    while parse_line(lines[line_index])[0][0].strip() not in psse_terminuses:
        trans_count += 1
        line_index += 1
    if trans_count > 0:
        warnings.warn('skipped {} lines of transformer correction data'.format(trans_count), PSSEDataWarning)
        #print_err('parsed {} transformer corrections'.format(len(transformer_corrections)))

    if parse_line(lines[line_index])[0][0].strip() != psse_record_terminus:
        line_index += 1

    #multi-terminal dc line data
    mtdc_count = 0
    while parse_line(lines[line_index])[0][0].strip() not in psse_terminuses:
        mtdc_count += 1
        line_index += 1
    if mtdc_count > 0:
        warnings.warn('skipped {} lines of multi-terminal dc line data'.format(mtdc_count), PSSEDataWarning)
        #print_err('parsed {} multi-terminal dc lines'.format(len(mt_dc_lines)))

    if parse_line(lines[line_index])[0][0].strip() != psse_record_terminus:
        line_index += 1

    #multi-section line grouping data
    msline_count = 0 
    while parse_line(lines[line_index])[0][0].strip() not in psse_terminuses:
        msline_count += 1
        line_index += 1
    if msline_count > 0:
        warnings.warn('skipped {} lines of multi-section line grouping data'.format(msline_count), PSSEDataWarning)
        #print_err('parsed {} multi-section lines'.format(len(line_groupings)))

    if parse_line(lines[line_index])[0][0].strip() != psse_record_terminus:
        line_index += 1

    while parse_line(lines[line_index])[0][0].strip() not in psse_terminuses:
        line_parts, comment = parse_line(lines[line_index])
        zones.append(Zone(*line_parts))
        line_index += 1
    print_err('parsed {} zones'.format(len(zones)))

    if parse_line(lines[line_index])[0][0].strip() != psse_record_terminus:
        line_index += 1

    # inter area transfer data
    intarea_count = 0
    while parse_line(lines[line_index])[0][0].strip() not in psse_terminuses:
        intarea_count += 1
        line_index += 1
    if intarea_count > 0:
        warnings.warn('skipped {} lines of inter area transfer data'.format(intarea_count), PSSEDataWarning)
        #print_err('parsed {} inter area transfers'.format(len(transfers)))

    if parse_line(lines[line_index])[0][0].strip() != psse_record_terminus:
        line_index += 1

    while parse_line(lines[line_index])[0][0].strip() not in psse_terminuses:
        line_parts, comment = parse_line(lines[line_index])
        owners.append(Owner(*line_parts))
        line_index += 1
    print_err('parsed {} owners'.format(len(owners)))

    if parse_line(lines[line_index])[0][0].strip() != psse_record_terminus:
        line_index += 1

    # facts device data block
    facts_count = 0
    while parse_line(lines[line_index])[0][0].strip() not in psse_terminuses:
        facts_count += 1
        line_index += 1
    if facts_count > 0:
        warnings.warn('skipped {} lines of facts data'.format(facts_count), PSSEDataWarning)
        #print_err('parsed {} facts devices'.format(len(facts)))

    if parse_line(lines[line_index])[0][0].strip() != psse_record_terminus:
        line_index += 1

    # switched shunt data block 
    swithced_shunt_index_offset = line_index
    while parse_line(lines[line_index])[0][0].strip() not in psse_terminuses:
        line_parts, comment = parse_line(lines[line_index])
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
    indm_count = 0
    while parse_line(lines[line_index])[0][0].strip() not in psse_terminuses:
        indm_count += 1
        line_index += 1
    if indm_count > 0:
        warnings.warn('skipped {} lines of induction machine data'.format(indm_count), PSSEDataWarning)
        #print_err('parsed {} induction machines'.format(len(induction_machines)))

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