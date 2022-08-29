import math
from qiskit import *
from qiskit.visualization import utils as q_utils

"""
Module for calculate execution time and clarify the quantum gate type
"""


def calculate_crossbar_exec_time(gate_info_list, num_of_qubits=10, num_of_gates=22, precision=8):
    L_read = 2.871  # Read latency (nanosecond)
    L_write = 5.230  # Write latency (nanosecond)
    crossbar_capacity = 2 ** num_of_qubits * 2 ** num_of_qubits  # rows x columns
    N_burst = 512  # 64bytes burst write

    # FIXME: Need optimization
    # num_of_qpus == # of gates
    num_of_qpus = num_of_gates
    T_load = (crossbar_capacity / N_burst) * L_write * num_of_qpus  # write time

    T_extract = T_extract_m = 0  # read time
    # for gate_info in gate_info_list:
    #     if gate_info['gate_type'] == 'one_qubit_gate':
    #         T_extract_m = 2 ** num_of_qubits * L_read
    #     elif gate_info['gate_type'] == 'two_qubit_gate':
    #         T_extract_m = 2 ** num_of_qubits * L_read / 2
    #     else:
    #         print('No matched gate type')

    for i in range(0, num_of_qpus):
        if num_of_qubits <= 12:
            T_extract_m = L_read
        else:
            cycle = pow(2, num_of_qubits-12)
            T_extract_m = L_read * cycle

        T_extract += T_extract_m

    T_exec = T_load + T_extract

    print(f"Crossbar size: {2 ** num_of_qubits} x {2 ** num_of_qubits}\n"
          f"Load time: {round(T_load, 2)}ns\n"
          f"Extract time: {round(T_extract, 2)}ns\n"
          f"Total: {round(T_exec, 2)}ns\n")


def eval_qiskit(qc, num_of_cores=0, processor_type="CPU"):
    qc.measure_all()

    sim = Aer.get_backend('statevector_simulator')

    if processor_type in sim.avaiable_devices():
        sim.set_option("device", processor_type)
    else:
        print(f"Processor Type {processor_type} not available in this device.")
        return 0

    sim.set_option("max_parallel_threads", num_of_cores)

    qc = transpile(qc, sim)
    job = sim.run(qc, shots=1024)
    # job = execute(qc, sim, shots=1024)
    result = job.result()
    counts = result.get_counts()
    # print(counts)
    return result.time_taken


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
