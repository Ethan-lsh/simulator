from qiskit import *
from qiskit.quantum_info import Statevector
from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit
import numpy as np
import cProfile
from bitstring import BitArray

"""
Module for calculate execution time and clarify the quantum gate type
"""

L_read = 5.2775  # Read latency (nanosecond)
L_write = 7.76179  # Write latency (nanosecond)
crossbar_capacity = 1024 * 1024  # rows x columns
N_burst = 512  # 64bytes burst write


def cal_stride(target_qubit):
    # calculate the stride value
    stride = 1 << target_qubit
    return stride


def find_rs(rs, index):
    try:
        value = np.where(rs[:, 0] == index)[0].real[0]
        if (value >= 0) and (rs[value, 2] == False):
            rs[value, 2] = True
            return rs[value]
    except IndexError:
        t_rs = np.array([index, 0.0+0.0j, True])
        return t_rs


def find_matrix(inst):
    # check whether the control gate or not
    gate_name = ''
    if inst.num_qubits == 1:
        gate_name = inst.name.upper()
    elif inst.num_qubits == 2:
        gate_name = inst.name[1:].upper()
    params = inst.params

    gate = None
    if len(params) == 0:
        gate = globals()[gate_name + "Gate"]()
    elif len(params) == 1:
        gate = globals()[gate_name + "Gate"](*params)
    elif len(params) == 2:
        gate = globals()[gate_name + "Gate"](*params)
    elif len(params) == 3:
        gate = globals()[gate_name + "Gate"](*params)
    else:
        print('Error: No matched param')

    matrix = gate.to_matrix()
    return matrix


def calculate_crossbar_exec_time(num_of_qubits, num_of_gates, gate_infos):
    num_of_qpus = num_of_gates

    count_single_gate = count_control_gate = 0
    for gate_info in gate_infos:
        if gate_info['gate_type'] == 'one_qubit_gate':
            count_single_gate += 1
        elif gate_info['gate_type'] == 'two_qubit_gate':
            count_control_gate += 1
        else:
            print('No matched gate type')

    T_load = (crossbar_capacity / N_burst) * L_write * num_of_qpus  # write time

    T_extract = T_extract_m = 0  # read time
    if num_of_qubits <= 10:
        T_extract = (L_read * count_single_gate) + (L_read * count_control_gate / 2)
    else:
        cycle = pow(2, num_of_qubits-10)
        T_extract = (L_read * count_single_gate * cycle) + (L_read * count_control_gate * cycle / 2)

    T_exec = (T_load + T_extract)

    print(f"Crossbar size: 1024 x 1024\n"
          f"Load time: {T_load}ns\n"
          f"Extract time: {T_extract}ns\n"
          f"Total: {T_exec}ns\n")


def eval_etri(trans_qc, gates):
    # initial statevector
    lrs = np.array([[0, 1.0 + 0.0j, False]])

    for i in range(0, len(gates)):
        # find the upper and lower array
        stride = 1 << gates[i]['target_qubit']
        # print('stride:', stride, "count:", i)

        for j in range(0, np.shape(lrs)[0]):
            upper_index = lrs[j][0].real
            upper_rs = find_rs(lrs, upper_index)

            if upper_rs is None:
                continue

            lower_index = upper_index + stride
            lower_rs = find_rs(lrs, lower_index)

            # combine and update
            if j == 0:
                pair_lrs = np.vstack([upper_rs, lower_rs])
                next_lrs = pair_lrs
            elif j > 0:
                next_lrs = np.vstack([next_lrs, upper_rs, lower_rs])

        lrs = next_lrs
        # print('previous lrs\n', lrs,)
        # print('-'*40)

        # find the quantum gate matrix
        qmatrix = find_matrix(trans_qc.data[i].operation)
        # print('qmatrix\n', qmatrix, end='\n')
        # print('-'*40)

        # derive first mvm result
        vector = lrs[0:2, 1].reshape(2, -1)
        mvm_result = np.matmul(qmatrix, vector)
        if mvm_result[0][0] == 0:
            mvm_rs = np.array([lrs[1][0], mvm_result[1][0], True])
        elif mvm_result[1][0] == 0:
            mvm_rs = np.array([lrs[0][0], mvm_result[0][0], True])
        else:
            mvm_rs = np.array([[lrs[0][0], mvm_result[0][0], True],
                               [lrs[1][0], mvm_result[1][0], True]])

        new_rs = mvm_rs

        for k in range(2, len(lrs), 2):
            vector = lrs[k:k+2, 1].reshape(2, -1)
            mvm_result = np.matmul(qmatrix, vector)
            if mvm_result[0][0] == 0:
                mvm_rs = np.array([lrs[k+1][0], mvm_result[1][0], True])
            elif mvm_result[1][0] == 0:
                mvm_rs = np.array([lrs[k][0], mvm_result[0][0], True])
            else:
                mvm_rs = np.array([[lrs[k][0], mvm_result[0][0], True],
                                   [lrs[k+1][0], mvm_result[1][0], True]])

            new_rs = np.vstack([new_rs, mvm_rs])

        lrs = new_rs
        length_of_lrs = len(lrs)
        # print('lrs\n', lrs, end='\n')

        if lrs.ndim == 1:
            lrs[2] = False
            lrs = np.array([lrs])
        else:
            lrs[:, 2] = False




def eval_qiskit(qc, num_of_cores=5, processor_type="CPU"):
    qc.measure_all()

    sim = Aer.get_backend('statevector_simulator')

    if processor_type in sim.available_devices():
        sim.set_option("device", processor_type)
    else:
        print(f"Processor Type {processor_type} not available in this device.")
        return 0

    sim.set_option("max_parallel_threads", num_of_cores)

    qc = transpile(qc, sim)
    job = sim.run(qc, shots=1)
    # job = execute(qc, sim, shots=1024)
    result = job.result()
    counts = result.get_counts()
    # print(counts)
    print(result.time_taken, end='\n')


def clarify_gate_type(qc):
    # gate info list
    gate_info_list = []

    # inst = qc.data
    for inst in qc.data:
        quantum_gate = inst.operation._name

        # qc.data.qubits
        gate_type = None
        control_qubit = target_qubit = 0

        if len(inst.qubits) == 1:
            gate_type = 'one_qubit_gate'
            control_qubit = 0
            target_qubit = inst.qubits[0]._index

        elif len(inst.qubits) == 2:
            gate_type = 'two_qubit_gate'
            control_qubit = inst.qubits[0]._index
            target_qubit = inst.qubits[1]._index

        gate_info_list.append({"quantum_gate": quantum_gate, "gate_type": gate_type, "control_qubit": control_qubit,
                               "target_qubit": target_qubit})

    return gate_info_list


def evaluate():
    param = 5

    qc = QuantumCircuit.from_qasm_file(f'./qasm/rcs_{param}.qasm')

    # trans_qc = transpile(qc, basis_gates=['h', 'x', 'y', 'z', 'cx'])

    gate_infos = clarify_gate_type(qc)
    # print('gate_infos', gate_infos, end='\n')

    num_of_qubits = qc.num_qubits

    num_of_gates = len(qc.count_ops())
    # print('kind of gates', num_of_gates)

    # length_of_circuits = len(gate_info)

    # print(f"========Crossbar: {param} of qubits and depth quantum circuit=========")
    # calculate_crossbar_exec_time(num_of_qubits, num_of_gates, gate_infos)
    #
    # print(f"========CPU: {param} of qubits and depth quantum circuit=========")
    # eval_qiskit(qc, processor_type="CPU", num_of_cores=0)

    print(f"\n========ETRI: {param} of qubits and depth quantum circuit==========")
    eval_etri(qc, gate_infos)


# For testing
if __name__ == '__main__':
    np.set_printoptions(suppress=True)
    evaluate()


















