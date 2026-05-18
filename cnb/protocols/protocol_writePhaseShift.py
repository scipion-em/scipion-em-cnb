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
import pyworkflow.protocol.constants as pwcts
import os
import pickle


class cnbWritePhaseShift(EMProtocol):
    """
    This protocol will store the ctf phaseshift in a determined file to be parse by SerialEM
    """
    """
        Write Phase Shift (cnbWritePhaseShift) — User Manual

        Overview

        The Write Phase Shift protocol is designed to monitor a streaming
        set of Contrast Transfer Function (CTF) estimations and extract the
        most recent phase shift value generated during acquisition or
        processing. Its primary purpose is to store this phase shift into a
        plain text file that can later be interpreted by external software
        such as SerialEM.

        Within cryo-EM workflows, this protocol is especially useful in
        automated acquisition environments where microscope parameters must
        remain synchronized with online image-processing results. Instead
        of performing image analysis itself, the protocol acts as a bridge
        between Scipion streaming workflows and external acquisition systems.

        Inputs and General Workflow

        The protocol requires a streaming SetOfCTF as input. Each CTF object
        may contain a phase shift estimation associated with phase plate
        cryo-EM experiments or related imaging conditions where phase
        modulation is relevant.

        The user also specifies an output directory and the filename where
        the extracted phase shift value will be stored. During execution,
        the protocol continuously monitors the input stream searching for
        newly generated CTF estimations.

        Whenever a new CTF object appears, the protocol retrieves the latest
        phase shift value and updates the output file accordingly. At the
        same time, it maintains an output SetOfCTF containing all processed
        CTF objects, preserving compatibility with larger Scipion workflows.

        Streaming and Incremental Processing

        A central characteristic of this protocol is its streaming-oriented
        design. Instead of waiting until the entire dataset is complete,
        the protocol incrementally processes incoming CTF estimations as
        they become available.

        Internally, the protocol periodically checks whether the number of
        CTF objects in the input stream has increased. If new entries are
        detected, dedicated execution steps are dynamically inserted to
        process the latest data.

        To avoid duplicate processing, the protocol stores identifiers of
        already processed CTFs inside a persistent pickle file. This allows
        stable long-running execution during automated acquisition sessions
        where new micrographs and CTF estimations may continuously appear.

        Phase Shift Extraction

        For each newly detected CTF object, the protocol retrieves the phase
        shift value using the corresponding getter method. If the value is
        available, it is written into the specified output text file.

        The generated file always contains the most recent phase shift
        estimation. This behavior is particularly useful in automated
        cryo-EM acquisition systems where external software needs immediate
        access to updated phase shift information.

        From a biological and operational perspective, this enables
        synchronization between online image processing and microscope
        control software such as SerialEM. In phase plate experiments,
        continuously monitoring phase shift evolution may help optimize
        acquisition conditions during long data-collection sessions.

        If a CTF object does not contain a valid phase shift estimation,
        the protocol reports the condition but continues execution without
        interrupting the streaming workflow.

        Output Management

        Besides generating the text file containing the phase shift value,
        the protocol also maintains an output SetOfCTF with all processed
        entries. The output set is incrementally updated as new CTFs arrive
        and remains synchronized with the streaming input dataset.

        Once the parent input stream finishes, the protocol closes the
        output set and establishes the corresponding source relations
        between input and output objects. This ensures compatibility with
        downstream Scipion protocols and larger automated workflows.

        Practical Considerations

        The protocol is primarily intended for online cryo-EM workflows
        involving phase plate imaging or live acquisition monitoring.
        Because the output file is continuously overwritten with the latest
        available phase shift value, external applications can always access
        the most recent estimation generated during processing.

        Since execution depends on streaming updates, the protocol is more
        appropriate for live-processing environments than for purely offline
        batch analysis. Reliable synchronization between acquisition,
        processing, and monitoring systems is important to guarantee stable
        operation.

        Final Perspective

        For automated cryo-EM facilities and streaming acquisition
        environments, the Write Phase Shift protocol provides a lightweight
        mechanism for exposing online CTF phase shift estimations to
        external software systems.

        Its role is not to compute CTF parameters, but rather to facilitate
        communication between Scipion workflows and microscope-control
        infrastructures. Through its incremental streaming architecture,
        the protocol enables real-time monitoring and integration workflows
        that are increasingly important in modern high-throughput cryo-EM
        pipelines.
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
        self.doneCTFsFn = self._getExtraPath('doneCTFs.pickle')
        if not os.path.exists(self.doneCTFsFn):
          self.pickleSave(set([]), self.doneCTFsFn)
        self.writtenCTFs = []
        self.ended = False
        self.closeSet = self._insertFunctionStep('closeSetStep', wait=True)

    def _stepsCheck(self):
        newDeps = []
        if not self.ended:
            closeStep = self._getFirstJoinStep()
            inputCTFs = self.inputCTFs.get()
            doneCTFs = self.pickleLoad(self.doneCTFsFn)

            if len(inputCTFs) > len(doneCTFs):
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
            print('Writing phase shift   {}   from   {}   \nin   {}'.
                  format(self.lastPhaseShift, self.lastCTF.getPsdFile().split('/')[-1], outFile))
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
      #print('Written CTFs: ', self.writtenCTFs)

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
        doneCTFs = self.pickleLoad(self.doneCTFsFn)
        for ctf in self.inputCTFs.get():
            if not ctf.getPsdFile() in doneCTFs:
                outCTFs.append(ctf)
                doneCTFs.add(ctf.getPsdFile())
        self.pickleSave(doneCTFs, self.doneCTFsFn)
        return outCTFs

    def checkIfParentFinished(self):
        inpCTFs = self.inputCTFs.get()
        inpCTFs.loadAllProperties()
        if not inpCTFs.isStreamOpen():
          return True
        return False

    def uploadPickleSet(self, filename, newValue):
      pSet = self.pickleLoad(filename)
      pSet.add(newValue)
      self.pickleSave(pSet, filename)

    def pickleSave(self, data, filename):
      with open(filename, 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def pickleLoad(self, filename):
      with open(filename, 'rb') as handle:
        b = pickle.load(handle)
      return b


