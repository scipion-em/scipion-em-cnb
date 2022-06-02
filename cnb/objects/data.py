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
from pwem.objects import EMObject
from pyworkflow.object import (Float, String)

class Atlas_Low(EMObject):
    """Atlas low magnification information"""

    def __init__(self, **kwargs):
        EMObject.__init__(self, **kwargs)
        self._filename = String()
        self._mdoc = String()
        self._magnification = Float(kwargs.get('magnification', None))
        # Microscope voltage in kV
        self._voltage = Float(kwargs.get('voltage', None))


    def getFileName(self):
        """ Use the _objValue attribute to store filename. """
        return self._filename.get()

    def setFileName(self, filename):
        """ Use the _objValue attribute to store filename. """
        self._filename.set(filename)

    def getmDoc(self):
        """ Use the _objValue attribute to store filename. """
        return self._mdoc.get()

    def setmDoc(self, filename):
        """ Use the _objValue attribute to store filename. """
        self._mdoc.set(filename)


    def setMagnification(self, _magnification):
        self._magnification = _magnification

    def setVoltage(self, _voltage):
        self._voltage = _voltage

    def getVoltage(self):
        return self._voltage.get()

    def getVMagnification(self):
        return self._magnification.get()


class Atlas_Medium(EMObject):
    """Atlas medium magnification information"""

    def __init__(self, **kwargs):
        EMObject.__init__(self, **kwargs)
        self._filename = String()
        self._mdoc = String()
        self._magnification = Float(kwargs.get('magnification', None))
        # Microscope voltage in kV
        self._voltage = Float(kwargs.get('voltage', None))


    def getFileName(self):
        """ Use the _objValue attribute to store filename. """
        return self._filename.get()

    def setFileName(self, filename):
        """ Use the _objValue attribute to store filename. """
        self._filename.set(filename)

    def getmDoc(self):
        """ Use the _objValue attribute to store filename. """
        return self._mdoc.get()

    def setmDoc(self, filename):
        """ Use the _objValue attribute to store filename. """
        self._mdoc.set(filename)

    def setMagnification(self, _magnification):
        self._magnification = _magnification

    def setVoltage(self, _voltage):
        self._voltage = _voltage

    def getVoltage(self):
        return self._voltage.get()

    def getVMagnification(self):
        return self._magnification.get()