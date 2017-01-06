import pyaudio
import numpy as np

p = pyaudio.PyAudio()

s = p.open(rate=44100, channels=2, format=p.get_format_from_width(2), output=True)

s.write(np.random.uniform(size=10000))
print(1)
s.write(np.random.uniform(size=160000))
print(2)
s.write(np.random.uniform(size=10000))
print(3)

p.terminate()
