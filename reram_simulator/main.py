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

    circuit = sys.argv[1]

    # load the QuantumCircuit from qasm file
    qc = QuantumCircuit.from_qasm_file(f'../qasm/TEST_QASMBench/{circuit}')
    
    # quantum gate information list
    gate_info_list = utils.clarify_gate_type(qc)

    # number of qubits
    n_qubits = qc.num_qubits

    """
    Initilize realized state amplitude
    |000> = 1+0j
    """
    # amplitudes = [[1+0j], [0+0j], [0+0j], [0+0j], [0+0j], ..., [0+0j]]
    rsv = np.array([0, 1.0+0.0j, False])

    qpu = QPU()
    
    qpu.set_attribute(num_qubits=n_qubits, )

    # emulate 'do-while'
    intermediate_result = QPU.calculate
    try:
        for gate in gate_info_list[1:]:
            intermediate_result = quantum_simulation(num_qubits, qpu, )
    except StopIteration:
        quantum_simulation_result = intermediate_result

