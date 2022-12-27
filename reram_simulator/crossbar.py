from cross_sim import MakeCore
from cross_sim import Parameters
from precision import fpoint



def make_core():
    params = Parameters()

    error_rate = 0.0

    params.algorithm_params.crossbar_type = "OFFSET"
    params.algorithm_params.sim_type = "NUMERIC"
    params.algorithm_params.disable_clipping = False

    # xbar weight
    params.algorithm_params.weights.maximum = 1
    params.algorithm_params.weights.minimum = -1
    params.xbar_params.weights.maximum = 1
    params.xbar_params.weights.minimum = -1

    # xbar input
    params.algorithm_params.col_input.maximum = 1.0
    params.algorithm_params.col_input.minimum = -1.0
    params.algorithm_params.row_input.maximum = 1.0
    params.algorithm_params.row_input.minimum = -1.0

    # xbar output
    params.algorithm_params.col_output.maximum = 1
    params.algorithm_params.col_output.minimum = -1
    params.algorithm_params.row_output.maximum = 1
    params.algorithm_params.row_output.minimum = -1

    # xbar update
    params.algorithm_params.col_update.maximum = 1
    params.algorithm_params.col_update.minimum = -1
    params.algorithm_params.row_update.maximum = 1
    params.algorithm_params.row_update.minimum = -1

    # D/A property
    params.xbar_params.row_input.bits = fpoint
    params.xbar_params.row_input.sign_bit = True

    params.xbar_params.col_input.bits = fpoint
    params.xbar_params.col_input.sign_bit = True

    params.xbar_params.row_input.normal_error_post.sigma = error_rate
    params.xbar_params.row_input.uniform_error_post.keep_within_range = True

    # A/D property
    params.xbar_params.col_output.bits = fpoint
    params.xbar_params.col_output.sign_bit = True

    params.xbar_params.row_output.bits = fpoint
    params.xbar_params.row_output.sign_bit = True

    # Read/write noise
    params.numeric_params.read_noise.sigma = error_rate
    params.numeric_params.read_noise.proportional = False
    params.numeric_params.read_noise.keep_within_range = True
    params.numeric_params.update_model = "DG_LOOKUP"

    params.numeric_params.write_noise.sigma = error_rate
    params.numeric_params.write_noise.write_noise_model = "G_PROPORTIONAL"

    params.numeric_params.nonlinearity.alpha = 0.0
    params.numeric_params.nonlinearity.symmetric = False

    return MakeCore(params)
