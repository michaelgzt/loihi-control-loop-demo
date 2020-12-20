#include "nxsdk.h"
#define input_dim 5  // Input neuron layer dimension
#define input_chip 0  // Input neuron chip id
#define input_core 0  // Input neuron core id
#define input_axon_id_start 0  // Start point for input neuron axon id

/****************************************************************
Encoder SNIP in snip_spike read spike list from encoder channel
at every step of Loihi operation and inject spike to neurons.
****************************************************************/

int do_encoder(runState *s);
void run_encoder(runState *s);
