import sys

sys.path.append('./')
from loihi_network import LoihiNetwork


def check_input_layer_axon_id_list(layer_dim=5,
                                   input_core_list=[0, 0, 0, 0, 0],
                                   output_core_list=[0, 0, 0, 0, 0],
                                   snip_dir='./snip_spike'):
    """
    Check the axon id list for input layer

    Args:
        layer_dim (int): layer dimension
        input_core_list (list): input layer core list
        output_core_list (list): output layer core list
        snip_dir (str): SNIP directory

    """
    loihi_snn = LoihiNetwork(layer_dim, input_core_list, output_core_list)
    board, encoder_channel, decoder_channel = loihi_snn.setup_loihi_snn(layer_dim, layer_dim, snip_dir,
                                                                        print_axon=True)
    board.startDriver()
    board.disconnect()


def run_loihi_spike_online_interaction(layer_dim=5,
                                       input_core_list=[0, 0, 0, 0, 0],
                                       output_core_list=[0, 0, 0, 0, 0],
                                       snip_dir='./snip_spike'):
    """
    Online interaction simulation for interact each step with Loihi

    Args:
        layer_dim (int): layer dimension
        input_core_list (list): input layer core list
        output_core_list (list): output layer core list
        snip_dir (str): SNIP directory

    """
    loihi_snn = LoihiNetwork(layer_dim, input_core_list, output_core_list)
    board, encoder_channel, decoder_channel = loihi_snn.setup_loihi_snn(layer_dim, layer_dim, snip_dir)

    # Start Loihi simulation
    loihi_sim_step = layer_dim + 2
    board.startDriver()
    board.run(loihi_sim_step, aSync=True)

    # Begin control loop (for first layer_dim step active input neuron in sequence)
    for ii in range(loihi_sim_step):
        input_spike_list = [0 for _ in range(layer_dim)]
        if ii < layer_dim:
            input_spike_list[ii] = 1

        # Write input_spike_list to Loihi
        encoder_channel.write(layer_dim, input_spike_list)

        # Read output_spike_list from Loihi
        output_spike_list = decoder_channel.read(layer_dim)

        print("Loihi step: ", ii, " Input Spike: ", input_spike_list, " Output Spike: ", output_spike_list)

    # Stop Loihi simulation
    board.finishRun()
    board.disconnect()


def run_loihi_window_regular_online_interaction(layer_dim=5,
                                                input_core_list=[0, 0, 0, 0, 0],
                                                output_core_list=[0, 0, 0, 0, 0],
                                                snip_dir='./snip_window_regular'):
    """
    Online interaction simulation for interact each control step with Loihi window steps
    (Input neurons generate regular spikes base on current input)

    Args:
        layer_dim (int): layer dimension
        input_core_list (list): input layer core list
        output_core_list (list): output layer core list
        snip_dir (str): SNIP directory

    """
    loihi_snn = LoihiNetwork(layer_dim, input_core_list, output_core_list)
    board, encoder_channel, decoder_channel = loihi_snn.setup_loihi_snn(layer_dim, layer_dim, snip_dir)

    # Start Loihi simulation
    loihi_sim_step = layer_dim * 12
    board.startDriver()
    board.run(loihi_sim_step, aSync=True)

    # Begin control loop (for each control loop iteration, give ii input neuron with (ii+1)*10 input current)
    for ii in range(layer_dim):
        input_current_list = [0 for _ in range(layer_dim)]
        input_current_list[ii] = (ii + 1) * 10

        # Write input_spike_list to Loihi
        encoder_channel.write(layer_dim, input_current_list)

        # Read output_spike_list from Loihi
        output_fr_list = decoder_channel.read(layer_dim)

        print("Control step: ", ii, " Input Current: ", input_current_list, " Output Spike Number: ", output_fr_list)

    # Stop Loihi simulation
    board.finishRun()
    board.disconnect()


def run_loihi_window_poisson_online_interaction(layer_dim=5,
                                                input_core_list=[0, 0, 0, 0, 0],
                                                output_core_list=[0, 0, 0, 0, 0],
                                                snip_dir='./snip_window_poisson'):
    """
    Online interaction simulation for interact each control step with Loihi window steps
    (Input neurons generate Poisson spikes base on input spike probability)

    Args:
        layer_dim (int): layer dimension
        input_core_list (list): input layer core list
        output_core_list (list): output layer core list
        snip_dir (str): SNIP directory

    """
    loihi_snn = LoihiNetwork(layer_dim, input_core_list, output_core_list)
    board, encoder_channel, decoder_channel = loihi_snn.setup_loihi_snn(layer_dim, layer_dim, snip_dir)

    # Start Loihi simulation
    loihi_sim_step = layer_dim * 102
    board.startDriver()
    board.run(loihi_sim_step, aSync=True)

    # Begin control loop (for each control loop iteration, give ii input neuron with (ii+1)*10 input spike probability)
    for ii in range(layer_dim):
        input_current_list = [0 for _ in range(layer_dim)]
        input_current_list[ii] = (ii + 1) * 10

        # Write input_spike_list to Loihi
        encoder_channel.write(layer_dim, input_current_list)

        # Read output_spike_list from Loihi
        output_fr_list = decoder_channel.read(layer_dim)

        print("Control step: ", ii, " Input Current: ", input_current_list, " Output Spike Number: ", output_fr_list)

    # Stop Loihi simulation
    board.finishRun()
    board.disconnect()

