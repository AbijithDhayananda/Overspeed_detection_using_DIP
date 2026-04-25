# 🚗 Car Speed Detection & Overspeed Monitoring System

## 📌 Overview

This project implements a **real-time car speed detection system** using computer vision techniques. It detects moving vehicles in a video, tracks them across frames, estimates their speed, and identifies overspeed violations.

The system also logs violations and captures snapshots of vehicles exceeding the speed limit, making it suitable for **traffic monitoring and smart surveillance applications**.

---

## 🎯 Features

* 🚗 Detect moving vehicles using image processing
* 📦 Track vehicles across frames
* 📊 Estimate speed in **km/h**
* 🔴 Highlight overspeed vehicles (> 80 km/h)
* ⚠️ Display real-time warning ("OVER SPEED")
* 📸 Capture snapshots of violating vehicles
* 📄 Log violations (ID, speed, timestamp)
* 🎬 Save processed output video

---

## 🧠 How It Works

1. **Video Input**

   * A traffic video is processed frame-by-frame.

2. **Motion Detection**

   * Uses background subtraction to detect moving objects.

3. **Object Tracking**

   * Tracks vehicles using centroid-based tracking.

4. **Speed Estimation**

   * Speed is calculated using:

     ```
     Speed = Distance / Time
     ```
   * Pixel movement is converted to real-world distance using a scaling factor.

5. **Overspeed Detection**

   * Vehicles exceeding the speed threshold are flagged.

6. **Output Generation**

   * Displays results, saves video, logs violations, and captures snapshots.

---

## ⚙️ Configuration

Modify these parameters in the code:

```python
VIDEO_PATH = "path_to_your_video"
fps = 30                # Frames per second
scale = 0.05            # meters per pixel
SPEED_LIMIT = 80        # km/h
```

---

## ▶️ How to Run

1. Install dependencies:

```bash
pip install opencv-python
```

2. Run the script:

```bash
python speed.py
```

---

## 📂 Output

After execution, the following files are generated:

* 🎬 `car_speed_output.mp4` → Processed video
* 📸 `overspeed_cars/` → Snapshots of violating vehicles
* 📄 `overspeed_log.txt` → Log file with details

---

## ⚠️ Limitations

* Uses basic motion detection (may detect non-car objects)
* Speed estimation depends on manual calibration (`scale`)
* Tracking is simple and may lose IDs in dense traffic
* Accuracy depends on camera angle and video quality

---

## 🚀 Future Improvements

* Integrate YOLO for accurate vehicle detection
* Use DeepSORT for robust tracking
* Apply perspective transformation for precise speed calculation
* Add license plate recognition
* Deploy as a real-time system with live camera feed

---

## 🛠️ Technologies Used

* Python
* OpenCV
* NumPy

---

## 📌 Use Cases

* Traffic monitoring systems
* Smart city surveillance
* Speed limit enforcement
* Academic and research projects

---

## 👨‍💻 Author

Developed as part of a computer vision project focusing on real-world applications of image processing.

---

## ⭐ If you like this project

Give it a star ⭐ and feel free to contribute!
