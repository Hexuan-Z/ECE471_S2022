import time
import cv2

"""
Replace following with your own algorithm logic

Two random coordinate generator has been provided for testing purposes.
Manual mode where you can use your mouse as also been added for testing purposes.
"""
def GetLocation(move_type, env, current_frame, previous_frame, previous_target):
    # time.sleep(1) #artificial one second processing time

    current_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    previous_gray = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)
    dframe = cv2.absdiff(current_gray, previous_gray)

    # cv2.imwrite('savedImage.jpg', cv2.cvtColor(dframe, cv2.COLOR_BGR2RGB))
    blurred = cv2.GaussianBlur(dframe, (11, 11), 0)
    ret, tframe = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    (cnts, _) = cv2.findContours(tframe.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    #Use relative coordinates to the current position of the "gun", defined as an integer below
    if move_type == "relative":
        """
        North = 0
        North-East = 1
        East = 2
        South-East = 3
        South = 4
        South-West = 5
        West = 6
        North-West = 7
        NOOP = 8
        """
        coordinate = env.action_space.sample() 
    #Use absolute coordinates for the position of the "gun", coordinate space are defined below
    else:
        """
        (x,y) coordinates
        Upper left = (0,0)
        Bottom right = (W, H) 
        """
        # coordinate = env.action_space_abs.sample()
        # print(len(cnts))
        if len(cnts) > 0:
            targetX = []
            targetY = []
            for cnt in cnts:
                x, y, w, h = cv2.boundingRect(cnt[0])
                center_y = x+w//2
                center_x = y+h//2
                if abs(center_x - previous_target[0]) > 5 and abs(center_y - previous_target[1]) > 5 and abs(center_x - 1024//2) > 5 and abs(center_y - 512//2) > 5:
                    targetY.append(center_y)
                    targetX.append(center_x)

            if len(targetX) > 0:
                coordinate = (targetX[0], targetY[0])
            else:
                coordinate = (1024//2, 768//2)

        else:
            coordinate = (1024//2, 768//2)
    return {'coordinate' : coordinate, 'move_type' : move_type}

