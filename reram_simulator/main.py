from scipy.linalg import block_diag
from qiskit.circuit.random import random_circuit
from qiskit import QuantumCircuit
from qiskit.utils import *
import numpy as np

import utils
from QPU import *
import sys


   
    

   

# TODO: Fix the cascading problem of complex number from cross-sim
if __name__ == "__main__":
    ############################
    ### Quantumcircuit setup ###
    ############################

    # circuit = sys.argv[1]

    # load the QuantumCircuit from qasm file
    # qc = QuantumCircuit.from_qasm_file(f'../qasm/TEST_QASMBench/{circuit}')
    qc = QuantumCircuit.from_qasm_file(f'../qasm/TEST_QASMBench/small/lpn_n5.qasm')

    # quantum gate information list
    gate_info_list = utils.clarify_gate_type(qc)
    # print(gate_info_list)

    # number of qubits
    n_qubits = qc.num_qubits

    """
    Initilize realized state amplitude
    |000> = 1+0j
    """
    # amplitudes = [[1+0j], [0+0j], [0+0j], [0+0j], [0+0j], ..., [0+0j]]
    rsv = np.array([[0, 1.0+0.0j, False]])

    qpu = QPU()

    # FIXME: Modify the process that set_attribute for automatically
    # unpacking the quantum gate list
    qpu.set_attribute(n_qubits, **gate_info_list[1])

    # set the quanutm gate matrix called weight
    qpu.set_weight(qc.data[1].operation)

    print(qpu.gate_type)

    qpu.quantum_gate_process(rsv)

    # qpu.get_weight()

    # # emulate 'do-while'
    # intermediate_result = QPU.calculate
    # try:
    #     for gate in gate_info_list[1:]:
    #         intermediate_result = quantum_simulation(num_qubits, qpu, )
    # except StopIteration:
    #     quantum_simulation_result = intermediate_result

