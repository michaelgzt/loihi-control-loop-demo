#include "nxsdk.h"
#define output_dim 5  // Output neuron layer dimension

/****************************************************************
Decoder SNIP in snip_spike record spike from output neurons
at every step of Loihi operation and send through decoder channel.
****************************************************************/

int do_decoder(runState *s);
void run_decoder(runState *s);