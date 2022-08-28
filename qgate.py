import numpy as np

X_gate = np.array([[0, 1],
                   [1, 0]], dtype=np.complex64)

Y_gate = np.array([[0, -1j],
                   [1j, 0]], dtype=np.complex64)

Z_gate = np.array([[1, 0],
                   [0, -1]], dtype=np.complex64)

H_gate = np.array([[0.7, 0.7],
                   [0.7, -0.7]], dtype=np.complex64)

quantum_gate = {'x': X_gate, 'y': Y_gate, 'z': Z_gate, 'h': H_gate, 'cx': X_gate}
