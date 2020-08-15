import csv

from datetime import datetime
from mpu6050_i2c import *

if __name__ == '__main__':

    timestamp = datetime.now()
    print('Beginning monitoring at {}'.format(timestamp))
    filename = 'vibration_data+{}.csv'.format(datetime.strftime(timestamp, '%Y-%m-%d_%H%M%S'))

    with open(filename, 'w') as outfile:
        outfile_writer = csv.writer(outfile,
                                    delimiter=',',
                                    quotechar='"',
                                    quoting=csv.QUOTE_MINIMAL)
        outfile_writer.writerow(['timestamp', 'ax', 'ay', 'az'])
        
        while 1:
            try:
                ax,ay,az,wx,wy,wz = mpu6050_conv() # read and convert mpu6050 data
            except Exception as e:
                print('Exception encountered, ignoring: {}'.format(e))
                continue

            print('accel [g]: x = {}, y = {}, z = {}'.format(ax,ay,az))
            outfile_writer.writerow([datetime.now(), ax, ay, az])
            time.sleep(0.01)


