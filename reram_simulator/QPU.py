import numpy as np
from scipy.linalg import block_diag
from bitstring import Bits, BitArray
import crossbar
import utils
import param
from fxpmath import Fxp
from inspect import currentframe, getframeinfo

cf = currentframe()
filename = getframeinfo(cf).filename


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
        self._num_gates = 1

    # set the input parameter
    def set_attribute(self, num_qubits, gate_name, gate_type, ccontrol_qubit, control_qubit, target_qubit):
        self.num_qubits = num_qubits
        self.gate_name = gate_name
        self.gate_type = gate_type
        self.ccontrol_qubit = ccontrol_qubit
        self.control_qubit = control_qubit
        self.target_qubit = target_qubit

    # optimization function
    def optimize(self, num_gates):
        self._num_gates = num_gates

    # set the xbar weight
    def set_weight(self, instruction, optimization=None):
        # default number of matrix stored in xbar
        number_of_matrix = self._num_gates

        if optimization is not None:
            number_of_matrix = optimization

        # ! Make the fixed point matrix
        matrix = Fxp(utils.find_matrix(instruction), signed=True, n_word=param.word, n_frac=param.frac)

        # make the diagonal matrix both real and imaginary
        real_weight = block_diag(*([matrix.real] * number_of_matrix))
        imag_weight = block_diag(*([matrix.imag] * number_of_matrix))

        self.real_xbar.set_matrix(real_weight)
        self.imag_xbar.set_matrix(imag_weight)

    # get the xbar weight
    def read_weight(self):
        print('weight\n', self.real_xbar._read_matrix())
        print('weight\n', self.imag_xbar._read_matrix())

    # calculate the stride value and initialize the offset value
    def cal_stride(self):
        if self.target_qubit <= self.num_qubits:
            self.stride = 1 << self.target_qubit
        else:
            print("The target index is larger than the qubits range")

    # matrix-vector multiplication function
    def vmm(self, reordered_rsv):
        reordered_rsv = reordered_rsv.get_val()
        # divide the reordered rsv into real and imaginary vector
        real_reordered_rsv = reordered_rsv.real
        img_reordered_rsv = reordered_rsv.imag

        # reshape the amplitude vector
        row = 2**self._num_gates
        column = len(reordered_rsv)

        real = img = None
        real_vmm_result = img_vmm_result = np.array([], dtype=complex).reshape(0, 2)
        for j in range(0, column, 2):
            amp = reordered_rsv[j:j+2]
            amp = amp[amp[:, 0].argsort()]
            real_amp = amp.real
            img_amp = amp.imag
            # real_amp = real_reordered_rsv[j:j+2, 1]
            # real_amp = real_reordered_rsv[j:j+2]
            # real_amp = real_amp[real_amp[:, 0].argsort()]

            # img_amp = img_reordered_rsv[j:j+2, 1]
            # img_amp = img_reordered_rsv[j:j+2]
            # img_amp = img_amp[img_amp[:, 0].argsort()]

            # Extract the real part of result
            real_xbar_output = self.real_xbar.run_xbar_mvm(real_amp[:, 1]) - self.imag_xbar.run_xbar_mvm(img_amp[:, 1])
            
            # Extract the imaginary part of result
            img_xbar_output = self.real_xbar.run_xbar_mvm(img_amp[:, 1]) + self.imag_xbar.run_xbar_mvm(real_amp[:, 1])
            
            # if n_stride > 0:
            #     real_vmm_result = np.vstack((real_vmm_result, real_xbar_output))
            #     img_vmm_result = np.vstack((img_vmm_result, img_xbar_output))
            # else:
            real_vmm_result = np.vstack((real_vmm_result, real_xbar_output[::-1]))
            img_vmm_result = np.vstack((img_vmm_result, img_xbar_output[::-1]))

            # real_vmm_result = np.vstack((real_vmm_result, real_xbar_output))
            # img_vmm_result = np.vstack((img_vmm_result, img_xbar_output))

        vmm_result = real_vmm_result + 1j * img_vmm_result

        # combine real and img
        reordered_rsv[:, 1] = vmm_result.flatten()

        # NOTICE The vmm result is Fxp object
        return reordered_rsv

    # reorder the rsv of each qubit state according to the stride value
    def reorder(self, realized_rsv, unrealized_rsv=None):
        # reshape
        realized_rsv = np.reshape(realized_rsv, (-1, 3))

        if unrealized_rsv is not None:
            unrealized_rsv = np.reshape(unrealized_rsv, (-1, 3))


        length_of_rsv = realized_rsv.shape[0]

        reordered_rsv = []

        for i in range(0, length_of_rsv):
            lower_index = upper_index = 0

            lower_index = int(realized_rsv[i][0].get_val())
            # bin_lower_index = BitArray(uint=lower_index, length=self.num_qubits)
            bin_lower_index = BitArray(uint=lower_index, length=param.word)

            if bin_lower_index.any(False, [(param.word - 1) - self.target_qubit]):
                upper_index = lower_index + self.stride
            else:
                upper_index = lower_index
                lower_index = upper_index - self.stride

            lower_rsv, reordered_ursv = utils.find_rs(realized_rsv, lower_index, unrealized_rsv)

            if lower_rsv is None or []:
                continue

            upper_rsv, reordered_ursv = utils.find_rs(realized_rsv, upper_index, unrealized_rsv)
            if upper_rsv is None or []:
                continue

            # combine and store in reordered rsv
            if i == 0:
                pair_rsv = np.vstack([upper_rsv, lower_rsv])
                reordered_rsv = pair_rsv
            elif i > 0:
                pair_rsv = np.vstack([upper_rsv, lower_rsv])
                reordered_rsv = np.concatenate((reordered_rsv, pair_rsv), axis=0)
                # pair_rsv = np.vstack([[reordered_rsv, upper_rsv, lower_rsv]])
                # reordered_rsv = pair_rsv

        # ! Make the Fxp object with 'same' precision
        reordered_rsv = Fxp(reordered_rsv, signed=True, n_word=param.word, n_frac=param.frac)
        reordered_rsv.config.const_op_sizing = 'same'

        reordered_ursv = Fxp(reordered_ursv, signed=True, n_word=param.word, n_frac=param.frac)
        reordered_ursv.config.const_op_sizing = 'same'

        # return with sorting
        return reordered_rsv, reordered_ursv

    # qubit gate operation depends on the gate type
    def quantum_gate_process(self, rsv):
        # calculate the stride value and initialize the offset value
        if self.target_qubit <= self.num_qubits:
            self.stride = 1 << self.target_qubit
        else:
            print("The target index is larger than the qubits range")


        # do the mvm operation according to the gate type
        if self.gate_type == 'one_qubit_gate':
            # reorder all rsv without changing the index
            reordered_rsv, reordered_ursv = self.reorder(rsv)
            # print('one qubit: reordered_rsv\n', reordered_rsv)

            # do the matrix-vector multiplication
            next_rsv = self.vmm(reordered_rsv)

            # remove the zero amplitude state
            try:
                next_rsv = next_rsv[np.where(next_rsv[:, 1] != 0)]
            except IndexError:
                print('Index error\n')

            # reset the rsv status
            next_rsv[:, 2] = False
            # print('QPU Output:: \n', next_rsv)

            return Fxp(next_rsv[next_rsv[:, 0].argsort()], signed=True, n_word=param.word, n_frac=param.frac)

        elif self.gate_type == 'two_qubit_gate':
            # initialize the empty list to store the realized states
            realized_rsv = []

            # initialize the empty np_arr to store the unrealized states
            unrealized_rsv = []

            # convert the decimal control_qubit into the binary representation
            # if control qubit index is 1, the bin_control_qubit should be |010> (2nd => |100>)
            bin_control_qubit = BitArray(uint= 2**self.control_qubit, length=self.num_qubits)

            # make the empty index list for unrealized rsv
            realized_index = []
            unrealized_index = []

            # find the realized rsv
            for k in range(0, list(rsv.shape)[0]):
                # extract the offset(=index)
                offset = int(rsv[k][0].get_val())

                # convert the decimal offset into the binary representation
                bin_offset = BitArray(uint=offset, length=self.num_qubits)

                # check the offset has the control index as 1
                # ex) |010> & |000> = 0, |010> & |001> = 0, |010> & |010> > 0, ...
                enable = bin_control_qubit & bin_offset

                # enable = 1 if rsv[offset][1] > 0 else 0

                # if the control qubit is |1>
                if enable.uint > 0:
                    # add the realized index
                    realized_index = np.append(realized_index, k)

                    # add the realized rsv
                    realized_rsv = np.append(realized_rsv, rsv[k].get_val())

                elif enable.uint == 0:
                    # add the unrealized index
                    unrealized_index = np.append(unrealized_index, k)

                    # add the unrealized rsv
                    unrealized_rsv = np.append(unrealized_rsv, rsv[k].get_val())

                else:
                    continue

            if len(realized_rsv) == 0:
                return Fxp(unrealized_rsv.reshape((-1, 3)), signed=True, n_word=param.word, n_frac=param.frac)
            else:
                realized_rsv = Fxp(realized_rsv, signed=True, n_word=param.word, n_frac=param.frac)
                unrealized_rsv = Fxp(unrealized_rsv, signed=True, n_word=param.word, n_frac=param.frac)
                reordered_rsv, reordered_ursv = self.reorder(realized_rsv, unrealized_rsv)
            # print('two qubit: reordered\n', reordered_rsv)

            # Do the matrix-vector multiplication
            next_rsv = self.vmm(reordered_rsv)

            if reordered_ursv is not None:
                # NOTICE Fxp object cannot implement np.vstack
                # combine with unrealized rsv
                next_rsv = np.vstack((next_rsv, reordered_ursv.get_val()))

                # remove the zero amplitudes
                next_rsv = next_rsv[~np.any(next_rsv[:, 1].reshape((-1, 1)) == 0, axis=1)]

                next_rsv[:, 2] = False

                return Fxp(next_rsv[next_rsv[:, 0].argsort()], signed=True, n_word=param.word, n_frac=param.frac)

            else:
                # remove the zero amplitudes
                next_rsv = next_rsv[np.where(next_rsv[:, 1] != 0)]

                next_rsv[:, 2] = False

                return Fxp(next_rsv[next_rsv[:, 0].argsort()], signed=True, n_word=param.word, n_frac=param.frac)

        elif self.gate_type == 'three_qubit_gate':
            # initialize the empty list to store the realized states
            realized_rsv = []

            # initialize the empty np_arr to store the unrealized states
            unrealized_rsv = []

            # convert the decimal control_qubit into the binary representation
            # if control qubit index is 1, the bin_control_qubit should be |010> (2nd => |100>)
            bin_ccontrol_qubit = BitArray(uint=1 << self.ccontrol_qubit, length=2**self.num_qubits)
            bin_control_qubit = BitArray(uint=1 << self.control_qubit, length=2**self.num_qubits)

            # make the empty index list for unrealized rsv
            realized_index = []
            unrealized_index = []

            # find the realized rsv
            for k in range(0, list(rsv.shape)[0]):
                # extract the offset(=index)
                offset = int(rsv[k][0].get_val())

                # convert the decimal offset into the binary representation
                bin_offset = BitArray(uint=offset, length=2**self.num_qubits)

                # check the offset has the control index as 1
                # ex) |010> & |000> = 0, |010> & |001> = 0, |010> & |010> > 0, ...
                enable = bin_control_qubit & bin_offset
                eenable = bin_control_qubit & bin_offset

                # enable = 1 if rsv[offset][1] > 0 else 0

                # when enable == 1, it means the qubit of control index on offset is '1' named 'realized'
                if enable.uint > 0 and eenable.uint > 0:
                    # add the realized index
                    realized_index = np.append(realized_index, k)

                    # add the realized rsv
                    realized_rsv = np.append(realized_rsv, rsv[k].get_val())

                elif (enable.uint > 0 & eenable.uint == 0) \
                    or (enable.uint == 0 & eenable.uint > 0) \
                    or (enable.uint == 0 & eenable.uint == 0) :
                    # add the unrealized index
                    unrealized_index = np.append(unrealized_rsv, k)

                    # add the unrealized rsv
                    unrealized_rsv = np.append(unrealized_rsv, rsv[k].get_val())

                else:
                    continue

            if len(realized_rsv) == 0:
                return Fxp(unrealized_rsv.reshape((-1, 3)), signed=True, n_word=param.word, n_frac=param.frac)
            else:
                realized_rsv = Fxp(realized_rsv, signed=True, n_word=param.word, n_frac=param.frac)
                unrealized_rsv = Fxp(unrealized_rsv, signed=True, n_word=param.word, n_frac=param.frac)
                reordered_rsv, reordered_ursv = self.reorder(realized_rsv, unrealized_rsv)

            # Do the matrix-vector multiplication
            next_rsv = self.vmm(reordered_rsv)

            if reordered_ursv is not None:
                # NOTICE Fxp object cannot implement np.vstack
                # combine with unrealized rsv
                next_rsv = np.vstack((next_rsv, reordered_ursv.get_val()))

                # remove the zero amplitudes
                next_rsv = next_rsv[~np.any(next_rsv[:, 1].reshape((-1, 1)) == 0, axis=1)]

                next_rsv[:, 2] = False

                return Fxp(next_rsv[next_rsv[:, 0].argsort()], signed=True, n_word=param.word, n_frac=param.frac)

            else:
                # remove the zero amplitudes
                next_rsv = next_rsv[np.where(next_rsv[:, 1] != 0)]

                next_rsv[:, 2] = False

                return Fxp(next_rsv[next_rsv[:, 0].argsort()], signed=True, n_word=param.word, n_frac=param.frac)

        else:
            print("No matched gate type!")

