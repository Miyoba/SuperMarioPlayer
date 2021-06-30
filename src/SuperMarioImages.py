from PIL import Image
import numpy as np
import cv2

from src.SuperMarioConfig import SuperMarioConfig as SuperMarioConfig

##
# This class deals with everything related to the detection of obstacles in the game.
# Furthermore it contains a function to convert the state array generated by gym_super_mario bros into Images.
# @author Wolfgang Mair, Lukas Geyrhofer
# @version 18. January 2021
##

class Images:
   
    def __init__(self, imageDetectionConfiguration, imageAssetsDirectory, debugAll):
        # Initializing img_gray and state for later use in detection functions
        self.__img_gray = 0
        self.__state = 0

        # To save Image Data received from SuperMarioConfig (JSON FIle) and ready to use assets for OpenCV2
        self.__imageDetectionConfiguration = imageDetectionConfiguration
        self.__imageAssetsDirectory = imageAssetsDirectory
        self.__AssetsForCV2 = {}
        self.__debugAll = debugAll

    ##
    # Converts all the assets into a format so that openCV can work with them.
    # @author Lukas Geyrhofer
    #
    ##
    def loadAllAssets(self):
        for asset in self.__imageDetectionConfiguration:
            print(self.__imageDetectionConfiguration[asset]["fileName"])
            fullPathToAsset = self.__imageAssetsDirectory + self.__imageDetectionConfiguration[asset]["fileName"]
            self.__AssetsForCV2[asset] = cv2.imread(fullPathToAsset, 0)



    ##
    # Converts the current state array of the game into an grayscale image to be used for detection
    # by opencv2
    # @author Lukas Geyrhofer
    # 
    # @param state State array provided by the gym-super-mario-bros class of type ndarray:(240, 256, 3)
    ##

    def processImage(self, state):
        self.__state = state

        # converts state (pixel array) to image
        img = Image.fromarray(self.__state, 'RGB')
        self.__img_gray = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)

    ##
    # Checks for every asset if it is associated with the current theme. If there is a match the function tries
    # to detect the asset in the current frame. All locations that are found are written into a dictionary as value with the
    # corresponding detection symbol as key. Returns that dictionary.
    # @author Lukas Geyrhofer
    #
    # @param currentTheme Current Theme detected at the current picture
    ##

    def detectOnlyThemeSpecificAssets(self, currentTheme):
        detectedAssets = {}
        for asset in self.__imageDetectionConfiguration:
            assetData = self.__imageDetectionConfiguration[asset]
            for theme in assetData["levelTheme"]:
                if theme == currentTheme:
                    resemblanceValue = cv2.matchTemplate(self.__img_gray, self.__AssetsForCV2[asset], cv2.TM_CCOEFF_NORMED)
                    loc = np.where(resemblanceValue >= assetData["threshold"])

                    if len(loc[0]) != 0:
                        loc[0][:] = loc[0][:] - assetData["correctionY"]
                        loc[1][:] = loc[1][:] - assetData["correctionX"]
                        detectedAssets[assetData["detectionSymbol"]] = loc

                    if assetData["debug"] or self.__debugAll:
                        self.writeDebugDataForDetection(loc, assetData["color"])


        return detectedAssets


    ##
    # Colors the y and x axis of the point(s) in loc
    # @author Lukas Geyrhofer
    # @param loc Location of the Point which is to mark
    # @param color Color which shall be used to mark detections in debug mode
    ##

    def writeDebugDataForDetection(self, loc, color):
        for pt in zip(*loc[::-1]):
                # cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
                # print(pt[0], pt[1])
                self.__state[:, pt[0]] = color
                self.__state[pt[1], :] = color
                print("Object position x:", pt[0] / 16, "Object position y:", pt[1] / 16, "\n")