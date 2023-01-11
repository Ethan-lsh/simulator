from qiskit import *
from qiskit.quantum_info import Statevector
from qiskit.circuit.library import *
from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit
import numpy as np
from fxpmath import Fxp
import param


"""
Module for calculate execution time and clarify the quantum gate type
"""

L_read = 2.8717
L_write = 5.23066

OL_read = 3.9984  # Read latency (nanosecond)
OL_write = 6.4441  # Write latency (nanosecond)
crossbar_capacity = 1024 * 1024  # rows x columns
N_burst = 512  # 64bytes burst write



def find_rs(rs, index, urs=None):
    rs_index = np.where(rs[:, 0] == index)[0]

    if urs is not None:
        urs_index = np.where(urs[:, 0] == index)[0]
    else:
        urs_index = np.array([])

    if rs_index.size > 0 and urs_index.size == 0:
        if rs[rs_index, 2] == False:
            rs[rs_index, 2] = True
            return rs[rs_index].get_val(), urs
        else:
            return None, urs

    elif rs_index.size == 0 and urs_index.size == 0:
        return np.array([index, 0.0+0.0j, True]), urs

    elif rs_index.size == 0 and urs_index.size > 0:
        if urs[urs_index, 2] == False:
            urs[urs_index] = True
            t_rs = urs[urs_index]
            d_urs = np.delete(urs, urs_index, axis=0)
            return t_rs.get_val(), d_urs
        else:
            return None, urs


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
        if gate_name == 'CX': # CX gate
            gate_name = 'X'
        elif gate_name == 'CCX':  # CCX gate
            gate_name = 'X'

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
    # print('matrix \n', matrix, end='\n')
    return matrix


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
    print(counts)
    print(result.time_taken, end='\n')


def clarify_gate_type(qc):
    # gate info list
    gate_info_list = []

    # inst = qc.data
    for inst in qc.data:
        gate_name = inst.operation._name

        # qc.data.qubits
        gate_type = None
        ccontrol_qubit = control_qubit = target_qubit = 0

        if len(inst.qubits) == 1:
            gate_type = 'one_qubit_gate'
            control_qubit = 0
            target_qubit = inst.qubits[0]._index

        elif len(inst.qubits) == 2:
            gate_type = 'two_qubit_gate'
            control_qubit = inst.qubits[0]._index
            target_qubit = inst.qubits[1]._index

        elif len(inst.qubits) == 3:
            gate_type = 'three_qubit_gate'
            ccontrol_qubit = inst.qubits[0]._index
            control_qubit = inst.qubits[1]._index
            target_qubit = inst.qubits[2]._index

        gate_info_list.append({"gate_name": gate_name, 
                                "gate_type": gate_type, 
                                "ccontrol_qubit": ccontrol_qubit,
                                "control_qubit": control_qubit,
                                "target_qubit": target_qubit})

    return gate_info_list
