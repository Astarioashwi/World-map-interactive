import pickle
import cv2
import numpy as np
from PIL.ImageChops import overlay

#from Step1_GetCornerPoints.get_map import warp_image

###################################
map_file_path = "../Step1_GetCornerPoints/map.p"
countries_file_path = "countries.p"
#Camera settings
cam_id = 3
width, height = 1920, 1080
###################################

# Open a connection to the webcam
cap = cv2.VideoCapture(cam_id)
cap.set(3, width)
cap.set(4, width)

file_obj = open(map_file_path, 'rb')
map_points = pickle.load(file_obj)
file_obj.close()
print(f"Loaded map coordinates.", map_points)

#Temprory list to store the four points of the current polygon being marked
current_polygon = []

# Counter to keep track of how many polygons have been created
counter = 0

# Load previously defined Regions of Interest (ROIs) polygons from a file
if countries_file_path:
    file_obj = open(countries_file_path, 'rb')
    polygons = pickle.load(file_obj)
    file_obj.close()
    print(f"Loaded {len(polygons)} countries.")
else:
    polygons = []

#Function for warp image(also in get_map)
def warp_image(img, points, size=[1920, 1080]):
    """
    Wraps an image based on the selected points.

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

    global counter, current_polygon

    #If left mouse button is clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        #Append the clicked point (x,y) to the current_polygon list
        current_polygon.append((x, y))

while True:
    # Read a frame from the webcam
    success, img = cap.read()
    imgWarped, _ = warp_image(img, map_points)

    # print(current_polygon)
    key = cv2.waitKey(1)

    # If the 'c' key is pressed, clear the current polygon
    if key == ord("s") and len(current_polygon) > 2:
        country_name = input("Enter the Country name: ")
        polygons.append([current_polygon, country_name])  # Add the polygon to the list
        current_polygon = []  # Reset for the next polygon
        counter += 1  # Increment the counter
        print("Number of countries saved: ", len(polygons))  # Print the collected polygons

    # If the "q" key is pressed, save the polygons and exit the loop
    if key == ord("q"):
        fileObj = open(countries_file_path, 'wb')
        pickle.dump(polygons, fileObj)  # Save the polygons to a file
        fileObj.close()
        print(f"Saved {len(polygons)} countries")
        break

    if key == ord("d"):
        polygons.pop()

    if current_polygon:
        cv2.polylines(imgWarped, [np.array(current_polygon)], isClosed=True, color=(0, 0, 255), thickness=2)

    overlay = imgWarped.copy()

    # Draw the collected polygons on the image
    for polygon, name in polygons:
        cv2.polylines(imgWarped, [np.array(polygon)], isClosed=True, color=(0, 255, 0), thickness=2)
        cv2.fillPoly(overlay, [np.array(polygon)], (0, 255, 0))

    cv2.addWeighted(overlay, 0.35, imgWarped, 0.65, 0, imgWarped)

    # Display the image with marked polygons
    cv2.imshow("Warped Image", imgWarped)
    cv2.imshow("Original Image", img)



    # Set the mouse callback function for making points
    cv2.setMouseCallback("Warped Image", mousePoints)
    cv2.waitKey(1)




