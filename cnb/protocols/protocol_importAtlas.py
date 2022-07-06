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
import shutil

from ..objects import AtlasLow
import os
from pwem.protocols.protocol_import.base import ProtImportFiles, ProtImport
from pyworkflow.constants import BETA
from pyworkflow.protocol import params
from pyworkflow.utils import Message
from ..objects.data import *
from datetime import datetime
from pwem.emlib.image import ImageHandler
import numpy as np

class ProtImportAtlas(ProtImport):
    """ Protocol to import Atlas. """
    _label = 'import Atlas'
    _mdoc_file = ''
    _devStatus = BETA

    def _defineParams(self, form):
        form.addSection(label=Message.LABEL_INPUT)
        form.addParam('mrc_file', params.FileParam,
                  label='mrc file',
                  help="Select the Atlas mrc file that contain all the \n"
                           "slices of the Atlas. The protocol will import the"
                       " mdoc file (it has the same name that the mrc file)")

    def readMdocFile(self):
        return str(self.mrc_file.get() + '.mdoc')

    def _insertAllSteps(self):
        self.initializeParams()
        self._insertFunctionStep('readParameters')
        self._insertFunctionStep('createOutputStep')

    def initializeParams(self):
        self.mdoc_file = self.readMdocFile()
        self.headerDict = {}
        self.zvalueList = []


    def readParameters(self):
        mdoc = MDoc(self.mdoc_file)
        hDict, valueList = mdoc.parseMdoc()
        self.zvalueList = []
        self.headerDict = {}
        for k, v in hDict.items():
            self.headerDict[k] = self.getStringType(v)

        for l in valueList:
            dic = {}
            for k, v in l.items():
                dic[k] = self.getStringType(v)
                #print(k, v, dic[k])
            self.zvalueList.append(dic)

        self.createImagesSlices()
        shutil.copyfile(self.mdoc_file, self._getExtraPath(os.path.basename(self.mdoc_file)))



    def createOutputStep(self):
        atlasLow = AtlasLow()
        atlasLow.setObjId(1)
        atlasLow.setFileName(self.mrc_file.get())
        atlasLow.setVoltage(self.headerDict['Voltage'])
        atlasLow.setPixelSpacing(self.headerDict['PixelSpacing'])
        atlasLow.setImageFile(self.headerDict['ImageFile'])
        atlasLow.setImageSize(self.headerDict['ImageSize'])
        atlasLow.setMontage(self.headerDict['Montage'])
        atlasLow.setDataMode(self.headerDict['DataMode'])
        atlasLow.setMagnification(self.zvalueList[0]['Magnification'])
        atlasLow.setBinning(self.zvalueList[0]['Binning'])

        self.info('self._getPath(): {}'.format(self._getPath()))

        setOflmi = SetOfLowMagImages.create(outputPath=self._getPath())
        setOflmi.setAtlasLowID(atlasLow.getObjId())
        self.info('atlasLow.getObjId(): {}'.format(atlasLow.getObjId()))
        #setOflmi.__str__()

        # setOflmi.setVoltage(self.headerDict['Voltage'])
        # setOflmi.setPixelSpacing(self.headerDict['PixelSpacing'])
        # setOflmi.setImageFile(self.headerDict['ImageFile'])
        # setOflmi.setImageSize(self.headerDict['ImageSize'])
        # setOflmi.setMontage(self.headerDict['Montage'])
        # setOflmi.setDataMode(self.headerDict['DataMode'])
        # setOflmi.setMagnification(self.zvalueList[0]['Magnification'])
        # setOflmi.setBinning(self.zvalueList[0]['Binning'])

        for dict in self.zvalueList:
            lmi = AtlasLowImage()

            lmi.setAtlasLowID(atlasLow.getObjId())
            lmi.setPieceCoordinates(dict['PieceCoordinates'])
            lmi.setMinMaxMean(dict['MinMaxMean'])
            lmi.setTiltAngle(dict['TiltAngle'])
            lmi.setStageZ(dict['StageZ'])
            lmi.setIntensity(dict['Intensity'])
            lmi.setExposureDose(dict['ExposureDose'])
            lmi.setDoseRate(dict['DoseRate'])
            lmi.setPixelSpacing(dict['PixelSpacing'])
            lmi.setSpotSize(dict['SpotSize'])
            lmi.setDefocus(dict['Defocus'])
            lmi.setImageShift(dict['ImageShift'])
            lmi.setRotationAngle(dict['RotationAngle'])
            lmi.setExposureTime(dict['ExposureTime'])
            lmi.setBinning(dict['Binning'])
            lmi.setCameraIndex(dict['CameraIndex'])
            lmi.setDividedBy2(dict['DividedBy2'])
            lmi.setOperatingMode(dict['OperatingMode'])
            lmi.setUsingCDS(dict['UsingCDS'])
            lmi.setMagIndex(dict['MagIndex'])
            lmi.setLowDoseConSet(dict['LowDoseConSet'])
            lmi.setCountsPerElectron(dict['CountsPerElectron'])
            lmi.setTargetDefocus(dict['TargetDefocus'])
            lmi.setDateTime(dict['DateTime'])
            lmi.setFilterSlitAndLoss(dict['FilterSlitAndLoss'])
            lmi.setUncroppedSize(dict['UncroppedSize'])
            lmi.setRotationAndFlip(dict['RotationAndFlip'])
            lmi.setAlignedPieceCoords(dict['AlignedPieceCoords'])
            #lmi.setXedgeDxy(dict['XedgeDxy'])
            #lmi.setYedgeDxy(dict['YedgeDxy'])

            setOflmi.append(lmi)


        #atlasLow.setSetOfMagImages(setOflmi)
        self.info('Output: {}'.format(atlasLow.getMagnification()))
        self.debug('Solo si esta activado modo debug')
        #self._defineOutputs(atlasLow=atlasLow)
        self.outputsToDefine = {'atlas': atlasLow, 'setOflmi': setOflmi}
        self._defineOutputs(**self.outputsToDefine)


    def _validate(self):
        pass



    def createImagesSlices(self):
        if os.path.isfile(self.mrc_file.get()):
            atlasImages = ImageHandler().read(self.mrc_file.get())
            images = atlasImages.getData()
            # print('self.mrc_file.get(): {}'.format(self.mrc_file.get()))
            # print(atlasImages)
            # print(np.shape(images))
            for d in range(np.shape(images)[0]):
                slice_image = ImageHandler().createImage()
                sliceMatrix = images[d, :, :]
                slice_image.setData(sliceMatrix)
                numberDigit = str(d).rjust(3, '0')
                slice_image.write(os.path.join(self._getExtraPath(),
                                               '{}_slice.mrc'.format(numberDigit)))




    #UTILS
    def getStringType(self, string):
        if string == 'None':
            return string
        try:#date
            date = datetime.strptime(string, '%d-%b-%y %H:%M:%S')
            return date
        except ValueError:
            pass
        if string.__contains__(' '): #list
            str2Csv = string.replace(' ', ',')
            return str2Csv
        try:#int
            return Integer(string)
        except ValueError:
            pass
        try:#float
            return Float(string)
        except ValueError:
            pass

        return string



# def setAttribute(obj, label, value):
#     if value is None:
#         return
#     setattr(obj, label, getScipionObj(value))