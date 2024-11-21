import torch
from queue import Queue
import time
import warnings
import argparse
import os
import cv2
import numpy as np
import gi

gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

# Ignoring model related warning which should be fixed in next updates.
warnings.filterwarnings("ignore", category=FutureWarning)

# Frame queue
frame_queue = Queue(maxsize=10)

# Loading the object detection model.
model = torch.hub.load('./yolov5', 'custom', path='yolov5s.pt', source='local')

# Initialize GStreamer
Gst.init(None)

def parse_arguments():
    parser = argparse.ArgumentParser(description="Video processing application with GStreamer and YOLOv5.")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_video = os.path.join(script_dir, "demo_videos", "people_walking.mp4")
    parser.add_argument(
        "--source",
        type=str,
        default=default_video,
        help="Path to the video file or 0 for camera input."
    )
    return parser.parse_args()

args = parse_arguments()
input_source = args.source

# Callback function for appsink to process new frames.
def on_new_sample(sink):
    
    # Pulling a GStreamer object from the appsink which contains the current frame raw data and capabilities.
    sample = sink.emit("pull-sample")
    
    # Checking if there is data in the sample variable.
    if not sample:
        return Gst.FlowReturn.ERROR
    
    # Getting the frame raw data in bytes wrapped with GStreamer object.
    buf = sample.get_buffer()
    
    # Getting the frame capabilities (width, height).
    caps = sample.get_caps()
    width = caps.get_structure(0).get_value("width")
    height = caps.get_structure(0).get_value("height")
    
    # Extracts the bytes of the frame data from the buffer.
    data = buf.extract_dup(0, buf.get_size())
    """Converting the byte python object to numpy array.
    Each pixel will be represented as a 3d array of size height * width * 3(BGR format) of BGR values"""
    frame = np.frombuffer(data, dtype=np.uint8).reshape((height, width, 3))

    # Perform YOLOv5 inference on the raw frame
    results = model(frame)

    # Annotate the frame with detection results
    # Render returns a list, in our case we process only 1 frame but still as a list so the list contain 1 frame aswell, we access it using [0].
    annotated_frame = results.render()[0]

    # Push the annotated frame to the queue
    if not frame_queue.full():
        frame_queue.put(annotated_frame)

    return Gst.FlowReturn.OK

# Create GStreamer pipeline
"""Pipeline elements explaination:
   filesrc - Is the path of the source which the pipeline gets his input from, in our case it is an mp4 file.
   decodebin - An element which decoding the raw video file for processing.
   videoconvert - An element which makes sure the next element pad will understand the format of the video.
   video/x-raw,format=BGR - Specifying that the data stream consists of raw video frames, format=BGR specifies the format of the video frmaes.
   v4l2src device= - An element which specifies the input source which in our case is the defult camera on our device.
   appsink - An element which responsible to act as a bridge between the GStreamer pipeline and the python app to get the frame from the pipeline.
   """
if input_source == '0':
    pipeline = Gst.parse_launch(
        f"v4l2src device=/dev/video{input_source} ! videoconvert ! video/x-raw,format=BGR ! appsink name=sink"
    )
else:
    pipeline = Gst.parse_launch(
        f"filesrc location={input_source} ! decodebin ! videoconvert ! video/x-raw,format=BGR ! appsink name=sink"
    )

# Get and access the appsink element
# For each frame the callback function on_new_sample is called.
appsink = pipeline.get_by_name("sink")
appsink.set_property("emit-signals", True)
appsink.set_property("sync", False)
appsink.connect("new-sample", on_new_sample)

# Start the pipeline
state_change = pipeline.set_state(Gst.State.PLAYING)

# Main application loop for displaying frames
try:
    while True:
        if not frame_queue.empty():
            frame = frame_queue.get()
            frame = cv2.resize(frame, (800, 600))
            cv2.imshow("Frame", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            # We would like to avoid busy waiting by calling a small delay for not checking the frame queue aggressively.
            time.sleep(0.01)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    # Setting the pipeline state to NULL to free the resources it uses and making sure a good termination is executed.
    pipeline.set_state(Gst.State.NULL)
    cv2.destroyAllWindows()
