# Robotic control loop with Intel's Loihi chip

This package contains the control-loop demo that shows how to interact with Spiking Neural Networks (SNNs) on 
Intel's Loihi neuromorphic chip during runtime for real-time robotic control.

## Related Works ##

We have been using control-loops shown here to construct interaction frameworks to enable real-time control on different kinds of robotic tasks. Details for the application of the control-loop can be found in these papers:


- Guangzhi Tang, Neelesh Kumar, and Konstantinos P. Michmizos. 
"Reinforcement co-Learning of Deep and Spiking Neural Networks for Energy-Efficient Mapless Navigation with Neuromorphic Hardware." 
IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS 2020). 
[[Paper]](https://arxiv.org/abs/2003.01157) [[Code]](https://github.com/combra-lab/spiking-ddpg-mapless-navigation)

- Ioannis Polykretis, Guangzhi Tang, and Konstantinos P. Michmizos. 
"An Astrocyte-Modulated Neuromorphic Central Pattern Generator for Hexapod Robot Locomotion on Intel’s Loihi." 
International Conference on Neuromorphic Systems (ICONS 2020). 
[[Paper]](https://dl.acm.org/doi/abs/10.1145/3407197.3407205)

- Guangzhi Tang, Neelesh Kumar, Raymond Yoo, and Konstantinos P. Michmizos. 
"Deep Reinforcement Learning with Population-Coded Spiking Neural Network for Continuous Control." 
4th Conference on Robot Learning (CoRL 2020). 
[[Paper]](https://arxiv.org/abs/2010.09635) [[Code]](https://github.com/combra-lab/pop-spiking-deep-rl)

## Software Installation ##

- Ubuntu 16.04
- Python 3.5.2
- NxSDK 0.9

Intel's neuromorphic library NxSDK is only required for SNN deployment on the Loihi neuromorphic chip. 
If you are interested in deploying SNN on Loihi, please contact the [Intel Neuromorphic Lab](https://www.intel.com/content/www/us/en/research/neuromorphic-community.html).

## Example Usage ##

To simplify the network structure, the demo defines a 2-layer SNN with the 5 neurons in the input layer and 5 neurons in the output layer. 
Neurons in the output layer copy the spike activities from the input layer by using one-to-one connections.
We demonstrate 3 different ways to interact with the SNN on Loihi:

1. (1 Control Iteration = 1 Loihi step) Inject spikes to the input layer. Record spikes from the output layer.

2. (1 Control Iteration = 10 Loihi steps) Inject current to Loihi and generate spikes for the input layer using Integrate-and-Fire neurons.
Record the number of spikes from the output layer.

3. (1 Control Iteration = 100 Loihi steps) Inject spike probability to Loihi and generate Poisson spikes for the input layer.
Record the number of spikes from the output layer.

More details on how to use the demo can be found in this ipython notebook.

## Acknowledgment ##

This work is supported by Intel's Neuromorphic Research Community Grant Award. 
Part of our code was inspired by Intel's NxSDK and discussions with Intel engineers.
