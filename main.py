import tkinter as tk
from tkinter import messagebox
import cv2
import mediapipe as mp

# Hand Tracking using MediaPipe
class HandTrackingApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Hand Tracking App")
        self.window.geometry("400x200")

        # Add a button to open the hand tracking window
        self.track_button = tk.Button(self.window, text="Start Hand Tracking", command=self.start_hand_tracking)
        self.track_button.pack(pady=50)

    def start_hand_tracking(self):
        # Open a new window for hand tracking using OpenCV
        self.hand_tracking_window()

    def hand_tracking_window(self):
        # Initialize OpenCV webcam capture
        cap = cv2.VideoCapture(0)

        # Initialize MediaPipe hand detection and drawing utilities
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        mp_draw = mp.solutions.drawing_utils

        while True:
            # Capture frame-by-frame
            ret, frame = cap.read()

            # Flip the frame for a mirror effect
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.flip(frame, 1)

            # Process the frame to detect hands
            results = hands.process(frame)

            # Draw landmarks and connections on the hands if detected
            if results.multi_hand_landmarks:
                for landmarks in results.multi_hand_landmarks:
                    mp_draw.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

            # Convert back to BGR for OpenCV
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

            # Display the frame with hand tracking
            cv2.imshow("Hand Tracking", frame)

            # Close the hand tracking window when the user presses 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release resources
        cap.release()
        cv2.destroyAllWindows()

# Create the main Tkinter window
root = tk.Tk()
app = HandTrackingApp(root)

# Start the Tkinter event loop
root.mainloop()
