import numpy as np
import preprocessor as pre
import crossbar as cb


"""
3-qubits amplitudes
ex) amplitudes[0] = (|000>, |001>)
upper(amplitudes[0][0]) = |000>
"""
amplitudes = np.array([[1, 0], [0, 0], [0, 0], [0, 0]])

# make the crossbar array (=xbar_array)
xbar_array = cb.make_core()

stride_unit = pre.Preprocessor()

if __name__ == "__main__":
    # TODO: set the weight on crossbar
    stride_unit.set_attribute(3, 'one_qubit_gate', 1, 0)

