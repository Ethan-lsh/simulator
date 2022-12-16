import numpy as np
from bitstring import Bits, BitArray
import crossbar
from qiskit.circuit.library import *


class QPU:
    def __init__(self):
        self.rsv = None
        self.num_qubits = 0
        self.target_qubit = 0
        self.control_qubit = 0
        self.stride = 0
        self.gate_type = None
        self.xbar = crossbar.make_core()

    # set the input parameter
    def set_attribute(self, num_qubits, gate_type, control_qubit, target_qubit):
        self.num_qubits = num_qubits
        self.gate_type = gate_type
        self.control_qubit = control_qubit
        self.target_qubit = target_qubit

    # set the rsv
    def set_rsv(self, rsv):
        self.rsv = rsv

    # get the rsv
    def get_rsv(self):
        print('rsv\n', self.rsv)
        return self.rsv

    # set the xbar weight
    def set_weight(self, instruction):
        # check whether the control gate or not
        gate_name = ''

        if instruction.name.find('c') == -1:
            gate_name = instruction.name.upper()
            if gate_name == 'SDG':
                gate_name = 'Sdg'
            elif gate_name == 'TDG':
                gate_name = 'Tdg'
            elif gate_name == 'ID':
                gate_name = 'I'
        elif instruction.name.find('c') == 0:
            gate_name = instruction.name[1:].upper()
            if gate_name == 'CX': gate_name = 'X'

        params = instruction.params

        gate = None
        if len(params) == 0:
            gate = globals()[gate_name + "Gate"]()
        elif len(params) == 1:
            gate = globals()[gate_name + "Gate"](*params)
        elif len(params) == 2:
            gate = globals()[gate_name + "Gate"](*params)
        elif len(params) == 3:
            gate = globals()[gate_name + "Gate"](*params)
        else:
            print('Error: No matched param')

        matrix = gate.to_matrix()
        self.xbar.set_matrix(matrix)


    # get the xbar weight
    def get_weight(self):
        print('weight\n', self.xbar._read_matrix)
        return self.xbar._read_matrix

    # calculate the stride value and initialize the offset value
    def cal_stride(self):
        if self.target_qubit <= self.num_qubits:
            self.stride = 1 << self.target_qubit
        else:
            print("The target index is larger than the qubits range")

    # qubit gate operation depends on the gate type
    def quantum_gate_process(self):
        # do the mvm operation according to the gate type
        if self.gate_type == 'one_qubit_gate':
            # reorder all rsv without changing the index
            reordered_rsv = reorder(self.stride, self.gate_type, self.rsv)

            # return after reshape for making a pair of rsv, (2,1) vector
            return reordered_rsv.reshape((-1, 2)), reordered_index, None

        elif self.gate_type == 'two_qubit_gate':
            # initialize the empty list to store the realized states
            realized_rsv = []

            # initialize the empty np_arr to store the unrealized states
            unrealized_rsv = []

            # convert the decimal control_qubit into the binary representation
            # if control qubit index is 1, the bin_control_qubit should be |010> (2nd => |100>)
            bin_control_qubit = BitArray(uint=1 << self.control_qubit, length=self.num_qubits)

            # make the empty index list for unrealized rsv
            realized_index = []
            unrealized_index = []

            # find the realized rsv
            for offset in range(0, 2 ** self.num_qubits):
                # convert the decimal offset into the binary representation
                bin_offset = BitArray(uint=offset, length=self.num_qubits)

                # check the offset has the control index as 1
                # ex) |010> & |000> = 0, |010> & |001> = 0, |010> & |010> > 0, ...
                enable = bin_control_qubit & bin_offset

                # when enable == 1, it means the qubit of control index on offset is '1' named 'realized'
                if enable.uint > 0:
                    # add the realized index
                    realized_index.append(offset)

                    # add the realized rsv
                    realized_rsv.append(flatten_rsv[offset])

                elif enable.uint == 0:
                    # add the unrealized index
                    unrealized_index.append(offset)

                    # add the unrealized rsv
                    unrealized_rsv.append(flatten_rsv[offset])

                else:
                    print("Cannot check the realized states")

            print('realized', realized_rsv)
            # reorder the realized rsv
            reordered_rsv, reordered_index = reorder(self.stride, self.gate_type,
                                                            np.array(realized_rsv), realized_index)

            # return after reshape for making a pair of rsv, (2,1) vector
            return reordered_rsv.reshape((-1, 2)), reordered_index, unrealized_rsv, unrealized_index

        else:
            print("No matched gate type!")


        def find_rs(rs, index):
            try:
                value = np.where(rs[:, 0] == index)[0].real[0]
                if (value >= 0) and (rs[value, 2] == False):
                    rs[value, 2] = True
                    return rs[value]
            except IndexError:
                t_rs = np.array([index, 0.0 + 0.0j, True])
                return t_rs

        
        # reorder the rsv of each qubit state according to the stride value
        @staticmethod
        def reorder(stride, gate_type, rsv):
            length_of_rsv = np.shape(rsv)[0]
            
            for i in range(0, length_of_rsv):
                upper_index = lower_index = 0

                upper_index = rsv[i][0].real
                upper_rsv = find_rs(rsv, upper_index)

                if upper_rsv is None or []:
                    continue

                lower_index = upper_index + stride
                lower_rsv = find_rs(rsv, lower_index)

                # combine and store in reorderd rsv
                if i == 0:
                    pair_rsv = np.vstack([upper_rsv, lower_rsv])
                    reordered_rsv = pair_rsv
                elif i > 0:
                    pair_rsv = np.vstack([reordered_rsv, upper_rsv, lower_rsv])

            return reordered_rsv
