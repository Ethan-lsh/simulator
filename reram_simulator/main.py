from qiskit import QuantumCircuit
from QPU import *
import sys

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

    # amplitudes = [[1+0j], [0+0j], [0+0j], [0+0j], [0+0j], ..., [0+0j]]
    rsv = np.array([[0, 1.0+0.0j, False]])

    qpu0 = QPU()
    qpu1 = QPU()

    # FIXME: Modify the process that set_attribute for automatically
    # unpacking the quantum gate list
    qpu0.set_attribute(n_qubits, **gate_info_list[0])
    qpu1.set_attribute(n_qubits, **gate_info_list[1])

    # set the quantum gate matrix called weight
    qpu0.set_weight(qc.data[0].operation)
    qpu1.set_weight(qc.data[1].operation)

    phase0 = qpu0.quantum_gate_process(rsv)

    phase1 = qpu1.quantum_gate_process(phase0)

    # qpu.get_weight()

    # # emulate 'do-while'
    # intermediate_result = QPU.calculate
    # try:
    #     for gate in gate_info_list[1:]:
    #         intermediate_result = quantum_simulation(num_qubits, qpu, )
    # except StopIteration:
    #     quantum_simulation_result = intermediate_result

