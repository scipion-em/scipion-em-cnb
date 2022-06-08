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
from pwem.objects import EMObject, Image
from pyworkflow.object import (Float, String, List, Integer)

class Atlas_Low(EMObject):
    """Atlas low magnification information"""
    #T ODO create viewers as viewer:tomograms.py scipion-em-tomo
    def __init__(self, **kwargs):
        EMObject.__init__(self, **kwargs)
        self._filename = String()
        self._mdoc = String()
        self._magnification = Float(kwargs.get('magnification', None))
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



class Atlas_Medium(EMObject):
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



class Low_mag_image(Image):
    """ Represents an image (slice) of an Atlas object """

    def __init__(self, location=None, **kwargs):
        Image.__init__(self, location, **kwargs)
        self._imageName = String()

        # definition list parameters : https://bio3d.colorado.edu/SerialEM/hlp/html/about_formats.htm
        self.PieceCoordinates = List(kwargs.get('PieceCoordinates', None))
        self.MinMaxMean = List(kwargs.get('MinMaxMean', None))
        self.TiltAngle = List(kwargs.get('TiltAngle', None))
        self.StagePosition = List(kwargs.get('StagePosition', None))
        self.StageZ = List(kwargs.get('StageZ', None))
        self.Magnification = Integer(kwargs.get('Magnification', None))
        self.Intensity = Float(kwargs.get('Intensity', None))
        self.ExposureDose = Float(kwargs.get('ExposureDose', None))
        self.DoseRate = Float(kwargs.get('DoseRate', None))
        self.PixelSpacing = Float(kwargs.get('PixelSpacing', None))
        self.SpotSize = Float(kwargs.get('SpotSize', None))
        self.Defocus = Float(kwargs.get('Defocus', None))
        self.ImageShift = List(kwargs.get('ImageShift', None))
        self.RotationAngle = Float(kwargs.get('RotationAngle', None))
        self.ExposureTime = Float(kwargs.get('ExposureTime', None))
        self.Binning = Float(kwargs.get('Binning', None))
        self.CameraIndex = Integer(kwargs.get('CameraIndex', None))
        self.DividedBy2 = Integer(kwargs.get('DividedBy2', None))
        self.OperatingMode = Integer(kwargs.get('OperatingMode', None))
        self.UsingCDS = Integer(kwargs.get('UsingCDS', None))
        self.MagIndex = Integer(kwargs.get('MagIndex', None))
        self.LowDoseConSet = Float(kwargs.get('LowDoseConSet', None))
        self.CountsPerElectron = Integer(kwargs.get('CountsPerElectron', None))
        self.TargetDefocus = Float(kwargs.get('TargetDefocus', None))
        self.DateTime = String(kwargs.get('DateTime', None))
        self.FilterSlitAndLoss = List(kwargs.get('FilterSlitAndLoss', None))
        self.UncroppedSize = List(kwargs.get('UncroppedSize', None))
        self.RotationAndFlip = Integer(kwargs.get('RotationAndFlip', None))
        self.AlignedPieceCoords = List(kwargs.get('AlignedPieceCoords', None))
        self.XedgeDxy = List(kwargs.get('XedgeDxy', None))
        self.YedgeDxy = List(kwargs.get('YedgeDxy', None))

    def setImageName(self, imageName):
        self._imageName.set(imageName)

    def getImageName(self):
        if self._imageName.get():
            return self._imageName.get()
        else:
            self.getFileName()




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
        self._mdocFileName = fileName

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
                elif line.strip():  # global variables no in [T sections]
                    key, value = line.split('=')
                    if not headerParsed:
                        headerDict[key.strip()] = value.strip()
                    if zvalueList:
                        zvalueDict[key.strip()] = value.strip()

        return headerDict, zvalueList
