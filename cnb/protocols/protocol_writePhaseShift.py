# -*- coding: utf-8 -*-
# **************************************************************************
# *
# * Authors:     you (you@yourinstitution.email)
# *
# * your institution
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
# *  e-mail address 'you@yourinstitution.email'
# *
# **************************************************************************

from pwem.protocols.protocol import EMProtocol
from pwem.objects import SetOfCTF, Set
from pyworkflow.protocol import params, STATUS_NEW
from pyworkflow.utils import Message
import pyworkflow.protocol.constants as pwcts
import os


class cnbWritePhaseShift(EMProtocol):
    """
    This protocol will store the ctf phaseshift in a determined file to be parse by SerialEM
    """
    _label = 'Write phase shift'

    def __init__(self, **kwargs):
        EMProtocol.__init__(self, **kwargs)
        self.stepsExecutionMode = pwcts.STEPS_PARALLEL

    # -------------------------- DEFINE param functions ----------------------
    def _defineParams(self, form):
        form.addSection(label=Message.LABEL_INPUT)
        form.addParam('inputCTFs', params.PointerParam,
                      pointerClass='SetOfCTF',
                      label='Set of CTFs', important=True,
                      help='Set of CTF to parse the phaseShift')

        form.addParam('writePath', params.FileParam,
                      default=os.getcwd(),
                      label='Output folder', important=True,
                      help='Folder path where to save the phaseShift')

        form.addParam('writeFilename', params.StringParam,
                      default='phaseShift.txt', label='Filename',
                      help='Name of the saved file')
        form.addParallelSection(threads=1, mpi=1)

        self._defineStreamingParams(form)

    # --------------------------- STEPS functions ------------------------------
    def _insertAllSteps(self):
        self.doneCTFs = set([])
        self.writtenCTFs = []
        self.ended = False
        self.closeSet = self._insertFunctionStep('closeSetStep', wait=True)

    def _stepsCheck(self):
        newDeps = []
        if not self.ended:
            closeStep = self._getFirstJoinStep()
            inputCTFs = self.inputCTFs.get()
            for ctf in inputCTFs:
                self.lastCTF = ctf
            if len(inputCTFs) > len(self.doneCTFs):
                newDeps.append(self._insertFunctionStep('getLastPhaseShift', prerequisites=[]))
                newDeps.append(self._insertFunctionStep('createOutputStep', prerequisites=[newDeps[-1]]))
                closeStep.addPrerequisites(*newDeps)
            if self.checkIfParentFinished():
                closeStep.setStatus(STATUS_NEW)

            self.updateSteps()

    def getLastPhaseShift(self):
        ctfs = self.inputCTFs.get()
        if len(ctfs)>0:
            for ctf in ctfs:
                self.lastCTF = ctf
            self.lastPhaseShift = self.lastCTF.getPhaseShift()
        else:
            self.lastPhaseShift = None

    def createOutputStep(self):
        self.writePhaseShift()
        outputName = "outputCTFs"
        outCTFs = self._loadOutputSet(SetOfCTF, outputName + '.sqlite')
        outCTFs = self.addNewCTFs(outCTFs)
        self._updateOutputSet(outputName, outCTFs)

    def writePhaseShift(self):
        if self.writeFilename.get():
            outFn = self.writeFilename.get()
        else:
            outFn = 'phaseShift.txt'
        if self.lastPhaseShift != None:
            outFile = self.writePath.get() + outFn
            print('Writing phase shift {} in {}'.format(self.lastPhaseShift, outFile))
            with open(outFile, 'w') as f:
                f.write(str(self.lastPhaseShift))
            self.writtenCTFs.append(self.lastCTF.getPsdFile())
        else:
            print('Selected CTFs has no phaseShift associated')

    def closeSetStep(self):
      outputName = "outputCTFs"
      outCTFs = self._loadOutputSet(SetOfCTF, outputName+'.sqlite')
      outCTFs = self.addNewCTFs(outCTFs)
      self._updateOutputSet(outputName, outCTFs, state=Set.STREAM_CLOSED)

      self._defineSourceRelation(self.inputCTFs.get(), self.outputCTFs)
      self.ended = True
      print('Written CTFs: ', self.writtenCTFs)

    # --------------------------- INFO functions -----------------------------------
    def _summary(self):
        """ Summarize what the protocol has done"""
        summary = []

        return summary

    def _methods(self):
        methods = []

        return methods

    # --------------------------- UTILS functions -----------------------------------
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

    def _loadOutputSet(self, SetClass, baseName):
      """
      Load the output set if it exists or create a new one.
      """
      setFile = self._getPath(baseName)
      if os.path.exists(setFile) and os.path.getsize(setFile) > 0:
        outputSet = SetClass(filename=setFile)
        outputSet.loadAllProperties()
        outputSet.enableAppend()
      else:
        outputSet = SetClass(filename=setFile)
        outputSet.setStreamState(outputSet.STREAM_OPEN)
        outputSet.setObjLabel('Output CTFs')
        outputSet.copyInfo(self.inputCTFs.get())

      return outputSet

    def _updateOutputSet(self, outputName, outputSet, state=Set.STREAM_OPEN):
      outputSet.setStreamState(state)
      if self.hasAttribute(outputName):
        outputSet.write()  # Write to commit changes
        outputAttr = getattr(self, outputName)
        # Copy the properties to the object contained in the protcol
        outputAttr.copy(outputSet, copyId=False)
        # Persist changes
        self._store(outputAttr)
      else:
        # Here the defineOutputs function will call the write() method
        self._defineOutputs(**{outputName: outputSet})
        self._store(outputSet)

      # Close set databaset to avoid locking it
      outputSet.close()

    def addNewCTFs(self, outCTFs):
        for ctf in self.inputCTFs.get():
            if not ctf.getPsdFile() in self.doneCTFs:
                outCTFs.append(ctf)
                self.doneCTFs.add(ctf.getPsdFile())
        return outCTFs

    def checkIfParentFinished(self):
        inpCTFs = self.inputCTFs.get()
        inpCTFs.loadAllProperties()
        if not inpCTFs.isStreamOpen():
          return True
        return False


