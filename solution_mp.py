import time
import cv2
from math import hypot

"""
Replace following with your own algorithm logic

Two random coordinate generator has been provided for testing purposes.
Manual mode where you can use your mouse as also been added for testing purposes.
"""
def GetLocation(move_type, action_space, current_frame, ref_frame, ref_targets):
    # time.sleep(1) #artificial one second processing time

    current_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    ref_gray = cv2.cvtColor(ref_frame, cv2.COLOR_BGR2GRAY)
    dframe = cv2.absdiff(current_gray, ref_gray)
    blurred = cv2.GaussianBlur(dframe, (11, 11), 0)
    ret, tframe = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    (cnts, _) = cv2.findContours(tframe.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # print(len(cnts))

    result = []
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
        coordinate = action_space.sample() 
    # Use absolute coordinates for the position of the "gun", coordinate space are defined below
    else:
        """
        (x,y) coordinates
        Upper left = (0,0)
        Bottom right = (W, H) 
        """

        if len(cnts) > 0:
            for cnt in cnts:
                # print(len(cnt))
                x, y, w, h = cv2.boundingRect(cnt[0])
                target_y = x+w//2
                target_x = y+h//2
                dists = []
                for ref_target in ref_targets:
                    dist = hypot(ref_target[0] - target_x, ref_target[1] - target_y)
                    dists.append(dist)
                print(dists)
                if len(dists) and min(dists) > 10:
                    result.append({'coordinate': (target_x, target_y), 'move_type': 'absolute'})
        
        if len(result) == 0:
            result.append({'coordinate': (1024//2, 768//2), 'move_type': 'absolute'})

    return result

