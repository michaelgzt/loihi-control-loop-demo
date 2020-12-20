import os
import numpy as np
import nxsdk.api.n2a as nx
from nxsdk.graph.monitor.probes import SpikeProbeCondition
from nxsdk.graph.processes.phase_enums import Phase


"""
The LoihiNetwork class defines a two-layer network with
input layer and output layer having the same dimensions.

Input layer has one-to-one connection to the output layer.
"""


class LoihiNetwork:
    """ SNN for Loihi control loop demo """

    def __init__(self, layer_dim, input_core_list, output_core_list):
        """

        Args:
            layer_dim (int): layer dimension
            input_core_list (list): input neuron core list
            output_core_list (list): output neuron core list
        """
        self.net = nx.NxNet()
        self.layer_dim = layer_dim
        self.input_core_list = input_core_list
        self.output_core_list = output_core_list

    def setup_loihi_snn(self, encode_dim, decode_dim, snip_dir, print_axon=False):
        """
        Setup Spiking Neural Network (SNN) on Loihi with input and output channels for online communication

        Args:
            encode_dim (int): encode channel dimension
            decode_dim (int): decode channel dimension
            snip_dir (str): directory of snip folder
            print_axon (bool): if true print axon id list of input layer

        Returns:
            board: compiled Loihi board object
            encoder_channel: encoder channel
            decoder_channel: decoder channel

        """
        # First we need to setup the layer we want to decode on Loihi
        output_layer = self.set_neuron_layer(self.net, self.output_core_list)
        self.set_output_decoding(output_layer)

        # Then setup input layer that we want to inject spikes
        input_layer = self.set_neuron_layer(self.net, self.input_core_list)
        fake_input_conn = self.set_input_encoding(self.net, self.layer_dim, input_layer, self.input_core_list)

        # Setup connections between layers
        input_output_conn = self.set_neuron_connection(self.layer_dim, input_layer, output_layer)

        # Compile Network
        compiler = nx.N2Compiler()
        board = compiler.compile(self.net)

        # We can know the axon id only after compiling the network
        if print_axon:
            input_axon_id_list = self.get_fake_connection_axon_id(self.net, fake_input_conn)
            print("Input Axon Id List: ")
            print(input_axon_id_list)

        # Setup encoder and decoder SNIP on the chip
        include_dir = os.path.abspath(snip_dir)
        encoder_snip = board.createSnip(
            Phase.EMBEDDED_SPIKING,
            name='encoder',
            includeDir=include_dir,
            cFilePath=include_dir + '/encoder.c',
            funcName='run_encoder',
            guardName='do_encoder'
        )
        decoder_snip = board.createSnip(
            Phase.EMBEDDED_MGMT,
            name='decoder',
            includeDir=include_dir,
            cFilePath=include_dir + '/decoder.c',
            funcName='run_decoder',
            guardName='do_decoder'
        )

        # Setup communication channels between host computer and SNIPs on Loihi
        encoder_channel = board.createChannel(b'encodeinput', "int", encode_dim)
        encoder_channel.connect(None, encoder_snip)
        decoder_channel = board.createChannel(b'decodeoutput', "int", decode_dim)
        decoder_channel.connect(decoder_snip, None)
        return board, encoder_channel, decoder_channel

    @staticmethod
    def set_neuron_layer(loihi_net, core_list):
        """
        Setup Neuron Layer on Loihi

        Args:
            loihi_net (nx.NxNet): Loihi network object
            core_list (list): core list

        Returns:
            neuron_layer: Loihi compartment group

        """
        neuron_prototype = nx.CompartmentPrototype(
            compartmentCurrentDecay=2 ** 12
        )
        neuron_layer = loihi_net.createCompartmentGroup(size=0)
        for core in core_list:
            neuron = loihi_net.createCompartment(prototype=neuron_prototype)
            neuron.logicalCoreId = core
            neuron_layer.addCompartments(neuron)
        return neuron_layer

    @staticmethod
    def set_neuron_connection(layer_dim, pre_neuron_layer, post_neuron_layer):
        """
        Setup connection between layers

        Args:
            layer_dim (int): layer dimension
            pre_neuron_layer (CompartmentGroup): pre-synaptic neuron layer
            post_neuron_layer (CompartmentGroup): post-synaptic neuron layer

        Returns:
            pre_post_conn: Loihi connection group

        """
        conn_w = np.eye(layer_dim) * 120
        conn_mask = np.int_(np.eye(layer_dim))
        pre_post_conn = pre_neuron_layer.connect(
            post_neuron_layer,
            prototype=nx.ConnectionPrototype(signMode=nx.SYNAPSE_SIGN_MODE.EXCITATORY),
            connectionMask=conn_mask,
            weight=conn_w
        )
        return pre_post_conn

    @classmethod
    def set_input_encoding(cls, loihi_net, layer_dim, input_neuron_layer, core_list):
        """
        Create fake connections to input neuron layer for online input encoding

        Args:
            loihi_net (nx.NxNet): Loihi network object
            layer_dim (int): layer dimension
            input_neuron_layer (CompartmentGroup): input neuron layer
            core_list (list): input core list

        Returns:
            fake_input_conn: Loihi connection group

        """
        neuron_prototype = nx.CompartmentPrototype()
        pseudo_layer = loihi_net.createCompartmentGroup(size=0)
        for core in core_list:
            pseudo_neuron = loihi_net.createCompartment(prototype=neuron_prototype)
            pseudo_neuron.logicalCoreId = core
            pseudo_layer.addCompartments(pseudo_neuron)

        # Connect fake neuron layer with input neuron layer
        fake_input_conn = cls.set_neuron_connection(layer_dim, pseudo_layer, input_neuron_layer)
        return fake_input_conn

    @staticmethod
    def set_output_decoding(output_neuron_layer):
        """
        Create fake spike probe to output neuron layer for online output decoding

        Args:
            output_neuron_layer (CompartmentGroup): output neuron layer

        """
        custom_probe_cond = SpikeProbeCondition(tStart=10000000000)
        # With the custom probe condition the spike probe will not active
        pseudo_spike_probe = output_neuron_layer.probe(nx.ProbeParameter.SPIKE, custom_probe_cond)

    @staticmethod
    def get_fake_connection_axon_id(loihi_net, fake_conn):
        """
        Get axon id for fake connection

        Args:
            loihi_net (nx.NxNet): Loihi network object
            fake_conn (ConnectionGroup): Fake connection

        Returns:
            axon_id_list: list of axon id

        """
        axon_id_list = []
        for conn in fake_conn:
            axon_id_list.append(loihi_net.resourceMap.inputAxon(conn.inputAxon.nodeId))
        return axon_id_list
