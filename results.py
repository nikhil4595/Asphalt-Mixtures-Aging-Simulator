# -*- coding: utf-8 -*-
"""
Created on Sun Jan 25 16:21:14 2015

@author: sjdps
"""
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

class Result(object):
    def __init__(self, matrix_materials):
        self.materials = matrix_materials
        heatmap = self.thermalResults()
        displacements = self.mechanicalResults()

        plt.figure(1)
        plt.clf() # clear figure
        plt.title('Heat Map')
        plt.imshow(heatmap, interpolation='nearest', cmap=cm.jet)
        plt.colorbar()
        plt.show()

        plt.figure(2)
        plt.clf()
        clines = np.linspace(0., 1., 10) # contour line levels
        plt.title('Displacements field')
        C = plt.contour(displacements, colors='k')
        plt.clabel(C, inline=10, fontsize=10)
        plt.show()

    def thermalResults(self):
        heatmap = np.zeros(self.materials.shape)

        for i in xrange(self.materials.shape[0]):
            for j in xrange(self.materials.shape[1]):
                heatmap[i,j] = self.materials[i,j].temperature

        return heatmap

    def mechanicalResults(self):
        displacements = np.zeros(self.materials.shape)

        for i in xrange(self.materials.shape[0]):
            for j in xrange(self.materials.shape[1]):
                displacements[i,j] = self.materials[i,j].displacement

        return displacements