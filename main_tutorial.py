# Objective: Start video recording using external camera
import cv2
import time
import send_email as send
import clean_folder as clean
import os
import glob
from pathlib import Path
from threading import Thread

video = cv2.VideoCapture(1)
# Sleep 1s to allow camera to bootup
time.sleep(1)
first_frame = None
status_list = list()
count = 1
while True:
    status = 0
    # Frame stores pixels numpy matrix
    check, frame = video.read()

    # Turn frame into grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Blur grayscale frame to reduce noise
    blur_size = (21, 21)
    blur_gray_frame = cv2.GaussianBlur(gray_frame, blur_size, 0)

    # Variable to hold first static frame
    if first_frame is None:
        first_frame = blur_gray_frame

    # Calculate frame difference
    diff_frame = cv2.absdiff(first_frame, blur_gray_frame)

    # Map the frame
    thresh_frame = cv2.threshold(diff_frame, 20, 255, cv2.THRESH_BINARY)[1]

    # Dilate the frame
    dilate_frame = cv2.dilate(thresh_frame, None, iterations=2)

    cv2.imshow("My Video", dilate_frame)

    # Find contours in the frame
    contours, check = cv2.findContours(dilate_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:

        # Ignore contours that is less than 7000 pixels
        if cv2.contourArea(contour) < 7000:
            continue
        x_pos, y_pos, w, h = cv2.boundingRect(contour)
        rectangle = cv2.rectangle(frame, (x_pos, y_pos), (x_pos + w, y_pos + h), (0,255,0), 3)

        # If no "images" directory then create one
        if not os.path.exists("images/"):
            os.mkdir("images/")

        # If there is any rectangle on the screen
        if rectangle.any():
            # Write image{count}.png for as long as there is rectangle on the video frame
            cv2.imwrite(f"images/{count}.png", frame)
            count += 1
            status = 1

        # Get all images
        images = glob.glob("images/*.png")
        # Image to send is the images in the middle (Appears to be one that is the most clear)
        image_to_send = images[int(len(images) / 2)]


    # Send email only when a rectangle disappears
    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:
        email_thread = Thread(target=send.emailing, args=(image_to_send,))
        email_thread.daemon = True

        clean_thread = Thread(target=clean.clean_folder)
        clean_thread.daemon = True
        email_thread.start()

    cv2.imshow("Spot Me", frame)
    # Wait 1s for user to hit "q"
    key = cv2.waitKey(1)

    # Break if user hit "q"
    if key == ord("q"):
        clean_thread.start()
        break

# Exit the video recording
video.release()
