import csv

from datetime import datetime
from mpu6050_i2c import *

if __name__ == '__main__':

    timestamp = datetime.now()
    print('Beginning monitoring at {}'.format(timestamp))
    filename = 'vibration_data_{}.csv'.format(datetime.strftime(timestamp, '%Y-%m-%d_%H%M%S'))

    with open(filename, 'w') as outfile:
        outfile_writer = csv.writer(outfile,
                                    delimiter=',',
                                    quotechar='"',
                                    quoting=csv.QUOTE_MINIMAL)
        outfile_writer.writerow(['timestamp', 'ax', 'ay', 'az'])
        
        start_time = datetime.now()
        while 1:
            current_time = datetime.now()
            try:
                ax,ay,az,wx,wy,wz,temp = mpu6050_conv() # read and convert mpu6050 data
            except Exception as e:
                print('Exception encountered, ignoring: {}'.format(e))
                continue
            elapsed_time = current_time - start_time

            print('accel [g]: x = {}, y = {}, z = {}'.format(ax,ay,az))
            outfile_writer.writerow([elapsed_time, ax, ay, az, temp])
            time.sleep(0.01)


