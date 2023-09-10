import time

from datetime import datetime
from picamera2 import Picamera2, Preview

log_file = '/srv/pi-camera/camera_mode.log'
camera_output = '/srv/pi-camera'
loop_duration = 3

#
# This script is for controlling the Raspi-camera in the backgroud
#

class PiCamera:
    mode_waiting = 'WAIT'
    mode_picture = 'PICTURE'
    mode_video = 'VIDEO'
    mode_error = 'ERROR'

    def __init__(self):
        self.check_mode()
        self.picamera = Picamera2()

    def check_mode(self):
        with open(log_file) as f:
            l = f.readlines()[-1]
            self.current_mode = l.split(':')[0]

    def start_camera(self):
        print('Start shooting')
        now = datetime.now()
        # try:
        # config = self.picamera.create_still_configuration()
        file_name = camera_output + '/' + now.strftime("%Y%m%d%H%M%S") + '.jpg'
        # self.picamera.configure(config)
        self.picamera.start()
        time.sleep(5)
        self.picamera.capture_file(file_name)
        print('shoot: ' + file_name)
        # except as e:
        #     print()
        #     with open(log_file, mode='a') as f:
        #         f.write(self.mode_error + ':' + now.strftime("%Y%m%d%H%M%S") + ':' + 'Camera error' + '\n')

def main_loop():
    cam = PiCamera()
    while True:
        cam.check_mode()
        if cam.current_mode == cam.mode_picture:
            cam.start_camera()
        time.sleep(loop_duration)

if __name__ == '__main__':
    main_loop()
