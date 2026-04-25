import cv2
import math
import os
import time

# =========================
# CONFIG
# =========================
VIDEO_PATH = r"C:\Users\Vikas V B\Downloads\bleh.mp4"
OUTPUT_PATH = "car_speed_output.mp4"
SNAPSHOT_FOLDER = "overspeed_cars"

fps = 30
scale = 0.05
SPEED_LIMIT = 80  # km/h

# Create folder for snapshots
if not os.path.exists(SNAPSHOT_FOLDER):
    os.makedirs(SNAPSHOT_FOLDER)

# =========================
# LOAD VIDEO
# =========================
cap = cv2.VideoCapture(VIDEO_PATH)

if not cap.isOpened():
    print("Error: Cannot open video")
    exit()

# =========================
# VIDEO WRITER
# =========================
frame_width = 800
frame_height = 600

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(OUTPUT_PATH, fourcc, fps, (frame_width, frame_height))

# =========================
# BACKGROUND SUBTRACTOR
# =========================
fgbg = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)

# =========================
# TRACKING
# =========================
prev_positions = {}
car_id_counter = 0

# To avoid duplicate captures
captured_ids = set()

# Log file
log_file = open("overspeed_log.txt", "w")

print("Processing video... Press ESC to stop")

# =========================
# MAIN LOOP
# =========================
while True:
    ret, frame = cap.read()
    if not ret:
        print("End of video")
        break

    frame = cv2.resize(frame, (frame_width, frame_height))

    fgmask = fgbg.apply(frame)
    _, thresh = cv2.threshold(fgmask, 200, 255, cv2.THRESH_BINARY)
    thresh = cv2.medianBlur(thresh, 5)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    current_positions = {}

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 800:
            continue

        x, y, w, h = cv2.boundingRect(cnt)
        if w < 30 or h < 30:
            continue

        cx = x + w // 2
        cy = y + h // 2

        matched_id = None

        for car_id, (px, py) in prev_positions.items():
            if abs(cx - px) < 50 and abs(cy - py) < 50:
                matched_id = car_id
                break

        if matched_id is None:
            matched_id = car_id_counter
            car_id_counter += 1

        current_positions[matched_id] = (cx, cy)

        # =========================
        # SPEED CALCULATION
        # =========================
        if matched_id in prev_positions:
            px, py = prev_positions[matched_id]

            dx = cx - px
            dy = cy - py

            dist_pixels = math.sqrt(dx**2 + dy**2)
            dist_meters = dist_pixels * scale

            speed_mps = dist_meters * fps
            speed_kmh = speed_mps * 3.6

            if speed_kmh > 200:
                speed_kmh = 0

            # =========================
            # COLOR BASED ON SPEED
            # =========================
            if speed_kmh > SPEED_LIMIT:
                color = (0, 0, 255)  # RED

                # Warning text
                cv2.putText(frame, "OVER SPEED!",
                            (x, y - 30),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.7, color, 2)

                # =========================
                # SAVE SNAPSHOT (only once per car)
                # =========================
                if matched_id not in captured_ids:
                    timestamp = int(time.time())
                    filename = f"{SNAPSHOT_FOLDER}/car_{matched_id}_{timestamp}.jpg"

                    cv2.imwrite(filename, frame)

                    # Log entry
                    log_file.write(f"Car ID: {matched_id}, Speed: {speed_kmh:.2f} km/h, Time: {timestamp}\n")

                    captured_ids.add(matched_id)

            else:
                color = (0, 255, 0)  # GREEN

            # Display speed
            cv2.putText(frame, f"{speed_kmh:.1f} km/h",
                        (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6, color, 2)

        else:
            color = (0, 255, 0)

        # Draw box
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

    prev_positions = current_positions

    # Save frame
    out.write(frame)

    # Show video
    cv2.imshow("Car Speed Detection", frame)

    if cv2.waitKey(30) & 0xFF == 27:
        break

# =========================
# CLEANUP
# =========================
cap.release()
out.release()
log_file.close()
cv2.destroyAllWindows()

print("Saved video:", OUTPUT_PATH)
print("Snapshots saved in:", SNAPSHOT_FOLDER)
print("Log saved as: overspeed_log.txt")
