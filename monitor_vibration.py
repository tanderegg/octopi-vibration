import csv
import time

from datetime import datetime
from mpu6050_i2c import *

if __name__ == '__main__':

    timestamp = datetime.now()
    print('Beginning monitoring at {}'.format(timestamp))
    filename = 'vibration_data_{}.csv'.format(datetime.strftime(timestamp, '%Y-%m-%d_%H%M%S'))

    sampling_rate = 50
    frame_length = time.delta(seconds=1.0) / sampling_rate

    with open(filename, 'w') as outfile:
        outfile_writer = csv.writer(outfile,
                                    delimiter=',',
                                    quotechar='"',
                                    quoting=csv.QUOTE_MINIMAL)
        outfile_writer.writerow(['timestamp', 'ax', 'ay', 'az'])
        
        start_time = datetime.now()
        last_time = start_time
        while 1:
            sample_time = datetime.now()
            total_elapsed_time = sample_time - start_time
            try:
                ax,ay,az,wx,wy,wz,temp = mpu6050_conv() # read and convert mpu6050 data
            except Exception as e:
                print('Exception encountered, ignoring: {}'.format(e))
                continue

            print('accel [g]: x = {}, y = {}, z = {}'.format(ax,ay,az))
            outfile_writer.writerow([total_elapsed_time, ax, ay, az, temp])

            while 1:
                sample_elapsed_time = (datetime.now() - sample_time)
                if sample_elapsed_time >= frame_length:
                    break


