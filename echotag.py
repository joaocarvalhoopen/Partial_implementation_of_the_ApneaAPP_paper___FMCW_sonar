import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

from chirp_generator import generate_chirp

# t --- time
# s --- samples

def lixo_generate_chirp():
    sample_rate = 44100 # samples per second.
    start = 0.0
    stop = 1.0
    step = 1.0 / sample_rate
    t = np.arange(start, stop, step, dtype='float')
    s = np.ones(t.size)
    return t, s


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


def plot_spetrogram(x, fs):
    ''' x  - Array of the temporal series
        fs - Sample rate
    '''
    f, t, Sxx = signal.spectrogram(x, fs)
    plt.pcolormesh(t, f, Sxx)
    plt.ylabel('Frequency [Hz]')
    plt.xlabel('Time [sec]')
    plt.show()


if __name__ == "__main__":
    print("....begin")
    # t , s = lixo_generate_chirp()

    sample_rate    = 44100
    #chirp_duration = 0.010   # 10 miliseconds.
    chirp_duration = 1.0  # 10 miliseconds.
    start_freq     = 10000#500
    end_freq       = 20000#5000

    t, s, len_s = generate_chirp(sample_rate, chirp_duration, start_freq, end_freq)
    print("len_s: ", len_s)
    title = 'Sweep 500 to 1000 Hz'
    plot(t, s, title)


    delta_sig = 20000 #100

    sig_sum = np.zeros(len_s)
    sig_sum += s
    sig_sum[delta_sig : len_s] += s[0 : len_s - delta_sig]
    title = 'Two sweeps 500 to 1000 Hz displaced ' + str(delta_sig) + ' , summed'
    plot(t, sig_sum, title)

    #self.fftx, self.fft, ret_lenFFT = getFFT(self.data, self.rate)

    data = sig_sum
    fftx, fft, ret_lenFFT = getFFT(data, sample_rate)
    title = 'FFT dos 2 sinais'
    plot(fftx, fft, title)

    fs = 44100
    x = sig_sum
    plot_spetrogram(x, fs)

    # Apply a mixer, between the output signal and the input signal.
    sig_sum_2 = s * sig_sum


    x = sig_sum_2
    plot_spetrogram(x, fs)


    print("end....")

