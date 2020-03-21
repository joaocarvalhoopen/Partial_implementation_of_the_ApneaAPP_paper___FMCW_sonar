import matplotlib.pyplot as plt
import numpy as np
import pyaudio

# t -- time
# s -- samples

def generate_chirp(sample_rate, chirp_duration, start_freq, end_freq):
    f_0 = start_freq
    f_1 = end_freq
    start = 0.0
    stop = chirp_duration
    step = 1.0 / sample_rate
    t = np.arange(start, stop, step, dtype='float')
    phase = 0.0
    chirp_period = chirp_duration # 1 / 100.0 #1.0
    k = (f_1 - f_0) / chirp_period
    s = np.sin(phase + 2*np.pi * ( f_0*t + (k/2)*np.square(t)) )
    len_s = s.size
    return (t, s, len_s)

def play_audio(t, s, sample_rate):
    # Scale to int16 for sound card
    max_int16 = 32768
    samples_int16 = (s * max_int16).astype(np.int16)

    # Opens a stream to sound card, device 0.
    p = pyaudio.PyAudio()

    stream = p.open(rate=sample_rate,
                    format=pyaudio.paInt16,
                    channels=1, # Mono
                    output=True)

    stream.write(samples_int16.tobytes())

    # The close() blocks until the buffer is flushed by the sound card.
    stream.close()
    p.terminate()

def play_audio_open(s, sample_rate):
    # Scale to int16 for sound card
    max_int16 = 32768
    samples_int16 = (s * max_int16).astype(np.int16)

    # Opens a stream to sound card, device 0.
    p = pyaudio.PyAudio()

    stream = p.open(rate=sample_rate,
                    format=pyaudio.paInt16,
                    channels=1, # Mono
                    output=True)

    return (p, stream, samples_int16)

def play_audio_write(stream, samples_int16):
    stream.write(samples_int16.tobytes())

def play_audio_close(p,stream):
    # The close() blocks until the buffer is flushed by the sound card.
    stream.close()
    p.terminate()

def plot_chirp(t, s, start_freq, end_freq):
    plt.plot(t, s)

    plt.xlabel('time (s)')
    plt.ylabel('amplitude')
    plt.title('chirp  from ' + str(start_freq) + 'Hz  to ' + str(end_freq) + 'Hz' )
    plt.grid(True)
    #plt.savefig("test.png")
    plt.show()

if __name__ == "__main__":
    sample_rate = 44100

    start_freq = 500
    end_freq   = 5000 # 1000
    #end_freq  = 15000

    chirp_duration = 0.010
    chirp_duration = 1.00

    t, s, len_s = generate_chirp(sample_rate, chirp_duration, start_freq, end_freq)

    plot_chirp(t, s, start_freq, end_freq)
    play_audio(t, s, sample_rate)

    p, stream, samples_int16 = play_audio_open(s, sample_rate)
    num_times = 20
    for i in range(0, num_times):
        play_audio_write(stream, samples_int16)
    play_audio_close(p, stream)


