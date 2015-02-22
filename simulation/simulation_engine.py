'''
Copyright (C) 2015 Jeison Pacateque, Santiago Puerto

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
'''

from thermal_model import ThermalModel
from fem_mechanics import FEMMechanics
import numpy as np
from material import Material
import copy

class SimulationEngine(object):
    """
    This class configures the sample as a materials array in order to run the
    simulations defined in the thermal, mechanical and chemical models.
    """
    def __init__(self, aggregate_parameters, mastic_parameters, air_parameters, collection, slice_id=50, steps=10000):

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

    def loadVerticalSlice(self, collection, slice_id):
        """Cut the slice of the collection in the position id"""
        vertical_slice = collection[:, :, slice_id]
        return vertical_slice.transpose()

    def getMatrixMaterials(self, vertical_slice):
        """Create the matrix material from a vertical slice"""
        material_matrix = np.empty(vertical_slice.shape, dtype=object)

        for (x,y), _ in np.ndenumerate(vertical_slice):
            if vertical_slice[x, y] == 2:
                material_matrix[x,y] = copy.deepcopy(self.aggregate)
            elif vertical_slice[x,y] == 1:
                material_matrix[x,y] = copy.deepcopy(self.mastic)
            elif vertical_slice[x,y] == 0:
                material_matrix[x,y] = copy.deepcopy(self.airvoid)

        print "Materials matrix created, size:", material_matrix.shape
        return material_matrix

    def simulationCicle(self, no_mech_iter=1, no_thermal_iter=200,
                        no_chemic_iter=1):
#==============================================================================
#       Thermal model implementation (Every model should run on a loop)
#==============================================================================
        max_TC = max(self.mastic.thermal_conductivity,
                     self.airvoid.thermal_conductivity,
                     self.aggregate.thermal_conductivity)

        temp_ambient = self.getTempAmbient()
        self.thermal = ThermalModel(self.matrix_materials, max_TC)
        self.thermal.applySimulationConditions()
        self.matrix_materials = self.thermal.simulate(no_thermal_iter)
#==============================================================================
#       Mechanical model implementation
#==============================================================================
        self.mechanics = FEMMechanics(self.matrix_materials)
        self.mechanics.applySimulationConditions(800)
        self.mechanics.simulate()

        return self.matrix_materials

    def getTempAmbient(self):
        """
        Returns the ambient temperature set on the Configure Simulation dialog
        """
        temp_ambient = 50
        return temp_ambient