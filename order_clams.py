# import the necessary packages
import argparse
import imutils
import cv2
import imghdr

from functools import reduce
from os import listdir
from os.path import isfile, join

# output image with cv2
def output_image(image):
    cv2.imshow("Image", image)

# reduce callback
def return_longest_array(x, y): 
    return x if len(x) > len(y) else y

# find longest contour array from the stack
def find_biggest_contour(contours):
    longest_contour = reduce(return_longest_array, contours)
    return longest_contour

# draw contour on image
def show_clam(image, contour, text="center"):
    # compute the center of the contour
    M = cv2.moments(contour)

    if (M["m00"] == 0):
        M["m00"] = 1

    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    # draw the contour and center of the shape on the image
    cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)
    cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
    cv2.putText(image, text, (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # show the image
    output_image(image)
    cv2.waitKey(0)

# get clam name from the filename
def get_clam_name(filename): return filename.split('.')[0]

def calculate_clam_area(clam, track):
    clam_track = join(track, clam)
    
    # load the image, convert it to grayscale, blur it slightly,
    # and threshold it
    image = cv2.imread(clam_track)
    image = imutils.resize(image, width=600)
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY)[1]

    # find contours in the thresholded image
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if imutils.is_cv2() else cnts[1]
    
    # find biggest clam contour
    main_contour = find_biggest_contour(cnts)

    # calculate clam contour area
    clam_area = cv2.contourArea(main_contour)

    # return {'name': get_clam_name(clam), 'area': clam_area}
    return (get_clam_name(clam), clam_area, image, main_contour)

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--directory", required=True, help="Path to clam shelter directory")
ap.add_argument("-v", "--visualize", required=False, help="Show clam images ordered by size (true/false)?")
args = vars(ap.parse_args())

# draw_text(image, main_contour, clam)
visualize = args["visualize"] == 'true'
# clams directory images
clam_bay = args["directory"]

clams_shelter = [clam_shell for clam_shell in listdir(clam_bay) if isfile(join(clam_bay, clam_shell)) and imghdr.what(join(clam_bay, clam_shell)) != None ]

clam_areas = [calculate_clam_area(clam, clam_bay) for clam in clams_shelter]
sorted_clam_areas = sorted(clam_areas, key=lambda item: item[1], reverse=True)

print("Here is your clams correct order (clam name - area):")
for name, area, image, contour in sorted_clam_areas: 
    print("Clam:", name, " | Area:", area)
    if visualize: show_clam(image, contour, name) 

