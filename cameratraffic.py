
import cv2
import pandas as pd

# Read CSV file for color names
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)

# Function to find the closest color name
def getColorName(R, G, B):
    minimum = float('inf')
    color_name = "Undefined"
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i, "R"])) + abs(G - int(csv.loc[i, "G"])) + abs(B - int(csv.loc[i, "B"]))
        if d < minimum:
            minimum = d
            color_name = csv.loc[i, "color_name"]
    return color_name

# Function to detect the traffic signal
def getTrafficSignal(R, G, B):
    if R > 150 and G < 100 and B < 100:  # Predominantly red
        return "STOP"
    elif G > 150 and R < 100 and B < 100:  # Predominantly green
        return "GO"
    elif R > 150 and G > 150 and B < 100:  # Predominantly yellow
        return "WAIT"
    else:
        return "UNDEFINED"

# Open webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not access the webcam.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to capture video.")
        break

    # Get frame dimensions
    height, width, _ = frame.shape

    # Extract the center pixel for color detection
    center_x, center_y = width // 2, height // 2
    b, g, r = frame[center_y, center_x]
    b, g, r = int(b), int(g), int(r)

    # Get color name and traffic signal
    color_name = getColorName(r, g, b)
    signal = getTrafficSignal(r, g, b)

    # Draw rectangle and display color information
    cv2.rectangle(frame, (20, 20), (600, 100), (b, g, r), -1)
    text = f"Color: {color_name}, Signal: {signal}"
    cv2.putText(frame, text, (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # Display text in black for light colors
    if r + g + b > 600:
        cv2.putText(frame, text, (30, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

    # Show the frame
    cv2.imshow("Traffic Light Detection", frame)

    # Exit on pressing 'Esc'
    if cv2.waitKey(20) & 0xFF == 27:
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
