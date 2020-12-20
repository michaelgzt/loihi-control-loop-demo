#include <stdlib.h>
#include "nxsdk.h"
#include "encoder.h"

// Input spike probability list
int input_spike_probability[input_dim] = {0};

int do_encoder(runState *s){
    return 1;
}

void run_encoder(runState *s){
    int time = s->time_step;

    // Read input spike probability for each window at the start of the window (time start at 1)
    if(time % encode_window_step == 1){
        int input_channel_id = getChannelID("encodeinput");
        readChannel(input_channel_id, &input_spike_probability, input_dim);
    }

    // Generate spikes base on input spike probability (Spike if random number larger then threshold)
    if(time % encode_window_step > 0 && time % encode_window_step <= encode_window_end){
        for(int ii=0; ii<input_dim; ii++){
            int random_number = rand();
            int spike_threshold = (RAND_MAX / input_spike_probability_precision) * input_spike_probability[ii];
            if(random_number < spike_threshold){
                int input_axon_id = input_axon_id_start + ii;
                uint16_t axonId = 1<<14 | ((input_axon_id) & 0x3FFF);
                ChipId chipId = nx_nth_chipid(input_chip);
                nx_send_remote_event(time, chipId, (CoreId){.id=4+input_core}, axonId);
            }
        }
    }
}
