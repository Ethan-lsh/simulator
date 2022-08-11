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

    # stride_unit.get_amplitudes()

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
        qpu_result = qpu.run_xbar_mvm(reordered)
        print('result', qpu_result)

        # make empty restored amplitudes list
        restored_amplitudes = []

        for i, val in enumerate(qpu_result):
            restored_amplitudes.insert(r_index[i], val)

        print('restored', restored_amplitudes)
        return restored_amplitudes

    elif gate_info['gate_type'] == 'two_qubit_gate':
        weight = block_diag(*([gate_info['quantum_gate']] * (qubits - 1)))

        qpu.set_matrix(weight)

        # reordered amplitudes, realized index, unrealized index
        reordered, r_index, un_reordered, u_index = stride_unit.quantum_gate_process()

        # matrix-vector multiplication
        qpu_result = qpu.run_xbar_mvm(reordered)
        # print('result', qpu_result)

        # make empty restored amplitudes list
        restored_amplitudes = []

        # concatenate the index and amplitudes of realized and unrealized states
        index = r_index + u_index

        for i, val in enumerate(np.concatenate((qpu_result, un_reordered))):
            restored_amplitudes.insert(index[i], val)

        print('restored', restored_amplitudes)
        return restored_amplitudes


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
    amplitudes = [[1, 0], [0, 0], [0, 0], [0, 0]]

    gate_info_first = {"control_qubit": 0, "target_qubit": 0, "quantum_gate": gate.H,
                       "gate_type": 'one_qubit_gate'}  # Pauli-X
    gate_info_second = {"control_qubit": 0, "target_qubit": 1, "quantum_gate": gate.X,
                        "gate_type": 'two_qubit_gate'}  # CNOT

    first_result = quantum_simulation(qubits, qpu, stride_unit, gate_info_first, amplitudes)
    second_result = quantum_simulation(qubits, qpu, stride_unit, gate_info_second, np.array(first_result))
