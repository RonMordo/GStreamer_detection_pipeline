# GStreamer Detection Pipeline

## Overview
This project is a real-time video processing application that utilizes **GStreamer** for multimedia processing and a **YOLOv5** object detection model for analyzing video frames. It is designed to be versatile, handling both pre-recorded video files and live camera feeds with ease.

The application is lightweight, modular, and extensible, making it suitable for a wide range of object detection tasks in real-time environments.

## Demo

Below is a demonstration of the application in action:

![Application Demo](assets/demo.gif)


---

## Technologies Used
### **1. GStreamer**
- A powerful multimedia framework for processing and handling video and audio streams.
- Used in this project for creating a video pipeline to handle video input, decoding, and conversion for further processing.

### **2. YOLOv5**
- A state-of-the-art object detection model capable of identifying multiple object classes in real-time.
- Provides highly accurate and fast predictions on video frames.

### **3. PyTorch**
- A deep learning framework used to run the YOLOv5 model.
- Provides the flexibility to integrate the pre-trained model seamlessly into the application.

### **4. OpenCV**
- A computer vision library used to handle and display video frames.
- Allows resizing, rendering, and visualizing the processed frames with annotations.

### **5. PyGObject**
- A Python binding for GObject-based libraries, enabling interaction with GStreamer pipelines.
- Used to manage the GStreamer multimedia pipeline and handle video frame processing.

---

This combination of technologies provides a robust, efficient, and scalable solution for object detection in multimedia streams.

---

## Installation

### Setup
Run the following commands to set up the project:

Clone the repository
```bash
git clone git@github.com:RonMordo/GStreamer_detection_pipeline.git
```
Change directory to the cloned repo
```bash
cd GStreamer_detection_pipeline
```
Run the setup script in sudo mode
```bash
sudo ./setup.sh
```

---

## Usage

Make sure to source the venv in every new terminal session before running the app
```bash
source venv/bin/activate
```
To run the app with the demo media file
```bash
python3 detection_app.py
```
To exit you can press q or ^C

### Run with different input source  

To run using your pc webcam
```bash
python3 detection_app.py --source 0
```
To run using a local media file
```bash
python3 detection_app.py --source path_to_your_media_file
```
