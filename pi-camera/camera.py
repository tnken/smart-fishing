#!/usr/bin/env python3

import time

from datetime import datetime
from picamera2 import Picamera2, Preview
from picamera2.encoders import H264Encoder
from picamera2.outputs import FfmpegOutput

log_file = '/srv/pi-camera/camera_mode.log'
camera_output = '/srv/pi-camera'
loop_duration = 3
video_duration = 30

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

    def start_video(self):
        print('Start shooting video')
        now = datetime.now()
        try:
            video_config = self.picamera.create_video_configuration()
            self.picamera.configure(video_config)

            encoder = H264Encoder(10000000)
            file_name = camera_output + '/' + now.strftime("%Y%m%d%H%M%S") + '.mp4'
            output = FfmpegOutput(file_name)

            self.picamera.start_recording(encoder, output)
            time.sleep(video_duration)
            self.picamera.stop_recording()
        except:
            with open(log_file, mode='a') as f:
                f.write(self.mode_error + ':' + now.strftime("%Y%m%d%H%M%S") + ':' + 'Video error' + '\n')

    def start_camera(self):
        print('Start shooting camera')
        now = datetime.now()
        try:
            file_name = camera_output + '/' + now.strftime("%Y%m%d%H%M%S") + '.jpg'
            self.picamera.start()
            time.sleep(4)
            self.picamera.capture_file(file_name)
            print('shoot: ' + file_name)
        except:
            with open(log_file, mode='a') as f:
                f.write(self.mode_error + ':' + now.strftime("%Y%m%d%H%M%S") + ':' + 'Camera error' + '\n')

def main_loop():
    cam = PiCamera()
    while True:
        cam.check_mode()
        if cam.current_mode == cam.mode_picture:
            cam.start_camera()
        if cam.current_mode == cam.mode_video:
            cam.start_video()
        time.sleep(loop_duration)

if __name__ == '__main__':
    main_loop()
