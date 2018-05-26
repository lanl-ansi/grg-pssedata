def compare_component_lists(list_1, list_2, comp_name, index_name = 'index'):
    '''compares two lists and prints the differences to stdout.  Objects in the
    lists are assumed to have an identification attribute.

    Args:
        list_1 (list): the first list
        list_2 (list): the second list
        comp_name (string): the name of components being compared
        index_name (string): the name of the object identification attribute
    Returns (int):
        returns the number of items that differed in the two lists
    '''

    if not len(list_1) == len(list_2):
        print('%s counts: %s %s' % (comp_name, len(list_1), len(list_2)))
        return abs(len(list_1) - len(list_2))
    else:
        diff_count = 0
        for index in range(0, len(list_1)):
            comp_1 = list_1[index]
            comp_2 = list_2[index]
            if not comp_1 == comp_2:
                print('different %s (%d): %d %d' % (comp_name, index, 
                    getattr(comp_1, index_name), getattr(comp_1, index_name)))
                print('case 1: %s' % str(comp_1))
                print('case 2: %s' % str(comp_2))
                print('')
                diff_count += 1
        return diff_count


def diff(case_1, case_2):
    '''Compares two :class:`grg_pssedata.struct.Case` objects and prints the 
    differences to stdout.

    Args:
        case_1: the first psse case
        case_2: the second psse case
    Returns (int):
        returns the number of items that differed in the two cases
    '''

    diff_count = 0
    if not case_1 == case_2:
        if not case_1.ic == case_2.ic:
            print('ic: %d %d' % (case_1.ic, case_2.ic))
            diff_count += 1
        if not case_1.sbase == case_2.sbase:
            print('sbase: %s %s' % (case_1.sbase, case_2.sbase))
            diff_count += 1
        if not case_1.rev == case_2.rev:
            print('rev: %s %s' % (case_1.rev, case_2.rev))
            diff_count += 1
        if not case_1.xfrrat == case_2.xfrrat:
            print('xfrrat: %s %s' % (case_1.xfrrat, case_2.xfrrat))
            diff_count += 1
        if not case_1.nxfrat == case_2.nxfrat:
            print('nxfrat: %s %s' % (case_1.nxfrat, case_2.nxfrat))
            diff_count += 1
        if not case_1.basfrq == case_2.basfrq:
            print('basfrq: %s %s' % (case_1.basfrq, case_2.basfrq))
            diff_count += 1
        if not case_1.record1 == case_2.record1:
            print('record1: %s %s' % (case_1.record1, case_2.record1))
            diff_count += 1
        if not case_1.record2 == case_2.record2:
            print('record2: %s %s' % (case_1.record2, case_2.record2))
            diff_count += 1

        if not case_1.buses == case_2.buses:
            diff_count += compare_component_lists(
                case_1.buses, case_2.buses, 'bus', 'i')

        if not case_1.loads == case_2.loads:
            diff_count += compare_component_lists(
                case_1.loads, case_2.loads, 'load')

        if not case_1.fixed_shunts == case_2.fixed_shunts:
            diff_count += compare_component_lists(
                case_1.fixed_shunts, case_2.fixed_shunts, 'fixed shunt')

        if not case_1.generators == case_2.generators:
            diff_count += compare_component_lists(
                case_1.generators, case_2.generators, 'generator')

        if not case_1.branches == case_2.branches:
            diff_count += compare_component_lists(
                case_1.branches, case_2.branches, 'branch')

        if not case_1.transformers == case_2.transformers:
            diff_count += compare_component_lists(
                case_1.transformers, case_2.transformers, 'transformer')

        if not case_1.areas == case_2.areas:
            diff_count += compare_component_lists(
                case_1.areas, case_2.areas, 'areas', 'i')

        if not case_1.tt_dc_lines == case_2.tt_dc_lines:
            diff_count += compare_component_lists(
                case_1.tt_dc_lines, case_2.tt_dc_lines, 'two terminal dc line')

        if not case_1.vsc_dc_lines == case_2.vsc_dc_lines:
            diff_count += compare_component_lists(
                case_1.vsc_dc_lines, case_2.vsc_dc_lines, 'vsc dc line')

        if not case_1.transformer_corrections == case_2.transformer_corrections:
            diff_count += compare_component_lists(
                case_1.transformer_corrections, case_2.transformer_corrections, 'transformer correction')

        if not case_1.mt_dc_lines == case_2.mt_dc_lines:
            diff_count += compare_component_lists(
                case_1.mt_dc_lines, case_2.mt_dc_lines, 'multi terminal dc line')

        if not case_1.line_groupings == case_2.line_groupings:
            diff_count += compare_component_lists(
                case_1.line_groupings, case_2.line_groupings, 'line group')

        if not case_1.zones == case_2.zones:
            diff_count += compare_component_lists(
                case_1.zones, case_2.zones, 'zones', 'i')

        if not case_1.transfers == case_2.transfers:
            diff_count += compare_component_lists(
                case_1.transfers, case_2.transfers, 'inter-area transfer')

        if not case_1.owners == case_2.owners:
            diff_count += compare_component_lists(
                case_1.owners, case_2.owners, 'owners', 'i')

        if not case_1.facts == case_2.facts:
            diff_count += compare_component_lists(
                case_1.facts, case_2.facts, 'facts device')

        if not case_1.switched_shunts == case_2.switched_shunts:
            diff_count += compare_component_lists(
                case_1.switched_shunts, case_2.switched_shunts, 'switched shunt')

        if not case_1.gnes == case_2.gnes:
            diff_count += compare_component_lists(
                case_1.gnes, case_2.gnes, 'generic network element')

        if not case_1.induction_machines == case_2.induction_machines:
            diff_count += compare_component_lists(
                case_1.induction_machines, case_2.induction_machines, 'induction machine')

    else:
        print('the files are identical')

    return diff_count


def eq(case_1, case_2):
    if case_1 == case_2:
        print('the case file data structures are identical')
        case_1_str = case_1.to_matpower()
        case_2_str = case_2.to_matpower()
        if case_1_str == case_2_str:
            print('the psse strings are identical')
            return True
        else:
            print('the psse encodings differ, this is most likely an '
                'implementation bug')
    else:
        print('the case files differ')
    return False


def build_cmd_parser():
    parser = argparse.ArgumentParser(
        description='''grg_pssedata.cmd provides tools for analyzing and
            transforming psse network datasets.''',

        epilog='''Please file bugs at...''',
    )

    subparsers = parser.add_subparsers(help='sub-commands', dest='cmd')

    parser_eq = subparsers.add_parser('eq', help = 'tests if two case files '
        'are equal')
    parser_eq.add_argument('file_1', help='a psse data file (.raw)')
    parser_eq.add_argument('file_2', help='a psse data file (.raw)')

    parser_diff = subparsers.add_parser('diff', help = 'presents the '
        'differences between two case files')
    parser_diff.add_argument('file_1', help='a psse data file (.raw)')
    parser_diff.add_argument('file_2', help='a psse data file (.raw)')

    #parser.add_argument('--foo', help='foo help')
    version = __import__('grg_pssedata').__version__
    parser.add_argument('-v', '--version', action='version', \
        version='grg_pssedata.cmd (version '+version+')')

    return parser


def main(args):
    '''reads a psse case files and processes them based on command
    line arguments.

    Args:
        args: an argparse data structure
    '''

    if args.cmd == 'eq':
        case_1 = parse_mp_case_file(args.file_1)
        case_2 = parse_mp_case_file(args.file_2)

        return eq(case_1, case_2)

    if args.cmd == 'diff':
         case_1 = parse_mp_case_file(args.file_1)
         case_2 = parse_mp_case_file(args.file_2)

         return diff(case_1, case_2)


if __name__ == '__main__':
    import sys
    parser = build_cmd_parser()
    main(parser.parse_args())
