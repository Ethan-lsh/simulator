from qiskit import *
from qiskit.quantum_info import Statevector
from qiskit.circuit.random import random_circuit
import cProfile
from qiskit import Aer
from bitstring import BitArray
import numpy as np

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



def find_rs(rs, index):
    try:
        value = np.where(rs[:, 0] == index)[0].real[0]
        if (value >= 0) and (rs[value, 2] == False):
            rs[value, 2] = True
            return rs[value]
    except IndexError:
        t_rs = np.array([index, 0.0+0.0j, True])
        return t_rs


def eval_etri(gates):
    '''
    Option #1
    # # check the intermediate statevector amp
    # qasm_header = 'OPENQASM 2.0; include "qelib1.inc";'

    # str_qasm = rc.qasm()
    # # print(str_qasm)
    # str_qasm = str_qasm.split('\n')

    # qasm_header += str_qasm[2] + str_qasm[3]

    # rs_length = list()

    # count_single_gate = count_control_gate = 0
    # for inst, gate_info in zip(range(4, len(str_qasm)), gate_infos[1:]):
    #     qasm_header += str_qasm[inst]

    #     dummy_circuit = QuantumCircuit.from_qasm_str(qasm_header)

    #     st = Statevector.from_instruction(dummy_circuit).to_dict()
    #     # print(st, end='\n')
    #     # st_keys = list(st.keys())

    #     stride = BitArray(uint=1 << gate_info['target_qubit'], length=n)

    #     rs_list = list()
    #     for st_key, _ in st.items():
    #         rs_list.append(st_key)

    #         bin_st_key = BitArray(bin=st_key)

    #         pair_key = bin_st_key | stride
    #         if pair_key.bin in list(st.keys()):
    #             continue
    #         elif pair_key.bin not in list(st.keys()):
    #             rs_list.append(pair_key.bin)

    #     rs_length.append(len(rs_list))
    #     # print(len(rs_list))
    #     if len(rs_list) > pow(2, n):
    #         print('Error')
    #         print('\n')

    # qasm_header += str_qasm[-1]
    # dummy_circuit = QuantumCircuit.from_qasm_str(qasm_header)
    # st = Statevector.from_instruction(dummy_circuit).to_dict()
    # # print(st)

    # rs_length = np.array(rs_length)
    # # print(rs_length)

    # index_under_1024 = np.where(rs_length < 1024)
    # index_over_1024 = np.where(rs_length >= 1024, rs_length // 1024, 0)
    '''

    # initial statevector
    lrs = np.array([[0, 1.0 + 0.0j, False]])

    for i in range(0, len(gates)):
        # find the upper and lower array
        stride = 1 << gates[i]['target_qubit']
        print('stride', stride, '\n')

        for j in range(0, np.shape(lrs)[0]):
            upper_index = lrs[j][0].real
            upper_rs = find_rs(lrs, upper_index)

            lower_index = upper_index + stride
            lower_rs = find_rs(lrs, lower_index)

            # combine and update
            if j == 0:
                pair_lrs = np.vstack([upper_rs, lower_rs])
                next_lrs = pair_lrs
            elif j > 0:
                next_lrs = np.vstack([next_lrs, upper_rs, lower_rs])

        lrs = next_lrs

        lrs[:, 2] = False
        print(lrs, '\n')

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
    param = 3

    qc = random_circuit(param, param, 2, measure=False)

    gate_infos = clarify_gate_type(qc)

    num_of_qubits = qc.num_qubits

    num_of_gates = len(qc.count_ops())

    # length_of_circuits = len(gate_info)

    # print(f"========Crossbar: {param} of qubits and depth quantum circuit=========")
    # calculate_crossbar_exec_time(num_of_qubits, num_of_gates, gate_infos)
    #
    # print(f"========CPU: {param} of qubits and depth quantum circuit=========")
    # eval_qiskit(qc, processor_type="CPU", num_of_cores=0)

    print(f"\n========ETRI: {param} of qubits and depth quantum circuit==========")
    eval_etri(gate_infos)

# For testing
if __name__ == '__main__':
    # cProfile.run('evaluate()', 'report.txt')
    evaluate()


















