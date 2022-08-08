import numpy as np
from bitstring import Bits, BitArray


class Preprocessor:
    def __init__(self):
        self.amplitudes = None
        self.num_qubits = 0
        self.target_index = 0
        self.control_index = 0
        self.gate_type = None

    # set the input parameter
    def set_attribute(self, num_qubits, gate_type, control_index, target_index):
        self.num_qubits = num_qubits
        self.gate_type = gate_type
        self.control_index = control_index
        self.target_index = target_index

    # set the amplitudes
    def set_amplitudes(self, amplitudes):
        self.amplitudes = amplitudes

    # get the amplitudes
    def get_amplitudes(self):
        return self.amplitudes

    # calculate the stride value and initialize the offset value
    def cal_stride(self):
        if self.target_index <= self.num_qubits:
            stride = 1 << self.target_index
            # offset = 0  # to check the qubit state
        else:
            print("The target index is larger than the qubits range")

        return stride

    # qubit gate operation depends on the gate type
    def quantum_gate_operation(self):
        if self.gate_type == 'one_qubit_gate':
            # reorder all amplitudes without changing the index
            reorder(self.amplitudes)

        elif self.gate_type == 'two_qubit_gate':
            # change the decimal control_index into the binary representation
            bin_control_index = BitArray(uint=1<<self.control_index, length=self.num_qubits)

            # TODO: write the for loop sentence (algorithm.11~17)
            # find the realized amplitudes


            # make flatten amplitudes
            flatten_amplitudes = self.amplitudes.flat

            # check the control qubit
            for offset in range(0, flatten_amplitudes.size):


            # reorder the realized amplitudes

            # reorder(realized_amplitudes)
        else:
            print("No matched gate type!")


# reorder the amplitudes of each qubit state according to the stride value
def reorder(stride, amplitudes):
    # initialize the zero reordered_amplitudes numpy array same size as amplitudes
    reordered_amplitudes = np.zeros(amplitudes.size)

    # empty list to check the selected index
    selected_index = []

    # change the value
    flatten_amplitudes = amplitudes.flat
    for  index, amplitude in np.ndenumerate(flatten_amplitudes):
        if index not in selected_index:
            # add the unselected index
            selected_index.append(index)

            # store the upper state
            upper_state = amplitude

            # store the lower state (index + stride)
            pair_index = index + stride
            selected_index.append(pair_index)
            lower_state = flatten_amplitudes[pair_index]

            # store the pair qubit states
            reordered_amplitudes[index] = upper_state
            reordered_amplitudes[index + 1] = lower_state

        elif index in selected_index:
            continue

        else:
            print("Index error!")

