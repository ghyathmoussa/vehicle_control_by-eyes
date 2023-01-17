import cv2
from gaze_tracking import GazeTracking
import socket
import time


gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

serverAddressPort   = ("192.168.4.1", 9999)
bufferSize          = 1024

msgFromClient = "ST "
bytesToSend = str.encode(msgFromClient)

prev_text = 'test'
count = 0
while True:
    # We get a new frame from the webcam
    _, frame = webcam.read()

    # We send this frame to GazeTracking to analyze it
    gaze.refresh(frame)

    frame = gaze.annotated_frame()
    text = ""
    start_time = time.perf_counter()
    # Inside the loop after the position of the eye is acquired
    current_time = time.perf_counter()
    if gaze.is_blinking():
        text = "Stop"
        msgFromClient = "ST "
    elif gaze.is_right():
        text = "Looking right"
        msgFromClient = "R "
    elif gaze.is_left():
        text = "Looking left"
        msgFromClient = "L "
    elif gaze.is_center():
        if gaze.is_up():
            text = "Looking up"
            msgFromClient = "FW "
        elif gaze.is_down():
            text = "Looking down"

            msgFromClient = "BW "
        else:
            text = "Looking center"
            msgFromClient = "ST "
    print(count)
    if prev_text == text :
        count += 1
    else:
        count = 0
    if  count == 10 and text != '':
        UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        
        bytesToSend = str.encode(msgFromClient)

        UDPClientSocket.sendto(bytesToSend, serverAddressPort)

        msgFromServer = UDPClientSocket.recvfrom(bufferSize)

        msg = "Message from Server {}".format(msgFromServer[0])

        print(msg)

        UDPClientSocket.sendto(str.encode("ST "), serverAddressPort)
        count = 0
    if  count == 10 and text != '':
        msgFromClient = "ST "
    prev_text = text
    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)
    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    cv2.imshow("Ekran", frame)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break
webcam.release()
cv2.destroyAllWindows()


# yarim saniyede resim alip isliyor 
# yer islemede komut gondermektedir
