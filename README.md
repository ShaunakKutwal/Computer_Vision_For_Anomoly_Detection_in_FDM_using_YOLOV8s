3D Print Anomaly Detection Pipeline
This project implements an automated quality control pipeline for FDM (Fused Deposition Modeling) 3D printing. It leverages the YOLOv8s computer vision model to detect and classify common printing anomalies in real-time and alerts the user via email.

Project Overview
The pipeline was developed to enhance the reliability of 3D printing workflows by identifying defects as they occur. By using a lightweight and efficient model, this system provides near real-time feedback, helping to reduce material waste and print failures.

Key Features
Automated Detection: Real-time identification of specific FDM print anomalies using YOLOv8s.

Anomaly Classification: The system is trained to detect:

Cracking

Off-platform prints

Stringing

Automated Notification System: The project includes an automated alert mechanism:

Email Alerts: Using the src/notifier.py module, the system automatically sends an email notification to the user the moment an anomaly is detected on the live camera feed.

Real-time Monitoring: The system continuously monitors the printing process, triggering the notification workflow only when a defect is confirmed.

Analytics: Integrated tools for log analysis and performance evaluation of the trained models.

Repository Structure
analytics/: Scripts for evaluating model performance and processing logs.

data_prep/: Pre-processing scripts for image cleaning, labeling, and dataset splitting.

src/: Core source code for training, prediction, and notification systems.

run_camera.py: Main entry point for running the anomaly detection on live camera feeds.

data.yaml: Configuration file defining the dataset classes and paths.

Tech Stack
Core Model: YOLOv8s (Ultralytics)

Language: Python

Workflow: Custom data collection, annotation, and automated training pipeline.

Getting Started
1. Prerequisites
Clone the repository:

Bash
git clone https://github.com/ShaunakKutwal/Computer_Vision_For_Anomoly_Detection_in_FDM_using_YOLOV8s.git
Install dependencies:

Bash
pip install -r requirements.txt
2. Configuration
To use the email notification system, you must configure your credentials locally:

Create a file named .env in your project root (this file is ignored by Git for your security).

Add your SMTP email credentials inside the .env file (e.g., EMAIL_USER=your_email@example.com and EMAIL_PASS=your_app_password).

Ensure your src/notifier.py is configured to load these variables using a library like python-dotenv.
3. Execution
Run the detection pipeline:

Bash
python run_camera.py
Future Scope
Integration with MQTT for remote, low-latency status updates.

Expanding the dataset to include more complex printing materials.

Deploying to edge computing devices (e.g., Raspberry Pi or Jetson Nano) for a standalone print-monitor unit.
