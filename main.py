import cv2
import mediapipe as mp
import pyautogui

hand_detection = mp.solutions.hands
hands = hand_detection.Hands()
BaseOptions = mp.tasks. BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

# Create a gesture recognizer instance with the image mode
options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path=str("resource/gesture_recognizer.task")),
    running_mode=VisionRunningMode.IMAGE)

mp.tasks.vision.GestureRecognizer.create_from_options(options)

screen_size = pyautogui.size()

capture = cv2.VideoCapture(0)

while capture.isOpened():
    success, image = capture.read()
    if not success:
        break

    image = cv2.flip(image, 1)

    result = mp.tasks.vision.GestureRecognizer.recognize(image)
    landmarks = result.hand_landmarks

    if landmarks:
        for hand_landmarks in landmarks:
            x = hand_landmarks.landmark[hand_detection.HandLandmark.INDEX_FINGER_TIP].x
            y = hand_landmarks.landmark[hand_detection.HandLandmark.INDEX_FINGER_TIP].y

            x_new = int(x * screen_size[0])
            y_new = int(y * screen_size[1])

            pyautogui.moveTo(x_new, y_new)
            top_gesture = result.gestures[0][0]
            print(top_gesture.category_name, top_gesture.score)
            mp.solutions.drawing_utils.draw_landmarks(image, hand_landmarks, hand_detection.HAND_CONNECTIONS)


    cv2.imshow("Virtual Mouse", image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()

# import mediapipe as mp
# from show_images import display_batch_of_images_with_gestures_and_hand_landmarks
#
# BaseOptions = mp.tasks. BaseOptions
# GestureRecognizer = mp.tasks.vision.GestureRecognizer
# GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
# VisionRunningMode = mp.tasks.vision.RunningMode
#
# results = []
# images = []
#
# # Change to the location on your machine
# resources = 'C:/Users/samue/PycharmProjects/pythonProject/resources'
#
# # Create a gesture recognizer instance with the image mode
# options = GestureRecognizerOptions(
#     base_options=BaseOptions(model_asset_path=str(resources + '/gesture_recognizer.task')),
#     running_mode=VisionRunningMode.IMAGE)
#
# with GestureRecognizer.create_from_options(options) as c:
#     for x in range(2, 6):
#         file = str(resources + '/0' + str(x) + '.jpeg')
#         print(file + ' processed')
#         image = mp.Image.create_from_file(file)
#         recognition_result = recognizer.recognize(image)
#         images.append(image)
#         top_gesture = recognition_result.gestures[0][0]
#         hand_landmarks = recognition_result.hand_landmarks
#         results.append((top_gesture, hand_landmarks))
#
# print(recognition_result)
# display_batch_of_images_with_gestures_and_hand_landmarks(images, results)
# # are you working
