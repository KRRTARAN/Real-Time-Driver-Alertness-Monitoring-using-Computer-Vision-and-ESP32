🚗 Vision-Enhanced Driver Drowsiness Detection & Alert System using AI and ESP32

📌 Overview
This project presents an intelligent, real-time driver monitoring system designed to enhance road safety by detecting drowsiness and distraction. Leveraging computer vision and AI, the system continuously analyzes eye blink patterns and head movements, issuing immediate alerts through an ESP32-based buzzer and displaying driver status on an I2C LCD.

🎯 Key Features
* Real-time eye blink and drowsiness detection
* Head pose estimation (left, right, down tracking)
* Instant audio alerts via buzzer
* Live status display on ESP32-connected LCD
* Automatic user calibration for improved accuracy
* Low-cost and scalable ADAS prototype

⚙️ Execution Workflow

🔹Step 1: Camera Validation
Before running the main system, verify that the camera is functioning correctly by executing the camera testing script. This ensures that the webcam is properly initialized and provides a stable video feed without distortion or color issues.

🔹Step 2: ESP32 Configuration
Open the Arduino IDE and confirm that the ESP32 board is properly connected. Identify the correct communication port and ensure it matches the port used in the main project configuration. This step is critical for seamless serial communication between the AI system and the hardware module.

🔹Step 3: System Execution
Run the main driver monitoring application. At startup, the system performs an automatic calibration phase where the user is required to sit in a normal, straight position for a few seconds. This establishes a baseline for accurate head pose detection.

🔹Step 4: Real-Time Monitoring

Once initialized, the system continuously:
* Tracks eye movement to detect drowsiness
* Monitors head orientation to identify distraction
* Classifies driver state (Normal, Drowsy, Looking Left/Right/Down)

The detected status is transmitted to the ESP32, which:
* Displays the current state on the LCD
* Activates the buzzer during unsafe conditions

🔌 Hardware Integration

The system integrates AI-based vision processing with embedded hardware:
* ESP32 acts as the alert and display controller
* I2C LCD provides real-time driver status
* Buzzer ensures immediate warning feedback

🚀 Benefits
* Enhances driver safety through proactive alerting
* Provides a cost-effective alternative to high-end ADAS systems
* Demonstrates practical integration of AI with embedded systems
* Suitable for real-world deployment and research applications
* Highly customizable and scalable for future enhancements

🌟 Applications
* Driver Monitoring Systems (DMS)
* Automotive safety solutions
* Smart transportation systems
* Fleet and logistics monitoring

🔮 Future Scope
* Integration with mobile applications for remote alerts
* Yawning detection for enhanced fatigue analysis
* Vehicle control mechanisms for automatic intervention
* Night vision and thermal imaging support

👨‍💻 Conclusion
This project showcases a powerful combination of artificial intelligence and embedded systems to address a critical real-world problem. It serves as a strong foundation for developing advanced driver assistance systems with practical impact.



⭐ If you find this project useful, consider supporting it by starring the repository!

