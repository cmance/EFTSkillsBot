import cv2
import pyautogui
import numpy as np
import random
import time
import win32api, win32con

# fullScreen = cv2.imread('./FullImages/EFTPrepareToEscapeFullScreen.png', cv2.IMREAD_COLOR)
# button = cv2.imread('./SnippedImages/EFTnextbutton.png', cv2.IMREAD_COLOR)

# # cv2.imshow('Full Start Screen', fullScreen)
# # cv2.waitKey()
# # cv2.destroyAllWindows()

# # cv2.imshow('Start Screen Button', no_stamina_icon)
# # cv2.waitKey()
# # cv2.destroyAllWindows()

# result = cv2.matchTemplate(button, fullScreen, cv2.TM_CCOEFF_NORMED)

# # cv2.imshow('Result', result)
# # cv2.waitKey()
# # cv2.destroyAllWindows()

# # # Unpack the result array
# min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

# # # draw a rectangle around the matched region
# h, w = button.shape[:2]  # Get the dimensions of the template
# top_left = max_loc
# bottom_right = (top_left[0] + w, top_left[1] + h)  # Add the width and height of the template to the top left point to get the bottom right point
# cv2.rectangle(fullScreen, top_left, bottom_right, (0, 255, 255), 2)

# cv2.imshow('Matched', fullScreen)
# cv2.waitKey()
# cv2.destroyAllWindows()

# threshold = 0.4
# yloc, xloc = np.where(result >= threshold) # returns a tuple of arrays, one for each dimension of the input array

# for (x, y) in zip(xloc, yloc):
#     cv2.rectangle(fullScreen, (x, y), (x + w, y + h), (0, 255, 255), 2)

# rectangles = []
# for (x, y) in zip(xloc, yloc):
#     rectangles.append([int(x), int(y), int(w), int(h)])
#     rectangles.append([int(x), int(y), int(w), int(h)])

# rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
# print(rectangles)

# cv2.imshow('Matched', fullScreen)
# cv2.waitKey()
# cv2.destroyAllWindows()

# for rect in rectangles:
#     x, y, w, h = rect
#     cv2.rectangle(fullScreen, (x, y), (x + w, y + h), (0, 255, 255), 2) # draw a rectangle around the matched region
    
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

def load_and_process_template(path):
    img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
    return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

def draw_rectangle(image, top_left, dimensions, color=(0, 255, 255), thickness=2):
    bottom_right = (top_left[0] + dimensions[0], top_left[1] + dimensions[1])
    cv2.rectangle(image, top_left, bottom_right, color, thickness)

def cubic_bezier(t, p0, p1, p2, p3): # Cubic Bezier curve function to move the mouse to a point
    return (1 - t)**3 * p0 + 3 * (1 - t)**2 * t * p1 + 3 * (1 - t) * t**2 * p2 + t**3 * p3

def move_to(x, y, duration=1): # Move the mouse to a point using a cubic bezier curve at a random speed from point to point
    start_x, start_y = win32api.GetCursorPos()
    cp1_x, cp1_y = random.randint(min(start_x, x), max(start_x, x)), random.randint(min(start_y, y), max(start_y, y))
    cp2_x, cp2_y = random.randint(min(start_x, x), max(start_x, x)), random.randint(min(start_y, y), max(start_y, y))
    steps = int(duration * 100)
    for i in range(steps):
        t = i / steps
        pos_x = int(cubic_bezier(t, start_x, cp1_x, cp2_x, x))
        pos_y = int(cubic_bezier(t, start_y, cp1_y, cp2_y, y))
        win32api.SetCursorPos((pos_x, pos_y))
        time.sleep(random.uniform(0.001, 0.005))

def click_random_point_in_rectangle(rect):
    x, y, w, h = rect
    random_x = random.randint(x, x + w)
    random_y = random.randint(y, y + h)
    move_to(random_x, random_y, random.uniform(0.1, 0.25))
    win32api.SetCursorPos((random_x, random_y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, random_x, random_y, 0, 0)
    time.sleep(random.uniform(0.1, 0.25))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, random_x, random_y, 0, 0)
    time.sleep(random.uniform(1, 2.5)) # Wait so not clicking same button again
    

def process_template_and_capture_screenshot(template_path, screenshot_region):
    template = load_and_process_template(template_path)
    screenshot = capture_screenshot(screenshot_region)
    return template, screenshot

def match_template_and_draw_rectangle(template, screenshot, threshold=0.9):
    result = cv2.matchTemplate(template, screenshot, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    h, w = template.shape[:2]
    top_left = max_loc
    yloc, xloc = np.where(result >= threshold)
    rectangles = []
    for (x, y) in zip(xloc, yloc):
        rectangles.append([int(x), int(y), int(w), int(h)])
        rectangles.append([int(x), int(y), int(w), int(h)])
    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.2)
    # print(rectangles)
    for rect in rectangles:
        draw_rectangle(screenshot, (rect[0], rect[1]), (rect[0] + w, rect[1] + h))
    return rectangles

def main():
    time.sleep(2)
    while True:

        # Click the Escape From Tarkov button on the main menu
        start_screen_button, start_screen_screenshot = process_template_and_capture_screenshot('./SnippedImages/EFTstartscreen.png', (0, 0, 1920, 1080))
        start_button_rectangles = match_template_and_draw_rectangle(start_screen_button, start_screen_screenshot)
        for rect in start_button_rectangles:
            click_random_point_in_rectangle(rect)

        # Add a delay to allow the next screen to load
        time.sleep(1)

        # Optional click the PMC button if it isn't already selected

        # Click the "next" button
        next_button, next_screen_screenshot = process_template_and_capture_screenshot('./SnippedImages/EFTnextbutton.png', (0, 0, 1920, 1080))
        next_button_rectangles = match_template_and_draw_rectangle(next_button, next_screen_screenshot, threshold=0.40) # 0.40 detects title page, cant do much about it
        print(next_button_rectangles)
        for rect in next_button_rectangles:
            click_random_point_in_rectangle(rect)

        time.sleep(1)

        # Click the woods map button !!! needs to be changed to factory map button
        woods_map_button, woods_map_screenshot = process_template_and_capture_screenshot('./SnippedImages/EFTwoodsbutton.png', (0, 0, 1920, 1080))
        woods_map_button_rectangles = match_template_and_draw_rectangle(woods_map_button, woods_map_screenshot, threshold=0.6)
        print(woods_map_button_rectangles)
        for rect in woods_map_button_rectangles:
            click_random_point_in_rectangle(rect)
            
        time.sleep(1)

        # Click the ready button
        ready_button, ready_screenshot = process_template_and_capture_screenshot('./SnippedImages/EFTreadyraidbutton.png', (0, 0, 1920, 1080))
        ready_button_rectangles = match_template_and_draw_rectangle(ready_button, ready_screenshot, threshold=0.45)
        print(ready_button_rectangles)
        for rect in ready_button_rectangles:
            x, y, w, h = rect
            random_x = random.randint(x, x + w)
            random_y = random.randint(y, y + h)
            move_to(random_x, random_y, random.uniform(0.1, 0.25))
            win32api.SetCursorPos((random_x, random_y)) #Doesnt click the ready button, just moves the mouse to the ready button

        # This gets me into a game, I need to read the image when I'm about to get into raid, now I need to press W and shift once to sprint
        # set a time limit to press shift again when my stamina is empty. Then I need a check to see if I have died or not, if I have died, go back to the main menu
        # and reset loop.
        

        if cv2.waitKey(1) == ord('q'):
            break
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

# TODO:
# X Have a way to click the Escape From Tarkov button on the main menu
# / Add way to click the PMC button after the main menu button is clicked, just as a failsafe if PMC isnt already selected
# / Add full screen image (optional) and snip the PMC button to click it and put in file structure
# X Click next button after PMC button is clicked
# X Click woods map button
# X Click ready button
# - Add a way to detect when the game is about to start, set 10 second time.sleep
# - Have bot press shift go in a circle
# - See if the empty stamina detection is working, if not, use time.sleep() to wait for stamina to be empty/full
# - Add template detection for death screen, if dead, go back to main menu