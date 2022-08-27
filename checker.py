"""
Module for calculate execution time and clarify the quantum gate type
"""


def calculate_exec_time(gate_type, num_of_qubits, num_of_qpus, precision=8):
    L_read = 0.841  # Read latency (nanosecond)
    L_write = 10.20  # Write latency (nanosecond)
    crossbar_capacity = 2 ** num_of_qubits * 2 ** num_of_qubits  # rows x columns
    N_burst = 64  # 64bytes burst write

    T_load = (crossbar_capacity / N_burst) * L_write * num_of_qpus   # write time

    T_extract = 0  # read time
    if gate_type == 'one_qubit_gate':
        T_extract = 2 ** num_of_qubits * L_read
    elif gate_type == 'two_qubit_gate':
        T_extract = 2 ** num_of_qubits * L_read / 2
    else:
        print('No matched gate type')

    T_exec = T_load + T_extract


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
