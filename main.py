import numpy as np
from scipy.linalg import block_diag
import gate
import preprocessor as pre
import crossbar as cb


# TODO: make 'function restore' to restore the original order of amplitudes
def quantum_simulation(qubits, qpu, stride_unit, gate_info, amplitudes):
    # 3-qubits, one-qubit-gate, control=1, target=0
    stride_unit.set_attribute(qubits,
                              gate_info['gate_type'],
                              gate_info['control_qubit'],
                              gate_info['target_qubit'])

    # set the amplitudes in stride_unit
    stride_unit.set_amplitudes(amplitudes)

    stride_unit.get_amplitudes()

    # calculate the stride value
    stride_unit.cal_stride()

    if gate_info['gate_type'] == 'one_qubit_gate':
        # make the diagonal weight
        weight = block_diag(*([gate_info['quantum_gate']] * (qubits + 1)))

        # set the matrix on crossbar
        qpu.set_matrix(weight)

        # reordered amplitudes, realized index, None
        reordered, r_index, _ = stride_unit.quantum_gate_process()

        # matrix-vector multiplication
        result = qpu.run_xbar_mvm(reordered)
        print('result', result)

    elif gate_info['gate_type'] == 'two_qubit_gate':
        weight = block_diag(*([gate_info['quantum_gate']] * (qubits - 1)))

        qpu.set_matrix(weight)

        # reordered amplitudes, realized index, unrealized index
        reordered, r_index, u_index = stride_unit.quantum_gate_process()

        # matrix-vector multiplication
        result = qpu.run_xbar_mvm(reordered)
        print('result', result)


if __name__ == "__main__":
    # make the crossbar array (=xbar_array)
    qpu = cb.make_core()

    # make the stride unit
    stride_unit = pre.Preprocessor()

    # number of qubits
    qubits = 3

    """
    3-qubits amplitudes
    ex) amplitudes[0] = (|000>, |001>)
    upper(amplitudes[0][0]) = |000>
    """
    amplitudes = np.array([[1, 0], [0, 0], [0, 0], [0, 0]])

    gate_info = {"control_qubit": 0, "target_qubit": 1, "quantum_gate": gate.X, "gate_type": 'two_qubit_gate'}

    quantum_simulation(qubits, qpu, stride_unit, gate_info, amplitudes)
