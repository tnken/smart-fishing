from datetime import datetime
from flask import Flask, jsonify, render_template

app = Flask(__name__)

camera_log_file = '/srv/pi-camera/camera_mode.log'
mode_waiting = 'WAIT'
mode_picture = 'Picture'
mode_video = 'Video'

#
# Client App to operate pi-camera
#

def write_camera_log(mode, comment):
    now = datetime.now()
    with open(camera_log_file, mode='a') as f:
        f.write(mode + ':' + now.strftime("%Y%m%d%H%M%S") + ':' + '\n')

def current_status():
    with open(camera_log_file) as f:
        status = f.readlines()[-1].split(':')[0]
        return status

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/status', methods=['GET'])
def status():
    status = current_status()
    return jsonify({'status': status})

@app.route('/start', methods=['GET'])
def start():
    write_camera_log(mode_picture, '')
    status = current_status()
    return jsonify({'status': status})

@app.route('/stop', methods=['GET'])
def stop():
    write_camera_log(mode_waiting, '')
    status = current_status()
    return jsonify({'status': status})

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0")
