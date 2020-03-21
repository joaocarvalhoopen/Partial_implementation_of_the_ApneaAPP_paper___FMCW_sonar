# Objective: Analyse a input microphone file from a FMCW chirp signal in the feq.
#            range from 3KHz to 10Kz with a 10 millisecond duration, repeated 1000 times.


import numpy as np
import scipy.io.wavfile
import matplotlib
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import correlate

from chirp_generator import generate_chirp

import matplotlib.animation as animation


#sample_rate = 44100

def read_wav_file(filename):
    # Reads the input WAV file from HDD disc.
    sample_rate, input_buffer = scipy.io.wavfile.read(filename)
    print("sample_rate: " + str(sample_rate))
    print("input_buffer.size: " + str(input_buffer.size) )
    print("seconds: " + str(input_buffer.size/sample_rate) + " s")
    print("type: " + str(input_buffer.dtype) )
    return sample_rate, input_buffer

def getFFT(data, rate):
    # returns FFTfreq and FFT, half.

    # print("len(data): " + str(len(data)) + " --- " + " rate: " + str(rate) )
    len_data = len(data)
    data = data * np.hamming(len_data)
    fft = np.fft.rfft(data)
    fft = np.abs(fft)

    ret_len_FFT = len(fft)

    freq = np.fft.rfftfreq(len_data, 1.0 / rate)
    return ( freq[:int(len(freq) / 2)], fft[:int(ret_len_FFT / 2)], ret_len_FFT )

def plot(t, s, title):
    # Draws the plot.
    fig, ax = plt.subplots()
    #fig = plt.figure()
    #ax = fig.add_subplot(111)
    ax.plot(t, s)

    ax.set(xlabel='time (s)', ylabel='amplitude', title=title)
    ax.grid()

    #fig.savefig("test.png")
    plt.show()

def plot_spetrogram(x, fs):
    ''' x  - Array of the temporal series
        fs - Sample rate
    '''
    f, t, Sxx = signal.spectrogram(x, fs)
    plt.pcolormesh(t, f, Sxx)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.show()

def butter_highpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

def butter_highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = signal.filtfilt(b, a, data)
    return y

def process_buffer_with_10_chirps(sub_input_buffer, chirp_repeat_10):

    # First approach.
    #sub_input_buffer = input_buffer[0 : chirp_len * 10]

    #chirp_repeat_10 = np.repeat(chirp_buffer, 10)


    #t_4 = np.arange(0, len(sub_input_buffer))
    #title = "Plot 10 first chirps"
    #plot(t_4, sub_input_buffer, title)


    ## Plot spetrogram.
    #x = sub_input_buffer
    #plot_spetrogram(x, sample_rate)

    #data = sub_input_buffer
    #fftx, fft, ret_lenFFT = getFFT(data, sample_rate)
    #title = 'FFT micro input_buffer_0 before remove static echoes'
    #plot(fftx, fft, title)



    # Remove the fixed location echoes.
    sub_input_buffer  = sub_input_buffer - input_buffer_accumulator

    #data = sub_input_buffer
    #fftx, fft, ret_lenFFT = getFFT(data, sample_rate)
    #title = 'FFT micro input_buffer_0 before mixer'
    #plot(fftx, fft, title)

    ## Plot spectrogram.
    #x = sub_input_buffer
    #plot_spetrogram(x, sample_rate)


    # RF Mixer
    sub_input_buffer =  sub_input_buffer * chirp_repeat_10

    data = sub_input_buffer
    fftx, fft, ret_lenFFT = getFFT(data, sample_rate)
    title = 'FFT micro input_buffer_0 after mixer'
    #plot(fftx, fft, title)

    return (fftx, fft, title)

    ## Plot spetrogram.
    #x = sub_input_buffer
    #plot_spetrogram(x, sample_rate)



# def plot(t, s, title):
#     # Draws the plot.
#     fig, ax = plt.subplots()
#     #fig = plt.figure()
#     #ax = fig.add_subplot(111)
#     ax.plot(t, s)
#
#     ax.set(xlabel='time (s)', ylabel='amplitude', title=title)
#     ax.grid()
#
#     #fig.savefig("test.png")
#     plt.show()

def init():  # only required for initting to give a clean slate.
    print("...init")

    sub_input_buffer = input_buffer[0 * chirp_10_len: (0 + 1) * chirp_10_len]
    fftx, fft, title = process_buffer_with_10_chirps(sub_input_buffer.copy(), chirp_repeat_10)

    line.set_data(fftx, fft)
    return line,

movement_buffer = np.zeros(184, dtype=np.float32 )

def animate(i):
    print("...animate" + str(i))
    if i < 184:
        sub_input_buffer = input_buffer[i * chirp_10_len: (i + 1) * chirp_10_len]
        fftx, fft, title = process_buffer_with_10_chirps(sub_input_buffer.copy(), chirp_repeat_10)

        # Finds the max_bucket of the FFT.
        movement_buffer[i] = ( fft[150: ].argmax() ) + 150

        line.set_data(fftx, fft)  # update the data.
    return line,

if __name__ == "__main__":
    # Reads the input WAV file from HDD disc.
    filename = 'input_v001___copy.wav'
    sample_rate, input_buffer = read_wav_file(filename)

    # Apply a ButterWorth filter of 2500 Hz.
    filter_order = 5
    cut_off_freq = 2500 # Hz
    filtered_signal = butter_highpass_filter(input_buffer, cut_off_freq, sample_rate, filter_order)
    input_buffer = filtered_signal

    # Plot spetrogram.
    x = input_buffer
    fs = sample_rate
    plot_spetrogram(x, fs)


    data = input_buffer
    fftx, fft, ret_lenFFT = getFFT(data, sample_rate)
    title = 'FFT from microphone'
    plot(fftx, fft, title)

    # Filter out the DC component of the 10 first bins.
    #fft[0:1000] = 0.0
    #fft[0:2000] = 0.0
    #fft[0:10000] = 0.0
    #fft[0:20000] = 0.0
    title = 'FFT from microphone'
    plot(fftx, fft, title)

    # Regenerate the initial chirp that was pushed out to the speakers.
    chirp_duration = 0.010  # 10 milliseconds.  # Note: 1 meter distance.
    start_freq = 3000  # Hz
    end_freq   = 10000  # Hz
    t, chirp_buffer, len_chirp = generate_chirp(sample_rate, chirp_duration, start_freq, end_freq)

    # Find the begining of the buffer, using a cross_correlation.
    # NOTE: We now that the beggining of the chirp is in the first 100.000 samples,
    #       it's hear that we will find our maximum index.
    cross_correlation = correlate(input_buffer[0 : 100000], chirp_buffer)
    max_correctation_index = cross_correlation.argmax()

    print( "max_correctation: " + str(max_correctation_index) )

    t_2 = np.arange(0, len(cross_correlation))
    title = "Plot cross_correlation"
    plot(t_2, cross_correlation, title)

    t_3 = np.arange(0, len(input_buffer))
    title = "Plot cross_correlation"
    plot(t_3, input_buffer, title)

    # We are going to synchronize the beginning of the buffer with received direct path
    # sound from the speaker to the microphone, the echoes will come later on.
    input_buffer = input_buffer[max_correctation_index : ]

    # Devide the input_buffer into segments of 10 chirps, 100 milliseconds (10 each).
    chirp_len = chirp_buffer.size
    #chirp_10_len = chirp_len * 10
    chirp_10_len = chirp_len * 5
    num_segments = int(input_buffer.size // chirp_10_len)
    print("num_segments: " + str(num_segments) )

    #chirp_repeat_10 = np.repeat(chirp_buffer, 10)
    chirp_repeat_10 = np.repeat(chirp_buffer, 5)


    # Determine the mean value for the buffer with 10 chirps.
    input_buffer_accumulator = np.zeros(chirp_10_len, dtype=np.float32 )
    for i in range(0, num_segments):
        # Process each segment
        #print("i: " + str(i))
        sub_array = input_buffer[i * chirp_10_len : (i + 1) * chirp_10_len ]
        #print("sub_array.size: " + str( sub_array.size ))
        input_buffer_accumulator += sub_array
        # input_buffer_accumulator += input_buffer[i * input_buffer_0.size : (i + 1) * input_buffer_0.size ]

    input_buffer_accumulator = input_buffer_accumulator / num_segments


    #for i in range(0, num_segments):
    #    # Process each segment
    #    sub_input_buffer = input_buffer[ i * chirp_10_len : (i + 1) * chirp_10_len]
    #    process_buffer_with_10_chirps(sub_input_buffer.copy(), chirp_repeat_10)

    fig, ax = plt.subplots()

    sub_input_buffer = input_buffer[0 :  chirp_10_len]
    fftx, fft, title = process_buffer_with_10_chirps(sub_input_buffer.copy(), chirp_repeat_10)

    line, = ax.plot(fftx, fft)

    ax.set_ylim(0, 0.06)
    #ax.set_xlim(0, 10)


    ani = animation.FuncAnimation(fig, animate, init_func=init, interval=500,
                                  blit=False, repeat=False,
                                  save_count=10)

    plt.show()


    t = np.arange(0, len(movement_buffer) )
    title = "movement graph"
    plot(t, movement_buffer, title)

