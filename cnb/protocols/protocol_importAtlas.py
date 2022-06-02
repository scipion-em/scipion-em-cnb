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
        self._insertFunctionStep('readParameters')

    def readParameters(self):
        print('mrc file: {}'.format(self.mrc_file.get()))
        #TODO read all the parameters from mdoc
        #TODO dictionary self.dic

    def createOutputStep(self):
        #TODO create ATLAS_LOW class
        pass

    def _validate(self):
        pass
