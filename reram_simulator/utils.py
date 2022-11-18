from qiskit import *
from qiskit.quantum_info import Statevector
from qiskit.circuit.library import *
from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit
import numpy as np
import sys
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
        t_rs = np.array([index, 0.0 + 0.0j, True])
        return t_rs


def find_matrix(inst):
    # check whether the control gate or not
    gate_name = ''

    if inst.name.find('c') == -1:
        gate_name = inst.name.upper()
        if gate_name == 'SDG':
            gate_name = 'Sdg'
        elif gate_name == 'TDG':
            gate_name = 'Tdg'
        elif gate_name == 'ID':
            gate_name = 'I'
    elif inst.name.find('c') == 0:
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

    # print(gate_name)
    matrix = gate.to_matrix()
    return matrix


def do_mvm(lrs, qmatrix):
    # split the lrs into 3-pars
    # value of qubit state
    value = lrs[:, 0].reshape(-1, 1)

    # amplitude of qubit state
    amp = lrs[:, 1]

    # status of qubit state
    state = lrs[:, 2].reshape(-1, 1)

    # make the lrs into ndarray(-1, 2, 1)
    amp = amp.reshape([-1, 2, 1])

    # matmul with broadcasting
    mvm_result = np.matmul(qmatrix, amp).reshape((-1, 1))

    # find the non-zero value
    no_zero_index = np.nonzero(mvm_result)
    # print('non zero index', no_zero_index)

    # no zero value of qubit state
    no_zero_value = value[no_zero_index].reshape((-1, 1))
    # print(no_zero_value)

    # no zero amplitude of qubit state
    no_zero_amp = mvm_result[no_zero_index].reshape((-1, 1))
    # print(no_zero_amp)

    # no zero state of qubit state
    no_zero_state = state[no_zero_index].reshape((-1, 1))
    # print(no_zero_state)

    if no_zero_value.ndim == 1:
        new_lrs = np.concatenate((no_zero_value, no_zero_amp, no_zero_state), axis=0)
        new_lrs = np.array([new_lrs])
        new_lrs[0, 2] = False
    else:
        new_lrs = np.concatenate((no_zero_value, no_zero_amp, no_zero_state), axis=1)
        new_lrs[:, 2] = False

    # print(new_lrs)

    return new_lrs


def calculate_crossbar_exec_time(num_of_qubits, kind_of_gates, gate_infos):
    count_single_gate = count_control_gate = 0
    for gate_info in gate_infos:
        if gate_info['gate_type'] == 'one_qubit_gate':
            count_single_gate += 1
        elif gate_info['gate_type'] == 'two_qubit_gate':
            count_control_gate += 1
        else:
            print('No matched gate type')

    # T_load = (crossbar_capacity / N_burst) * L_write * num_of_qpus  # write time
    T_load = 1024 * L_write * (1024 / N_burst)

    T_extract = T_extract_m = 0  # read time
    if num_of_qubits <= 10:
        T_extract = (L_read * count_single_gate) + (L_read * count_control_gate / 2)
    else:
        cycle = pow(2, num_of_qubits - 10)
        T_extract = (L_read * count_single_gate * cycle) + (L_read * count_control_gate * cycle / 2)

    T_exec = (T_load + T_extract)

    print(f"#### QCL method on Crossbar (ns) ####\n"
          f"Load time: {T_load}\n"
          f"Extract time: {T_extract}\n"
          f"Total: {T_exec}\n")


def eval_etri(qc, gates, kind_of_gates):
    # initial statevector
    lrs = np.array([[0, 1.0 + 0.0j, False]])

    T_extract = T_extract_m = 0  # read time

    
    for i in range(0, len(gates)):
        # find the upper and lower array
        stride = 1 << gates[i]['target_qubit']
        # print('stride:', stride, "count:", i)

        for j in range(0, np.shape(lrs)[0]):
            upper_index = lower_index = 0

            upper_index = lrs[j][0].real
            upper_rs = find_rs(lrs, upper_index)

            if upper_rs is None or []:
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
        # print('previous lrs\n', lrs)
        # print('-'*40)

        # find the quantum gate matrix
        qmatrix = find_matrix(qc.data[i].operation)
        # print('qmatrix\n', qmatrix, end='\n')
        # print('-'*40)

        lrs = do_mvm(lrs, qmatrix)

        length_of_lrs = len(lrs)
        # print('length of lrs: ', length_of_lrs)

        if length_of_lrs <= 1024:
            T_extract_m = L_read
        elif length_of_lrs > 1024:
            T_extract_m = L_read * (length_of_lrs / pow(2, 10))

        T_extract += T_extract_m

    # T_load = (crossbar_capacity / N_burst) * L_write * kind_of_gates  # write time
    T_load = 1024 * L_write * (1024 / N_burst)

    T_exec = T_load + T_extract

    print(f"#### ETRI method on Crossbar (ns) ####\n"
          f"Load time: {T_load}\n"
          f"Extract time: {T_extract}\n"
          f"Total: {T_exec}\n")
    

    '''
    ratio = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

    T_write = (crossbar_capacity / N_burst) * L_write * kind_of_gates  # write time
    print(f'Load time: {T_write}\n')

    T_read = 0
    for i in range(0, len(ratio)):
        RS_length = pow(2, qc.num_qubits) * ratio[i]

        if RS_length <= 1024:
            T_read= L_read * 2 * len(gates)
        else:
            T_read = L_read * 2 * (RS_length / 1024) * len(gates)

        T_total = T_write + T_read

        print(f"Extract time: {T_read}\n"
            f"Total: {T_total}\n")
    '''

def eval_qiskit(qc, num_of_cores, processor_type="CPU"):
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
    print("#### CPU (s) ####")
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
    # param = int(sys.argv[1])

    qc = QuantumCircuit.from_qasm_file(f'../qasm/TEST_QASMBench/large/ghz_state_n23.qasm')


    gate_infos = clarify_gate_type(qc)
    # print('gate_infos', gate_infos, end='\n')

    num_of_qubits = qc.num_qubits

    kind_of_gates = len(qc.count_ops())
    # print('kind of gates', num_of_gates)

    # length_of_circuits = len(gate_info)

    print(f"============== Crossbar Array : 1024 x 1024 =============")
    # print(f"-------------- {param} qubits ----------------")
    
    # calculate_crossbar_exec_time(num_of_qubits, kind_of_gates, gate_infos)
    
    eval_etri(qc, gate_infos, kind_of_gates)
    
    eval_qiskit(qc, processor_type="CPU", num_of_cores=24)

   


# For testing
if __name__ == '__main__':
    np.set_printoptions(suppress=True)
    evaluate()
