# 🎓 Attendance Automator

A desktop application for automated student attendance using face recognition, built with Python and OpenCV.

## 📋 Project Overview

This system provides a professional solution for taking attendance by automatically recognizing students through face detection and recognition technology.

### ✨ Features
- **Real-time Face Detection & Recognition** - Identifies students using camera
- **Automatic Attendance Logging** - Records attendance with timestamps
- **Student Database Management** - Add, edit, and manage student profiles
- **Attendance Reports** - View history and export to Excel/PDF
- **User-Friendly Interface** - Professional desktop application

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Webcam
- Git (for version control)

### Installation
1. Clone the repository:
```bash
git clone https://github.com/KirubelSeifu/Attendance_Automator.git
cd Attendance_Automator

2. Create and activate virtual environment:
```bash
python -m venv attendance_env
# Windows:
attendance_env\Scripts\activate
# Mac/Linux:
source attendance_env/bin/activate
3. Install dependencies:
```bash
pip install -r requirements.txt
4. Run the application:
```bash
python attendance_system.py

📁 Project Structure
Attendance_Automator/
├── attendance_system.py    # Main application
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── LICENSE                # MIT License
├── .gitignore            # Git ignore rules
├── known_faces/          # Student face database
└── attendance_logs/      # Attendance records

📊 Version History
Version	Chapter	Features
v1.0.0	1	Basic face detection foundation
v1.1.0	2	Face recognition engine
v1.2.0	3	Professional GUI interface
v1.3.0	4	Student management system
v1.4.0	5	Attendance reporting
v1.5.0	6	Polish & optimization
🛠️ Development
This project follows chapter-based development:

Chapter 1: Camera access and basic face detection

Chapter 2: Face recognition and matching engine

Chapter 3: Professional user interface

Chapter 4: Student database management

Chapter 5: Reporting and export features

Chapter 6: Polish and optimization

📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

👤 Author
Kirubel Seifu

GitHub: @KirubelSeifu

Project Link: https://github.com/KirubelSeifu/Attendance_Automator
