#!/usr/bin/env python
import wave, math, array
SAMPFREQ = 96000
LENGTH = 3

def wave_init(fname, sampf):
    f = wave.open(fname, 'w')
    f.setnchannels(2)
    f.setsampwidth(3)
    f.setframerate(sampf)
    f.setcomptype('NONE', 'not compressed')
    return f
    
def prepare_array(n):
    data = array.array('h')
    data.extend([0]*n)
    return data
    
def wave_write(f, data):
    f.writeframesraw(data.tostring())
    f.close()
    
def sin_wave(fname, freq):
    f = wave_init(fname, SAMPFREQ)
    data = prepare_array(SAMPFREQ * LENGTH)
    a = math.pi * 2.0 * float(freq) / float(SAMPFREQ)
    for i in range(SAMPFREQ * LENGTH):
        ft  = int(math.sin(a * float(i)) * 30000.0)
    
    data[i] = ft
    wave_write(f, data)
    
if __name__ == "__main__":
    sin_wave('sinwave1.wav', 1800)