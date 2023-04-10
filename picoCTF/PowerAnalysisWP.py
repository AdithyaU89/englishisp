from netcat import NC
import scared
import time
import numpy as np
from tqdm.notebook import tqdm
from estraces import read_ths_from_ram
port = 51011
nc = NC('saturn.picoctf.net', port, timeout=1, debug=True)
nc.receive()
def encrypt_and_leak(plaintext):
    plaintext = plaintext.tobytes().hex()
    
    nc = NC('saturn.picoctf.net', port, timeout=1, debug=False)
    nc.receive()
    time.sleep(0.005)
    resp = nc.query(plaintext, sleep=0.005)    
    
    return int(resp.strip().split(': ')[1].strip())
  plaintexts = []
leaks = []
for _ in tqdm(range(500)):
    plaintext = np.random.randint(0, 256, 16, dtype='uint8')
    plaintexts.append(plaintext)
    leak = encrypt_and_leak(plaintext)
    leaks.append([leak, leak])  # A trace must have at least two samples to be processed by our side-channel framework
ths = read_ths_from_ram(samples=np.array(leaks), plaintext=np.array(plaintexts))
ths
attack = scared.CPAAttack(selection_function=scared.aes.selection_functions.encrypt.FirstSubBytes(), 
                          model=scared.Monobit(0), 
                          discriminant=scared.nanmax,  # Positive correlation expected
                          convergence_step=50)
attack.run(scared.Container(ths))
found_key = np.nanargmax(attack.scores, axis=0).astype('uint8')
print(f'picoCTF{{{found_key.tobytes().hex()}}}')
