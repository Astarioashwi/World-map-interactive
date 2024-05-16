import pickle
import cv2
import numpy as np

####################################

#Camera settings
cam_id = 3
width, height = 1920, 1080

####################################

#Initialize variables
cap = cv2.VideoCapture(cam_id)
cap.set(3, width)
cap.set(4, width)

points = np.zeros((4, 2), int) #Array to store clicked points
counter = 0 #Counter to track the number of clicked points


def mousePoints(event, x, y, flags, params):
    """
    Callback function for mouse clicks.

    Args:
    :param events: OpenCV event type (e.g., cv2.EVENT_LBUTTONDOWN)
    :param x: X - coordinate of the mouse click
    :param y: Y - coordinate of the mouse click
    :param flags: Additional flags associated with the event
    :param params: User-defined parameters passed to the callback function

    :return: None
    """

    global counter
    if event == cv2.EVENT_LBUTTONDOWN:
        points[counter] = x, y #Store the clicked point
        counter += 1 #Increment counter
        print(f"Clicked points: {points}")


def warp_image(img, points, size=[1920, 1080]):
    """
    Wraps an inage based on the selected points.

    :param img: The image to be wraped
    :param points: Array containing four clicked points
    :param size: Desired size of the wraped image

    :return:
        imgOutput: The warped image
        matrix: The perspective transformation matrix
    """
    pts1 = np.float32(points)  # Convert points to float32
    pts2 = np.float32([[0, 0], [size[0], 0], [0, size[1]], [size[0], size[1]]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2) # Calculate perspective transformation matrix
    imgOutput = cv2.warpPerspective(img, matrix, (size[0], size[1]))  # Wrap the image
    return imgOutput, matrix


while True:
    success, img = cap.read()

    if counter == 4:
        # Save selected points to file
        fileObj = open("map.p", "wb")
        pickle.dump(points, fileObj)
        fileObj.close()
        print("Points saved to file: map.p")

        # Wrap the image
        imgOutput, matrix = warp_image(img, points)
        #Display warped image
        cv2.imshow("Output Image", imgOutput)
        cv2.waitKey(0)

    # Draw circles at clicked points
    for x in range(0, 4):
        cv2.circle(img, (points[x][0], points[x][1]), 3, (0, 225, 0), cv2.FILLED)

    cv2.imshow("Original Image", img)
    cv2.setMouseCallback("Original Image", mousePoints)

    cv2.waitKey(1) #wait for a press key

# Release resources
cap.release()
cv2.destroyAllWindows()