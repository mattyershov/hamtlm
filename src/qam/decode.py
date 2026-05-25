import numpy as np
from scipy.io import wavfile
from scipy import signal
import matplotlib.pyplot as plt

def wav_to_array(data, sample_rate=44100, carr_freq=1800):
    if data.dtype == np.int16:
        data = data.astype(np.float32) / 32768.0
    elif data.ndim > 1:
        data = data[:, 0]

    # Downconverter isolates baseband data from carrier
    t = np.arange(len(data)) / sample_rate
    downconverted = data * np.exp(-1j * 2 * np.pi * carr_freq * t)

    # LPF to remove 600 Hz sum frequency from downconversion
    window_size = int(sample_rate / carr_freq) * 2
    kernel = np.ones(window_size) / window_size
    complex_signal = np.convolve(downconverted, kernel, mode='same')

    return complex_signal

def phase_correction(sig, sample_rate=44100):
    # Generate the same preamble as on the TX side locally to compare phase offset

    return sig_corrected

def extract_points(rx_sig_array, sample_rate=44100, alphabet_size=16):
    n = int(np.sqrt(alphabet_size))

    points = np.arange(-(n-1), n, 2)

    normalized_real = (rx_sig_array.real + (n - 1)) / 2
    normalized_imag = (rx_sig_array.imag + (n - 1)) / 2

    real_idx = np.clip(np.round(normalized_real), 0, n - 1).astype(int)
    imag_idx = np.clip(np.round(normalized_imag), 0, n - 1).astype(int)

    return points[real_idx] + points[imag_idx] * 1j

def decode(signal, sampled_sample_rate):
    sps = int(sampled_sample_rate * 0.05)
    payload_start_idx = peak_idx + len(local_preamble_sig)
    rx_payload_symbols = continuous_sig_corrected[payload_start_idx :: sps]

    # scale the received array up to the expected amplitude
    max_expected_amp = np.sqrt((np.sqrt(16)-1)**2 + (np.sqrt(16)-1)**2) # 4.2426n
    current_max_amp = np.max(np.abs(rx_payload_symbols))

    if current_max_amp > 0:
        rx_payload_symbols *= (max_expected_amp / current_max_amp)

    # remove DC bias
    rx_payload_symbols -= np.mean(rx_payload_symbols)
    return rx_payload_symbols

def main():
    sampled_sample_rate, data = wavfile.read("outputs/qam.wav")
    continuous_sig = wav_to_array(data, sampled_sample_rate)
    rx_symbols = process_symbols(continuous_sig, sampled_sample_rate)

    print(rx_symbols)
    print(i for i in decode(continuous_sig))

    plt.figure(figsize=(6,6))
    plt.scatter(rx_symbols.real, rx_symbols.imag, color='blue', zorder=2)
    plt.axhline(0, color='red', lw=1, zorder=1)
    plt.axvline(0, color='red', lw=1, zorder=1)
    plt.title("Decoded Constellation (Center Samples)")
    plt.grid(True)
    plt.xlim(-5, 5); plt.ylim(-5, 5)
    plt.show()

if __name__ == "__main__":
    main()