from PIL import Image
import cv2
from flask import Flask, render_template, Response
import cv2
app = Flask(__name__)

#@app.route('/')
#def index():
#    return render_template('index.html')

@app.route('/')
def hello_world():
    return 'olaaaa'

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def gen_frames():
    cap = cv2.VideoCapture(0)

    # Set the desired frame rate (frames per second)
    desired_fps = 15
    capture_fps = int(cap.get(cv2.CAP_PROP_FPS))  # Get the actual frame rate of the webcam
    frame_skip = max(1, int(capture_fps / desired_fps))  # Calculate the number of frames to skip

    frame_count = 0
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
        else:
            if frame_count % frame_skip == 0:
                    ret, buffer = cv2.imencode('.jpg', frame)
                    frame = buffer.tobytes()
                    yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
        frame_count += 1

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)