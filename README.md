# TP Image Detection
## Features
This TP plugin allows you to search for an image on a specified screen.
It can return the coordinates of the centre of the image for use with other plugins
and it can return a True or False depending on if the image was found or not.

## Installation
During Installation it will probably say failed to load plugin
in this case just restart TP

## **Usage:**
Both actions use the same style of inputs. Both actions are pretty much the same but one of them will click the centre of the image.
Confidence controls how confident the program has to be in order for it to declare the image as found. This must be a float (eg 80% = 0.8). 
The action also updates the states giving the coords and True or False if the image has been found.

