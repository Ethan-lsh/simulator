from collections import OrderedDict
from qiskit import QuantumCircuit
from QPU import *
from precision import fpoint

############################
### Quantumcircuit setup ###
############################

# set the numpy precision
fpoint = fpoint
np.set_printoptions(precision=fpoint, floatmode='fixed', suppress=True)
print('precision', np.get_printoptions())

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

# quantum processor
# Contains all quantum processing unit instance
qp = OrderedDict()

if __name__ == "__main__":
    import warnings
    warnings.simplefilter("ignore", np.ComplexWarning)

    # Make the quantum processing unit according to the number of quantum gates
    for k in range(0, len(gate_info_list)):
        qp["qpu"+str(k)] = QPU()

        qp["qpu"+str(k)].set_attribute(n_qubits, **gate_info_list[k])

        qp["qpu"+str(k)].set_weight(qc.data[k].operation)

    try:
        for qpu in qp.values():
            rsv = qpu.quantum_gate_process(rsv)

        with open('test.csv', 'a') as csvfile:
            np.savetxt(csvfile, rsv,
                       delimiter=',',
                       fmt=f'%.{fpoint}f',
                       header=f'\n{fpoint} precision\n Qubit State \t Amplitude \t Status')
    except StopIteration:
        simulation_result = rsv


