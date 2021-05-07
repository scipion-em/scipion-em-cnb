# **************************************************************************
# *
# * Authors:     Daniel Del Hoyo (daniel.delhoyo.gomez@alumnos.upm.es)
# *
# * Unidad de  Bioinformatica of Centro Nacional de Biotecnologia , CSIC
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 2 of the License, or
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

from .protocols import cnbWriteParameter
from pyworkflow.wizard import Wizard
from .constants import *


class writeParameterWizard(Wizard):
  _targets = [(cnbWriteParameter, ['paramsToWrite'])]

  def _getSetType(self, scipionSet):
    return scipionSet.__str__().split()[0]

  def _getWriteIndex(self, protocol):
    if protocol.inputSet.get() != None:
      setType = self._getSetType(protocol.inputSet.get())
      print('Set type: ', setType)
      if setType in setTypeDic:
        return setTypeDic[setType]
      else:
        return UNKNOWNSET
    else:
      return UNKNOWNSET

  def show(self, form):
    form.setVar('paramsToWrite', self._getWriteIndex(form.protocol))