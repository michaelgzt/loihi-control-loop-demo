#include "nxsdk.h"
#define input_dim 5  // Input neuron layer dimension
#define input_chip 0  // Input neuron chip id
#define input_core 0  // Input neuron core id
#define input_axon_id_start 0  // Start point for input neuron axon id
#define encode_window_step 102  // Number of steps for each window
#define encode_window_end 100  // Ending step for spike injection
#define input_spike_probability_precision 100  // Precision for input spike probability

/***************************************************************************
Encoder SNIP in snip_window_regular read input spike probability (0 - precision)
from encoder channel at every control loop step. The probability is then used to generate
spike activities for input neuron layer in steps within encode_window_end.
***************************************************************************/

int do_encoder(runState *s);
void run_encoder(runState *s);
