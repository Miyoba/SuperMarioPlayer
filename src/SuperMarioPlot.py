import matplotlib.pyplot as plt
import numpy as np


class SuperMarioPlot:

    def __init__(self):
        self.count = 5
        self.count2 = 0
        self.macroList = []
        self.deathList = []
        self.xlabel = 'x-Achse'
        self.ylabel = 'y-Achse'

    def printPlot(self):
        loc, labels = plt.yticks()
        plt.yticks(np.arange(0, max(loc), step=1))  # make sure the y-Axis only shows whole number values
        loc, labels = plt.xticks()  # make sure the x-Axis shows each x-Value on the axis
        plt.xticks(np.arange(0, max(loc), step=1))
        plt.xlabel(self.xlabel)
        plt.ylabel(self.ylabel)
        plt.show()

    def bestRunPlot(self):
        return

    def sessionPlot(self, macroCycleCount, deathCount):
        self.macroList.append(macroCycleCount)
        self.deathList.append(deathCount)
        self.count2 += 1
        if self.count2 >= self.count:
            self.count2 = 0
            plt.bar(self.macroList, self.deathList)
            self.xlabel = 'Macro Cycle Count'
            self.ylabel = 'Death Count per Cycle'
            self.printPlot()
