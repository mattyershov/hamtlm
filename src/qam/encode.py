def ascii_to_bin(data:string):
    data_list = data.split()
    data_bin = []
    

def qam16_format(data_str: str):
    # Ensure that data is a string of bits
    chunks = [data_str[i:i+4] for i in range(0, len(data_str), 4)]
    
    preamble_iq_vals = [+1, +1, +1, -1, -1, -1, +1, -1, -1, +1, -1]

    mapping = {
        '00': -3,
        '01': -1,
        '11': 1,
        '10': 3
    }
    
    iq_values = []
    for chunk in chunks:
        if len(chunk) < 4: continue # Handle trailing bits
        I = mapping[chunk[0:2]]
        Q = mapping[chunk[2:4]]
        iq_values.append((I, Q))

    return np.concatenate(iq_values, preamble_iq_vals)

def encode(iq_values: list, carr_af: int = 1800, rate: int = 44100, duration: float = 0.05):
    full_wave = []
    num_samples = int(rate * duration)
    
    # creates a linspace array so that the concatenation takes place along one axis to avoid clicks
    total_samples = num_samples * len(iq_values)
    t_full = np.linspace(0, total_samples / rate, total_samples, endpoint=False)
    
    for idx, (I, Q) in enumerate(iq_values):
        # Slice the time for this specific symbol
        t = t_full[idx * num_samples : (idx + 1) * num_samples]
        
        iq_wave = I * np.cos(2 * np.pi * carr_af * t) - Q * np.sin(2 * np.pi * carr_af * t)
        full_wave.append(iq_wave)

    cont_wave = np.concatenate(full_wave).astype(np.float32)
    
    # Normalize to prevent audio clipping (-1 to 1 range)
    cont_wave = cont_wave / np.max(np.abs(cont_wave))
    
    scipy.io.wavfile.write("outputs/qam.wav", rate, cont_wave)

def main():
    data = ""