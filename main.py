#Myron Peoples, Logan Herrera, Priscilla Devadhas, Judah Lomo, Chouchi Naotour
import tkinter as tk
import cv2
import mediapipe as mp
import sys

# Hand Tracking using MediaPipe
class HandTrackingApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Hand Tracking App")
        self.window.geometry("400x200")

        # Add a button to start hand tracking
        self.track_button = tk.Button(self.window, text="Start Hand Tracking", command=self.start_hand_tracking)
        self.track_button.pack(pady=50)

        # Bind the window close event (when you click the "X" in the window)
        self.window.protocol("WM_DELETE_WINDOW", self.on_close)

        # Variable to store OpenCV capture so we can release it properly
        self.cap = None
        self.hand_tracking_running = False  # Flag to check if hand tracking is running

    def start_hand_tracking(self):
        if not self.hand_tracking_running:  # Only start if not already running
            self.hand_tracking_running = True
            # Start the hand tracking in a separate window
            self.hand_tracking_window()

    def hand_tracking_window(self):
        # Initialize OpenCV webcam capture
        self.cap = cv2.VideoCapture(0)

        # Initialize MediaPipe hand detection and drawing utilities
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        mp_draw = mp.solutions.drawing_utils

        while True:
            # Capture frame-by-frame
            ret, frame = self.cap.read()

            if not ret:
                break

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

        # Release resources after tracking ends
        self.cap.release()
        cv2.destroyAllWindows()

        # Reset the flag
        self.hand_tracking_running = False

    def on_close(self):
        # This method will be called when the Tkinter window is closed
        if self.cap:
            self.cap.release()  # Release the OpenCV capture
        cv2.destroyAllWindows()  # Close any OpenCV windows
        self.window.quit()  # Close the Tkinter window
        sys.exit()  # Exit the program

# Create the main Tkinter window
root = tk.Tk()
app = HandTrackingApp(root)

# Start the Tkinter event loop
root.mainloop()
