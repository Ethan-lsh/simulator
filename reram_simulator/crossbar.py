import cross_sim
from cross_sim import MakeCore
from cross_sim import Parameters
from param import frac


def make_core():
    params = Parameters()

    error_rate = 0.0

    ######################
    ##  algorithm param ##
    ######################
    params.algorithm_params.crossbar_type = "OFFSET"
    params.algorithm_params.sim_type = "NUMERIC"
    params.algorithm_params.disable_clipping = True

    # xbar weight
    params.algorithm_params.weights.maximum = 1
    params.algorithm_params.weights.minimum = -1


    # xbar input
    params.algorithm_params.col_input.maximum = 1
    params.algorithm_params.col_input.minimum = -1
    params.algorithm_params.row_input.maximum = 1
    params.algorithm_params.row_input.minimum = -1

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

    

    ######################
    ##     xbar param   ##
    ######################
    params.xbar_params.weights.maximum = 1
    params.xbar_params.weights.minimum = -1
    # params.xbar_params.bits = 0
    # params.xbar_params.sign_bit = True

    # Input
    # params.xbar_params.row_input.minimum = -1
    # params.xbar_params.row_input.maximum = 1
    # params.xbar_params.row_input.bits = 2 
    # params.xbar_params.row_input.sign_bit = True

    params.xbar_params.col_input.minimum = -1
    params.xbar_params.col_input.maximum = 1
    params.xbar_params.col_input.bits = frac - 1 
    params.xbar_params.col_input.sign_bit = True


    ## Output
    params.xbar_params.row_output.minimum = -1
    params.xbar_params.row_output.maximum = 1
    params.xbar_params.row_output.bits = frac - 1
    params.xbar_params.row_output.sign_bit = True

    # A/D property
    # params.xbar_params.col_output.minimum = -1
    # params.xbar_params.col_output.maximum = 1
    # params.xbar_params.col_output.bits = 1
    # params.xbar_params.col_output.sign_bit = True

    
    params.xbar_params.row_input.normal_error_post.sigma = error_rate
    params.xbar_params.row_input.uniform_error_post.keep_within_range = True

    ####################
    ## Neumeric param ## 
    ####################
    # Read/write noise
    params.numeric_params.read_noise.sigma = error_rate
    params.numeric_params.read_noise.proportional = False
    params.numeric_params.read_noise.keep_within_range = True
    # params.numeric_params.update_model = "DG_LOOKUP"

    # params.numeric_params.write_noise.sigma = error_rate
    # params.numeric_params.write_noise.write_noise_model = "G_PROPORTIONAL"

    # params.numeric_params.nonlinearity.alpha = 0.0
    # params.numeric_params.nonlinearity.symmetric = False

    return MakeCore(params)
