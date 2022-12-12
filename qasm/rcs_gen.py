import numpy as np

from qiskit.circuit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.circuit import Reset
from qiskit.circuit.library.standard_gates import (IGate, U1Gate, XGate, YGate, ZGate, HGate, SGate, SdgGate as SDGGate, TGate,
                                                   TdgGate as TDGGate, RXGate, RZGate, CXGate,
                                                   CZGate, SwapGate as SWAPGate,
                                                   CCXGate)
from qiskit.circuit.exceptions import CircuitError
from qiskit.util import deprecate_arguments

import sys

@deprecate_arguments({'n_qubits': 'num_qubits'})
def random_circuit(num_qubits, depth, max_operands=3, measure=False,
                   conditional=False, reset=False, seed=None,
                   *, n_qubits=None):  # pylint:disable=unused-argument
    """Generate random circuit of arbitrary size and form.
    This function will generate a random circuit by randomly selecting gates
    from the set of standard gates in :mod:`qiskit.extensions`. For example:
    .. jupyter-execute::
        from qiskit.circuit.random import random_circuit
        circ = random_circuit(2, 2, measure=True)
        circ.draw(output='mpl')
    Args:
        num_qubits (int): number of quantum wires
        depth (int): layers of operations (i.e. critical path length)
        max_operands (int): maximum operands of each gate (between 1 and 3)
        measure (bool): if True, measure all qubits at the end
        conditional (bool): if True, insert middle measurements and conditionals
        reset (bool): if True, insert middle resets
        seed (int): sets random seed (optional)
        n_qubits (int): deprecated, use num_qubits instead
    Returns:
        QuantumCircuit: constructed circuit
    Raises:
        CircuitError: when invalid options given
    """
    if max_operands < 1 or max_operands > 3:
        raise CircuitError("max_operands must be between 1 and 3")

    one_q_ops = [IGate, U1Gate, XGate, YGate, ZGate,
                 HGate, SGate, SDGGate, TGate, TDGGate, RXGate, RZGate]
    one_param = [U1Gate, RXGate, RZGate]
    two_q_ops = [CXGate, CZGate, SWAPGate]

    qr = QuantumRegister(num_qubits, 'q')
    qc = QuantumCircuit(num_qubits)

    if measure or conditional:
        cr = ClassicalRegister(num_qubits, 'c')
        qc.add_register(cr)

    if reset:
        one_q_ops += [Reset]

    if seed is None:
        seed = np.random.randint(0, np.iinfo(np.int32).max)
    rng = np.random.default_rng(seed)

    # apply arbitrary random operations at every depth
    for _ in range(depth):
        # choose either 1, 2, or 3 qubits for the operation
        remaining_qubits = list(range(num_qubits))
        while remaining_qubits:
            max_possible_operands = min(len(remaining_qubits), max_operands)
            num_operands = rng.choice(range(max_possible_operands)) + 1
            rng.shuffle(remaining_qubits)
            operands = remaining_qubits[:num_operands]
            remaining_qubits = [q for q in remaining_qubits if q not in operands]
            if num_operands == 1:
                operation = rng.choice(one_q_ops)
            elif num_operands == 2:
                operation = rng.choice(two_q_ops)
            if operation in one_param:
                num_angles = 1
            else:
                num_angles = 0
            angles = [rng.uniform(0, 2 * np.pi) for x in range(num_angles)]
            register_operands = [qr[i] for i in operands]

            if operation is SWAPGate:
                op = CXGate(*angles)
                op1 = CXGate(*angles)
                op2 = CXGate(*angles)

                qc.append(op, register_operands)
                qc.append(op1, register_operands[::-1])  # reverse CXGate
                qc.append(op2, register_operands)
            else:
                op = operation(*angles)

                # with some low probability, condition on classical bit values
                if conditional and rng.choice(range(10)) == 0:
                    value = rng.integers(0, np.power(2, num_qubits))
                    op.condition = (cr, value)

                qc.append(op, register_operands)

    if measure:
        qc.measure(qr, cr)

    qc.qasm(formatted=False, filename=f'./rcs/rcs_{num_qubits}.qasm')
    return qc


if __name__ == '__main__':
    qubits = int(sys.argv[1])
    random_circuit(qubits, qubits, 2, measure=False, conditional=False)