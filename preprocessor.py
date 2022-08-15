import numpy as np
from bitstring import Bits, BitArray


class Preprocessor:
    def __init__(self):
        self.amplitudes = None
        self.num_qubits = 0
        self.target_index = 0
        self.control_index = 0
        self.stride = 0
        self.gate_type = None

    # set the input parameter
    def set_attribute(self, num_qubits, gate_type, control_index, target_index):
        self.num_qubits = num_qubits
        self.gate_type = gate_type
        self.control_index = control_index
        self.target_index = target_index

    # set the amplitudes
    def set_amplitudes(self, amplitudes):
        self.amplitudes = np.array(amplitudes)

    # get the amplitudes
    def get_amplitudes(self):
        print('amplitudes\n', self.amplitudes)
        return self.amplitudes

    # calculate the stride value and initialize the offset value
    def cal_stride(self):
        if self.target_index <= self.num_qubits:
            self.stride = 1 << self.target_index
        else:
            print("The target index is larger than the qubits range")

    # qubit gate operation depends on the gate type
    def quantum_gate_process(self):
        # make flatten amplitudes ndarray due to easily count the index
        flatten_amplitudes = self.amplitudes.flatten()
        # print('flatten', flatten_amplitudes)

        if self.gate_type == 'one_qubit_gate':
            # reorder all amplitudes without changing the index
            reordered_amplitudes, reordered_index = reorder(self.stride, self.gate_type, flatten_amplitudes)

            # return after reshape for making a pair of amplitudes, (2,1) vector
            return reordered_amplitudes.reshape((-1, 2)), reordered_index, None

        elif self.gate_type == 'two_qubit_gate':
            # initialize the empty list to store the realized states
            realized_amplitudes = []

            # initialize the empty np_arr to store the unrealized states
            unrealized_amplitudes = []

            # convert the decimal control_index into the binary representation
            # if control qubit index is 1, the bin_control_index should be |010> (2nd => |100>)
            bin_control_index = BitArray(uint=1 << self.control_index, length=self.num_qubits)

            # make the empty index list for unrealized amplitudes
            realized_index = []
            unrealized_index = []

            # find the realized amplitudes
            for offset in range(0, 2 ** self.num_qubits):
                # convert the decimal offset into the binary representation
                bin_offset = BitArray(uint=offset, length=self.num_qubits)

                # check the offset has the control index as 1
                # ex) |010> & |000> = 0, |010> & |001> = 0, |010> & |010> > 0, ...
                enable = bin_control_index & bin_offset

                # when enable == 1, it means the qubit of control index on offset is '1' named 'realized'
                if enable.uint > 0:
                    # add the realized index
                    realized_index.append(offset)

                    # add the realized amplitudes
                    realized_amplitudes.append(flatten_amplitudes[offset])

                elif enable.uint == 0:
                    # add the unrealized index
                    unrealized_index.append(offset)

                    # add the unrealized amplitudes
                    unrealized_amplitudes.append(flatten_amplitudes[offset])

                else:
                    print("Cannot check the realized states")

            print('realized', realized_amplitudes)
            # reorder the realized amplitudes
            reordered_amplitudes, reordered_index = reorder(self.stride, self.gate_type,
                                                            np.array(realized_amplitudes), realized_index)

            # return after reshape for making a pair of amplitudes, (2,1) vector
            return reordered_amplitudes.reshape((-1, 2)), reordered_index, unrealized_amplitudes, unrealized_index

        else:
            print("No matched gate type!")


# reorder the amplitudes of each qubit state according to the stride value
def reorder(stride, gate_type, flatten_amplitudes, realized_index=None):
    # make the empty index list for realized amplitudes
    stride_index = []
    # reordered_offset = []

    # initialize the zero reordered_amplitudes numpy array same size as amplitudes
    reordered = []

    # change the value
    for indexes, amplitude in np.ndenumerate(flatten_amplitudes):
        index = int(indexes[0])  # indexes is tuple (0,)
        if index not in stride_index:
            # add the index
            stride_index.append(index)

            # store the upper state
            upper_state = amplitude

            # store the lower state (index + stride)
            pair_index = 0
            if gate_type == 'one_qubit_gate':
                pair_index = index + stride
            elif gate_type == 'two_qubit_gate':
                realized_state = realized_index[index]
                pair_index = realized_index.index(realized_state+stride)
            else:
                print('stride error')

            if pair_index not in stride_index:
                stride_index.append(pair_index)
            else:
                continue

            lower_state = flatten_amplitudes[pair_index]

            # store the pair of reordered amplitudes
            reordered.append(upper_state)
            reordered.append(lower_state)

        elif index in stride_index:
            continue

        else:
            print("Index error!")

    print('stride_index', stride_index)
    # return the reordered amplitudes, realized_index together
    return np.array(reordered), stride_index
