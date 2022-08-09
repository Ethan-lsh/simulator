import numpy as np
import crossbar as cb


def gate(gate_type, target, amplitudes, control=0):
    stride = 1 << target

    reordered_amplitudes[0] = amplitudes[0]
    reordered_amplitudes[1] = amplitudes[2]
    reordered_amplitudes[2] = amplitudes[1]
    reordered_amplitudes[3] = amplitudes[3]
    reordered_amplitudes[4] = amplitudes[4]
    reordered_amplitudes[5] = amplitudes[6]
    reordered_amplitudes[6] = amplitudes[5]
    reordered_amplitudes[7] = amplitudes[7]

    reorder = np.array(reordered_amplitudes).reshape((4,2))

    if gate_type == 'hadamard':
        h_gate = np.array([[0.7, 0.7],
                      [0.7, -0.7]])

        neural_core.set_matrix(h_gate)

        result = neural_core.run_xbar_vmm(reorder[0, :])

        print(result)

    elif gate_type == 'X':
        x_gate = np.array([[0, 1],
                           [1, 0]])

        neural_core.set_matrix(x_gate)

        neural_core.run_xbar_vmm(reorder)

    else:
        print('no matched gate')



amplitudes = [1, 0, 0, 0, 0, 0, 0, 0]

reordered_amplitudes = [0] * len(amplitudes)

neural_core = cb.make_core()

type = 'hadamard'

gate(type, 0, amplitudes)
