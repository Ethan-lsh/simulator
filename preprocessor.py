import math


class Preprocessor:
    def __init__(self):
        self.start_address = 0
        self.target_index = 0
        self.control_index = 0
        self.gate_type = None

    def set_attribute(self, start_address, gate_type, control_index, target_index):
        self.start_address = start_address
        self.gate_type = gate_type
        self.control_index = control_index
        self.target_index = target_index

    def cal_stride(self):
        stride = 1 << self.target_index

    def reorder(self, amplitudes):
        # initialize empty reordered_amplitudes list
        reordered_amplitudes = list()

        # initialize upper and lower qubit state
        upper_state, lower_state = 0, 0



    # def one_qubit_operation(self):
