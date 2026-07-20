def to_binary(data:str, delimiter:str):
    data_list = data.split(delimiter)
    data_bin = []
    for n in data_list:
        data_bin.append(format(ord(n)))
    return data_bin
    
def to_binary(data:str):
    data_list = list(data)
    data_bin = []
    for n in data_list:
        data_bin.append(format(ord(n)))
    return data_bin

def encode(M:int, shift_vals:list, base_af:int=1800):

