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
from pwem.objects import EMObject, Image, EMSet
from pyworkflow.object import (Float, String, List, Integer)

class AtlasLow(EMObject):
    """Atlas low magnification information"""
    #TO DO create viewers as viewer:tomograms.py scipion-em-tomo
    def __init__(self, **kwargs):
        EMObject.__init__(self, **kwargs)
        self._filename = String()
        self._mdoc = String()
        self._magnification = Float(kwargs.get('magnification', None))
        self._voltage = Float(kwargs.get('voltage', None))
        self._PixelSpacing = Float(kwargs.get('PixelSpacing', None))
        self._ImageFile = String(kwargs.get('ImageFile', None))
        self._ImageSize = List(kwargs.get('ImageSize', None))
        self._Montage = Integer(kwargs.get('Montage', None))
        self._DataMode = Integer(kwargs.get('DataMode', None))


    def setFileName(self, filename):
        """ Use the _objValue attribute to store filename. """
        print("TYPE:" + str(type(filename)))
        self._filename.set(filename)

    def setmDoc(self, filename):
        """ Use the _objValue attribute to store filename. """
        self._mdoc.set(filename)

    def setMagnification(self, _magnification):
        self._magnification = float(_magnification)

    def setVoltage(self, _voltage):
        self._voltage = float(_voltage)

    def setPixelSpacing(self, _PixelSpacing):
        self._PixelSpacing = float(_PixelSpacing)

    def setImageFile(self, _ImageFile):
        self._ImageFile = str(_ImageFile)

    def setImageSize(self, _ImageSize):
        self._ImageSize = _ImageSize

    def setMontage(self, _Montage):
        self._Montage = int(_Montage)

    def setDataMode(self, _DataMode):
        self._DataMode = int(_DataMode)

    def setBinning(self, _Binning):
        self._Binning = int(_Binning)



    def getFileName(self):
        """ Use the _objValue attribute to store filename. """
        return self._filename.get()

    def getmDoc(self):
        """ Use the _objValue attribute to store filename. """
        return self._mdoc.get()

    def getVoltage(self):
        return self._voltage.get()

    def getMagnification(self):
        return self._magnification

    def getPixelSpacing(self):
        return self._PixelSpacing.get()

    def getImageFile(self):
        return self._ImageFile.get()

    def getImageSize(self):
        return self._ImageSize.get()

    def getMontage(self):
        return self._Montage.get()

    def getDataMode(self):
        return self._DataMode.get()

    def getBinning(self):
        return self._Binning.get()


class AtlasMedium(EMObject):
    """Atlas medium magnification information"""

    def __init__(self, **kwargs):
        EMObject.__init__(self, **kwargs)
        self._filename = String()
        self._mdoc = String()
        self._magnification = Float(kwargs.get('magnification', None))
        # Microscope voltage in kV
        self._voltage = Float(kwargs.get('voltage', None))
        self._PixelSpacing = Float(kwargs.get('PixelSpacing', None))
        self._ImageFile = Float(kwargs.get('ImageFile', None))
        self._ImageSize = Float(kwargs.get('ImageSize', None))
        self._Montage = Float(kwargs.get('Montage', None))
        self._DataMode = Float(kwargs.get('DataMode', None))


    def setFileName(self, filename):
        """ Use the _objValue attribute to store filename. """
        self._filename.set(filename)

    def setmDoc(self, filename):
        """ Use the _objValue attribute to store filename. """
        self._mdoc.set(filename)

    def setMagnification(self, _magnification):
        self._magnification = _magnification

    def setVoltage(self, _voltage):
        self._voltage = _voltage

    def setPixelSpacing(self, _PixelSpacing):
        self._PixelSpacing = _PixelSpacing

    def setImageFile(self, _ImageFile):
        self._ImageFile = _ImageFile

    def setImageSize(self, _ImageSize):
        self._ImageSize = _ImageSize

    def setMontage(self, _Montage):
        self._Montage = _Montage

    def setDataMode(self, _DataMode):
        self._DataMode = _DataMode

    def setBinning(self, _Binning):
        self._Binning = _Binning




    def getFileName(self):
        """ Use the _objValue attribute to store filename. """
        return self._filename.get()

    def getmDoc(self):
        """ Use the _objValue attribute to store filename. """
        return self._mdoc.get()

    def getVoltage(self):
        return self._voltage.get()

    def getVMagnification(self):
        return self._magnification.get()

    def getPixelSpacing(self):
        return self._PixelSpacing.get()

    def getImageFile(self):
        return self._ImageFile.get()

    def getImageSize(self):
        return self._ImageSize.get()

    def getMontage(self):
        return self._Montage.get()

    def getDataMode(self):
        return self._DataMode.get()

    def getBinning(self):
        return self._Binning.get()


class LowMagImage(EMObject):
    """ Represents an image (slice) of an Atlas object """

    def __init__(self, location=None, **kwargs):
        EMObject.__init__(self, location, **kwargs)
        self._imageName = String()
        # definition list parameters : https://bio3d.colorado.edu/SerialEM/hlp/html/about_formats.htm
        self._PieceCoordinates = List(kwargs.get('PieceCoordinates', None))
        self._MinMaxMean = List(kwargs.get('MinMaxMean', None))
        self._TiltAngle = Float(kwargs.get('TiltAngle', None))
        self._StagePosition = List(kwargs.get('StagePosition', None))
        self._StageZ = Float(kwargs.get('StageZ', None))
        self._Magnification = Integer(kwargs.get('Magnification', None))
        self._Intensity = Float(kwargs.get('Intensity', None))
        self._ExposureDose = Float(kwargs.get('ExposureDose', None))
        self._DoseRate = Float(kwargs.get('DoseRate', None))
        self._PixelSpacing = Float(kwargs.get('PixelSpacing', None))
        self._SpotSize = Float(kwargs.get('SpotSize', None))
        self._Defocus = Float(kwargs.get('Defocus', None))
        self._ImageShift = List(kwargs.get('ImageShift', None))
        self._RotationAngle = Float(kwargs.get('RotationAngle', None))
        self._ExposureTime = Float(kwargs.get('ExposureTime', None))
        self._Binning = Float(kwargs.get('Binning', None))
        self._CameraIndex = Integer(kwargs.get('CameraIndex', None))
        self._DividedBy2 = Integer(kwargs.get('DividedBy2', None))
        self._OperatingMode = Integer(kwargs.get('OperatingMode', None))
        self._UsingCDS = Integer(kwargs.get('UsingCDS', None))
        self._MagIndex = Integer(kwargs.get('MagIndex', None))
        self._LowDoseConSet = Float(kwargs.get('LowDoseConSet', None))
        self._CountsPerElectron = Integer(kwargs.get('CountsPerElectron', None))
        self._TargetDefocus = Float(kwargs.get('TargetDefocus', None))
        self._DateTime = String(kwargs.get('DateTime', None))
        self._FilterSlitAndLoss = List(kwargs.get('FilterSlitAndLoss', None))
        self._UncroppedSize = List(kwargs.get('UncroppedSize', None))
        self._RotationAndFlip = Integer(kwargs.get('RotationAndFlip', None))
        self._AlignedPieceCoords = List(kwargs.get('AlignedPieceCoords', None))
        self._XedgeDxy = List(kwargs.get('XedgeDxy', None))
        self._YedgeDxy = List(kwargs.get('YedgeDxy', None))

    #imageName
    def setImageName(self, imageName):
        self._imageName.set(imageName)

    def getImageName(self):
        self._imageName.get()
        
    #PieceCoordinates
    def setPieceCoordinates(self, PieceCoordinates):
        self._PieceCoordinates.set(PieceCoordinates)

    def getPieceCoordinates(self):
        self._PieceCoordinates.get()

    #MinMaxMean
    def setMinMaxMean(self, MinMaxMean):
        self._MinMaxMean.set(MinMaxMean)

    def getMinMaxMean(self):
        self._MinMaxMean.get()

    #TiltAngle
    def setTiltAngle(self, TiltAngle):
        self._TiltAngle.set(TiltAngle)

    def getTiltAngle(self):
        self._TiltAngle.get()

    #StagePosition
    def setStagePosition(self, StagePosition):
        self._StagePosition.set(StagePosition)

    def getStagePosition(self):
        self._StagePosition.get()

    #StageZ
    def setStageZ(self, StageZ):
        self._StageZ.set(StageZ)

    def getStageZ(self):
        self._StageZ.get()

    #Magnification
    def setMagnification(self, Magnification):
        self._Magnification.set(Magnification)

    def getMagnification(self):
        self._Magnification.get()

    #Intensity
    def setIntensity(self, Intensity):
        self._Intensity.set(Intensity)

    def getIntensity(self):
        self._Intensity.get()

    #ExposureDose
    def setExposureDose(self, ExposureDose):
        self._ExposureDose.set(ExposureDose)

    def getExposureDose(self):
        self._ExposureDose.get()

    #DoseRate
    def setDoseRate(self, DoseRate):
        self._DoseRate.set(DoseRate)

    def getDoseRate(self):
        self._DoseRate.get()

    #PixelSpacing
    def setPixelSpacing(self, PixelSpacing):
        self._PixelSpacing.set(PixelSpacing)

    def getPixelSpacing(self):
        self._PixelSpacing.get()

    #SpotSize
    def setSpotSize(self, SpotSize):
        self._SpotSize.set(SpotSize)

    def getSpotSize(self):
        self._SpotSize.get()

    #Defocus
    def setDefocus(self, Defocus):
        self._Defocus.set(Defocus)

    def getDefocus(self):
        self._Defocus.get()

    #ImageShift
    def setImageShift(self, ImageShift):
        self._ImageShift.set(ImageShift)

    def getImageShift(self):
        self._ImageShift.get()

    #RotationAngle
    def setRotationAngle(self, RotationAngle):
        self._RotationAngle.set(RotationAngle)

    def getRotationAngle(self):
        self._RotationAngle.get()

    #ExposureTime
    def setExposureTime(self, ExposureTime):
        self._ExposureTime.set(ExposureTime)

    def getExposureTime(self):
        self._ExposureTime.get()

    #Binning
    def setBinning(self, Binning):
        self._Binning.set(Binning)

    def getBinning(self):
        self._Binning.get()

    #CameraIndex
    def setCameraIndex(self, CameraIndex):
        self._CameraIndex.set(CameraIndex)

    def getCameraIndex(self):
        self._CameraIndex.get()

    #DividedBy2
    def setDividedBy2(self, DividedBy2):
        self._DividedBy2.set(DividedBy2)

    def getDividedBy2(self):
        self._DividedBy2.get()

    #OperatingMode
    def setOperatingMode(self, OperatingMode):
        self._OperatingMode.set(OperatingMode)

    def getOperatingMode(self):
        self._OperatingMode.get()

    #UsingCDS
    def setUsingCDS(self, UsingCDS):
        self._UsingCDS.set(UsingCDS)

    def getUsingCDS(self):
        self._UsingCDS.get()

    #MagIndex
    def setMagIndex(self, MagIndex):
        self._MagIndex.set(MagIndex)

    def getMagIndex(self):
        self._MagIndex.get()

    #LowDoseConSet
    def setLowDoseConSet(self, LowDoseConSet):
        self._LowDoseConSet.set(LowDoseConSet)

    def getLowDoseConSet(self):
        self._LowDoseConSet.get()

    #CountsPerElectron
    def setCountsPerElectron(self, CountsPerElectron):
        self._CountsPerElectron.set(CountsPerElectron)

    def getCountsPerElectron(self):
        self._CountsPerElectron.get()

    #TargetDefocus
    def setTargetDefocus(self, TargetDefocus):
        self._TargetDefocus.set(TargetDefocus)

    def getTargetDefocus(self):
        self._TargetDefocus.get()

    #DateTime
    def setDateTime(self, DateTime):
        self._DateTime.set(DateTime)

    def getDateTime(self):
        self._DateTime.get()

    #FilterSlitAndLoss
    def setFilterSlitAndLoss(self, FilterSlitAndLoss):
        self._FilterSlitAndLoss.set(FilterSlitAndLoss)

    def getFilterSlitAndLoss(self):
        self._FilterSlitAndLoss.get()

    #UncroppedSize
    def setUncroppedSize(self, UncroppedSize):
        self._UncroppedSize.set(UncroppedSize)

    def getUncroppedSize(self):
        self._UncroppedSize.get()

    #RotationAndFlip
    def setRotationAndFlip(self, RotationAndFlip):
        self._RotationAndFlip.set(RotationAndFlip)

    def getRotationAndFlip(self):
        self._RotationAndFlip.get()

    #AlignedPieceCoords
    def setAlignedPieceCoords(self, AlignedPieceCoords):
        self._AlignedPieceCoords.set(AlignedPieceCoords)

    def getAlignedPieceCoords(self):
        self._AlignedPieceCoords.get()

    #XedgeDxy
    def setXedgeDxy(self, XedgeDxy):
        self._XedgeDxy.set(XedgeDxy)

    def getXedgeDxy(self):
        self._XedgeDxy.get()

    #YedgeDxy
    def setYedgeDxy(self, YedgeDxy):
        self._YedgeDxy.set(YedgeDxy)

    def getYedgeDxy(self):
        self._YedgeDxy.get()


class SetClassOfLowMagImages(EMSet):
    ITEM_TYPE = LowMagImage
    def __init__(self, **kwargs):
        EMSet.__init__(self, **kwargs)
        self._magnification = Float(kwargs.get('magnification', None))
        self._voltage = Float(kwargs.get('voltage', None))
        self._PixelSpacing = Float(kwargs.get('PixelSpacing', None))
        self._ImageFile = String(kwargs.get('ImageFile', None))
        self._ImageSize = List(kwargs.get('ImageSize', None))
        self._Montage = Integer(kwargs.get('Montage', None))
        self._DataMode = Integer(kwargs.get('DataMode', None))


    def setMagnification(self, _magnification):
        self._magnification = float(_magnification)

    def setVoltage(self, _voltage):
        self._voltage = float(_voltage)

    def setPixelSpacing(self, _PixelSpacing):
        self._PixelSpacing = float(_PixelSpacing)

    def setImageFile(self, _ImageFile):
        self._ImageFile = str(_ImageFile)

    def setImageSize(self, _ImageSize):
        self._ImageSize = _ImageSize

    def setMontage(self, _Montage):
        self._Montage = int(_Montage)

    def setDataMode(self, _DataMode):
        self._DataMode = int(_DataMode)

    def setBinning(self, _Binning):
        self._Binning = int(_Binning)


    def getVoltage(self):
        return self._voltage.get()

    def getMagnification(self):
        return self._magnification

    def getPixelSpacing(self):
        return self._PixelSpacing.get()

    def getImageFile(self):
        return self._ImageFile.get()

    def getImageSize(self):
        return self._ImageSize.get()

    def getMontage(self):
        return self._Montage.get()

    def getDataMode(self):
        return self._DataMode.get()

    def getBinning(self):
        return self._Binning.get()


    # def append(self, image):
    #     """ Add a image to the set. """
    #     EMSet.append(self, image)



class MDoc:
    """class define mdoc files from SerialEM
    This format consists of keyword-value pairs organized into blocks
    called sections.
    A section begins with a bracketed key-value pair:
      [sectionType = name]
    where the section "name" or value will typically be unique.
    Lines below a section header of the form
      key = value
    provide data associated with that section.

    In addition, key-value pairs can occur at the beginning of the file,
    before any section header, and these are referred to as global values.
    Files with extension ".mdoc" provides data about an MRC file and has
    the same name as the image file, with the additional extension ".mdoc".
    In these files, the main section type is "ZValue" and the name
    for each section is the Z value of the image in the file, numbered from 0.
    A description of each key is available at URL:
    https://bio3d.colorado.edu/SerialEM/hlp/html/about_formats.htm

    Additional information may be stored in section headers of the type "T"
    (i.e. [T  a = b ]). In theory these information in also stored in the
    "titles" of the MRC files.
    """

    def __init__(self, fileName):
        self._mdocFileName = str(fileName)

    def parseMdoc(self):
        """
        Parse the mdoc file and return a list with a dict key=value for each
        of the [Zvalue = X] sections and a dictionary for the first lines
        global variables.

        :return: dictionary (header), list of dictionaries (Z slices)
        """
        headerDict = {}
        headerParsed = False
        zvalueList = []  # list of dictionaries with
        with open(self._mdocFileName) as f:
            for line in f:
                #print(line)
                if line.startswith('[ZValue'):  # each tilt movie
                    # We have found a new z value
                    headerParsed = True
                    zvalue = int(line.split(']')[0].split('=')[1])
                    if zvalue != len(zvalueList):
                        raise Exception("Unexpected ZValue = %d" % zvalue)
                    zvalueDict = {}
                    zvalueList.append(zvalueDict)
                elif line.startswith('[T'):  # auxiliary global information
                    strLine = line.strip().replace(' ', '').\
                                           replace(',', '').lower()
                    headerDict['auxiliary'] = strLine
                elif line.strip():  # global variables no in [T sections]
                    key, value = line.split('=')
                    if not headerParsed:
                        headerDict[key.strip()] = value.strip()
                    if zvalueList:
                        zvalueDict[key.strip()] = value.strip()

        return headerDict, zvalueList

