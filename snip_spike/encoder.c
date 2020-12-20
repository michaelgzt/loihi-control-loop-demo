#include <stdlib.h>
#include "nxsdk.h"
#include "encoder.h"

// Spike activity list
int input_spike_activity[input_dim] = {0};

int do_encoder(runState *s){
    return 1;
}

void run_encoder(runState *s){
    int time = s->time_step;

    // Read neuron spike activity from encoder channel
    int input_channel_id = getChannelID("encodeinput");
    readChannel(input_channel_id, &input_spike_activity, input_dim);

    // Inject spikes to neurons
    for(int ii=0; ii<input_dim; ii++){
        if(input_spike_activity[ii] == 1){
            int input_axon_id = input_axon_id_start + ii;
            uint16_t axonId = 1<<14 | ((input_axon_id) & 0x3FFF);
            ChipId chipId = nx_nth_chipid(input_chip);
            nx_send_remote_event(time, chipId, (CoreId){.id=4+input_core}, axonId);

            // Reset spike activity list
            input_spike_activity[ii] = 0;
        }
    }
}
