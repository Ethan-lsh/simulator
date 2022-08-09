import numpy as np

import gate
import preprocessor as pre
import crossbar as cb


"""
3-qubits amplitudes
ex) amplitudes[0] = (|000>, |001>)
upper(amplitudes[0][0]) = |000>
"""
amplitudes = np.array([[1, 0], [0, 0], [0, 0], [0, 0]])

# make the crossbar array (=xbar_array)
xbar_array = cb.make_core()

stride_unit = pre.Preprocessor()

if __name__ == "__main__":
    # set the matrix on crossbar
    xbar_array.set_matrix(gate.H)

    # 3-qubits, one-qubit-gate, control=1, target=0
    stride_unit.set_attribute(3, 'one_qubit_gate', 1, 2)

    # set the amplitudes in stride_unit
    stride_unit.set_amplitudes(amplitudes)
    stride_unit.get_amplitudes()

    # calculate the stride value
    stride_unit.cal_stride()

    # quantum gate process
    # derive the reordered amplitudes
    qubit_state_vector = stride_unit.quantum_gate_process()
    print(qubit_state_vector)

    # matrix-vector multiplication
    test = xbar_array.run_xbar_vmm(qubit_state_vector[0, :])
    print('test', test)

