'''data structures for encoding pss/e data files'''

import os

def _guard_none(fun, val):
    '''guards the application of a unary function for values taking None
    useful for typing optional values

    Args:
        fun: a function
        val: a unary value
    Returns:
        None if val was None, otherwise the application of fun to val
    '''

    if val is None:
        return None
    else:
        return fun(val)


def _set_defaults(args, defaults):
    assert(len(args) == len(defaults))
    for i,val in enumerate(defaults):
        if args[i] is not None and len(args[i].strip()) == 0:
            args[i] = defaults[i]
    return args


def _check_range(value, name, component_type, component_id, lb, ub):
    if not (value >= lb and value <= ub):
        warnings.warn('the {} value {} on {} {} is not in the valid range {} to {}'
            .format(name, value, component_type, component_id, lb, ub),
            PSSEDataWarning)


def _check_boolean(value, name, component_type, component_id):
    _check_range(value, name, component_type, component_id, 0, 1)


def _check_owners(component, component_type, component_id):
    _check_range(component.o1, 'owner one', component_type, component_id, 1, 9999)
    _check_range(component.o2, 'owner two', component_type, component_id, 1, 9999)
    _check_range(component.o3, 'owner three', component_type, component_id, 1, 9999)
    _check_range(component.o4, 'owner four', component_type, component_id, 1, 9999)

    _check_range(component.f1, 'owner faction one', component_type, component_id, 0.0, 1.0)
    _check_range(component.f2, 'owner faction two', component_type, component_id, 0.0, 1.0)
    _check_range(component.f3, 'owner faction three', component_type, component_id, 0.0, 1.0)
    _check_range(component.f4, 'owner faction four', component_type, component_id, 0.0, 1.0)


def unquote_string(s):
    '''strips single quotes from a PSSE string'''
    return str(s).strip().strip('\'')

def quote_string(s):
    '''adds PSSE single quotes to a string'''
    return '\'{}\''.format(s)


CASE_DEFAULTS = [0, 100.0, 33, 0, 0, 60]
class Case(object):
    def __init__(self, ic, sbase, rev, xfrrat, nxfrat, basfrq, record1, record2,
        buses, loads, fixed_shunts, generators, branches, transformers, areas,
        tt_dc_lines, vsc_dc_lines, transformer_corrections, mt_dc_lines,
        line_groupings, zones, transfers, owners, facts, switched_shunts,
        gnes, induction_machines):
        '''This data structure contains lists of all the key components in a
        pss/e power network.  At this time, only pss/e case version 33 is supported.

        Args:
            ic (int): case type, 0 for base, 1 for incremental
            sbase (float): the system MVA base value (MVA)
            rev (int): file type version number
            xfrrat (float): transformer rating units
            nxfrat (float): units of branch ratings
            basfrq (float): base frequency (Hertz)
            record1 (string): system description part 1, up to 60 characters
            record2 (string): system description part 2, up to 60 characters
            buses (list of Bus): buses
            loads (list of Load): loads
            fixed_shunts (list of TBD): fixed shunts
            generators (list of Generator): generators
            branches (list of Branch): branches
            transformers (list of TwoWindingTransformer and ThreeWindingTransformer): two and three winding transformers
            areas (list of Area): areas
            tt_dc_lines (list of TBD): two-terminal dc lines
            vsc_dc_lines (list of TBD): vsc dc lines
            transformer_corrections (list of TBD): transformer correction tables
            mt_dc_lines (list of TBD): multi-terminal dc lines
            line_groupings (list of TBD): line groupings
            zones (list of Zone): zones
            transfers (list of TBD): inter-area transfers
            owners (list of Owner): owners
            facts (list of TBD): FACTS devices
            switched_shunts (list of SwitchedShunt): switched shunt devices
            gnes (list of TBD): general network elements
            induction_machines (list of TBD): induction machines
        '''

        args = [ic, sbase, rev, xfrrat, nxfrat, basfrq]
        _set_defaults(args, CASE_DEFAULTS)
        ic, sbase, rev, xfrrat, nxfrat, basfrq = args

        self.ic = int(ic)
        self.sbase = float(sbase)
        self.rev = int(rev)
        self.xfrrat = float(xfrrat)
        self.nxfrat = float(nxfrat)
        self.basfrq = float(basfrq)
        self.record1 = str(record1)
        self.record2 = str(record2)
        self.buses = buses
        self.loads = loads
        self.fixed_shunts = fixed_shunts
        self.generators = generators
        self.branches = branches
        self.transformers = transformers
        self.areas = areas
        self.tt_dc_lines = tt_dc_lines
        self.vsc_dc_lines = vsc_dc_lines
        self.transformer_corrections = transformer_corrections
        self.mt_dc_lines = mt_dc_lines
        self.line_groupings = line_groupings
        self.zones = zones
        self.transfers = transfers
        self.owners = owners
        self.facts = facts
        self.switched_shunts = switched_shunts
        self.gnes = gnes
        self.induction_machines = induction_machines

        self.component_lists = [self.buses, self.loads, self.fixed_shunts,
            self.generators, self.branches, self.transformers, self.areas,
            self.tt_dc_lines, self.vsc_dc_lines, self.transformer_corrections,
            self.mt_dc_lines, self.line_groupings, self.zones, self.transfers,
            self.owners, self.facts, self.switched_shunts, self.gnes,
            self.induction_machines]


    def __str__(self):
        tmp = []
        tmp += ['Base:\n']
        tmp += [str(self.ic)+' '+str(self.sbase)+' '+str(self.rev)+' '+str(self.xfrrat)+' '+str(self.nxfrat)+' '+str(self.basfrq)+'\n']
        tmp += [self.record1+'\n']
        tmp += [self.record2+'\n']
        tmp += ['\n']

        tmp += ['Buses:\n']
        tmp += ['\n'.join([str(x) for x in self.buses])]
        tmp += ['\n \n']

        tmp += ['Loads:\n']
        tmp += ['\n'.join([str(x) for x in self.loads])]
        tmp += ['\n \n']

        tmp += ['Fixed Shunts:\n']
        tmp += ['\n'.join([str(x) for x in self.fixed_shunts])]
        tmp += ['\n \n']

        tmp += ['Generators:\n']
        tmp += ['\n'.join([str(x) for x in self.generators])]
        tmp += ['\n \n']

        tmp += ['Branches:\n']
        tmp += ['\n'.join([str(x) for x in self.branches])]
        tmp += ['\n \n']

        tmp += ['Transformers:\n']
        tmp += ['\n'.join([str(x) for x in self.transformers])]
        tmp += ['\n \n']

        tmp += ['Areas:\n']
        tmp += ['\n'.join([str(x) for x in self.areas])]
        tmp += ['\n \n']

        tmp += ['Two-Terminal DC Lines:\n']
        tmp += ['\n'.join([str(x) for x in self.tt_dc_lines])]
        tmp += ['\n \n']

        tmp += ['VSC DC Lines:\n']
        tmp += ['\n'.join([str(x) for x in self.vsc_dc_lines])]
        tmp += ['\n \n']

        tmp += ['Transformer Corrections:\n']
        tmp += ['\n'.join([str(x) for x in self.transformer_corrections])]
        tmp += ['\n \n']

        tmp += ['Multi-Terminal DC Lines:\n']
        tmp += ['\n'.join([str(x) for x in self.mt_dc_lines])]
        tmp += ['\n \n']

        tmp += ['Line Groupings:\n']
        tmp += ['\n'.join([str(x) for x in self.line_groupings])]
        tmp += ['\n \n']

        tmp += ['Zones:\n']
        tmp += ['\n'.join([str(x) for x in self.zones])]
        tmp += ['\n \n']

        tmp += ['Inter Area Transfers:\n']
        tmp += ['\n'.join([str(x) for x in self.transfers])]
        tmp += ['\n \n']

        tmp += ['Owners:\n']
        tmp += ['\n'.join([str(x) for x in self.owners])]
        tmp += ['\n \n']

        tmp += ['Switched Shunts:\n']
        tmp += ['\n'.join([str(x) for x in self.switched_shunts])]
        tmp += ['\n \n']

        tmp += ['Generic Network Elements:\n']
        tmp += ['\n'.join([str(x) for x in self.gnes])]
        tmp += ['\n \n']

        tmp += ['Induction Machines:\n']
        tmp += ['\n'.join([str(x) for x in self.induction_machines])]
        tmp += ['\n \n']

        return ''.join(tmp)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def validate(self):
        '''Checks that this data structure conforms to the pss/e data
        specification.
        '''

        if self.rev != 33:
            warnings.warn('only version 33 is supported, given version {}'.format(self.rev),
            PSSEDataWarning)

        if len(self.record1) > 60:
            warnings.warn('the first record has {} characters, only 60 are supported'.format(len(self.record1)),
            PSSEDataWarning)

        if len(self.record2) > 60:
            warnings.warn('the first record has {} characters, only 60 are supported'.format(len(self.record2)),
            PSSEDataWarning)

        _check_boolean(self.ic, 'case type flag', 'case', '-')

        for component_list in self.component_lists:
            for component in component_list:
                component.validate()

    def to_psse(self):
        '''Returns: a pss/e encoding of this data structure as a string'''

        psse_lines = []
        case_datra = [str(self.ic), str(self.sbase), str(self.rev),
            str(self.xfrrat), str(self.nxfrat), str(self.basfrq)]
        psse_lines.append(', '.join(case_datra))
        psse_lines.append(self.record1)
        psse_lines.append(self.record2)

        for bus in self.buses:
            psse_lines.append('  '+bus.to_psse())
        psse_lines.append('0 / END OF BUS DATA, BEGIN LOAD DATA')

        for load in self.loads:
            psse_lines.append('  '+load.to_psse())
        psse_lines.append('0 / END OF LOAD DATA, BEGIN FIXED SHUNT DATA')

        for fixed_shunt in self.fixed_shunts:
            psse_lines.append('  '+fixed_shunt.to_psse())
        psse_lines.append('0 / END OF FIXED SHUNT DATA, BEGIN GENERATOR DATA')

        for gen in self.generators:
            psse_lines.append('  '+gen.to_psse())
        psse_lines.append('0 / END OF GENERATOR DATA, BEGIN BRANCH DATA')

        for branch in self.branches:
            psse_lines.append('  '+branch.to_psse())
        psse_lines.append('0 / END OF BRANCH DATA, BEGIN TRANSFORMER DATA')

        for transformer in self.transformers:
            psse_lines.append('  '+transformer.to_psse())
        psse_lines.append('0 / END OF TRANSFORMER DATA, BEGIN AREA DATA')

        for area in self.areas:
            psse_lines.append('  '+area.to_psse())
        psse_lines.append('0 / END OF AREA DATA, BEGIN TWO-TERMINAL DC DATA')

        for tt_dc_line in self.tt_dc_lines:
            psse_lines.append('  '+tt_dc_line.to_psse())
        psse_lines.append('0 / END OF TWO-TERMINAL DC DATA, BEGIN VOLTAGE SOURCE CONVERTER DATA')

        for vsc_dc_line in self.vsc_dc_lines:
            psse_lines.append('  '+vsc_dc_line.to_psse())
        psse_lines.append('0 / END OF VOLTAGE SOURCE CONVERTER DATA, BEGIN IMPEDANCE CORRECTION DATA')

        for transformer_correction in self.transformer_corrections:
            psse_lines.append('  '+transformer_correction.to_psse())
        psse_lines.append('0 / END OF IMPEDANCE CORRECTION DATA, BEGIN MULTI-TERMINAL DC DATA')

        for mt_dc_line in self.mt_dc_lines:
            psse_lines.append('  '+mt_dc_line.to_psse())
        psse_lines.append('0 / END OF MULTI-TERMINAL DC DATA, BEGIN MULTI-SECTION LINE DATA')

        for line_grouping in self.line_groupings:
            psse_lines.append('  '+line_grouping.to_psse())
        psse_lines.append('0 / END OF MULTI-SECTION LINE DATA, BEGIN ZONE DATA')

        for zone in self.zones:
            psse_lines.append('  '+zone.to_psse())
        psse_lines.append('0 / END OF ZONE DATA, BEGIN INTER-AREA TRANSFER DATA')

        for transfer in self.transfers:
            psse_lines.append('  '+transfer.to_psse())
        psse_lines.append('0 / END OF INTER-AREA TRANSFER DATA, BEGIN OWNER DATA')

        for owner in self.owners:
            psse_lines.append('  '+owner.to_psse())
        psse_lines.append('0 / END OF OWNER DATA, BEGIN FACTS CONTROL DEVICE DATA')

        for fact in self.facts:
            psse_lines.append('  '+fact.to_psse())
        psse_lines.append('0 / END OF FACTS CONTROL DEVICE DATA, BEGIN SWITCHED SHUNT DATA')

        for switched_shunt in self.switched_shunts:
            psse_lines.append('  '+switched_shunt.to_psse())
        psse_lines.append('0 / END OF SWITCHED SHUNT DATA, BEGIN GNE DEVICE DATA')

        for gne in self.gnes:
            psse_lines.append('  '+gne.to_psse())
        psse_lines.append('0 / END OF GNE DEVICE DATA, BEGIN INDUCTION MACHINE DATA')

        for induction_machine in self.induction_machines:
            psse_lines.append('  '+induction_machine.to_psse())
        psse_lines.append('0 / END INDUCTION MACHINE DATA')

        psse_lines.append('Q')

        return os.linesep.join(psse_lines)



BUS_DEFAULTS = ["            ", 0.0, 1, 1, 1, 1, 1.0, 0.0, 0.9, 1.1, 0.9, 1.1]
class Bus(object):
    def __init__(self, i, name, basekv, ide, area, zone, owner, vm, va, nvhi, nvlo, evhi, evlo):
        '''This data structure contains bus parameters.

        Args:
            i (int): unique bus identifier 1-999997
            name (string): bus name, 8 characters, must be enclosed in single quotes
            basekv (float): base voltage (kilo volts)
            ide (int): bus type, PQ = 1, PV = 2, reference = 3, isolated = 4
            area (int): area id, 1-9999 (default = 1)
            zone (int): zone id, 1-9999 (default = 1)
            owner (int): owner id, 1-9999 (default = 1)
            vm (float): voltage magnitude (volts p.u.) (default = 1.0)
            va (float): voltage angle (degrees) (default = 0.0)
            nvhi (float): voltage magnitude upper bound, normal conditions (volts p.u.) (default = 1.1)
            nvlo (float): voltage magnitude lower bound, normal conditions (volts p.u.) (default = 0.9)
            evhi (float): voltage magnitude upper bound, emergency conditions (volts p.u.) (default = 1.1)
            evlo (float): voltage magnitude lower bound, emergency conditions (volts p.u.) (default = 0.9)
        '''

        args = [name, basekv, ide, area, zone, owner, vm, va, nvhi, nvlo, evhi, evlo]
        _set_defaults(args, BUS_DEFAULTS)
        name, basekv, ide, area, zone, owner, vm, va, nvhi, nvlo, evhi, evlo = args

        self.i = int(i)
        self.name = unquote_string(name)
        self.basekv = float(basekv)
        self.ide = int(ide)
        self.area = int(area)
        self.zone = int(zone)
        self.owner = int(owner)
        self.vm = float(vm)
        self.va = float(va)
        self.nvhi = float(nvhi)
        self.nvlo = float(nvlo)
        self.evhi = float(evhi)
        self.evlo = float(evlo)

    def __str__(self):
        data = [self.i, self.name, self.basekv, self.ide, self.area, self.zone,
                self.owner, self.vm, self.va, self.nvhi, self.nvlo, self.evhi,
                self.evlo]
        return ' '.join([str(x) for x in data])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def validate(self):
        '''Checks that this data structure conforms to the pss/e data
        specification
        '''

        if not (self.i >= 1 and self.i <= 999997):
            warnings.warn('bus {} is not in the valid range 1 to 999997'.format(self.i), PSSEDataWarning)

        #_check_range(self.i, 'id', 'bus', self.i, 1, 999997)
        _check_range(self.area, 'area', 'bus', self.i, 1, 9999)
        _check_range(self.zone, 'zone', 'bus', self.i, 1, 9999)
        _check_range(self.owner, 'owner', 'bus', self.i, 1, 9999)

        # if not (self.area >= 1 and self.area <= 9999):
        #     warnings.warn('the area %d on bus %d is not in the valid range 1 to 9999' %
        #         (self.ia, self.i), PSSEDataWarning)

        # if not (self.zone >= 1 and self.zone <= 9999):
        #     warnings.warn('the zone %d on bus %d is not in the valid range 1 to 9999' %
        #         (self.zone, self.i), PSSEDataWarning)

        # if not (self.owner >= 1 and self.owner <= 9999):
        #     warnings.warn('the owner %d on bus %d is not in the valid range 1 to 9999' %
        #         (self.owner, self.i), PSSEDataWarning)


    def to_psse(self):
        '''Returns: a pss/e encoding of this data structure as a string'''

        data = [self.i, quote_string(self.name), self.basekv, self.ide,
                self.area, self.zone, self.owner, self.vm, self.va,
                self.nvhi, self.nvlo, self.evhi, self.evlo]

        return ', '.join([str(x) for x in data])


LOAD_DEFAULTS = [1, 1, 1, 1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 1, 0]
class Load(object):
    def __init__(self, index, i, id, status, area, zone, pl, ql, ip, iq, yp, yq, owner, scale, intrpt="0"):
        '''This data structure contains load parameters.

        Args:
            index (int): unique load identifier
            i (int): the identifier of the bus that this load is connected to
            id (string): load identifier (not unique)
            status (int): load status (in service = 1, out of service = 0)
            area (int): area id, 1-9999 (default = the area of the connecting bus)
            zone (int): zone id, 1-9999 (default = the zone of the connecting bus)
            pl (float): active power load (MW) (default = 0.0)
            ql (float): reactive power output (MVAr) (default = 0.0)
            ip (float): real current load (MW per unit voltage) (default = 0.0)
            iq (float): imaginary current load (MVAr per unit voltage) (default = 0.0)
            yp (float): real admittance load (MW per unit voltage) (default = 0.0)
            yq (float): imaginary admittance load (MVAr per unit voltage) (default = 0.0)
            owner (int): owner id, 1-9999 (default = the owner of the connecting bus)
            scale (int): scaling flag (scalable = 1, fixed = 0) (default = 1)
            intrpt (int): interruptible flag, (interruptible = 1, non-interruptible = 0) (optional, default = 0)
        '''

        args = [id, status, area, zone, pl, ql, ip, iq, yp, yq, owner, scale, intrpt]
        _set_defaults(args, LOAD_DEFAULTS)
        id, status, area, zone, pl, ql, ip, iq, yp, yq, owner, scale, intrpt = args

        self.index = int(index)
        self.i = int(i)
        self.id = unquote_string(id)
        self.status = int(status)
        self.area = int(area)
        self.zone = int(zone)
        self.pl = float(pl)
        self.ql = float(ql)
        self.ip = float(ip)
        self.iq = float(iq)
        self.yp = float(yp)
        self.yq = float(yq)
        self.owner = int(owner)
        self.scale = int(scale)
        self.intrpt = int(intrpt)


    def __str__(self):
        data = [self.index, self.i, self.id, self.status, self.area, self.zone,
            self.pl, self.ql, self.ip, self.iq, self.yp, self.yq, self.owner,
            self.scale, self.intrpt]
        return ' '.join([str(x) for x in data])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def validate(self):
        '''Checks that this data structure conforms to the pss/e data
        specification
        '''
        _check_boolean(self.status, 'status', 'load', self.index)

        _check_range(self.i, 'bus identifier', 'load', self.index, 1, 999997)
        _check_range(self.area, 'area', 'load', self.index, 1, 9999)
        _check_range(self.zone, 'zone', 'load', self.index, 1, 9999)
        _check_range(self.owner, 'owner', 'load', self.index, 1, 9999)

    def to_psse(self):
        '''Returns: a pss/e encoding of this data structure as a string'''

        data = [self.i, quote_string(self.id), self.status, self.area,
            self.zone, self.pl, self.ql, self.ip, self.iq, self.yp, self.yq,
            self.owner, self.scale, self.intrpt]

        return ', '.join([str(x) for x in data])


FIXED_SHUNT_DEFAULTS = [1, 1, 0.0, 0.0]
class FixedShunt(object):
    def __init__(self, index, i, id, status, gl, bl):
        '''This data structure contains fixed shunt parameters

        Args:
            index (int): unique fixed shunt identifier
            i (int): the identifier of the bus that this fixed shunt is connected to
            id (string): fixed shunt identifier (not unique)
            status (int): fixed shunt status (in service = 1, out of service = 0)
            gl (float): the conductance to ground in MW at one per unit voltage (default = 0.0)
            bl (float): the susceptance to ground in MVar at one per unit voltage (default = 0.0)
        '''

        args = [id, status, gl, bl]
        _set_defaults(args, FIXED_SHUNT_DEFAULTS)
        id, status, gl, bl = args

        self.index = int(index)
        self.i = int(i)
        self.id = unquote_string(id)
        self.status = int(status)
        self.gl = float(gl)
        self.bl = float(bl)

    def __str__(self):
        data = [self.index, self.i, self.id, self.status, self.gl, self.bl]
        return ' '.join([str(x) for x in data])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def validate(self):
        '''Checks that this data structure conforms to the pss/e data
        specification
        '''
        _check_boolean(self.status, 'status', 'fixed shunt', self.index)
        _check_range(self.i, 'bus identifier', 'fixed shunt', self.index, 1, 999997)

    def to_psse(self):
        '''Returns: a pss/e encoding of this data structure as a string'''

        data = [self.i, quote_string(self.id), self.status, self.gl, self.bl]

        return ', '.join([str(x) for x in data])


SWITCHED_SHUNT_DEFAULTS = [1, 0, 1, 1.0, 1.0, 0, 100.0, "", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
class SwitchedShunt(object):
    def __init__(self, index, i, modsw, adjm, stat, vswhi, vswlo, swrem, rmpct, rmidnt, binit, n1, b1,
                    n2=None, b2=None, n3=None, b3=None, n4=None, b4=None, n5=None, b5=None,
                    n6=None, b6=None, n7=None, b7=None, n8=None, b8=None):
        '''This data structure contains switch shunt parameters

        Args:
            index (int): unique switched shunt identifier
            i (int): the identifier of the bus that this switched shunt is connected to
            modsw (int): control mode (locked = 0, discrete = 1, continuous = 2, ... 6) (default = 1)
            adjm (int): adjustment method (input order = 0, admittance order = 1) (default = 0)
            stat (int): switched shunt status (in service = 1, out of service = 0)
            vswhi (float): control parameter upper bound (default = 1.0)
            vswlo (float): control parameter lower bound (default = 1.0)
            swrem (int): bus id to monitor reactive power (default = 0)
            rmpct (float): percentage of reactive power this shunt should contribute (default = 100.0)
            rmidnt (string): the name of the dc line or facts device where the reactive output should be controlled
            binit (float): initial shunt susceptance (MVAr per unit voltage) (default = 0.0)
            n1 (int): the number of steps in block 1 (default = 0)
            b1 (float): the susceptance increment of block 1 (default = 0.0)
            n2 (int): the number of steps in block 2 (default = 0)
            b2 (float): the susceptance increment of block 2 (default = 0.0)
            n3 (int): the number of steps in block 3 (default = 0)
            b3 (float): the susceptance increment of block 3 (default = 0.0)
            n4 (int): the number of steps in block 4 (default = 0)
            b4 (float): the susceptance increment of block 4 (default = 0.0)
            n5 (int): the number of steps in block 5 (default = 0)
            b5 (float): the susceptance increment of block 5 (default = 0.0)
            n6 (int): the number of steps in block 6 (default = 0)
            b6 (float): the susceptance increment of block 6 (default = 0.0)
            n7 (int): the number of steps in block 7 (default = 0)
            b7 (float): the susceptance increment of block 7 (default = 0.0)
            n8 (int): the number of steps in block 8 (default = 0)
            b8 (float): the susceptance increment of block 8 (default = 0.0)
        '''

        args = [modsw, adjm, stat, vswhi, vswlo, swrem, rmpct, rmidnt, binit, n1, b1, n2, b2, n3, b3, n4, b4, n5, b5, n6, b6, n7, b7, n8, b8]
        _set_defaults(args, SWITCHED_SHUNT_DEFAULTS)
        modsw, adjm, stat, vswhi, vswlo, swrem, rmpct, rmidnt, binit, n1, b1, n2, b2, n3, b3, n4, b4, n5, b5, n6, b6, n7, b7, n8, b8 = args

        self.index = int(index)
        self.i = int(i)
        self.modsw = int(modsw)
        self.adjm = int(adjm)
        self.stat = int(stat)
        self.vswhi = float(vswhi)
        self.vswlo = float(vswlo)
        self.swrem = int(swrem)
        self.rmpct = float(rmpct)
        self.rmidnt = unquote_string(rmidnt)
        self.binit = float(binit)
        self.n1 = int(n1)
        self.b1 = float(b1)
        self.n2 = _guard_none(int, n2)
        self.b2 = _guard_none(float, b2)
        self.n3 = _guard_none(int, n3)
        self.b3 = _guard_none(float, b3)
        self.n4 = _guard_none(int, n4)
        self.b4 = _guard_none(float, b4)
        self.n5 = _guard_none(int, n5)
        self.b5 = _guard_none(float, b5)
        self.n6 = _guard_none(int, n6)
        self.b6 = _guard_none(float, b6)
        self.n7 = _guard_none(int, n7)
        self.b7 = _guard_none(float, b7)
        self.n8 = _guard_none(int, n8)
        self.b8 = _guard_none(float, b8)

    def __str__(self):
        data = [self.index, self.i, self.modsw, self.adjm, self.stat, self.vswhi,
                self.vswlo, self.swrem, self.rmpct, self.rmidnt, self.binit,
                self.n1, self.b1, self.n2, self.b2, self.n3, self.b3, self.n4, self.b4,
                self.n5, self.b5, self.n6, self.b6, self.n7, self.b7, self.n8, self.b8]
        return ' '.join([str(x) for x in data])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def validate(self):
        '''Checks that this data structure conforms to the pss/e data
        specification
        '''
        _check_boolean(self.stat, 'status', 'switched shunt', self.index)
        _check_range(self.i, 'bus identifier', 'switched shunt', self.index, 1, 999997)
        _check_range(self.modsw, 'control mode', 'switched shunt', self.index, 0, 6)
        _check_boolean(self.adjm, 'status', 'switched shunt', self.index)
        _check_range(self.swrem, 'bus identifier', 'switched shunt', self.index, 0, 999997)
        _check_range(self.rmpct, 'reactive percentage', 'switched shunt', self.index, 0.0, 1.0)

        for key in ['n1','n2','n3','n4','n5','n6','n7','n8']:
            value = getattr(self, key)
            if value is not None:
                _check_range(value, 'bank {}'.format(key), 'switched shunt', self.index, 0, 9)

    def to_psse(self):
        '''Returns: a pss/e encoding of this data structure as a string'''

        data = [self.i, self.modsw, self.adjm, self.stat, self.vswhi,
                self.vswlo, self.swrem, self.rmpct, quote_string(self.rmidnt), self.binit,
                self.n1, self.b1]

        ids = [('n2', 'b2'), ('n3', 'b3'), ('n4', 'b4'), ('n5', 'b5'),
            ('n6', 'b6'), ('n7', 'b7'), ('n8', 'b8')]
        for ni, bi in ids:
            ni_value = getattr(self, ni)
            bi_value = getattr(self, bi)
            if ni_value is not None and bi_value is not None:
                data.append(ni_value)
                data.append(bi_value)

        return ', '.join([str(x) for x in data])


GENERATOR_DEFAULTS = [1, 0.0, 0.0, 9999.0, -9999.0, 1.0, 0, 100.0, 0.0, 1.0, 0.0, 0.0, 1.0, 1, 100.0, 9999.0, -9999.0, 1, 0, 0, 0, 1.0, 1.0, 1.0, 1.0, 0, 1.0]
class Generator(object):
    def __init__(self, index, i, id, pg, qg, qt, qb, vs, ireg, mbase, zr, zx,
                    rt, xt, gtap, stat, rmpct, pt, pb, o1, f1, o2, f2, o3, f3, o4, f4,
                    wmod, wpf):
        '''This data structure contains generator parameters.

        Args:
            index (int): unique generator identifier
            i (int): the identifier of the bus that this generator is connected to
            id (string): machine identifier (not unique)
            pg (float): active power output (MW)
            qg (float): reactive power output (MVAr)
            qt (float): reactive power output upper bound (MVAr)
            qb (float): reactive power output lower bound (MVAr)
            vs (float): voltage magnitude setpoint (volts p.u.)
            ireg (int): Remote controlled bus index (must be type 1), zero to control own voltage, and must be zero for gen at swing bus
            mbase (float): machine mva base (MVA)
            zr (float): machine resistance, pu on MBASE
            zx (float): machine reactance, pu on MBASE
            rt (float): step up transformer resistance, p.u. on MBASE
            xt (float): step up transformer reactance, p.u. on MBASE
            gtap (float): step up transformer off nominal turns ratio
            stat (int): generator status (in service = 1, out of service = 0)
            rmpct (float): percent of total VARS required to hold voltage at bus IREG to come from bus I - for remote buses controlled by several generators
            pt (float): active power output upper bound (MW)
            pb (float): active power output lower bound (MW)
            o1 (int): owner one id, 1-9999 (default = the owner of the connecting bus)
            f1 (float): owner one fraction of total ownership (default = 1.0)
            o2 (int): owner two id, 1-9999 (default = the owner of the connecting bus)
            f2 (float): owner two fraction of total ownership (default = 1.0)
            o3 (int): owner three id, 1-9999 (default = the owner of the connecting bus)
            f3 (float): owner three fraction of total ownership (default = 1.0)
            o4 (int): owner four id, 1-9999 (default = the owner of the connecting bus)
            f4 (float): owner four fraction of total ownership (default = 1.0)
            wmod (int): wind machine control mode, not-wind = 0, Q limits = 1, P limits as Q limits = 2, power factor = 4
            wpf (float): wind power factor (used when wmod is 2 or 3)
        '''

        args = [id, pg, qg, qt, qb, vs, ireg, mbase, zr, zx, rt, xt, gtap, stat, rmpct, pt, pb, o1, f1, o2, f2, o3, f3, o4, f4, wmod, wpf]
        _set_defaults(args, GENERATOR_DEFAULTS)
        id, pg, qg, qt, qb, vs, ireg, mbase, zr, zx, rt, xt, gtap, stat, rmpct, pt, pb, o1, f1, o2, f2, o3, f3, o4, f4, wmod, wpf = args

        self.index = int(index)
        self.i = int(i)
        self.id = unquote_string(id)
        self.pg = float(pg)
        self.qg = float(qg)
        self.qt = float(qt)
        self.qb = float(qb)
        self.vs = float(vs)
        self.ireg = int(ireg)
        self.mbase = float(mbase)
        self.zr = float(zr)
        self.zx = float(zx)
        self.rt = float(rt)
        self.xt = float(xt)
        self.gtap = float(gtap)
        self.stat = int(stat)
        self.rmpct = float(rmpct)
        self.pt = float(pt)
        self.pb = float(pb)
        self.o1 = int(o1)
        self.f1 = float(f1)
        self.o2 = int(o2)
        self.f2 = float(f2)
        self.o3 = int(o3)
        self.f3 = float(f3)
        self.o4 = int(o4)
        self.f4 = float(f4)
        self.wmod = int(wmod)
        self.wpf = float(wpf)

    def __str__(self):
        data = [self.index, self.i, self.id, self.pg, self.qg, self.qt, self.qb,
                self.vs, self.ireg, self.mbase, self.zr, self.zx, self.rt, self.xt,
                self.gtap, self.stat, self.rmpct, self.pt, self.pb, self.o1,
                self.f1, self.o2, self.f2, self.o3, self.f3, self.o4, self.f4,
                self.wmod, self.wpf]
        return ' '.join([str(x) for x in data])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def validate(self):
        '''Checks that this data structure conforms to the pss/e data
        specification
        '''
        _check_boolean(self.stat, 'stat', 'generator', self.index)

        _check_range(self.i, 'bus identifier', 'generator', self.index, 1, 999997)
        _check_range(self.ireg, 'regulator bus identifier', 'generator', self.index, 1, 999997)

        _check_owners(self, 'generator', self.index)
        # _check_range(self.o1, 'owner one', 'generator', self.index, 1, 9999)
        # _check_range(self.o2, 'owner two', 'generator', self.index, 1, 9999)
        # _check_range(self.o3, 'owner three', 'generator', self.index, 1, 9999)
        # _check_range(self.o4, 'owner four', 'generator', self.index, 1, 9999)

        # _check_range(self.f1, 'owner faction one', 'generator', self.index, 0.0, 1.0)
        # _check_range(self.f2, 'owner faction two', 'generator', self.index, 0.0, 1.0)
        # _check_range(self.f3, 'owner faction three', 'generator', self.index, 0.0, 1.0)
        # _check_range(self.f4, 'owner faction four', 'generator', self.index, 0.0, 1.0)

        _check_range(self.wmod, 'wmod', 'generator', self.index, 0, 3)
        _check_range(self.wpf, 'wpf', 'generator', self.index, 0.0, 1.0)

    def to_psse(self):
        '''Returns: a pss/e encoding of this data structure as a string'''

        data = [self.i, quote_string(self.id), self.pg, self.qg, self.qt, self.qb,
                self.vs, self.ireg, self.mbase, self.zr, self.zx, self.rt, self.xt,
                self.gtap, self.stat, self.rmpct, self.pt, self.pb, self.o1, self.f1,
                self.o2, self.f2, self.o3, self.f3, self.o4, self.f4, self.wmod,
                self.wpf]

        return ', '.join([str(x) for x in data])


BRANCH_DEFAULTS = [1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1, 1, 0.0, 1, 1.0, 0, 1.0, 0, 1.0, 0, 1.0]
class Branch(object):
    def __init__(self, index, i, j, ckt, r, x, b, ratea, rateb, ratec, gi, bi, gj, bj, st, met, len, o1, f1, o2, f2, o3, f3, o4, f4):
        '''This data structure contains branch parameters.

        Args:
            index (int): unique branch identifier
            i (int): the identifier of the from bus
            j (int): the identifier of the to bus, (note a leading minus indicates that the meter is on the from side of the line)
            ckt (str): circuit identifier
            r (float): the branch resistance (p.u.)
            x (float): the branch reactance (p.u.)
            b (float): the total branch charging susceptance (p.u.)
            ratea (float): base rating (MVA)
            rateb (float): shorter rating (MVA)
            ratec (float): shortest rating (MVA)
            gi (float): line shunt conductance at from end (bus i) (p.u.)
            bi (float): line shunt susceptance at from end (bus i) (p.u.)
            gj (float): line shunt conductance at to end (bus j) (p.u.)
            bj (float): line shunt susceptance at to end (bus j) (p.u.)
            st (int): branch status (in service = 1, out of service = 0)
            met (int): metered end flag (<= 1 indicates the i-bus, >= 2 indicates the j-bus)
            len (float): line length (user selected units)
            o1 (int): owner one id, 1-9999 (default = the owner of the connecting bus)
            f1 (float): owner one fraction of total ownership (default = 1.0)
            o2 (int): owner two id, 1-9999 (default = the owner of the connecting bus)
            f2 (float): owner two fraction of total ownership (default = 1.0)
            o3 (int): owner three id, 1-9999 (default = the owner of the connecting bus)
            f3 (float): owner three fraction of total ownership (default = 1.0)
            o4 (int): owner four id, 1-9999 (default = the owner of the connecting bus)
            f4 (float): owner four fraction of total ownership (default = 1.0)
        '''

        args = [ckt, b, ratea, rateb, ratec, gi, bi, gj, bj, st, met, len, o1, f1, o2, f2, o3, f3, o4, f4]
        _set_defaults(args, BRANCH_DEFAULTS)
        ckt, b, ratea, rateb, ratec, gi, bi, gj, bj, st, met, len, o1, f1, o2, f2, o3, f3, o4, f4 = args

        self.index = int(index)
        self.i = int(i)
        self.j = int(j)
        self.ckt = unquote_string(ckt)
        self.r = float(r)
        self.x = float(x)
        self.b = float(b)
        self.ratea = float(ratea)
        self.rateb = float(rateb)
        self.ratec = float(ratec)
        self.gi = float(gi)
        self.bi = float(bi)
        self.gj = float(gj)
        self.bj = float(bj)
        self.st = int(st)
        self.met = int(met)
        self.len = float(len)
        self.o1 = int(o1)
        self.f1 = float(f1)
        self.o2 = int(o2)
        self.f2 = float(f2)
        self.o3 = int(o3)
        self.f3 = float(f3)
        self.o4 = int(o4)
        self.f4 = float(f4)

    def __str__(self):
        data = [self.index, self.i, self.j, self.ckt, self.r, self.x, self.b,
                self.ratea, self.rateb, self.ratec, self.gi, self.bi, self.gj,
                self.bj, self.st, self.met, self.len, self.o1, self.f1, self.o2,
                self.f2, self.o3, self.f3, self.o4, self.f4]
        return ' '.join([str(x) for x in data])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def is_from_metered(self):
        return met <= 1

    def is_breaker(self):
        return '@' in self.ckt

    def is_switch(self):
        return '#' in self.ckt

    def validate(self):
        '''Checks that this data structure conforms to the pss/e data
        specification
        '''
        _check_boolean(self.st, 'st', 'branch', self.index)

        _check_range(self.i, 'bus i identifier', 'branch', self.index, 1, 999997)
        _check_range(self.j, 'bus j identifier', 'branch', self.index, 1, 999997)

        _check_owners(self, 'branch', self.index)

        if self.ckt[0] == '&':
            warnings.warn('on branch {} the ckt values cannot start with "&"'
                .format(self.index, self.i, self.j, self.st), PSSEDataWarning)

    def to_psse(self):
        '''Returns: a pss/e encoding of this data structure as a string'''

        data = [self.i, self.j, quote_string(self.ckt), self.r, self.x, self.b, self.ratea,
                self.rateb, self.ratec, self.gi, self.bi, self.gj, self.bj,
                self.st, self.met, self.len, self.o1, self.f1, self.o2, self.f2,
                self.o3, self.f3, self.o4, self.f4]

        return ', '.join([str(x) for x in data])



class TwoWindingTransformer(object):
    def __init__(self, index, p1, p2, w1, w2):
        '''This data structure contains two winding transformer parameters.

        Args:
            index (int): unique transformer identifier
            p1 (TransformerParametersFirstLine): first line of parameters
            p2 (TransformerParametersSecondLineShort): second line of parameters
            w1 (TransformerWinding): first winding data
            w2 (TransformerWindingShort): second winding data
        '''

        self.index = index
        self.p1 = p1
        self.p2 = p2
        self.w1 = w1
        self.w2 = w2

    def is_three_winding(self):
        return False

    def __str__(self):
        data = [self.index, self.p1, self.p2, self.w1, self.w2]
        return ' '.join([str(x) for x in data])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def validate(self):
        '''Checks that this data structure conforms to the pss/e data
        specification
        '''
        self.p1.validate(self.index)
        self.p2.validate(self.index)
        self.w1.validate(self.index)
        self.w2.validate(self.index)

    def to_psse(self):
        '''Returns: a pss/e encoding of this data structure as a string'''
        data = [self.p1, self.p2, self.w1, self.w2]
        return os.linesep.join([x.to_psse() for x in data])



class ThreeWindingTransformer(object):
    def __init__(self, index, p1, p2, w1, w2, w3):
        '''This data structure contains three winding transformer parameters.

        Args:
            index (int): unique transformer identifier
            p1 (TransformerParametersFirstLine): first line of parameters
            p2 (TransformerParametersSecondLine): second line of parameters
            w1 (TransformerWinding): first winding data
            w2 (TransformerWinding): second winding data
            w3 (TransformerWinding): third winding data
        '''

        self.index = index
        self.p1 = p1
        self.p2 = p2
        self.w1 = w1
        self.w2 = w2
        self.w3 = w3

    def __str__(self):
        data = [self.index, self.p1, self.p2, self.w1, self.w2, self.w3]
        return ' '.join([str(x) for x in data])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def is_three_winding(self):
        return True

    def validate(self):
        '''Checks that this data structure conforms to the pss/e data
        specification
        '''
        self.p1.validate(self.index)
        self.p2.validate(self.index)
        self.w1.validate(self.index)
        self.w2.validate(self.index)
        self.w3.validate(self.index)

    def to_psse(self):
        '''Returns: a pss/e encoding of this data structure as a string'''
        data = [self.p1, self.p2, self.w1, self.w2, self.w3]
        return os.linesep.join([x.to_psse() for x in data])



TRANSFORMER_FL_DEFAULTS = [0, 1, 1, 1, 1, 0.0, 0.0, 2, "            ", 1, 1, 1.0, 0, 1.0, 0, 1.0, 0, 1.0, "            "]
class TransformerParametersFirstLine(object):
    def __init__(self, i, j, k, ckt, cw, cz, cm, mag1, mag2, nmetr, name, stat, o1, f1, o2, f2, o3, f3, o4, f4, vecgrp):
        '''This data structure contains transformer parameters that are common to two and three winding transformers.

        Args:
            i (int): the identifier of the primary bus
            j (int): the identifier of the secondary bus
            k (int): the identifier of the tertiary bus (0 if a two winding transformer)
            ckt (string): circuit identifier
            cw (int): turn ratio units (1 = off-nominal pu winding bus base voltage, 2 = voltage kc, 3 = off-nominal pu nominal winding voltage)
            cz (int): winding impedance units (1 = pu on system mva base, 2 = pu on specified mva base, 3 = )
            cm (int): mag units (1 = pu on system mva, 2 = )
            mag1 (float): ground conductance on the primary bus
            mag2 (float): ground susceptance on the primary bus
            nmetr (int): the nonmetered end of the transformer the primary, secondary, and tertiary buses are specified by 1,2,3 respectively
            name (string): name of the transformer
            stat (int): transformer status (0 = out of service, 1 = in service, 2 = winding 2 out, 3 = winding 3 out, 4 = winding 1 out)
            o1 (int): owner one id, 1-9999 (default = the owner of the connecting bus)
            f1 (float): owner one fraction of total ownership (default = 1.0)
            o2 (int): owner two id, 1-9999 (default = the owner of the connecting bus)
            f2 (float): owner two fraction of total ownership (default = 1.0)
            o3 (int): owner three id, 1-9999 (default = the owner of the connecting bus)
            f3 (float): owner three fraction of total ownership (default = 1.0)
            o4 (int): owner four id, 1-9999 (default = the owner of the connecting bus)
            f4 (float): owner four fraction of total ownership (default = 1.0)
            vecgrp (string): vector group identifier (default = '            ')
        '''

        args = [k, ckt, cw, cz, cm, mag1, mag2, nmetr, name, stat, o1, f1, o2, f2, o3, f3, o4, f4, vecgrp]
        _set_defaults(args, TRANSFORMER_FL_DEFAULTS)
        k, ckt, cw, cz, cm, mag1, mag2, nmetr, name, stat, o1, f1, o2, f2, o3, f3, o4, f4, vecgrp = args

        self.i = int(i)
        self.j = int(j)
        self.k = int(k)
        self.ckt = unquote_string(ckt)
        self.cw = int(cw)
        self.cz = int(cz)
        self.cm = int(cm)
        self.mag1 = float(mag1)
        self.mag2 = float(mag2)
        self.nmetr = int(nmetr)
        self.name = unquote_string(name)
        self.stat = int(stat)
        self.o1 = int(o1)
        self.f1 = float(f1)
        self.o2 = int(o2)
        self.f2 = float(f2)
        self.o3 = int(o3)
        self.f3 = float(f3)
        self.o4 = int(o4)
        self.f4 = float(f4)
        self.vecgrp = unquote_string(vecgrp)

    def __str__(self):
        data = [self.i, self.j, self.k, self.ckt, self.cw, self.cz, self.cm,
                self.mag1, self.mag2, self.nmetr, self.name, self.stat, self.o1,
                self.f1, self.o2, self.f2, self.o3, self.f3, self.o4, self.f4,
                self.vecgrp]
        return ' '.join([str(x) for x in data])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def validate(self, transformer_id):
        '''Checks that this data structure conforms to the pss/e data
        specification
        '''
        _check_range(self.stat, 'stat', 'transformer', transformer_id, 0, 4)

        _check_range(self.i, 'bus i identifier', 'transformer', transformer_id, 1, 999997)
        _check_range(self.j, 'bus j identifier', 'transformer', transformer_id, 1, 999997)
        _check_range(self.k, 'bus k identifier', 'transformer', transformer_id, 0, 999997)

        _check_range(self.cw, 'cw', 'transformer', transformer_id, 1, 3)
        _check_range(self.cz, 'cz', 'transformer', transformer_id, 1, 3)
        _check_range(self.cm, 'cm', 'transformer', transformer_id, 1, 2)

        _check_owners(self, 'transformer', transformer_id)


    def to_psse(self):
        '''Returns: a pss/e encoding of this data structure as a string'''

        data = [self.i, self.j, self.k, quote_string(self.ckt), self.cw, self.cz, self.cm,
                self.mag1, self.mag2, self.nmetr, quote_string(self.name), self.stat, self.o1,
                self.f1, self.o2, self.f2, self.o3, self.f3, self.o4, self.f4,
                quote_string(self.vecgrp)]

        return ', '.join([str(x) for x in data])



TRANSFORMER_SL_DEFAULTS = [0.0, 100.0, 0.0, 100.0, 0.0, 100.0, 1.0, 0.0]
class TransformerParametersSecondLine(object):
    def __init__(self, r12, x12, sbase12, r23, x23, sbase23, r31, x31, sbase31, vmstar, anstar):
        '''This data structure contains transformer parameters for the second line of three winding transformers.

        Args:
            r12 (float): resistance between terminal i and j (default 0.0)
            x12 (float): reactance between terminal i and j
            sbase12 (float): the MVA base between terminal i and j
            r23 (float): resistance between terminal j and k (default 0.0)
            x23 (float): reactance between terminal j and k
            sbase23 (float): the MVA base between terminal j and k
            r31 (float): resistance between terminal k and i (default 0.0)
            x31 (float): reactance between terminal k and i
            sbase31 (float): the MVA base between terminal k and i
            vmstar (float): the voltage magnitude of the start point (default 1.0)
            anstar (float): the voltage angle of the start point (default 0.0)
        '''

        args = [r12, sbase12, r23, sbase23, r31, sbase31, vmstar, anstar]
        _set_defaults(args, TRANSFORMER_SL_DEFAULTS)
        r12, sbase12, r23, sbase23, r31, sbase31, vmstar, anstar = args

        self.r12 = float(r12)
        self.x12 = float(x12)
        self.sbase12 = float(sbase12)
        self.r23 = float(r23)
        self.x23 = float(x23)
        self.sbase23 = float(sbase23)
        self.r31 = float(r31)
        self.x31 = float(x31)
        self.sbase31 = float(sbase31)
        self.vmstar = float(vmstar)
        self.anstar = float(anstar)

    def __str__(self):
        data = [self.r12, self.x12, self.sbase12, self.r23, self.x23,
                self.sbase23, self.r31, self.x31, self.sbase31, self.vmstar,
                self.anstar]
        return ' '.join([str(x) for x in data])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def validate(self, transformer_id):
        '''Checks that this data structure conforms to the pss/e data
        specification
        '''
        pass

    def to_psse(self):
        '''Returns: a pss/e encoding of this data structure as a string'''

        data = [self.r12, self.x12, self.sbase12, self.r23, self.x23,
                self.sbase23, self.r31, self.x31, self.sbase31, self.vmstar,
                self.anstar]

        return ', '.join([str(x) for x in data])



TRANSFORMER_SLS_DEFAULTS = [0.0, 100.0]
class TransformerParametersSecondLineShort(object):
    def __init__(self, r12, x12, sbase12):
        '''This data structure contains transformer parameters for the second line of two winding transformers.

        Args:
            r12 (float): resistance between terminal i and j (default 0.0)
            x12 (float): reactance between terminal i and j
            sbase12 (float): the MVA base between terminal i and j
        '''

        args = [r12, sbase12]
        _set_defaults(args, TRANSFORMER_SLS_DEFAULTS)
        r12, sbase12 = args

        self.r12 = float(r12)
        self.x12 = float(x12)
        self.sbase12 = float(sbase12)

    def __str__(self):
        data = [self.r12, self.x12, self.sbase12]
        return ' '.join([str(x) for x in data])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def validate(self, transformer_id):
        '''Checks that this data structure conforms to the pss/e data
        specification
        '''
        pass

    def to_psse(self):
        '''Returns: a pss/e encoding of this data structure as a string'''

        data = [self.r12, self.x12, self.sbase12]

        return ', '.join([str(x) for x in data])


TRANSFORMER_WINDING_DEFAULTS = [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0, 0, 1.1, 0.9, 1.1, 0.9, 33, 0, 0.0, 0.0, 0.0]
class TransformerWinding(object):
    def __init__(self, index, windv, nomv, ang, rata, ratb, ratc, cod, cont, rma, rmi, vma, vmi, ntp, tab, cr, cx, cnxa):
        '''This data structure contains transformer winding parameters.

        Args:
            index (int): transformer winding identifier (1,2,3)
            windv (float): off-nominal turn ratio (p.u.) (default = 1.0)
            nomv (float): base voltage (kilo volts)
            ang (float): angle shift (degrees)
            rata (float): base rating (MVA)
            ratb (float): shorter rating (MVA)
            ratc (float): shortest rating (MVA)
            cod (int): transformer control mode
            cont (int): remote bus index for transformer voltage control ()
            rma (float): off-nominal turn ratio upper bound
            rmi (float): off-nominal turn ratio lower bound
            vma (float): controller band upper limit
            vmi (float): controller band lower limit
            ntp (int): number of tap positions available 2-9999 (default = 33)
            tab (int): the identifier of the transformer impedance correction table
            cr (float): load drop compensation resistance (p.u.)
            cx (float): load drop compensation reactance (p.u.)
            cnxa (float): winding connection angle (degrees) (default = 0.0)
        '''

        args = [windv, nomv, ang, rata, ratb, ratc, cod, cont, rma, rmi, vma, vmi, ntp, tab, cr, cx, cnxa]
        _set_defaults(args, TRANSFORMER_WINDING_DEFAULTS)
        windv, nomv, ang, rata, ratb, ratc, cod, cont, rma, rmi, vma, vmi, ntp, tab, cr, cx, cnxa = args

        self.index = int(index)
        self.windv = float(windv)
        self.nomv = float(nomv)
        self.ang = float(ang)
        self.rata = float(rata)
        self.ratb = float(ratb)
        self.ratc = float(ratc)
        self.cod = int(cod)
        self.cont = int(cont)
        self.rma = float(rma)
        self.rmi = float(rmi)
        self.vma = float(vma)
        self.vmi = float(vmi)
        self.ntp = int(ntp)
        self.tab = int(tab)
        self.cr = float(cr)
        self.cx = float(cx)
        self.cnxa = float(cnxa)

    def __str__(self):
        data = [self.index, self.windv, self.nomv, self.ang, self.rata, self.ratb,
                self.ratc, self.cod, self.cont, self.rma, self.rmi, self.vma,
                self.vmi, self.ntp, self.tab, self.cr, self.cx, self.cnxa]
        return ' '.join([str(x) for x in data])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def validate(self, transformer_id):
        '''Checks that this data structure conforms to the pss/e data
        specification
        '''
        winding_id = '{} winding {}'.format(transformer_id, self.index)
        _check_range(self.index, 'winding index', 'transformer', self.transformer_id, 1, 3)
        _check_range(self.ang, 'angle shift', 'transformer', winding_id, -180.0, 180.0)
        _check_range(self.cod, 'control mode', 'transformer', winding_id, -5, 5)
        _check_range(self.cont, 'bus identifier', 'transformer', winding_id, 1, 999997)
        _check_range(self.ntp, 'tap positions', 'transformer', winding_id, 2, 9999)
        _check_range(self.tab, 'impedance correction table', 'transformer', winding_id, 1, float('Inf'))

    def to_psse(self):
        '''Returns: a pss/e encoding of this data structure as a string'''

        data = [self.windv, self.nomv, self.ang, self.rata, self.ratb,
                self.ratc, self.cod, self.cont, self.rma, self.rmi, self.vma,
                self.vmi, self.ntp, self.tab, self.cr, self.cx, self.cnxa]

        return ', '.join([str(x) for x in data])


TRANSFORMER_WINDING_SHORT_DEFAULTS = [1.0, 0.0]
class TransformerWindingShort(object):
    def __init__(self, index, windv, nomv):
        '''This data structure contains the shortend transformer winding
        parameters for the secondary side of a two winding transformer

        Args:
            index (int): transformer winding identifier (1,2,3)
            windv (float): off-nominal turn ratio (p.u.) (default = 1.0)
            nomv (float): base voltage (kilo volts)
        '''

        args = [windv, nomv]
        _set_defaults(args, TRANSFORMER_WINDING_SHORT_DEFAULTS)
        windv, nomv = args

        self.index = int(index)
        self.windv = float(windv)
        self.nomv = float(nomv)

    def __str__(self):
        data = [self.index, self.windv, self.nomv]
        return ' '.join([str(x) for x in data])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def validate(self, transformer_id):
        '''Checks that this data structure conforms to the pss/e data
        specification
        '''
        winding_id = '{} winding {}'.format(transformer_id, self.index)
        _check_range(self.index, 'winding index', 'transformer', self.transformer_id, 1, 3)

    def to_psse(self):
        '''Returns: a pss/e encoding of this data structure as a string'''

        data = [self.windv, self.nomv]

        return ', '.join([str(x) for x in data])



AREA_DEFAULTS = [0, 0.0, 10.0, "            "]
class Area(object):
    def __init__(self, i, isw="0", pdes="0.0", ptol="0.0", arnam=''):
        '''This data structure contains area interchange parameters.

        Args:
            i (int): the identifier of the area
            isw (int): the identifier of the interchange slack bus
            pdes (float): desired net area interchange (MW)
            ptol (float): interchange tolerance (MW += out)
            arnam (string): area name, 8 characters, must be enclosed in single quotes
        '''

        args = [isw, pdes, ptol, arnam]
        _set_defaults(args, AREA_DEFAULTS)
        isw, pdes, ptol, arnam = args

        self.i = int(i)
        self.isw = int(isw)
        self.pdes = float(pdes)
        self.ptol = float(ptol)
        self.arnam = unquote_string(arnam)


    def __str__(self):
        data = [self.i, self.isw, self.pdes, self.ptol, self.arnam]
        return ' '.join([str(x) for x in data])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def validate(self):
        '''Checks that this data structure conforms to the pss/e data
        specification
        '''
        _check_range(self.i, 'id', 'area', self.i, 1, 9999)

    def to_psse(self):
        '''Returns: a pss/e encoding of this data structure as a string'''

        data = [self.i, self.isw, self.pdes, self.ptol, quote_string(self.arnam)]

        return ', '.join([str(x) for x in data])


ZONE_DEFAULTS = ["            "]
class Zone(object):
    def __init__(self, i, zoname):
        '''This data structure contains zone parameters.

        Args:
            i (int): the identifier of the zone
            zoname (string): zone name
        '''

        args = [zoname]
        _set_defaults(args, ZONE_DEFAULTS)
        zoname = args[0]

        self.i = int(i)
        self.zoname = unquote_string(zoname)


    def __str__(self):
        data = [self.i, self.zoname]
        return ' '.join([str(x) for x in data])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def validate(self):
        '''Checks that this data structure conforms to the pss/e data
        specification
        '''
        _check_range(self.i, 'id', 'zone', self.i, 1, 9999)


    def to_psse(self):
        '''Returns: a pss/e encoding of this data structure as a string'''

        data = [self.i, quote_string(self.zoname)]

        return ', '.join([str(x) for x in data])


OWNER_DEFAULTS = ["            "]
class Owner(object):
    def __init__(self, i, owname):
        '''This data structure contains owner parameters.

        Args:
            i (int): the identifier of the owner
            owname (string): owner name
        '''

        args = [owname]
        _set_defaults(args, OWNER_DEFAULTS)
        owname = args[0]

        self.i = int(i)
        self.owname = unquote_string(owname)

    def __str__(self):
        data = [self.i, self.owname]
        return ' '.join([str(x) for x in data])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def validate(self):
        '''Checks that this data structure conforms to the pss/e data
        specification
        '''
        _check_range(self.i, 'id', 'owner', self.i, 1, 9999)

    def to_psse(self):
        '''Returns: a pss/e encoding of this data structure as a string'''

        data = [self.i, quote_string(self.owname)]

        return ', '.join([str(x) for x in data])


FACTS_DEFAULTS = [0, 1, 0.0, 0.0, 1.0, 9999.0, 9999.0, 0.9, 1.1, 1.0, 0.0, 0.05, 100.0, 1, 0.0, 0.0, 0, 0, ""]
class FACTSDevice(object):
    def __init__(self, index, name, i, j, mode, pdes, qdes, vset, shmx, trmx, vtmn, vtmx, vsmx, imx, linx, rmpct, owner, set1, set2, vsref, remot="0", mname=''):
        '''This data structure contains FACTS device parameters.

        Args:
            index (int) : unique FACTS device identifier
            name (str) : name of device
            i (int) : sending end bus number
            j (int) : terminal end bus number
            mode (int) : control mode (status)
            pdes (float) : desired active power flow at j
            qdes (float) : desired reactive power flow at j
            vset (float) : voltage setpoint at i
            shmx (float) : max shunt current at i
            trmx (float) : max active power transfer
            vtmn (float) : min voltage at j
            vtmx (float) : max voltage at j
            vsmx (float) : max series voltage
            imx (float) : max series current
            linx (float) : reactance of dummy series element
            rmpct (float) : percent of Mvar required to hold voltage at bus controlled by shunt element
            owner (int) : owner number
            set1 (float) : resistance of constant impedance, or min of constant series voltage magnitude, or real component of constant series voltage
            set2 (float) : reactance of constant impedance, or max of constant series voltage magnitude, or imaginary component of constant series voltage
            vsref (int) : series voltage reference code
            remot (int) : bus number of bus regulated by shunt element
            mname (str) : name of the IPFC master FACTS Device
        '''

        args = [j, mode, pdes, qdes, vset, shmx, trmx, vtmn, vtmx, vsmx, imx, linx, rmpct, owner, set1, set2, vsref, remot, mname]
        _set_defaults(args, FACTS_DEFAULTS)
        j, mode, pdes, qdes, vset, shmx, trmx, vtmn, vtmx, vsmx, imx, linx, rmpct, owner, set1, set2, vsref, remot, mname = args

        self.index = index
        self.name = unquote_string(name)
        self.i = int(i)
        self.j = int(j)
        self.mode = int(mode)
        self.pdes = float(pdes)
        self.qdes = float(qdes)
        self.vset = float(vset)
        self.shmx = float(shmx)
        self.trmx = float(trmx)
        self.vtmn = float(vtmn)
        self.vtmx = float(vtmx)
        self.vsmx = float(vsmx)
        self.imx = float(imx)
        self.linx = float(linx)
        self.rmpct = float(rmpct)
        self.owner = int(owner)
        self.set1 = float(set1)
        self.set2 = float(set2)
        self.vsref = int(vsref)
        self.remot = int(remot)
        self.mname = unquote_string(mname)

    def __str__(self):
        data = [self.name, self.im, self.j, self.mode, self.pdes, self.qdes,
                self.vset, self.shmx, self.trmx, self.vtmn, self.vtmx, self.vsmx,
                self.imx, self.linx, self.rmpct, self.owner, self.set1, self.set2,
                self.vsref, self.remot, self.mname]
        return ' '.join([str(x) for x in data])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def validate(self):
        '''Checks that this data structure conforms to the pss/e data
        specification
        '''
        _check_range(self.owner, 'owner', 'bus', self.i, 1, 9999)

    def to_psse(self):
        '''Returns: a pss/e encoding of this data structure as a string'''

        data = [quote_string(self.name), self.i, self.j, self.mode, self.pdes, self.qdes,
                self.vset, self.shmx, self.trmx, self.vtmn, self.vtmx, self.vsmx,
                self.imx, self.linx, self.rmpct, self.owner, self.set1, self.set2,
                self.vsref, self.remot, quote_string(self.mname)]

        return ', '.join([str(x) for x in data])


class VSCDCLine(object):
    def __init__(self, index, params, c1, c2):
        '''This data structure contains VSC DC Line parameters.

        Args:
            index (int) : unique vsc dc line identifier
            params (VSCDCLineParameters) : first line of VSC DC line data entry
            c1 (VSCDCLineConverter) : second line of VSC DC Line data entry (converter 1)
            c2 (VSCDCLineConverter) : third line of VSC DC Line data entry (converter 2)
        '''
        self.index = index
        self.params = params
        self.c1 = c1
        self.c2 = c2

    def __str__(self):
        data = [self.params, self.c1, self.c2]
        return ' '.join([str(x) for x in data])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def validate(self):
        '''Checks that this data structure conforms to the pss/e data
        specification
        '''
        return NotImplemented

    def to_psse(self):
        '''Returns: a pss/e encoding of this data structure as a string'''
        data = [self.params, self.c1, self.c2]
        return os.linesep.join([x.to_psse() for x in data])



VSC_DCL_DEFAULTS = [1, 1, 1.0, 0, 1.0, 0, 1.0, 0, 1.0]
class VSCDCLineParameters(object):
    def __init__(self, name, mdc, rdc, o1="0", f1="1", o2="0", f2="1", o3="0", f3="1", o4="0", f4="1"):
        '''This data structure contains VSC DC line first-line parameters

        Args:
            name (str) : name of VSC DC Line
            mdc (int) : control mode (status)
            rdc (float) : dc line resistance
            oi (int) : owner number
            fi (float) : fraction of total ownership assigned to oi
        '''

        args = [mdc, o1, f1, o2, f2, o3, f3, o4, f4]
        _set_defaults(args, VSC_DCL_DEFAULTS)
        mdc, o1, f1, o2, f2, o3, f3, o4, f4 = args

        self.name = unquote_string(name)
        self.mdc = int(mdc)
        self.rdc = float(rdc)
        self.o1 = int(o1)
        self.f1 = float(f1)
        self.o2 = int(o2)
        self.f2 = float(f2)
        self.o3 = int(o3)
        self.f3 = float(f3)
        self.o4 = int(o4)
        self.f4 = float(f4)

    def __str__(self):
        data = [self.name, self.mdc, self.rdc, self.o1, self.f1,
                self.o2, self.f2, self.o3, self.f3, self.o4, self.f4]
        return ' '.join([str(x) for x in data])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def validate(self):
        '''Checks that this data structure conforms to the pss/e data
        specification
        '''
        pass

    def to_psse(self):
        '''Returns: a pss/e encoding of this data structure as a string'''
        data = [quote_string(self.name), self.mdc, self.rdc, self.o1, self.f1,
                self.o2, self.f2, self.o3, self.f3, self.o4, self.f4]
        return ', '.join([str(x) for x in data])



VSC_DCC_DEFAULTS = [1, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 9999.0, -9999.0, 0, 100.0]
class VSCDCLineConverter(object):
    def __init__(self, ibus, type, mode, dcset, acset, aloss, bloss, minloss, smax, imax, pwf, maxq, minq, remot="0", rmpct="100.0"):
        '''This data structure contains VSC DC Line Converter parameters

        Args:
            ibus (int) : bus number
            type (int) : type of converter dc control
            mode (int) : ac control mode
            dcset (float) : dc setpoint
            acset (float) : ac setpoint
            aloss (float) : coefficient to linear equation for converter losses
            bloss (float) : coefficient to linear equation for converter losses
            minloss (float) : minimum losses
            smax (float) : MVA rating
            imax (float) : ac current rating
            pwf (float) : power weighting factor
            maxq (float) : reactive power upper limit
            minq (float) : reactive power lower limit
            remot (int) : bus number of remote regulating bus
            rmpct (float) : percent of Mvar required to hold bus voltage
        '''

        args = [mode, acset, aloss, bloss, minloss, smax, imax, pwf, maxq, minq, remot, rmpct]
        _set_defaults(args, VSC_DCC_DEFAULTS)
        mode, acset, aloss, bloss, minloss, smax, imax, pwf, maxq, minq, remot, rmpct = args

        self.ibus = int(ibus)
        self.type = int(type)
        self.mode = int(mode)
        self.dcset = float(dcset)
        self.acset = float(acset)
        self.aloss = float(aloss)
        self.bloss = float(bloss)
        self.minloss = float(minloss)
        self.smax = float(smax)
        self.imax = float(imax)
        self.pwf = float(pwf)
        self.maxq = float(maxq)
        self.minq = float(minq)
        self.remot = int(remot)
        self.rmpct = float(rmpct)

    def __str__(self):
        data = [self.ibus, self.type, self.mode, self.dcset, self.acset, self.aloss,
                self.bloss, self.minloss, self.smax, self.imax, self.pwf, self.maxq,
                self.minq, self.remot, self.rmpct]
        return ' '.join([str(x) for x in data])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def validate(self):
        '''Checks that this data structure conforms to the pss/e data
        specification
        '''
        pass

    def to_psse(self):
        '''Returns: a pss/e encoding of this data structure as a string'''
        data = [self.ibus, self.type, self.mode, self.dcset, self.acset, self.aloss,
                self.bloss, self.minloss, self.smax, self.imax, self.pwf, self.maxq,
                self.minq, self.remot, self.rmpct]
        return ', '.join([str(x) for x in data])



class TwoTerminalDCLine(object):
    def __init__(self, index, params, rectifier, inverter):
        '''This data structure contains Two-Terminal DC Line parameters.

        Args:
            index (int) : unique two-terminal dc line identifier
            params (TwoTerminalDCLineParameters) : first line of two-terminal dc line data entry
            rectifier (TwoTerminalDCLineRectifier) : second line of two-terminal dc line data entry
            inverter (TwoTerminalDCLineInverter) : third line of two-terminal dc line data entry
        '''
        self.index = index
        self.params = params
        self.rectifier = rectifier
        self.inverter = inverter

    def __str__(self):
        data = [self.params, self.rectifier, self.inverter]
        return ' '.join([str(x) for x in data])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def validate(self):
        '''Checks that this data structure conforms to the pss/e data
        specification
        '''
        return NotImplemented

    def to_psse(self):
        '''Returns: a pss/e encoding of this data structure as a string'''
        data = [self.params, self.rectifier, self.inverter]
        return os.linesep.join([x.to_psse() for x in data])


TTDCL_PARAMETER_DEFAULTS = [0, 0.0, 0.0, 0.0, "I", 0.0, 20, 1.0]
class TwoTerminalDCLineParameters(object):
    def __init__(self, name, mdc, rdc, setvl, vschd, vcmod, rcomp, delti, meter, dcvmin, cccitmx, cccacc):
        '''This data structure contains Two-Terminal DC Line parameters for the first line of the data entry

        Args:
            name (str) : name of the dc line
            mdc (int) : control mode (status)
            rdc (float) : dc line resistance
            setvl (float) : current or power demand
            vschd (float) : scheduled dc voltage
            vcmod (float) : switch dc voltage
            rcomp (float) : compounding resistance
            delti (float) : margin of desired dc power or current
            meter (str) : metered end code
            dcvmin (float) : minimum compounded dc voltage
            cccitmx (int) : iteration limit for solution proceedure
            cccacc (float) : acceleration factor for solution proceedure
        '''

        args = [mdc, vcmod, rcomp, delti, meter, dcvmin, cccitmx, cccacc]
        _set_defaults(args, TTDCL_PARAMETER_DEFAULTS)
        mdc, vcmod, rcomp, delti, meter, dcvmin, cccitmx, cccacc = args

        self.name = unquote_string(name)
        self.mdc = int(mdc)
        self.rdc = float(rdc)
        self.setvl = float(setvl)
        self.vschd = float(vschd)
        self.vcmod = float(vcmod)
        self.rcomp = float(rcomp)
        self.delti = float(delti)
        self.meter = unquote_string(meter)
        self.dcvmin = float(dcvmin)
        self.cccitmx = int(cccitmx)
        self.cccacc = float(cccacc)

    def __str__(self):
        data = [self.name, self.mdc, self.rdc, self.setvl, self.vschd, self.vcmod,
                self.rcomp, self.delti, self.meter, self.dcvmin, self.cccitmx,
                self.cccacc]
        return ' '.join([str(x) for x in data])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def validate(self):
        '''Checks that this data structure conforms to the pss/e data
        specification
        '''
        return NotImplemented

    def to_psse(self):
        '''Returns: a pss/e encoding of this data structure as a string'''

        data = [quote_string(self.name), self.mdc, self.rdc, self.setvl, self.vschd,
                self.vcmod, self.rcomp, self.delti, self.meter, self.dcvmin, self.cccitmx,
                self.cccacc]

        return ', '.join([str(x) for x in data])


TTDCL_RECTIFIER_DEFAULTS = [1.0, 1.0, 1.5, 0.51, 0.00625, 0, 0, 0, "1", 0.0]
class TwoTerminalDCLineRectifier(object):
    def __init__(self, ipr, nbr, anmxr, anmnr, rcr, xcr, ebasr, trr, tapr, tmxr, tmnr, stpr, icr, ifr, itr, idr, xcapr):
        '''This data structure contains Two-Terminal DC Line parameters for the Rectifier (second line)

        Args:
            ipr (int) : bus number
            nbr (int) : number of bridges
            anmxr (float) : nominal max firing angle
            anmnr (float) : minimum steady-state firing angle
            rcr (float) : transformer resistance per bridge
            xcr (float) : transformer reactance per bridge
            ebasr (float) : primary base ac voltage
            trr (float) : transformer ratio
            tapr (float) : tap setting
            tmxr (float) : max tap setting
            tmnr (float) : min tap setting
            stpr (float) : tap step
            icr (int) : firing angle measuring bus number
            ifr (int) : winding 1 side from bus number
            itr (int) : winding 2 side to bus number
            idr (str) : circuit identifier
            xcapr (float) : capacitor resistance per bridge
        '''

        args = [trr, tapr, tmxr, tmnr, stpr, icr, ifr, itr, idr, xcapr]
        _set_defaults(args, TTDCL_RECTIFIER_DEFAULTS)
        trr, tapr, tmxr, tmnr, stpr, icr, ifr, itr, idr, xcapr = args

        self.ipr = int(ipr)
        self.nbr = int(nbr)
        self.anmxr = float(anmxr)
        self.anmnr = float(anmnr)
        self.rcr = float(rcr)
        self.xcr = float(xcr)
        self.ebasr = float(ebasr)
        self.trr = float(trr)
        self.tapr = float(tapr)
        self.tmxr = float(tmxr)
        self.tmnr = float(tmnr)
        self.stpr = float(stpr)
        self.icr = int(icr)
        self.ifr = int(ifr)
        self.itr = int(itr)
        self.idr = unquote_string(idr)
        self.xcapr = float(xcapr)

    def __str__(self):
        data = [self.ipr, self.nbr, self.anmxr, self.anmnr, self.rcr,
                self.xcr, self.ebasr, self.trr, self.tapr, self.tmxr,
                self.tmnr, self.stpr, self.icr, self.ifr, self.itr,
                self.idr, self.xcapr]
        return ' '.join([str(x) for x in data])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def validate(self):
        '''Checks that this data structure conforms to the pss/e data
        specification
        '''
        return NotImplemented

    def to_psse(self):
        '''Returns: a pss/e encoding of this data structure as a string'''

        data = [self.ipr, self.nbr, self.anmxr, self.anmnr, self.rcr,
                self.xcr, self.ebasr, self.trr, self.tapr, self.tmxr,
                self.tmnr, self.stpr, self.icr, self.ifr, self.itr,
                quote_string(self.idr), self.xcapr]

        return ', '.join([str(x) for x in data])



TTDCL_INVERTER_DEFAULTS = [1.0, 1.0, 1.5, 0.51, 0.00625, 0, 0, 0, "1", 0.0]
class TwoTerminalDCLineInverter(object):
    def __init__(self, ipi, nbi, anmxi, anmni, rci, xci, ebasi, tri, tapi, tmxi, tmni, stpi, ici, ifi, iti, idi, xcapi):
        '''This data structure contains Two-Terminal DC Line parameters for the Inverter (third line)

        Args:
            ipi (int) : bus number
            nbi (int) : number of bridges
            anmxi (float) : nominal max firing angle
            anmni (float) : minimum steady-state firing angle
            rci (float) : transformer resistance per bridge
            xci (float) : transformer reactance per bridge
            ebasi (float) : primary base ac voltage
            tri (float) : transformer ratio
            tapi (float) : tap setting
            tmxi (float) : max tap setting
            tmni (float) : min tap setting
            stpi (float) : tap step
            ici (int) : firing angle measuring bus number
            ifi (int) : winding 1 side from bus number
            iti (int) : winding 2 side to bus number
            idi (str) : circuit identifier
            xcapi (float) : capacitor resistance per bridge
        '''

        args = [tri, tapi, tmxi, tmni, stpi, ici, ifi, iti, idi, xcapi]
        _set_defaults(args, TTDCL_INVERTER_DEFAULTS)
        tri, tapi, tmxi, tmni, stpi, ici, ifi, iti, idi, xcapi = args

        self.ipi = int(ipi)
        self.nbi = int(nbi)
        self.anmxi = float(anmxi)
        self.anmni = float(anmni)
        self.rci = float(rci)
        self.xci = float(xci)
        self.ebasi = float(ebasi)
        self.tri = float(tri)
        self.tapi = float(tapi)
        self.tmxi = float(tmxi)
        self.tmni = float(tmni)
        self.stpi = float(stpi)
        self.ici = int(ici)
        self.ifi = int(ifi)
        self.iti = int(iti)
        self.idi = unquote_string(idi)
        self.xcapi = float(xcapi)

    def __str__(self):
        data = [self.ipi, self.nbi, self.anmxi, self.anmni, self.rci,
                self.xci, self.ebasi, self.tri, self.tapi, self.tmxi,
                self.tmni, self.stpi, self.ici, self.ifi, self.iti,
                self.idi, self.xcapi]
        return ' '.join([str(x) for x in data])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def validate(self):
        '''Checks that this data structure conforms to the pss/e data
        specification
        '''
        return NotImplemented

    def to_psse(self):
        '''Returns: a pss/e encoding of this data structure as a string'''

        data = [self.ipi, self.nbi, self.anmxi, self.anmni, self.rci,
                self.xci, self.ebasi, self.tri, self.tapi, self.tmxi,
                self.tmni, self.stpi, self.ici, self.ifi, self.iti,
                quote_string(self.idi), self.xcapi]

        return ', '.join([str(x) for x in data])


IMPEDANCE_CORRECTION_DEFAULTS = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
class TransformerImpedanceCorrection(object):
    def __init__(self, index, i, t1="0.0", f1="0.0", t2="0.0", f2="0.0", t3="0.0", f3="0.0", t4="0.0", f4="0.0", t5="0.0", f5="0.0", t6="0.0", f6="0.0", t7="0.0", f7="0.0", t8="0.0", f8="0.0", t9="0.0", f9="0.0", t10="0.0", f10="0.0", t11="0.0", f11="0.0"):
        '''This data structure contains Transformer Impedence Correction Table parameters

        Args:
            index (int) : unique transformer impedence correction identifier
            i (int) : transformer impedence correction table number
            ti (float) : off-nominal turns ratio or phase shift angle
            fi (float) : scaling factor
        '''

        args = [t1, f1, t2, f2, t3, f3, t4, f4, t5, f5, t6, f6, t7, f7, t8, f8, t9, f9, t10, f10, t11, f11]
        _set_defaults(args, IMPEDANCE_CORRECTION_DEFAULTS)
        t1, f1, t2, f2, t3, f3, t4, f4, t5, f5, t6, f6, t7, f7, t8, f8, t9, f9, t10, f10, t11, f11 = args

        self.index = index
        self.i = int(i)
        self.t1 = float(t1)
        self.f1 = float(f1)
        self.t2 = float(t2)
        self.f2 = float(f2)
        self.t3 = float(t3)
        self.f3 = float(f3)
        self.t4 = float(t4)
        self.f4 = float(f4)
        self.t5 = float(t5)
        self.f5 = float(f5)
        self.t6 = float(t6)
        self.f6 = float(f6)
        self.t7 = float(t7)
        self.f7 = float(f7)
        self.t8 = float(t8)
        self.f8 = float(f8)
        self.t9 = float(t9)
        self.f9 = float(f9)
        self.t10 = float(t10)
        self.f10 = float(f10)
        self.t11 = float(t11)
        self.f11 = float(f11)

    def __str__(self):
        data = [self.i, self.t1, self.f1, self.t2, self.f2, self.t3, self.f3,
                self.t4, self.f4, self.t5, self.f5, self.t6, self.f6, self.t7,
                self.f7, self.t8, self.f8, self.t9, self.f9, self.t10, self.f10,
                self.t11, self.f11]
        return ' '.join([str(x) for x in data])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def validate(self):
        '''Checks that this data structure conforms to the pss/e data
        specification
        '''
        return NotImplemented

    def to_psse(self):
        '''Returns: a pss/e encoding of this data structure as a string'''

        data = [self.i, self.t1, self.f1, self.t2, self.f2, self.t3, self.f3,
                self.t4, self.f4, self.t5, self.f5, self.t6, self.f6, self.t7,
                self.f7, self.t8, self.f8, self.t9, self.f9, self.t10, self.f10,
                self.t11, self.f11]

        return ', '.join([str(x) for x in data])


MULTISECTION_LINE_DEFAULTS = ["&1", 1]
class MultiSectionLineGrouping(object):
    def __init__(self, index, i, j, id, met, *dumi):
        '''This data structure contains Multi-Section Line Grouping parameters

        Args:
            index (int) : unique transformer impedence correction identifier
            i (int) : from bus number
            j (int) : to bus number
            id (str) : grouping identifier
            met (int) : metered end flag
            dumi (int) : bus numbers of dummy buses
        '''

        args = [id, met]
        _set_defaults(args, MULTISECTION_LINE_DEFAULTS)
        id, met = args

        self.index = index
        self.i = int(i)
        self.j = int(j)
        self.id = unquote_string(id)
        self.met = int(met)
        for n, dum in enumerate(dumi):
            setattr(self, "dum{0}".format(n+1), int(dum))

    def __str__(self):
        data = [self.i, self.j, self.id, self.met]
        for i in range(1, 10):
            if hasattr(self, "dum{0}".format(i)):
                data.append(getattr(self, "dum{0}".format(i)))
            else:
                break
        return ' '.join([str(x) for x in data])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def validate(self):
        '''Checks that this data structure conforms to the pss/e data
        specification
        '''
        return NotImplemented

    def to_psse(self):
        '''Returns: a pss/e encoding of this data structure as a string'''

        data = [self.i, self.j, self.id, self.met]
        dumi = []
        for i in range(1, 10):
            if hasattr(self, "dum{0}".format(i)):
                data.append(getattr(self, "dum{0}".format(i)))
            else:
                break

        return ', '.join([str(x) for x in data])


INTERAREA_TRANSFER_DEFAULTS = [1, 0.0]
class InterareaTransfer(object):
    def __init__(self, index, arfrom, arto, trid, ptran):
        '''This data structure contains Interarea Transfer parameters

        Args:
            index (int) : unique interarea transfer identifier
            arfrom (int) : from area identifier
            arto (int) : to area identifier
            trid (str) : interarea transfer identifier
            ptran (float) : MW of transfer
        '''

        args = [trid, ptran]
        _set_defaults(args, INTERAREA_TRANSFER_DEFAULTS)
        trid, ptran = args

        self.index = index
        self.arfrom = int(arfrom)
        self.arto = int(arto)
        self.trid = unquote_string(trid)
        self.ptran = float(ptran)

    def __str__(self):
        data = [self.arfrom, self.arto, self.trid, self.ptran]
        return ' '.join([str(x) for x in data])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def validate(self):
        '''Checks that this data structure conforms to the pss/e data
        specification
        '''
        return NotImplemented

    def to_psse(self):
        '''Returns: a pss/e encoding of this data structure as a string'''

        data = [self.arfrom, self.arto, self.trid, self.ptran]

        return ', '.join([str(x) for x in data])


INDUCTION_MACHINE_DEFAULTS = [1, 1, 1, 2, 1, 1, 1, 1, 1, 100.0, 0.0, 1, 1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 2.5, 999.0, 999.0, 999.0, 999.0, 0.0, 1.0, 0.0, 1.2, 0.0, 0.0, 0.0, 1]
class InductionMachine(object):
    def __init__(self, index, i, id, stat, scode, dcode, area, zone, owner, tcode, bcode, mbase,
                    ratekv, pcode, pset, h, a, b, d, e, ra, xa, xm, r1, x1, r2, x2, x3, e1, se1,
                    e2, se2, ia1, ia2, xamult):
        '''This data structure contains Induction Machine parameters

        Args:
            index (int) : unique interarea transfer identifier
            i (int) : bus number
            id (str) : machine identifier
            stat (int) : status
            scode (int) : standard code
            dcode (int) : design code
            area (int) : area
            zone (int) zone
            owner (int) : owner
            tcode (int) : type of mechanical load torque
            bcode (int) : base power code
            mbase (float) : base power
            ratekv (float) : rated voltage
            pcode (int) : scheduled power code
            pset (float) : scheduled active power
            h (float) : machine inertia
            a (float) : constant describing variation of torque with speed
            b (float) : constant describing variation of torque with speed
            d (float) : constant describing variation of torque with speed
            e (float) : constant describing variation of torque with speed
            ra (float) : armature resistance
            xa (float) : armature leakage reactance
            xm (float) : unsaturated magnetizing reactance
            r1 (float) : resistance of first rotor winding
            x1 (float) : reactance of first rotor winding
            r2 (float) : resistance of second rotor winding
            x2 (float) : reactance of second rotor winding
            x3 (float) : reactance of third rotor winding
            e1 (float) : first terminal voltage point
            se1 (float) : saturation factor at terminal voltage e1
            e2 (float) : second terminal voltage point
            se2 (float) : saturation factor at terminal voltage e2
            ia1 (float) : stator current
            ia2 (float) : stator current
            xamult (float) : multiplier for saturated value
        '''

        args = [id, stat, scode, dcode, area, zone, owner, tcode, bcode, mbase, ratekv, pcode, h, a, b, d, e, ra, xa, xm, r1, x1, r2, x2, x3, e1, se1, e2, se2, ia1, ia2, xamult]
        _set_defaults(args, INDUCTION_MACHINE_DEFAULTS)
        id, stat, scode, dcode, area, zone, owner, tcode, bcode, mbase, ratekv, pcode, h, a, b, d, e, ra, xa, xm, r1, x1, r2, x2, x3, e1, se1, e2, se2, ia1, ia2, xamult = args

        self.index = index
        self.i = int(i)
        self.id = unquote_string(id)
        self.stat = int(stat)
        self.scode = int(scode)
        self.dcode = int(dcode)
        self.area = int(area)
        self.zone = int(zone)
        self.owner = int(owner)
        self.tcode = int(tcode)
        self.bcode = int(bcode)
        self.mbase = float(mbase)
        self.ratekv = float(ratekv)
        self.pcode = int(pcode)
        self.pset = float(pset)
        self.h = float(h)
        self.a = float(a)
        self.b = float(b)
        self.d = float(d)
        self.e = float(e)
        self.ra = float(ra)
        self.xa = float(xa)
        self.xm = float(xm)
        self.r1 = float(r1)
        self.x1 = float(x1)
        self.r2 = float(r2)
        self.x2 = float(x2)
        self.x3 = float(x3)
        self.e1 = float(e1)
        self.se1 = float(se1)
        self.e2 = float(e2)
        self.se2 = float(se2)
        self.ia1 = float(ia1)
        self.ia2 = float(ia2)
        self.xamult = float(xamult)

    def __str__(self):
        data = [self.i, self.id, self.stat, self.scode, self.dcode, self.area, self.zone,
                self.owner, self.tcode, self.bcode, self.mbase, self.ratekv, self.pcode,
                self.pset, self.h, self.a, self.b, self.d, self.e, self.ra, self.xa,
                self.xm, self.r1, self.x1, self.r2, self.x2, self.x3, self.e1, self.se1,
                self.e2, self.se2, self.ia1, self.ia2, self.xamult]
        return ' '.join([str(x) for x in data])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def validate(self):
        '''Checks that this data structure conforms to the pss/e data
        specification
        '''
        return NotImplemented

    def to_psse(self):
        '''Returns: a pss/e encoding of this data structure as a string'''

        data = [self.i, self.id, self.stat, self.scode, self.dcode, self.area, self.zone,
                self.owner, self.tcode, self.bcode, self.mbase, self.ratekv, self.pcode,
                self.pset, self.h, self.a, self.b, self.d, self.e, self.ra, self.xa,
                self.xm, self.r1, self.x1, self.r2, self.x2, self.x3, self.e1, self.se1,
                self.e2, self.se2, self.ia1, self.ia2, self.xamult]

        return ', '.join([str(x) for x in data])


class MultiTerminalDCLine(object):
    def __init__(self, index, params, nconv, ndcbs, ndcln):
        '''This data structure contains Multi-Terminal DC Line parameters

        Args:
            index (int) : unique interarea transfer identifier
            params (MultiTerminalDCLineParameters) : first line of MultiTerminal DC Line entry
            nconv (list(MultiTerminalDCLineConverter)) : next nconv lines of MutliTerminal DC Line entries
            ndcbs (list(MultiTerminalDCLineDCBus)) : next ndcbs lines of MutliTerminal DC Line entries
            ndcln (list(MultiTerminalDCLineDCLink)) : next ndcln lines of MutliTerminal DC Line entries
        '''
        self.index = index
        self.params = params
        self.converters = nconv
        self.dc_buses = ndcbs
        self.dc_links = ndcln

    def __str__(self):
        data = []
        return ' '.join([str(x) for x in data])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def validate(self):
        '''Checks that this data structure conforms to the pss/e data
        specification
        '''
        return NotImplemented

    def to_psse(self):
        '''Returns: a pss/e encoding of this data structure as a string'''
        data = [self.params]
        data.extend(self.converters)
        data.extend(self.dc_buses)
        data.extend(self.dc_links)
        return os.linesep.join([x.to_psse() for x in data])


MTDCL_PARAMETER_DEFAULTS = [0, 0.0, 0]
class MultiTerminalDCLineParameters(object):
    def __init__(self, name, nconv, ndcbs, ndcln, mdc, vconv, vcmod, vconvn):
        '''This data structure contains MultiTerminal DC Line first-line parameters

        Args:
            name (str) : name of dc line
            nconv (int) : number of ac converters
            ndcbs (int) : number of dc buses
            ndcln (int) : number of dc links
            mdc (int) : control mode
            vconv (int) : bus number of positive pole controlling ac converter station
            vcmod (float) : mode switch dc voltage
            vconvn (int) : bus number of negative pole controlling ac converter station
        '''

        args = [mdc, vcmod, vconvn]
        _set_defaults(args, MTDCL_PARAMETER_DEFAULTS)
        mdc, vcmod, vconvn = args

        self.name = unquote_string(name)
        self.nconv = int(nconv)
        self.ndcbs = int(ndcbs)
        self.ndcln = int(ndcln)
        self.mdc = int(mdc)
        self.vconv = int(vconv)
        self.vcmod = float(vcmod)
        self.vconvn = int(vconvn)

    def __str__(self):
        data = [quote_string(self.name), self.nconv, self.ndcbs, self.ndcln, self.mdc, self.vconv, self.vcmod, self.vconvn]
        return ' '.join([str(x) for x in data])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def validate(self):
        '''Checks that this data structure conforms to the pss/e data
        specification
        '''
        return NotImplemented

    def to_psse(self):
        '''Returns: a pss/e encoding of this data structure as a string'''
        data = [quote_string(self.name), self.nconv, self.ndcbs, self.ndcln, self.mdc, self.vconv, self.vcmod, self.vconvn]
        return ', '.join([str(x) for x in data])



MTDCL_CONVERTER_DEFAULTS = [1.0, 1.0, 1.5, 0.51, 0.00625, 1, 0.0, 1]
class MultiTerminalDCLineConverter(object):
    def __init__(self, ib, n, angmx, angmn, rc, xc, ebas, tr, tap, tpmx, tpmn, tstp, setvl, dcpf, marg, cnvcod):
        '''This data structure contains MultiTerminal DC Line Converter parameters

        Args:
            ib (int) : ac converter bus number
            n (int) : number of bridges in series
            angmx (float) : nominal max alpha or gamma angle
            angmn (float) : nominal min alpha or gamma angle
            rc (float) : commutating resistance per bridge
            xc (float) : commutating reactance per bridge
            ebas (float) : primary base ac voltage
            tr (float) : actual transformer ratio
            tap (float) : tap setting
            tpmx (float) : max tap setting
            tpmn (float) : min tap setting
            tstp (float) : tap step
            setvl (float) : converter setpoint
            dcpf (float) : converter participation factor
            marg (float) : rectifier margin
            cnvcod (int) : converter code
        '''

        args = [tr, tap, tpmx, tpmn, tstp, dcpf, marg, cnvcod]
        _set_defaults(args, MTDCL_CONVERTER_DEFAULTS)
        tr, tap, tpmx, tpmn, tstp, dcpf, marg, cnvcod = args

        self.ib = int(ib)
        self.n = int(n)
        self.angmx = float(angmx)
        self.angmn = float(angmn)
        self.rc = float(rc)
        self.xc = float(xc)
        self.ebas = float(ebas)
        self.tr = float(tr)
        self.tap = float(tap)
        self.tpmx = float(tpmx)
        self.tpmn = float(tpmn)
        self.tstp = float(tstp)
        self.setvl = float(setvl)
        self.dcpf = float(dcpf)
        self.marg = float(marg)
        self.cnvcod = int(cnvcod)

    def __str__(self):
        data = [self.ib, self.n, self.angmx, self.angmn, self.rc, self.xc,
                self.ebas, self.tr, self.tap, self.tpmx, self.tpmn, self.tstp,
                self.setvl, self.dcpf, self.marg, self.cnvcod]
        return ' '.join([str(x) for x in data])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def validate(self):
        '''Checks that this data structure conforms to the pss/e data
        specification
        '''
        return NotImplemented

    def to_psse(self):
        '''Returns: a pss/e encoding of this data structure as a string'''
        data = [self.ib, self.n, self.angmx, self.angmn, self.rc, self.xc,
                self.ebas, self.tr, self.tap, self.tpmx, self.tpmn, self.tstp,
                self.setvl, self.dcpf, self.marg, self.cnvcod]
        return ', '.join([str(x) for x in data])



MTDCL_BUS_DEFAULTS = [0.0, 1, 1, "            ", 0, 0.0, 1]
class MultiTerminalDCLineDCBus(object):
    def __init__(self, idc, ib, area, zone, dcname, idc2, rgrnd, owner):
        '''This data structure contains MultiTerminal DC Line DC Bus parameters

        Args:
            idc (int) : dc bus number
            ib (int) : ac converter bus number
            area (int) : area number
            zone (int) : zone number
            dcname (str) : identifier
            idc2 (int) : second dc bus to which idc is connected
            rgrnd (float) : resistance to ground
            owner (int) : owner number

        '''

        args = [ib, area, zone, dcname, idc2, rgrnd, owner]
        _set_defaults(args, MTDCL_BUS_DEFAULTS)
        ib, area, zone, dcname, idc2, rgrnd, owner = args

        self.idc = int(idc)
        self.ib = int(ib)
        self.area = int(area)
        self.zone = int(zone)
        self.dcname = unquote_string(dcname)
        self.idc2 = int(idc2)
        self.rgrnd = float(rgrnd)
        self.owner = int(owner)

    def __str__(self):
        data = [self.idc, self.ib, self.area, self.zone, quote_string(self.dcname), self.idc2, self.rgrnd, self.owner]
        return ' '.join([str(x) for x in data])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def validate(self):
        '''Checks that this data structure conforms to the pss/e data
        specification
        '''
        return NotImplemented

    def to_psse(self):
        '''Returns: a pss/e encoding of this data structure as a string'''
        data = [self.idc, self.ib, self.area, self.zone, quote_string(self.dcname), self.idc2, self.rgrnd, self.owner]
        return ', '.join([str(x) for x in data])


MTDCL_LINE_DEFAULTS = [1, 1, 0.0]
class MultiTerminalDCLineDCLink(object):
    def __init__(self, idc, jdc, dcckt, met, rdc, ldc):
        '''This data structure contains MultiTerminal DC Line DC Link parameters

        Args:
            idc (int) : from bus dc number
            jdc (int) : to bus dc number
            dcckt (str) : circuit identifier
            met (int) : metered end flag
            rdc (float) : dc link resistance
            ldc (float) : dc link inductance
        '''

        args = [dcckt, met, ldc]
        _set_defaults(args, MTDCL_LINE_DEFAULTS)
        dcckt, met, ldc = args

        self.idc = int(idc)
        self.jdc = int(jdc)
        self.dcckt = unquote_string(dcckt)
        self.met = int(met)
        self.rdc = float(rdc)
        self.ldc = float(ldc)

    def __str__(self):
        data = [self.idc, self.jdc, quote_string(self.dcckt), self.met, self.rdc, self.ldc]
        return ' '.join([str(x) for x in data])

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self.__eq__(other)
        return NotImplemented

    def validate(self):
        '''Checks that this data structure conforms to the pss/e data
        specification
        '''
        return NotImplemented

    def to_psse(self):
        '''Returns: a pss/e encoding of this data structure as a string'''
        data = [self.idc, self.jdc, quote_string(self.dcckt), self.met, self.rdc, self.ldc]
        return ', '.join([str(x) for x in data])
