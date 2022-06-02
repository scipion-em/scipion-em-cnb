# -*- coding: utf-8 -*-
# **************************************************************************
# *
# * Authors:     Alberto Garcia Mena (alberto.garcia@cnb.csic.es)
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

from pwem.protocols.protocol import EMProtocol
from pwem.objects import SetOfCTF, Set
from pyworkflow.protocol import params, STATUS_NEW
from pyworkflow.utils import Message
from ..constants import *
import pyworkflow.protocol.constants as pwcts
import os, pickle
from datetime import datetime
import json
import requests
import ftplib
import os
import shutil
from pwem.objects import Movie, SetOfMovies, Float, String
import pyworkflow.utils as pwutils

class cnbManageThreshold(EMProtocol):
    """
    This protocol will store the astigmatism, coma and defocus, check a
    threshold for this parameters and call SerialEm to correct the value
    """
    _label = 'Manage threshold parameters'

    def __init__(self, **kwargs):
        EMProtocol.__init__(self, **kwargs)
        self.stepsExecutionMode = pwcts.STEPS_PARALLEL

    # -------------------------- DEFINE param functions ----------------------
    def _defineParams(self, form):
        form.addSection(label=Message.LABEL_INPUT)
        form.addParam('inputSet', params.PointerParam,
                      pointerClass='EMSet',
                      label='Set of interest', important=True,
                      help='Set where to extract the parameters of interest')
        form.addParam('writePath', params.FileParam,
                      default=os.getcwd()+'/',
                      label='SerialEM comunincation folder', important=True,
                      help='Folder path where to write the rscript to SerialEM')

        form.addParam('comaThreshold', params.FloatParam,
                      default=1, label='Coma Threshold',
                      help='Set the value of the coma threshold')

        form.addParam('astigmatismThreshold', params.FloatParam,
                      default=1, label='Astigmatism Threshold',
                      help='Set the value of the astigmatism threshold')

        form.addParam('defocusThreshold', params.FloatParam,
                      default=1, label='Defocus Threshold',
                      help='Set the value of the defocus threshold')


        form.addParallelSection(threads=1, mpi=1)

        self._defineStreamingParams(form)

    # --------------------------- STEPS functions ------------------------------
    def _insertAllSteps(self):
        pass

    def _stepsCheck(self):
        newDeps = []
        if not self.ended:
            pass


    def closeSetStep(self):
        """ Close the registered set. """
        pass
    # --------------------------- INFO functions -----------------------------------
    def _summary(self):
        """ Summarize what the protocol has done"""
        summary = []
        summary.append("Salida para probar pycharm.")
        return summary

    def _methods(self):
        methods = []

        return methods
