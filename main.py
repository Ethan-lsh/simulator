import numpy as np

import gate
import preprocessor as pre
import crossbar as cb

# TODO: Expand the simulation environment for a many of quantum logic gate

"""
3-qubits amplitudes
ex) amplitudes[0] = (|000>, |001>)
upper(amplitudes[0][0]) = |000>
"""
amplitudes = np.array([[1, 0], [0, 0], [0, 0], [0, 0]])

# make the crossbar array (=xbar_array)
xbar_array = cb.make_core()

stride_unit = pre.Preprocessor()


# restores the rearranged array to its original location
def restore(selected_index, xbar_result):
    # make the empty array for restored amplitudes
    restored_amplitudes = list(xbar_result.size)

    # TODO: iterate the xbar_result and assign the xbar result into the restored amplitudes at the corresponding index
    for i in xbar_result:


if __name__ == "__main__":
    # set the matrix on crossbar
    xbar_array.set_matrix(gate.X)

    # 3-qubits, one-qubit-gate, control=1, target=0
    stride_unit.set_attribute(3, 'two_qubit_gate', 1, 2)

    # set the amplitudes in stride_unit
    stride_unit.set_amplitudes(amplitudes)
    # stride_unit.get_amplitudes()

    # calculate the stride value
    stride_unit.cal_stride()

    # quantum gate process
    # derive the reordered amplitudes
    qubit_state_vector = stride_unit.quantum_gate_process()
    print('qubit state vector\n', qubit_state_vector)

    # matrix-vector multiplication
    xbar_output = xbar_array.run_xbar_mvm(qubit_state_vector[0, :])
    print('test', xbar_output)
