# Python Computer Vision Demos

A collection of computer vision demonstrations designed for various Raspberry Pi models, showcasing real-time object detection, color tracking, and human detection capabilities.

## Overview

This repository contains optimized computer vision applications for different Raspberry Pi hardware configurations, from the Pi 3B running Buster to the latest Pi 5 with Bullseye OS. Each implementation is tailored to leverage the specific capabilities of its target hardware.

## Features

- **Color Detection**: Real-time HSV color space tracking (blue, green, white)
- **Human Detection**: HOG (Histogram of Oriented Gradients) descriptor-based person detection
- **Hand Detection**: MediaPipe-powered hand landmark detection and tracking
- **Robot Control**: Tank-driven robot with computer vision integration

## Project Structure

```
├── Raspberry pi model 3b Buster/
│   ├── color_detection_pi3_buster.py          # HSV color detection
│   ├── human_detection_pi3_buster_hog_descriptor.py  # HOG human detection
│   └── TDCB/                                   # Tank Driven Computer Vision Bot
│       ├── README.md
│       └── robot_script.py                    # Robot control with CV
├── Raspberry pi model 4b Bullseye/
│   └── hand_detection_pi4_bullseye.py         # MediaPipe hand detection
└── Raspberry pi model 5 Bullseye/
    ├── hand_detection_pi5_bullseye.py         # Optimized hand detection
    ├── hand_detection_pi5_bullseye_v2.py      # Enhanced version
    └── human_detection_pi5_bullseye_hog_descriptor.py  # High-res human detection
```

## Hardware Requirements

### Raspberry Pi 3B (Buster)
- Raspberry Pi 3B
- Pi Camera (legacy)
- Optional: L298N motor controller + DC motors for TDCB project

### Raspberry Pi 4B (Bullseye)
- Raspberry Pi 4B
- Pi Camera Module v2/v3
- Adequate power supply (3A+)

### Raspberry Pi 5 (Bullseye)
- Raspberry Pi 5
- Pi Camera Module v3 (recommended)
- High-quality power supply (5A)

## Software Dependencies

### For Pi 3B (Buster)
```bash
sudo apt update
sudo apt install python3-picamera python3-opencv python3-numpy
```

### For Pi 4B/5 (Bullseye)
```bash
# Create virtual environment
python3 -m venv --system-site-packages cv_env
source cv_env/bin/activate

# Install dependencies
pip install picamera2 opencv-python numpy mediapipe
```

## Applications

### 1. Color Detection (`color_detection_pi3_buster.py`)
- **Platform**: Raspberry Pi 3B + Buster
- **Features**: Real-time HSV color tracking
- **Supported Colors**: Blue, Green, White
- **Resolution**: 640x480 @ 10fps

### 2. Human Detection (HOG)
- **Platforms**: Pi 3B, Pi 5
- **Algorithm**: HOG + SVM classifier
- **Features**: Bounding box detection, direction indicators
- **Performance**: Optimized for each platform's capabilities

### 3. Hand Detection (MediaPipe)
- **Platforms**: Pi 4B, Pi 5
- **Features**: 21-point hand landmark detection
- **Capabilities**: Gesture recognition, hand tracking
- **Optimization**: Resolution scaling for performance

### 4. Tank Driven Computer Vision Bot (TDCB)
- **Platform**: Raspberry Pi 3B
- **Features**: 
  - Dual motor control
  - Computer vision integration
  - GPIO-based motor driver interface
- **Hardware**: L298N motor controller required

## Getting Started

### Quick Start - Pi 3B
```bash
cd "Raspberry pi model 3b Buster"
python3 color_detection_pi3_buster.py
```

### Quick Start - Pi 4B/5
```bash
# Set up virtual environment
python3 -m venv --system-site-packages cv_env
source cv_env/bin/activate
pip install picamera2 opencv-python mediapipe

# Run hand detection
cd "Raspberry pi model 4b Bullseye"  # or Pi 5 directory
python3 hand_detection_pi4_bullseye.py
```

## Performance Notes

- **Pi 3B**: Limited to 640x480 resolution for real-time performance
- **Pi 4B**: Optimized resolution settings for balanced performance/quality
- **Pi 5**: Takes advantage of higher resolution (2304x1296) with intelligent downsampling

## Configuration

### Camera Settings
Each script includes camera configuration options:
- Resolution adjustment
- Frame rate optimization  
- Rotation settings
- Format specifications

### Detection Parameters
- HSV color thresholds (color detection)
- HOG detection confidence levels
- MediaPipe model complexity settings

## Contributing

Contributions are welcome! Please consider:
- Performance optimizations for different Pi models
- Additional detection algorithms
- New computer vision applications
- Documentation improvements

## License

This project is open source. Please check individual files for specific licensing information.

## Troubleshooting

### Common Issues
- **Camera not detected**: Ensure camera is enabled in `raspi-config`
- **Import errors**: Verify virtual environment activation and package installation
- **Performance issues**: Adjust resolution and frame rate settings
- **GPIO warnings**: Normal for robot control scripts

### Performance Tips
- Use appropriate resolution for your Pi model
- Enable GPU memory split for better camera performance
- Consider overclocking for demanding applications (with adequate cooling)

## Tested Configurations

| Pi Model | OS Version | Camera | Performance |
|----------|------------|---------|-------------|
| Pi 3B | Buster | v1/v2 | Stable @ 640x480 |
| Pi 4B | Bullseye | v2/v3 | Good @ 820x616 |
| Pi 5 | Bullseye | v3 | Excellent @ 2304x1296 |

---

**Note**: This repository demonstrates platform-specific optimizations for Raspberry Pi computer vision applications. Each implementation is tailored to maximize performance on its target hardware configuration.