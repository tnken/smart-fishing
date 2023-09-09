import time

log_file = '/srv/pi-camera/camera_mode.log'
time_duration = 3

#
# This script is for controlling the Raspi-camera in the backgroud
#

class PiCamera:
    mode_waiting = 'WAIT'
    mode_picture = 'PICTURE'
    mode_video = 'VIDEO'

    def __init__(self):
        self.check_mode()

    def check_mode(self):
        with open(log_file) as f:
            l = f.readlines()[-1]
            self.current_mode = l.split(':')[0]

    def start_camera(self):
        print('camera_mode')

def main_loop():
    cam = PiCamera()
    while True:
        cam.check_mode()
        if cam.current_mode == cam.mode_picture:
            cam.start_camera()
        time.sleep(time_duration)

if __name__ == '__main__':
    main_loop()
