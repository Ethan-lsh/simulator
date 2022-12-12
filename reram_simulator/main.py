from scipy.linalg import block_diag
from qiskit.circuit.random import random_circuit
from qiskit import QuantumCircuit
from qiskit.utils import *
import numpy as np

import utils
from qgate import quantum_gate
import preprocessor as pre
import crossbar as cb
import utils as ch
import math


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
        # weight = block_diag(*([gate_info['quantum_gate']] * (2**(qubits-1))))
        weight = block_diag(*([quantum_gate[gate_info['quantum_gate']]] * (2**(qubits-1))))

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

        # print('restored', restored_amplitudes)
        # print('\n')
        return np.array(restored_amplitudes)

    elif gate_info['gate_type'] == 'two_qubit_gate':
        # weight = block_diag(*([gate_info['quantum_gate']] * (2**(qubits - 2))))
        weight = block_diag(*([quantum_gate[gate_info['quantum_gate']]] * (2**(qubits-1))))

        qpu.set_matrix(weight)

        # reordered amplitudes, realized index, unrealized index
        reordered, r_index, un_reordered, u_index = stride_unit.quantum_gate_process()
        print('u_index', u_index)

        # matrix-vector multiplication
        qpu_result = qpu.run_xbar_mvm(reordered)
        print('result', qpu_result)

        # make empty restored amplitudes list
        restored_amplitudes = []

        # concatenate the index and amplitudes of realized and unrealized states
        index = r_index + u_index

        for i, val in enumerate(np.concatenate((qpu_result, un_reordered))):
            restored_amplitudes.insert(index[i], val)

        # print('restored', restored_amplitudes)
        # print('\n')
        return np.array(restored_amplitudes)

# TODO: Fix the cascading problem of complex number from cross-sim
if __name__ == "__main__":
    # make the crossbar array (=xbar_array)
    qpu = cb.make_core()

    # make the stride unit
    stride_unit = pre.Preprocessor()

    ############################
    ### Quantumcircuit setup ###
    ############################

    # load the QuantumCircuit from qasm file
    qc = QuantumCircuit.from_qasm_file('./qasm/small/test1.qasm')

    # number of qubits
    num_qubits = qc.num_qubits

    """
    3-qubits amplitudes
    ex) amplitudes[0] = (|000>, |001>)
    upper(amplitudes[0][0]) = |000>
    """
    # amplitudes = [[1+0j], [0+0j], [0+0j], [0+0j], [0+0j], ..., [0+0j]]
    amplitudes = np.zeros(2**num_qubits, dtype=np.complex64).reshape((-1, 1))
    amplitudes[0][0] = 1 + 0j

    # quantum gate information list
    gate_info_list = utils.clarify_gate_type(qc)

    # # emulate 'do-while'
    # intermediate_result = quantum_simulation(num_qubits, qpu, stride_unit, gate_info_list[0], amplitudes)
    # try:
    #     for gate in gate_info_list[1:]:
    #         intermediate_result = quantum_simulation(num_qubits, qpu, stride_unit, gate, intermediate_result)
    # except StopIteration:
    #     quantum_simulation_result = intermediate_result

    utils.calculate_crossbar_exec_time(gate_info_list, num_qubits, len(gate_info_list))
    utils.calculate_crossbar_exec_time(gate_info_list)
