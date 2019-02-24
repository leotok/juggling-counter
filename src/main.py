from imutils.video import VideoStream
import cv2
import imutils
import numpy as np
import time


def get_contours(hsv, lower, upper):
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return imutils.grab_contours(cnts)

def get_circle(cnts):
    c = max(cnts, key=cv2.contourArea)
    (x, y), radius = cv2.minEnclosingCircle(c)
    m = cv2.moments(c)
    center = (int(m["m10"] / m["m00"]), int(m["m01"] / m["m00"])) 
    return (x, y), radius, center

if __name__ == "__main__":
    print ("Juggling counter")

    print ('Starting camera...')
    vs = VideoStream(src=0).start()
    window_height = vs.frame.shape[0]
    window_width = vs.frame.shape[1]
    time.sleep(1.0)

    # blue lower and upper bounds
    color_lower = (82, 42, 14)
    color_upper = (139, 244, 255)
    
    y_score_limt = int(window_height / 2)
    y_reset_limit = y_score_limt + 20
    score = 0
    highscore = 0
    last_score_time = 0
    score_reset_iterval = 2
    last_ball_y = 400
    falling = False
    red_rgb = (0, 0, 255)
    yellow_rgb = (0, 255, 255)

    while True:
        frame = vs.read()
        if frame is None:
            break

        frame = cv2.flip(frame, 1)
        frame = imutils.resize(frame, width=window_width)
        blurred = cv2.GaussianBlur(frame, (11,11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        cts = get_contours(hsv, color_lower, color_upper)    

        if len(cts) > 0:
            (x, y), radius, center = get_circle(cts)

            if radius > 5:
                cv2.circle(frame, (int(x), int(y)), int(radius), yellow_rgb, 2)
                cv2.circle(frame, center, 5, red_rgb, -1)

                if last_ball_y <= y_score_limt:
                    if falling == False:
                        score += 1
                        last_score_time = time.time()
                    falling = True
                elif last_ball_y >= y_reset_limit:
                    falling = False

                last_ball_y = y

                if score > highscore:
                    highscore = score
        
        if time.time() - last_score_time > score_reset_iterval:
            score = 0
            last_score_time = 0
            
        cv2.putText(frame, 'Score: {}'.format(score), (0, 25), cv2.FONT_HERSHEY_SIMPLEX, 1,  red_rgb, 2)
        cv2.putText(frame, 'Highscore: {}'.format(highscore), (0, 60), cv2.FONT_HERSHEY_SIMPLEX, 1,  red_rgb, 2)
        cv2.line(frame, (0, y_score_limt), (window_width, y_score_limt), red_rgb, 1)
        cv2.imshow("Frame", frame)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

    vs.stop()
    cv2.destroyAllWindows()
