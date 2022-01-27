import mss
import numpy as np
import TouchPortalAPI  # Import the api
import cv2
import pyautogui
Debug = True
# Initiate the client (replace YourPluginID with your ID)
TPClient = TouchPortalAPI.Client('TP.Lucid.ImageDetection')

# This event handler will run once when the client connects to TouchPortal


def find_image(template_file, monitor, confidence):
    with mss.mss() as mss_instance:  # Create a new mss.mss instance
        # Identify the display to capture
        monitor = mss_instance.monitors[monitor]
    with mss.mss() as sct:
        img = np.array(sct.grab(monitor))

        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  # weird work around
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        if Debug == True:
            cv2.imshow("img", img)  # used for debugging
            cv2.waitKey()
    # find the template in img using open cv template matching methods
    template = cv2.imread(template_file)
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    if Debug == True:
        print(template.shape)

    if max_val >= confidence:
        with mss.mss() as mss_instance:
            if Debug == True:
                print(mss_instance.monitors)
            location = monitor["left"]
            monitor1 = mss_instance.monitors[1]
            heightdifference = monitor["height"]-monitor1["height"]
            if Debug == True:
                print(heightdifference)
        x, y = (max_loc[0]+template.shape[1], max_loc[1]+template.shape[0])

        if Debug == True:
            print(max_loc[0]+(template.shape[0]/2) +
                  location, max_loc[1]+(template.shape[1]/2))
        img = cv2.rectangle(
            img, max_loc, (x, y), (255, 0, 0), 2)

        if Debug == True:
            cv2.imshow("img", img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            print(max_loc[0]+(template.shape[0]/2) + location,
                  max_loc[1]+(template.shape[1]/2))
        return (max_loc[0]+(template.shape[1]/2) + location, (max_loc[1]+(template.shape[0]/2)-heightdifference)), True
    else:
        return (0, 0), False


@TPClient.on('info')
def onStart(data):
    global Debug
    # `data` is a Python `dict` object created from de-serialized JSON data sent by TP.
    print('I am Connected!', data)
    Debug = (data['settings'][0]["Debug"])
    print(Debug)


# Action handlers, called when user activates one of this plugin's actions in Touch Portal.


@TPClient.on('action')
def onActions(data):
    print(data)
    template = data["data"][0]["value"]
    monitor = int(float(data["data"][1]["value"]))
    confidence = float(data["data"][2]["value"])
    coordinates, found = find_image(template, monitor, confidence)
    print("finished running action")
    TPClient.stateUpdate("Found", f"{found}")
    print(coordinates[0])
    coords = [
        {
            "id": "xcoord",
            "value": f"{coordinates[0]}"
        },
        {
            "id": "ycoord",
            "value": f"{coordinates[1]}"
        }
    ]
    TPClient.stateUpdateMany(coords)
    if data["actionId"] == "Lucid.ImageDetection":
        _ = pyautogui.position()
        pyautogui.click(coordinates)
        pyautogui.moveTo(_)

# This function gets called every time when someone changes something in your plugin settings


@ TPClient.on('settings')
def onSettings(data):
    print('received data from settings!')
    print(data['values'])
    global Debug
    Debug = (data['values'][0]["Debug"])

# Shutdown handler, called when Touch Portal wants to stop your plugin.


@ TPClient.on('closePlugin')
def onShutdown(data):
    print('Received shutdown message!')
    # Terminates the connection and returns from connect()
    TPClient.disconnect()


# Connect to Touch Portal and block (wait) until disconnected
TPClient.connect()
# add comments to the code above:
import mss

