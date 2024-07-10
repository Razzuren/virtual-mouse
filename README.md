# Virtual Mouse with Gesture Control

This project implements a virtual mouse that uses hand gestures to control the mouse cursor and perform clicks. The project leverages OpenCV for video capture, MediaPipe for hand tracking and gesture recognition, and PyAutoGUI for controlling the mouse.

## Features

- Tracks hand movements and moves the mouse cursor accordingly.
- Recognizes the "Victory" gesture to perform a mouse click.
- Includes a 3-second buffer between consecutive clicks to prevent accidental multiple clicks.
