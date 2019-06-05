import cv2

def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)

def capture():
    take = True
    times = 2
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("webcam")
    img_counter = 0

    while take:
        ret, frame = cam.read()
        frame = rescale_frame(frame, percent=30)

        if times == 2:
            cv2.imshow("Player1!", frame)
        else:
            cv2.imshow("Player2!", frame)

        if not ret:
            take = False
        k = cv2.waitKey(1)

        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            take = False
        elif k%256 == 32:
            # SPACE pressed
            times -= 1
            img_name = "capture_{}.png".format(img_counter)
            cv2.imwrite(img_name, frame)
            print("{} written!".format(img_name))
            img_counter += 1
        if times == 0:
            take = False

    cam.release()
    cv2.destroyAllWindows()

capture()