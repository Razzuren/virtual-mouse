import cv2
import mediapipe as mp
import pyautogui
import time

hand_detection = mp.solutions.hands
hands = hand_detection.Hands()
BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path=str("resource/gesture_recognizer.task")),
    running_mode=VisionRunningMode.IMAGE)

screen_size = pyautogui.size()

capture = cv2.VideoCapture(0)
last_click_time = 0 

with GestureRecognizer.create_from_options(options) as recognizer:
    while capture.isOpened():
        success, frame = capture.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        gestures = recognizer.recognize(mp_image)
        result = hands.process(frame)
        landmarks = result.multi_hand_landmarks

        if landmarks:
            for hand_landmarks in landmarks:
                x = hand_landmarks.landmark[8].x
                y = hand_landmarks.landmark[8].y
                x_new = int(x * screen_size[0])
                y_new = int(y * screen_size[1])
                pyautogui.moveTo(x_new, y_new)
                mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, hand_detection.HAND_CONNECTIONS)

                if gestures:
                    try:
                        top_gesture = gestures.gestures[0][0]
                        current_time = time.time() 
                        if top_gesture.category_name == 'Victory' and top_gesture.score > 0.60:
                            if current_time - last_click_time >= 3: 
                                pyautogui.click()
                                last_click_time = current_time 
                    except:
                        continue

        cv2.imshow("Virtual Mouse", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()