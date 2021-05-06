# -*- coding: utf-8 -*-
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

from pwem.protocols.protocol import EMProtocol
from pwem.objects import SetOfCTF, Set
from pyworkflow.protocol import params, STATUS_NEW
from pyworkflow.utils import Message
from ..constants import *
import pyworkflow.protocol.constants as pwcts
import os, pickle
from datetime import datetime


class cnbWriteParameter(EMProtocol):
    """
    This protocol will store the ctf phaseshift in a determined file to be parse by SerialEM
    """
    _label = 'Write parameter'

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
        form.addParam('paramsToWrite', params.EnumParam, default=UNKNOWNSET,
                      label='Parameters to write',
                      choices= SetChoices,
                      help='List of parameters which will be written from the selected protocol')
        form.addParam('numberOfLines', params.IntParam, default=1,
                      label="Number of parameter lines", expertLevel=pwcts.LEVEL_ADVANCED,
                      help='Number of parameter lines (of objects) to write in the file')
        form.addParam('writeHeader', params.BooleanParam, default=True,
                      label="Write header", expertLevel=pwcts.LEVEL_ADVANCED,
                      help='Write a header containing the parameter names')
        form.addParam('addTime', params.BooleanParam, default=True,
                      label="Add line time", expertLevel=pwcts.LEVEL_ADVANCED,
                      help='Writes also the instant when the new line is added')

        form.addParam('writePath', params.FileParam,
                      default=os.getcwd()+'/',
                      label='Output folder', important=True,
                      help='Folder path where to save the parameters')

        form.addParam('writeFilename', params.StringParam,
                      default='parameters.txt', label='Filename',
                      help='Name of the saved file')
        form.addParallelSection(threads=1, mpi=1)

        self._defineStreamingParams(form)

    # --------------------------- STEPS functions ------------------------------
    def _insertAllSteps(self):
        self._insertFunctionStep('initializeStep')
        self.closeSet = self._insertFunctionStep('closeSetStep', wait=True)

    def _stepsCheck(self):
        newDeps = []
        if not self.ended:
            closeStep = self._getFirstJoinStep()
            inputSet = self.inputSet.get()
            doneParams = self.pickleLoad(self.doneParamsFn)

            if len(inputSet) > len(doneParams):
                newDeps.append(self._insertFunctionStep('getLastObjectStep', prerequisites=[]))
                newDeps.append(self._insertFunctionStep('writeParameterStep', prerequisites=[newDeps[-1]]))
                closeStep.addPrerequisites(*newDeps)
            if self.checkIfParentFinished():
                closeStep.setStatus(STATUS_NEW)

            self.updateSteps()

    def initializeStep(self):
      self.doneParamsFn = self._getExtraPath('doneParams.pickle')
      if not os.path.exists(self.doneParamsFn):
        self.pickleSave(set([]), self.doneParamsFn)

      self.outFile = self.writePath.get() + self.getOutputFileName()
      with open(self.outFile, 'w') as f:
        if self.writeHeader.get():
          f.write(self.getHeader())
      self.writtenIds, self.ended = [], False

    def getLastObjectStep(self):
        scipionSet = self.inputSet.get()
        if len(scipionSet)>0:
          doneParams = self.pickleLoad(self.doneParamsFn)
          for obj in scipionSet:
            if not obj.getObjId() in doneParams:
              doneParams.add(obj.getObjId())

          self.lastObject = obj
          self.pickleSave(doneParams, self.doneParamsFn)
        else:
            self.lastObject = None

    def writeParameterStep(self):
        if self.lastObject != None:
            print('Writing new object parameters in {}'.format(self.outFile))
            self.writeLastObject()
            self.writtenIds.append(self.lastObject.getObjId())
        else:
            print('Selected CTFs has no phaseShift associated')

    def closeSetStep(self):
      self.registerNewObjects()
      self.ended = True

    # --------------------------- INFO functions -----------------------------------
    def _summary(self):
        """ Summarize what the protocol has done"""
        summary = []

        return summary

    def _methods(self):
        methods = []

        return methods

    # --------------------------- UTILS functions -----------------------------------
    def getItemParams(self, obj):
      '''Returns a list with the values of the attributes of the object listed in constants.py'''
      params = []
      for atr in paramatersDic[self.paramsToWrite.get()]['item']:
        if hasattr(obj, atr):
          params.append(self.getObjAttribute(obj, atr))
        else:
          print('Attribute {} not found in object {}'.format(atr, obj))
      return params

    def getSetParams(self):
      '''Returns a list with the values of the attributes of the input set listed in constants.py'''
      params = []
      scipionSet = self.inputSet.get()
      for atr in paramatersDic[self.paramsToWrite.get()]['set']:
        if hasattr(scipionSet, atr):
          params.append(self.getObjAttribute(scipionSet, atr))
        else:
          print('Attribute {} not found in set {}'.format(atr, scipionSet))
      return params

    def getObjAttribute(self, obj, atr):
      '''Return the value of the object attribute'''
      try:
        objAtr = getattr(obj, atr, 'None').get()
      except:
        objAtr = getattr(obj, atr, 'None')
      return objAtr

    def getHeader(self):
      '''Return the header containing the attributes names'''
      headerList = paramatersDic[self.paramsToWrite.get()]['item'] + \
                   paramatersDic[self.paramsToWrite.get()]['set']
      header = '#' + '\t'.join(headerList)
      if self.addTime.get():
        header += '\tTime'
      header += '\n'
      return header

    def writeLastObject(self):
      '''Updates the parameters file with the last object'''
      obj = self.lastObject
      allParams = self.getItemParams(obj) + self.getSetParams()
      wParams = '\t'.join(map(str, allParams))
      if self.addTime.get():
        wParams += '\t' + datetime.now().strftime("%d/%m/%Y %H:%M:%S")
      wParams += '\n'

      self.updateParamsFile(wParams)

    def updateParamsFile(self, newParams):
      '''Update the parameter file with the new line'''
      nLines = self.numberOfLines.get()
      if not self.writeHeader.get():
        nLines -= 1

      prevF = open(self.outFile, 'r').readlines()
      with open(self.outFile, 'w') as f:
        if self.writeHeader.get():
          f.write(self.getHeader())
        f.write(newParams)

        for i, line in enumerate(prevF):
          if i == 0 and self.writeHeader.get():
            pass
          elif i >= nLines:
            break
          else:
            f.write(line)

    def getOutputFileName(self):
      if self.writeFilename.get():
        outFn = self.writeFilename.get()
      else:
        outFn = 'parameters.txt'
      return outFn

    def _getFirstJoinStep(self):
        for s in self._steps:
            if s.funcName == self._getFirstJoinStepName():
                return s
        return None

    def _getFirstJoinStepName(self):
        # This function will be used for streaming, to check which is
        # the first function that need to wait for all micrographs
        # to have completed
        return 'closeSetStep'

    def registerNewObjects(self):
      doneParams = self.pickleLoad(self.doneParamsFn)
      for obj in self.inputSet.get():
        if not obj.getObjId() in doneParams:
          doneParams.add(obj.getObjId())
      self.pickleSave(doneParams, self.doneParamsFn)

    def checkIfParentFinished(self):
        inpSet = self.inputSet.get()
        inpSet.loadAllProperties()
        if not inpSet.isStreamOpen():
          return True
        return False

    def pickleSave(self, data, filename):
      with open(filename, 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def pickleLoad(self, filename):
      with open(filename, 'rb') as handle:
        b = pickle.load(handle)
      return b


