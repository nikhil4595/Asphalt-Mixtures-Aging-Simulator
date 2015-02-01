# -*- coding: utf-8 -*-
"""
Created on Fri Jan 16 20:33:56 2015

@author: Santiago
"""

from thermal_model import ThermalModel
#from fem_mechanics import FEMMechanics
import numpy as np
from material import Material
import copy

class SimulationEngine(object):
    def __init__(self, aggregate_parameters, mastic_parameters,
                                  air_parameters, collection, slice_id=50):

        # [0] ---> young modules
        # [1] ---> thermical conductivity
        # [2] ---> chemical value
        self.mastic = Material(mastic_parameters[0], mastic_parameters[1],
                               mastic_parameters[2])
        self.aggregate = Material(aggregate_parameters[0], aggregate_parameters[1],
                                   aggregate_parameters[2])
        self.airvoid = Material(air_parameters[0], air_parameters[1],
                                air_parameters[2])

        vertical_slice = self.loadVerticalSlice(collection, slice_id=50)

        # Structure data where the simulation takes place
        self.matrix_materials = self.getMatrixMaterials(vertical_slice)

#        self.techanics = FEMMechanics(self.material)

#        self.thermicalConstantsMatrix = self.assignThermicalProperties(self.vertical_slice)
#        self.assignMechanicalProperties(self.vertical_slice)
#        self.generalStiffnessMatrixAssemble(self.vertical_slice.shape)


    def loadVerticalSlice(self, collection, slice_id):
        """Cut the slice of the collection in the position id"""
        vertical_slice = collection[:, :, slice_id]
        return vertical_slice.transpose()

    def getMatrixMaterials(self, vertical_slice):
        """Create the matrix material from a vertical slice"""
        material_matrix = np.empty(vertical_slice.shape, dtype=object)

#        salida = vertical_slice
#
#        plt.imshow(salida)
##        plt.imshow(salida, cmap=cm.jet, interpolation='nearest', origin='lower')
#        plt.colorbar()
#        plt.show()
#        np.set_printoptions(threshold=np.inf, linewidth=np.inf)
#        with open('mapa_termico.txt', 'w') as f:
#            f.write(np.array2string(salida, separator=', '))

        for (x,y), _ in np.ndenumerate(vertical_slice):
            if vertical_slice[x, y] == 2:
                material_matrix[x,y] = copy.deepcopy(self.aggregate)
            elif vertical_slice[x,y] == 1:
                material_matrix[x,y] = copy.deepcopy(self.mastic)
            elif vertical_slice[x,y] == 0:
                material_matrix[x,y] = copy.deepcopy(self.airvoid)

        print "matriz de materiales creada de tamano", material_matrix.shape
        return material_matrix

    def simulationCicle(self, no_mech_iter=1, no_thermal_iter=200,
                        no_chemic_iter=1):
        max_TC = max(self.mastic.thermal_conductivity,
                     self.airvoid.thermal_conductivity,
                     self.aggregate.thermal_conductivity)

        temp_ambient = self.getTempAmbient()

        self.thermal = ThermalModel(self.matrix_materials, max_TC)
        self.thermal.applySimulationConditions()
        self.matrix_materials = self.thermal.simulate()

        return self.matrix_materials

    def getTempAmbient(self):
        temp_ambient = 50
        return temp_ambient