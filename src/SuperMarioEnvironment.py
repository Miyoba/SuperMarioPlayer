import gym_super_mario_bros
import os
from nes_py.wrappers import JoypadSpace
import time


import datetime
import src.SuperMarioImages as SuperMarioImages
import src.SuperMarioMovement as SuperMarioMovement
import src.SuperMarioMarkov as SuperMarioMarkov
import src.SuperMarioMap as SuperMarioMap
import src.SuperMarioReinforcedLearning as SuperMarioReinforcedLearning
import src.SuperMarioConsoleDebugWindow as SuperMarioConsoleDebugWindow
from src.SuperMarioConfig import SuperMarioConfig as SuperMarioConfig


class SuperMarioEnvironment:

    def startPlayer(self):

        # SuperMarioConfig needs a concrete object to use json encoding/decoding
        config = SuperMarioConfig("SuperMarioConfig.json")

        # map = SuperMarioMap.Mario2DMap()
        movement = SuperMarioMovement.Movement(map)
        # images = SuperMarioImages.Images(config.imageDetectionConfiguration, config.imageAssetsDirectory, config.debugAll)
        # debugWindow = SuperMarioConsoleDebugWindow.SuperMarioConsoleDebugWindow(config.WindowsConsoleOutput)
        # markovMovement = SuperMarioMarkov.SuperMarioMarkov(map, config.markovStatesPath, config.markovStateDimensions)
        reinforcedLearningMovement = SuperMarioReinforcedLearning.SuperMarioReinforcedLearning()

        # images.loadAllAssets()

        # Instantiating Super Mario Bros. environment
        env = JoypadSpace(gym_super_mario_bros.make('SuperMarioBros-v0').env, movement.COMPLEX_MOVEMENT)
        # debugWindow.clear()

        consoleFrameCount = 0
        renderFrameCount = 0
        done = True
        reward = 0
        calculatedAction = 0
        learningCycle = 0
        max_x_pos = 100
        watch_replay = False
        replay_path = os.path.join("best_runs", "12022021-205633_replay.txt")
        replay = []
        now = datetime.datetime.now()
        runTime = now.strftime("%m%d%Y-%H%M%S")
        newBest = False


        if watch_replay:
            with open(replay_path, "r") as file:
                for line in file:
                    calculatedAction = int(line.strip())
                    env.step(calculatedAction)
                    env.render()
                    time.sleep(0.02)
            return


        # reinforcedLearningMovement.loadNeuralNetwork() <- takes last save
        # reinforcedLearningMovement.loadNeuralNetwork(modelpath="best_runs/12022021-205633_best.h5", statspath="best_runs/12022021-205633_best.txt") <- if you want to load specific save

        # if you want to start a new network
        # reinforcedLearningMovement.initNeuralNetwork()
        # reinforcedLearningMovement.saveNeuralNetwork()

        state, reward, done, info = env.step(0)
        while True:
            # if info["x_pos"] > 200:
                # print("ABC")

            # Identify current theme
            # currentTheme = config.themeIdentifier[str(info["world"])][str(info["stage"])]
            # print(currentTheme)

            # Detecting for all relevant kind of obstacles
            # images.processImage(state)
            # map.resetMap(False)

            # detectedAssetsAndCorrespondingSymbol = images.detectOnlyThemeSpecificAssets(currentTheme)
            # map.changeMapAll(detectedAssetsAndCorrespondingSymbol)

            # visualization
            if consoleFrameCount >= config.ConsoleFramerate:
                # debugWindow.debugPrint(map.toString())
                consoleFrameCount = 0
            else:
                consoleFrameCount = consoleFrameCount + 1

            if renderFrameCount >= config.RenderFramerate:
                env.render()
                renderFrameCount = 0
            else:
                renderFrameCount = renderFrameCount + 1

            # execute action
            # calculatedAction = markovMovement.nextStep(info["y_pos"])
            if reward==0:
                reward = -1

            calculatedAction = reinforcedLearningMovement.nextStep(reward, calculatedAction, state)
            #calculatedAction = movement.move()
            # debugWindow.debugPrint(map.toString() + "\n" + "Calculated Action: " + str(calculatedAction))
            # debugWindow.debugPrint("Hello World")
            # print(reward)
            state, reward, done, info = env.step(calculatedAction)
            replay.append(calculatedAction)

            if info["x_pos"] > max_x_pos:
                max_x_pos = info["x_pos"]
                newBest = True

            if done:
                if newBest:
                    newBest = False
                    with open(os.path.join("best_runs", runTime + "_replay.txt"), "w+") as file:
                        for action in replay:
                            file.write(str(action) + "\n")
                    replay.clear()
                    os.rename("saved_model.h5", os.path.join("best_runs",runTime + "_best.h5"))
                    os.rename("saved_model_stats.txt", os.path.join("best_runs", runTime + "_best.txt"))
                reinforcedLearningMovement.saveNeuralNetwork()
                env.reset()

        env.close()
