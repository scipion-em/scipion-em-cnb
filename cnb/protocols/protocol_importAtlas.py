# **************************************************************************
# *
# * Authors: Daniel Marchan (da.marchan@cnb.csic.es)
#            Alberto Garcia Mena   (alberto.garcia@cnb.csic.es)
# *
# *
# * Unidad de  Bioinformatica of Centro Nacional de Biotecnologia , CSIC
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 3 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'scipion@cnb.csic.es'
# *
# **************************************************************************

from ..objects import Atlas_Low
from pwem.protocols.protocol_import.base import ProtImportFiles, ProtImport
from pyworkflow.constants import BETA
from pyworkflow.protocol import params
from pyworkflow.utils import Message
from ..objects.data import *

class ProtImportAtlas(ProtImport):
    """ Protocol to import Atlas. """
    _label = 'import Atlas'
    _devStatus = BETA

    def _defineParams(self, form):
        form.addSection(label=Message.LABEL_INPUT)
        form.addParam('mrc_file', params.FileParam,
                  label='mrc file',
                  help="Select the Atlas mrc file that contain all the \n"
                           "slices of the Atlas.")
        form.addParam('mdoc_file', params.FileParam,
                  label='mdoc file',
                  help="Select the Atlas mdoc file that contain the \n"
                           "metadata of the Atlas.")

    def _insertAllSteps(self):
        self.initializeParams()
        self._insertFunctionStep('readParameters')
        self._insertFunctionStep('createOutputStep')

    def initializeParams(self):
        self.headerDict = {}
        self.zvalueList = []
        self.dictAtlas = {}

    def readParameters(self):
        print('mrc file: {}'.format(self.mdoc_file.get()))
        mdoc = MDoc(self.mdoc_file.get())
        low_mag_image = Low_mag_image()
        self.headerDict, self.zvalueList = mdoc.parseMdoc()

        # print(headerDict)
        # print(zvalueDict[0]['YedgeDxy'])
        #T ODO create objects Low_mag_image

    def createOutputStep(self):
        atlas = Atlas_Low()
        atlas.setVoltage(self.headerDict['Voltage'])
        atlas.setPixelSpacing(self.headerDict['PixelSpacing'])
        atlas.setImageFile(self.headerDict['ImageFile'])
        atlas.setImageSize(self.headerDict['ImageSize'])
        atlas.setMontage(self.headerDict['Montage'])
        atlas.setDataMode(self.headerDict['DataMode'])

        atlas.setMagnification(self.zvalueList[0]['Magnification'])
        atlas.setBinning(self.zvalueList[0]['Binning'])




        self._defineOutputs(atlas=atlas)


    def _validate(self):
        pass
