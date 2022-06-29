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

from ..objects import AtlasLow
import os
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
                           "slices of the Atlas. The protocol will import the"
                       " mdoc file (it has the same name that the mrc file)")

    def readMdocFile(self):
        self.mdcoc_file = str(self.mrc_file.get() + '.mdoc')
        print(type(self.mdcoc_file))


    def _insertAllSteps(self):
        self.initializeParams()
        self._insertFunctionStep('readParameters')
        self._insertFunctionStep('createOutputStep')

    def initializeParams(self):
        self.readMdocFile()
        self.headerDict = {}
        self.zvalueList = []

    def readParameters(self):
        mdoc = MDoc(self.mdoc_file)
        self.headerDict, self.zvalueList = mdoc.parseMdoc()
        # print(headerDict)
        print(self.zvalueList[0]['StagePosition'])
        #TOD O  create objects Low_mag_image

    def createOutputStep(self):
        atlas = AtlasLow()
        atlas.setFileName(self.mrc_file.get())
        atlas.setVoltage(self.headerDict['Voltage'])
        atlas.setPixelSpacing(self.headerDict['PixelSpacing'])
        atlas.setImageFile(self.headerDict['ImageFile'])
        atlas.setImageSize(self.headerDict['ImageSize'])
        atlas.setMontage(self.headerDict['Montage'])
        atlas.setDataMode(self.headerDict['DataMode'])
        atlas.setMagnification(self.zvalueList[0]['Magnification'])
        atlas.setBinning(self.zvalueList[0]['Binning'])

        setOflmi = SetClassOfLowMagImages()

        for dict in self.zvalueList:
            lmi = LowMagImage()

            lmi.setMagnification(dict['Magnification'])
            lmi.setMagnification(dict['Magnification'])
            lmi.setMagnification(dict['Magnification'])
            lmi.setMagnification(dict['Magnification'])
            lmi.setMagnification(dict['Magnification'])
            lmi.setMagnification(dict['Magnification'])
            lmi.setMagnification(dict['Magnification'])
            lmi.setMagnification(dict['Magnification'])



            setOflmi.append(lmi)




        print('Output: {}'.format(atlas.getMagnification()))



        self._defineOutputs(atlas=atlas, )


    def _validate(self):
        pass


# def setAttribute(obj, label, value):
#     if value is None:
#         return
#     setattr(obj, label, getScipionObj(value))