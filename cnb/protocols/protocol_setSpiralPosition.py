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

from pwem.protocols.protocol import ProtProcessMovies
from pwem.objects import SetOfCTF, Set
from pyworkflow.protocol import params, STATUS_NEW
from pyworkflow.utils import Message
from ..constants import *
import pyworkflow.protocol.constants as pwcts
import os, pickle
from datetime import datetime
from pyworkflow.utils.properties import Message
from pyworkflow.utils.path import moveFile
from pwem.emlib.image import ImageHandler
from pwem.objects import SetOfMovies, Movie


class CNBProtMovieSpiralPosition(ProtProcessMovies):
    """ Estimate the gain image of a camera, directly analyzing one of its movies.
    It can correct the orientation of an external gain image (by comparing it with the estimated).
    Finally, it estimates the residual gain (the gain of the movie after correcting with a gain).
    The gain used in the correction will be preferably the external gain, but can also be the estimated
    gain if the first is not found.
    The same criteria is used for assigning the gain to the output movies (external corrected > external > estimated)
    """
    _label = 'movie spiral position'
    _lastUpdateVersion = VERSION_1_1


    def __init__(self, **args):
        EMProtocol.__init__(self, **args)
        self.stepsExecutionMode = STEPS_PARALLEL
        self.estimatedIds = []
        self.spirals = {}

    # -------------------------- DEFINE param functions ----------------------
    def _defineParams(self, form):
        form.addSection(label=Message.LABEL_INPUT)
        form.addParam('inputMovies', PointerParam, pointerClass='SetOfMovies, '
                                                                'Movie',
                      label=Message.LABEL_INPUT_MOVS,
                      help='Select movies')

        # It should be in parallel (>2) in order to be able of attaching
        #  new movies to the output while estimating residual gain
        form.addParallelSection(threads=4, mpi=1)

    # -------------------------- STEPS functions ------------------------------
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


    def _processMovie(self, movie):
        movieId = movie.getObjId()

        print('entro aqui siendo la movie a procesar:')
        print(movieId)
       # if movieId not in self.estimatedIds:
        self.estimatedIds.append(movieId)
        spiral_position = self.getSpiralPosition(movie)
        
        self.spirals[movieId] = spiral_position
        
        #self.estimatedIds2.append(movieId)

        fnSummary = self._getPath("summary.txt")
        fnMonitorSummary = self._getPath("summaryForMonitor.txt")
        if not os.path.exists(fnSummary):
            fhSummary = open(fnSummary, "w")
            fnMonitorSummary = open(fnMonitorSummary, "w")
        else:
            fhSummary = open(fnSummary, "a")
            fnMonitorSummary = open(fnMonitorSummary, "a")

        #fhSummary.write("movie_%06d_poisson_count: mean=%f std=%f [min=%f,max=%f]\n" %
         #               (movieId, stats['mean'], stats['std'], stats['min'], stats['max']))

        fhSummary.close()
        fnMonitorSummary.close()

    def getSpiralPosition(self, movie):
        print(movie.getFileName())
        movieFn = movie.getFileName()
        
    
        return movieFn


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

            if isinstance(self.inputMovies.get(), SetOfMovies) or isinstance(self.inputMovies.get(), Movie):
                inputMovies = self.inputMovies.get()
                outputSet.copyInfo(inputMovies)

        return outputSet


    #def _checkNewInput(self):
     #   if isinstance(self.inputMovies.get(), SetOfMovies):
      #      ProtProcessMovies._checkNewInput(self)


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
        
        newMovies = [m.getObjId() not in self.insertedDict
                        for m in self.listOfMovies]
        
        outputStep = self._getFirstJoinStep()

        if newMovies:
            fDeps = self._insertNewMoviesSteps(self.insertedDict,
                                               newMovies)
            if outputStep is not None:
                outputStep.addPrerequisites(*fDeps)

            self.updateSteps()

    def _stepsCheck(self):
        # Input movie set can be loaded or None when checked for new inputs
        # If None, we load it
        self._checkNewInput()
        #self._checkNewOutput()

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
        if isinstance(self.inputMovies.get(), Movie):
            movie = self.inputMovies.get()
            movieId = movie.getObjId()
            streamMode = Set.STREAM_CLOSED
            saveMovie = self.getAttributeValue('doSaveMovie', False)
            moviesSet = self._loadOutputSet(SetOfMovies, 'movies.sqlite')
            moviesSet.append(movie)

            self._updateOutputSet('outputMovies', moviesSet, streamMode)
            outputStep = self._getFirstJoinStep()
            outputStep.setStatus(cons.STATUS_NEW)
            self.finished = True
        else:
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

            for movie in newDone:
                movieId = movie.getObjId()
                newMovie = movie.clone()
                
                # Echar un ojo a esta lista
                if movieId in self.estimatedIds2:
                    stats = self.stats[movieId]
                    mean = stats['mean']
                    std = stats['std']
                    min = stats['min']
                    max = stats['max']

                    setAttribute(newMovie, '_MEAN_DOSE_PER_FRAME', mean)
                    setAttribute(newMovie, '_STD_DOSE_PER_FRAME', std)
                    setAttribute(newMovie, '_MIN_DOSE_PER_FRAME', min)
                    setAttribute(newMovie, '_MAX_DOSE_PER_FRAME', max)

                moviesSet.append(newMovie)

            self._updateOutputSet('outputMovies', moviesSet, streamMode)

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
    

    # --------------------------- INFO functions -------------------------------
    def _validate(self):
        errors = []
        if errors:
            errors.append("An experimental gain can be associated with a "
                          "setOfMovies during its importing protocol. "
                          "Otherwise, no gain reorientation nor "
                          "gain normalization can be performed.")
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
