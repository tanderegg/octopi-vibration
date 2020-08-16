# SOURCE: https://blog.endaq.com/matlab-vs-python-speed-for-vibration-analysis-free-download

import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from scipy.fftpack import fft
from datetime import datetime, timedelta

def convert_time(date):
    try:
        t = datetime.strptime(date.decode(), '%H:%M:%S.%f')
    except ValueError:
        t = datetime.strptime(date.decode(), '%H:%M:%S')
    except Exception as e:
        print(e)
    delta = timedelta(hours=t.hour, minutes=t.minute, seconds=t.second, microseconds=t.microsecond).total_seconds()
    return delta

def invert_z(z):
    return 1.0 - (float(z) * -1)

file_path = 'vibration_data_2020-08-15_214649.csv'
dataset = file_path.split('.')[0]

# Load Data (assumes two column array
ts, ax, ay, az, temp = np.genfromtxt(file_path,
                                     delimiter=',',
                                     skip_header=1,
                                     unpack=True,
                                     converters={0: convert_time,
                                                 3: invert_z})
target = ax

# Determine variables
N = np.int(np.prod(ts.shape)) # length of the array
Fs = 1/(ts[1]-ts[0])  # sample rate (Hz)
print(f'Fs:{Fs}')
T = 1/Fs;
print(f'T:{T}')
print("# Samples: ", N)

# Plot Data
plt.figure(1)  
plt.plot(ts, target) # Plot chosen g value
plt.ylim([-1.5, 1.5])
plt.xlabel('Time (seconds)')
plt.ylabel('Accel (g)')
plt.title(file_path)
plt.grid()
plt.savefig(f'{dataset}.png')

# Compute RMS and Plot
w = np.int(np.floor(Fs)); # width of the window for computing RMS
steps = np.int_(np.floor(N/w)); # Number of steps for RMS
ts_RMS = np.zeros((steps,1)); # Create array for RMS time values
target_RMS = np.zeros((steps,1)); # Create array for RMS values

for i in range (0, steps):
    ts_RMS[i] = np.mean(ts[(i*w):((i+1)*w)])
    target_RMS[i] = np.sqrt(np.mean(target[(i*w):((i+1)*w)]**2))

plt.figure(2)  
plt.plot(ts_RMS, target_RMS)
plt.ylim([0.0, 0.4])
plt.xlabel('Time (seconds)')
plt.ylabel('RMS Accel (g)')
plt.title('RMS - ' + file_path)
plt.grid()
plt.savefig(f'{dataset}-RMS.png')

# Compute and Plot FFT
plt.figure(3)  
xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
yf = fft(target)
plt.plot(xf, 2.0/N * np.abs(yf[0:np.int(N/2)]))
plt.ylim([0, 0.005])
plt.xlim([0, 100])
plt.grid()
plt.xlabel('Frequency (Hz)')
plt.ylabel('Accel (g)')
plt.title('FFT - ' + file_path)
plt.show()
plt.savefig(f'{dataset}-FFT.png')
