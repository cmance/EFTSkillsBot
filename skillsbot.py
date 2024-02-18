import cv2
import pyautogui
import numpy as np
import random

# full_start_screen = cv2.imread('./FullImages/EFTMainMenuFullScreen.png', cv2.IMREAD_UNCHANGED)
# start_screen_button = cv2.imread('./SnippedImages/EFTstartscreen.png', cv2.IMREAD_UNCHANGED)

# # cv2.imshow('Full Start Screen', full_start_screen)
# # cv2.waitKey()
# # cv2.destroyAllWindows()

# # cv2.imshow('Start Screen Button', start_screen_button)
# # cv2.waitKey()
# # cv2.destroyAllWindows()

# result = cv2.matchTemplate(start_screen_button, full_start_screen, cv2.TM_CCOEFF_NORMED)

# # cv2.imshow('Result', result)
# # cv2.waitKey()
# # cv2.destroyAllWindows()

# # Unpack the result array
# min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

# # draw a rectangle around the matched region
# h, w = start_screen_button.shape[:2]
# top_left = max_loc
# bottom_right = (top_left[0] + w, top_left[1] + h) # add the width and height of the template to the top left point to get the bottom right point
# cv2.rectangle(full_start_screen, top_left, bottom_right, (0, 255, 255), 2)

# # cv2.imshow('Matched', full_start_screen)
# # cv2.waitKey()
# # cv2.destroyAllWindows()

# threshold = 0.9
# yloc, xloc = np.where(result >= threshold) # returns a tuple of arrays, one for each dimension of the input array

# for (x, y) in zip(xloc, yloc):
#     cv2.rectangle(full_start_screen, (x, y), (x + w, y + h), (0, 255, 255), 2)

# rectangles = []
# for (x, y) in zip(xloc, yloc):
#     rectangles.append([int(x), int(y), int(w), int(h)])
#     rectangles.append([int(x), int(y), int(w), int(h)])

# rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
# print(rectangles)

# # cv2.imshow('Matched', full_start_screen)
# # cv2.waitKey()
# # cv2.destroyAllWindows()

# for rect in rectangles:
#     x, y, w, h = rect
#     cv2.rectangle(full_start_screen, (x, y), (x + w, y + h), (0, 255, 255), 2) # draw a rectangle around the matched region
    
#     random_x = random.randint(x, x + w)
#     random_y = random.randint(y, y + h)

#     # cv2.imshow('Matched Region', full_start_screen) # display the image with the rectangle
#     # cv2.waitKey(0)
#     # cv2.destroyAllWindows()
    
#     pyautogui.click(random_x, random_y) # click a random point within the matched region

def capture_screenshot(region):
    screenshot = pyautogui.screenshot(region=region)
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    return screenshot

def click_random_point_in_rectangle(rect):
    x, y, w, h = rect
    random_x = random.randint(x, x + w)
    random_y = random.randint(y, y + h)
    pyautogui.click(random_x, random_y)

def draw_rectangle(image, top_left, dimensions, color=(0, 255, 255), thickness=2):
    bottom_right = (top_left[0] + dimensions[0], top_left[1] + dimensions[1])
    cv2.rectangle(image, top_left, bottom_right, color, thickness)

def click_random_point_in_rectangle(rect):
    x, y, w, h = rect
    random_x = random.randint(x, x + w)
    random_y = random.randint(y, y + h)
    pyautogui.click(random_x, random_y)


# # Create a loop to capture the screen
while True:
    start_screen_button = cv2.imread('./SnippedImages/EFTstartscreen.png', cv2.IMREAD_UNCHANGED)
    start_screen_button = cv2.cvtColor(start_screen_button, cv2.COLOR_BGRA2BGR)
    # Capture screenshot
    screenshot = capture_screenshot((0, 0, 1920, 1080))



    result = cv2.matchTemplate(start_screen_button, screenshot, cv2.TM_CCOEFF_NORMED)
    # Unpack the result array
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    # draw a rectangle around the matched region
    h, w = start_screen_button.shape[:2]  # Use the dimensions of the template image
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h) # add the width and height of the template to the top left point to get the bottom right point
    cv2.rectangle(screenshot, top_left, bottom_right, (0, 255, 255), 2)

    threshold = 0.9
    yloc, xloc = np.where(result >= threshold) # returns a tuple of arrays, one for each dimension of the input array

    for (x, y) in zip(xloc, yloc):
        # cv2.rectangle(screenshot, (x, y), (x + w, y + h), (0, 255, 255), 2)
        draw_rectangle(screenshot, (x, y), (x + w, y + h))
    
    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])

    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
    print(rectangles)

    for rect in rectangles:
        draw_rectangle(screenshot, (x, y), (x + w, y + h))
        click_random_point_in_rectangle(rect)
    
    # So far, we have found the main menu "Escape From Tarkov" button and clicked it

    if cv2.waitKey(1) == ord('q'):
        break

# # After the loop release everything if job is finished
cv2.destroyAllWindows()

# TODO:
# X Have a way to click the Escape From Tarkov button on the main menu
# - Add way to click the PMC button after the main menu button is clicked, just as a failsafe if PMC isnt already selected
# - Add full screen image (optional) and snip the PMC button to click it and put in file structure
# - Click next button after PMC button is clicked
# - Click woods map button
# - Click ready button
# - Have bot press shift to sprint in the game
# - See if the empty stamina detection is working, if not, use time.sleep() to wait for stamina to be empty/full
# - Press escape keyboard button to leave raid
# - Click leave
# - Confirm leave, loops repeats.