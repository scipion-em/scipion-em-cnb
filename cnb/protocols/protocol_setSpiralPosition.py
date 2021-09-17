# **************************************************************************
# *
# * Authors:     Daniel Marchán Torres (da.marchan@cnb.csic.es)
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
from pwem.protocols.protocol_movies import ProtProcessMovies
from pyworkflow import VERSION_3_0
from pwem.objects import Set
from pyworkflow.protocol import params, STATUS_NEW
import os
from datetime import datetime
from pyworkflow.utils.properties import Message
from pwem.objects import SetOfMovies, Movie, SetOfMicrographs
from pyworkflow.protocol.params import (PointerParam, LEVEL_ADVANCED)
from pyworkflow.protocol import STEPS_PARALLEL
import pyworkflow.utils as pwutils
import pwem.objects as emobj
from xmipp3.convert import getScipionObj
import pyworkflow.protocol.constants as cons



class CNBProtMovieSpiralPosition(ProtProcessMovies):
    """ Estimate the gain image of a camera, directly analyzing one of its movies.
    It can correct the orientation of an external gain image (by comparing it with the estimated).
    Finally, it estimates the residual gain (the gain of the movie after correcting with a gain).
    The gain used in the correction will be preferably the external gain, but can also be the estimated
    gain if the first is not found.
    The same criteria is used for assigning the gain to the output movies (external corrected > external > estimated)
    """
    _label = 'movie spiral position'
    _lastUpdateVersion = VERSION_3_0


    def __init__(self, **args):
        ProtProcessMovies.__init__(self, **args)
        self.stepsExecutionMode = STEPS_PARALLEL
        self.spirals = {}

    # -------------------------- DEFINE param functions ----------------------
    def _defineParams(self, form):
        form.addSection(label=Message.LABEL_INPUT)
        form.addParam('inputMovies', PointerParam, pointerClass='SetOfMovies',
                      label=Message.LABEL_INPUT_MOVS,
                      help='Select movies')

        # It should be in parallel (>2) in order to be able of attaching
        #  new movies to the output while estimating residual gain
        form.addParallelSection(threads=4, mpi=1)

    # -------------------------- STEPS functions ------------------------------

    def _insertAllSteps(self):
        # Build the list of all processMovieStep ids by
        # inserting each of the steps for each movie
        self.insertedDict = {}
        self.samplingRate = self.inputMovies.get().getSamplingRate()
        self.micsFn =  self._getMicsPath()
        self.hasAlignment = self.micsFn != None
        self.acquisition = self.inputMovies.get().getAcquisition()
        pwutils.makePath(self._getExtraPath('DONE'))

        movieSteps = self._insertNewMoviesSteps(self.insertedDict,
                                                self.inputMovies.get())
        finalSteps = self._insertFinalSteps(movieSteps)
        self._insertFunctionStep('createOutputStep',
                                 prerequisites=finalSteps, wait=True)

    def createOutputStep(self):
        pass


    def _insertNewMoviesSteps(self, insertedDict, inputMovies):
        """ Insert steps to process new movies (from streaming)
        Params:
            insertedDict: contains already processed movies
            inputMovies: input movies set to be check
        """
        deps = []
        for movie in inputMovies:
            if movie.getObjId() not in insertedDict:
                stepId = self._insertMovieStep(movie)
                deps.append(stepId)
                insertedDict[movie.getObjId()] = stepId

        return deps

    def _insertMovieStep(self, movie):
        """ Insert the processMovieStep for a given movie. """
        # Note1: At this point is safe to pass the movie, since this
        # is not executed in parallel, here we get the params
        # to pass to the actual step that is gone to be executed later on
        # Note2: We are serializing the Movie as a dict that can be passed
        # as parameter for a functionStep
        movieDict = movie.getObjDict(includeBasic=True)
        movieStepId = self._insertFunctionStep('processMovieStep',
                                               movieDict,
                                               movie.hasAlignment(),
                                               prerequisites=[])
        return movieStepId


    def _processMovie(self, movie):
        movieId = movie.getObjId()
        spiral_position = self.getSpiralPosition(movie)
        self.spirals[movieId] = spiral_position

        fnSummary = self._getPath("summary.txt")
        fnMonitorSummary = self._getPath("summaryForMonitor.txt")
        if not os.path.exists(fnSummary):
            fhSummary = open(fnSummary, "w")
            fnMonitorSummary = open(fnMonitorSummary, "w")
        else:
            fhSummary = open(fnSummary, "a")
            fnMonitorSummary = open(fnMonitorSummary, "a")

        fhSummary.write("movie_%06d: spiral position=%d\n" %
                        (movieId, spiral_position))

        fhSummary.close()
        fnMonitorSummary.close()

    def getSpiralPosition(self, movie):
        movieFn = movie.getFileName()
        movieFnBase = os.path.basename(movieFn)
        print('MOVIES PATH, NAME AND SPIRAL:')
        print(movieFn)
        print(movieFnBase)
        x = movieFnBase.find("movie_")
        substr = movieFnBase[x+6:]
        x1 = substr.find("_")
        spiral = substr[x1+1:x1+6]
        print(int(spiral))

        return int(spiral)


    def _loadOutputSet(self, SetClass, baseName):
        """
        Load the output set if it exists or create a new one.
        fixSampling: correct the output sampling rate if binning was used,
        except for the case when the original movies are kept and shifts
        refers to that one.
        """
        setFile = self._getPath(baseName)
        if os.path.exists(setFile):
            outputSet = SetClass(filename=setFile)
            outputSet.loadAllProperties()
            outputSet.enableAppend()
        else:
            outputSet = SetClass(filename=setFile)
            outputSet.setStreamState(outputSet.STREAM_OPEN)
            inputMovies = self.inputMovies.get()
            outputSet.copyInfo(inputMovies)

        return outputSet

    def _stepsCheck(self):
        # Input movie set can be loaded or None when checked for new inputs
        # If None, we load it
        self._checkNewInput()
        self._checkNewOutput()

    def _checkNewInput(self):
        # Check if there are new movies to process from the input set
        localFile = self.inputMovies.get().getFileName()
        now = datetime.now()
        self.lastCheck = getattr(self, 'lastCheck', now)
        mTime = datetime.fromtimestamp(os.path.getmtime(localFile))
        self.debug('Last check: %s, modification: %s'
                   % (pwutils.prettyTime(self.lastCheck),
                      pwutils.prettyTime(mTime)))
        # If the input movies.sqlite have not changed since our last check,
        # it does not make sense to check for new input data
        if self.lastCheck > mTime and hasattr(self, 'listOfMovies'):
            return None

        self.lastCheck = now
        # Open input movies.sqlite and close it as soon as possible
        self._loadInputList()

        newMovies = [movie.clone() for movie in self.listOfMovies if movie.getObjId() not in self.insertedDict]
        outputStep = self._getFirstJoinStep()

        if newMovies:
            fDeps = self._insertNewMoviesSteps(self.insertedDict,
                                               newMovies)
            if outputStep is not None:
                outputStep.addPrerequisites(*fDeps)

            self.updateSteps()

   
    def _loadInputList(self):
        """ Load the input set of movies and create a list. """
        moviesFile = self.inputMovies.get().getFileName()
        self.debug("Loading input db: %s" % moviesFile)
        movieSet = emobj.SetOfMovies(filename=moviesFile)
        movieSet.loadAllProperties()
        self.listOfMovies = [m.clone() for m in movieSet]
        self.streamClosed = movieSet.isStreamClosed()
        movieSet.close()
        self.debug("Closed db.")
        

    def _checkNewOutput(self):
        if getattr(self, 'finished', False):
            return

        # Load previously done items (from text file)
        doneList = self._readDoneList()
        # Check for newly done items
        newDone = [m.clone() for m in self.listOfMovies
                   if int(m.getObjId()) not in doneList and
                   self._isMovieDone(m)]

        allDone = len(doneList) + len(newDone)
        # We have finished when there is not more input movies
        # (stream closed) and the number of processed movies is
        # equal to the number of inputs
        self.finished = self.streamClosed and \
                        allDone == len(self.listOfMovies)
        streamMode = Set.STREAM_CLOSED if self.finished \
                     else Set.STREAM_OPEN

        if newDone:
            self._writeDoneList(newDone)
        elif not self.finished:
            # If we are not finished and no new output have been produced
            # it does not make sense to proceed and updated the outputs
            # so we exit from the function here
            return

        moviesSet = self._loadOutputSet(SetOfMovies, 'movies.sqlite')
        
        if self.hasAlignment:
            micSet = self._loadOutputSet(SetOfMicrographs, 'micrographs.sqlite')
            inputMicSet = self._loadInputMicrographSet(self.micsFn)

        for movie in newDone:
            movieId = movie.getObjId()
            newMovie = movie.clone()
            spiral = self.spirals[movieId]
            setAttribute(newMovie, '_SPIRAL_POSITION', spiral)
            moviesSet.append(newMovie)
            if self.hasAlignment:
                mic = inputMicSet[movieId].clone()
                setAttribute(mic, '_SPIRAL_POSITION', spiral)
                micSet.append(mic)

        moviesSet.setAcquisition(self.acquisition.clone())
        moviesSet.setSamplingRate(self.samplingRate)
        #    outputSet.copyInfo(inputMovies)
        self._updateOutputSet('outputMovies', moviesSet, streamMode)
        
        if self.hasAlignment:
            micSet.setAcquisition(self.acquisition.clone())
            micSet.setSamplingRate(self.samplingRate)
            self._updateOutputSet('outputMicrographs', micSet, streamMode)

        if self.finished:  # Unlock createOutputStep if finished all jobs
            outputStep = self._getFirstJoinStep()
            if outputStep and outputStep.isWaiting():
                outputStep.setStatus(cons.STATUS_NEW)


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


    # ------------------------- UTILS functions --------------------------------
    def _getMicsPath(self):
        prot1 = self.inputMovies.getObjValue()  # pointer to previous protocol

        if hasattr(prot1, 'outputMicrographs'):
            path1 = prot1.outputMicrographs.getFileName()
            if os.path.getsize(path1) > 0:
                return path1

        elif hasattr(prot1, 'outputMicrographsDoseWeighted'):
            path2 = prot1.outputMicrographsDoseWeighted.getFileName()
            if os.path.getsize(path2) > 0:
                return path2

        else:
            return None

    def _loadInputMicrographSet(self, micsFn):
        self.debug("Loading input db: %s" % micsFn)
        micSet = SetOfMicrographs(filename=micsFn)
        micSet.loadAllProperties()
        return micSet

    # --------------------------- INFO functions -------------------------------
    def _validate(self):
        errors = []
        if errors:
            pass
        return errors

    def _summary(self):
        fnSummary = self._getPath("summary.txt")
        if not os.path.exists(fnSummary):
            summary = ["No summary information yet."]
        else:
            fhSummary = open(fnSummary, "r")
            summary = []
            for line in fhSummary.readlines():
                summary.append(line.rstrip())
            fhSummary.close()
        return summary


# --------------------- WORKERS --------------------------------------
def setAttribute(obj, label, value):
    if value is None:
        return
    setattr(obj, label, getScipionObj(value))
