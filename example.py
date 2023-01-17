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
    
    prev_text = text
    # print(f'prev: {prev_text}')
    # print(f'text: {text}')
    print(count)
    if prev_text == text:
        count += 1
    if  count == 20:
        UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        
        bytesToSend = str.encode(msgFromClient)

        UDPClientSocket.sendto(bytesToSend, serverAddressPort)

        msgFromServer = UDPClientSocket.recvfrom(bufferSize)

        msg = "Message from Server {}".format(msgFromServer[0])

        print(msg)

        UDPClientSocket.sendto(str.encode("ST "), serverAddressPort)
        count = 0
    else:
        count += 0
        # prev_text = text
        # start_time = current_time
    #text = "vertical_ratio: " + str(gaze.vertical_ratio()) + " horizontal_ratio: " + str(gaze.horizontal_ratio()) + " " + text
    cv2.putText(frame, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)
    # if time.perf_counter() - start_time > 0.5:
    #     # Some where before the loop
    #     print('time > 0.5')
    #     print("text iris_position = ", text)
    #     print("prev iris_position = ", prev_text)
        # UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

        
        # bytesToSend = str.encode(msgFromClient)

        # UDPClientSocket.sendto(bytesToSend, serverAddressPort)

        # msgFromServer = UDPClientSocket.recvfrom(bufferSize)

        # msg = "Message from Server {}".format(msgFromServer[0])

        # print(msg)

        # UDPClientSocket.sendto(str.encode("ST "), serverAddressPort)
    # prev_text = text 
    left_pupil = gaze.pupil_left_coords()
    right_pupil = gaze.pupil_right_coords()
    # print(f'framede {(time.perf_counter() - start_time)}')
    # time.sleep(3)
    cv2.imshow("Demo", frame)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break
webcam.release()
cv2.destroyAllWindows()


# yarim saniyede resim alip isliyor 
# yer islemede komut gondermektedir
