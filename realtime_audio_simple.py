# Objective: Record samples of the microphone of the input audio when we generate the chirps,
#            in a way that we can try to learn how to do a partial implementation of the ApneaAPP
#            paper to analyse the movement.


#
# In my computer I have a constant gain in the frequency response between speaker and microphone between 3KHz and 10KHz.
# And an attenuation of 63dB in the range between 18KHz and 22KHz.
#

import pyaudio
import numpy as np
import time
import scipy.io.wavfile

from chirp_generator import generate_chirp

def callback(in_data, frame_count, time_info, status):
    global rolling_buffer
    global white_noise_buffer
    global buffer_seq_num
    global chirp_buffer

    ##########
    # Recording the input from microphone.
    #####

    # Already receives the samples in float32.
    samples = np.fromstring(in_data, dtype=np.float32)
    # Determines the rolling buffer step size.
    step = samples.size
    # Rolls the buffer to make empty space for the new samples.
    rolling_buffer = np.roll(rolling_buffer, -step)
    # Copies the new samples.
    rolling_buffer[-step:] = samples

    ##########
    # Playing the output to speakers
    #####

    # global rm_phase
    # samples = np.fromstring(in_data, dtype=np.float32)
    # out = np.zeros(len(samples), dtype=np.float32)
    # for i in range(len(samples)):
    #     out[i] = samples[i] * np.sin(rm_phase)
    #     rm_phase += rm_freq / RATE * 2 * np.pi
    # return (out.tostring(), pyaudio.paContinue)


    out = np.zeros(len(samples), dtype=np.float32)
    #out =  white_noise_buffer

    # Sends the 10 milisecond chirp on the 4th output buffer.
    if buffer_seq_num > 3:
        #out[0: len(chirp_buffer)] = chirp_buffer
        # out = chirp_buffer

        start_index = buffer_seq_num * samples.size
        end_index   = (buffer_seq_num + 1) * samples.size

        if (start_index < 0) or (end_index > chirp_buffer.size):
            print("start_index: " + str(start_index))
            print("end_index: " + str(end_index))
            return

        out = chirp_buffer[ start_index : end_index ]

        if samples.size != out.size:
            print("samples.size != out.size: " + str(out.size))
            return

    buffer_seq_num += 1

    return (out.tostring(), pyaudio.paContinue)

def generate_white_noise(frames_per_buffer):
    mean = 0
    std = 1
    num_samples = frames_per_buffer
    samples = np.random.normal(mean, std, size=num_samples).astype(np.float32)
    return samples

if __name__ == "__main__":
    CHANNELS = 1
    sample_rate = 44100
    record_duration = 10.0  # 60    # seconds
    frames_per_buffer = 4096

    buffer_seq_num = 0

    # Pre-allocates the rolling buffer.
    len_rolling_buffer = int(sample_rate * record_duration)
    # rolling_buffer = np.zeros(len_rolling_buffer, dtype=np.int16)
    rolling_buffer = np.zeros(len_rolling_buffer, dtype=np.float32)

    # Creates and fill's the white noise buffer.
    white_noise_buffer = generate_white_noise(frames_per_buffer)

    # Creates and fill's a buffer with a chirp.
    chirp_duration = 0.010   # 10 miliseconds.  # Note: 1 meter distance.
    # chirp_duration = 1.0  # 10 miliseconds.
    start_freq = 3000  # Hz
    end_freq   = 10000 # Hz
    t, chirp_buffer, len_chirp = generate_chirp(sample_rate, chirp_duration, start_freq, end_freq)

    chirp_buffer = chirp_buffer.astype(np.float32)

    # Makes a buffer with 10 second, 100 times 10 milliseconds.
    num_repeats = 1000
    chirp_buffer = np.repeat(chirp_buffer, num_repeats)


    #in_data = np.zeros(4096, dtype=np.float32)
    #frame_count = 1
    #time_info = None
    #status = None
    #callback(in_data, frame_count, time_info, status)
    #exit()

    p = pyaudio.PyAudio()

    rm_freq = 10.0
    rm_phase = 0

    stream = p.open(format=pyaudio.paFloat32,
                    channels=CHANNELS,
                    rate=sample_rate,
                    input=True,
                    output=True,
                    frames_per_buffer=frames_per_buffer,  # 4096,
                    stream_callback=callback)

    stream.start_stream()


    # Get the inital time value.
    init_time = time.time()

    while stream.is_active():
        # See's if one minute has passed, to stop the process.
        curr_time = time.time()
        if curr_time - init_time > record_duration:
            break
        time.sleep(0.1)


    stream.stop_stream()
    stream.close()

    p.terminate()

    # Saves the input WAV file to HDD disc.
    filename = 'input_v001.wav'
    scipy.io.wavfile.write(filename, sample_rate, rolling_buffer)



