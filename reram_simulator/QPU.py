import numpy as np
from scipy.linalg import block_diag
from bitstring import Bits, BitArray
import crossbar
from qiskit.circuit.library import *
import utils


class QPU:
    def __init__(self):
        self.num_qubits = 0
        self.gate_name = ''
        self.gate_type = None
        self.ccontrol_qubit = 0
        self.control_qubit = 0
        self.target_qubit = 0
        self.stride = 0
        self.real_xbar = crossbar.make_core()  # real part of matrix
        self.imag_xbar = crossbar.make_core()  # imaginary part of matrix

    # set the input parameter
    def set_attribute(self, num_qubits, gate_name, gate_type, ccontrol_qubit, control_qubit, target_qubit):
        self.num_qubits = num_qubits
        self.gate_name = gate_name
        self.gate_type = gate_type
        self.ccontrol_qubit = ccontrol_qubit
        self.control_qubit = control_qubit
        self.target_qubit = target_qubit

    # set the xbar weight
    def set_weight(self, instruction):
        # the number of matrix stored in the xbar
        number_of_matrix = 1024 / 2

        matrix = utils.find_matrix(instruction)
        # print('rm', matrix.real)
        # print('im', matrix.imag)

        # make the diagonal matrix both real and imaginary
        real_weight = block_diag(*(matrix.real * number_of_matrix))
        imag_weight = block_diag(*(matrix.imag * number_of_matrix))

        self.real_xbar.set_matrix(real_weight)
        self.imag_xbar.set_matrix(imag_weight)


    # get the xbar weight
    # FIXME: change read matrix attribute
    def get_weight(self):
        print('weight\n', self.real_xbar._read_matrix)
        print('weight\n', self.imag_xbar._read_matrix)

    # calculate the stride value and initialize the offset value
    def cal_stride(self):
        if self.target_qubit <= self.num_qubits:
            self.stride = 1 << self.target_qubit
        else:
            print("The target index is larger than the qubits range")


    # qubit gate operation depends on the gate type
    def quantum_gate_process(self, rsv):
        # do the mvm operation according to the gate type
        if self.gate_type == 'one_qubit_gate':
            # reorder all rsv without changing the index
            reordered_rsv = utils.reorder(self.stride, rsv)
            print('one qubit: reordered_rsv', reordered_rsv)

            # return after reshape for making a pair of rsv, (2,1) vector
            return reordered_rsv

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
            for k in range(0, np.shape(rsv)[0]):
                # extract the offset(=index)
                offset = rsv[k][0]

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
                    realized_rsv.append(rsv[offset])

                elif enable.uint == 0:
                    # add the unrealized index
                    unrealized_index.append(offset)

                    # add the unrealized rsv
                    unrealized_rsv.append(rsv[offset])

                else:
                    print("Cannot check the realized states")

            # print('realized', realized_rsv)
            # reorder the realized rsv
            reordered_rsv = utils.reorder(self.stride, realized_rsv)
            print('two qubit: reordered', reordered_rsv)

            # return after reshape for making a pair of rsv, (2,1) vector
            return reordered_rsv, unrealized_rsv

        else:
            print("No matched gate type!")

