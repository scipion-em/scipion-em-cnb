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

"""
This modules contains constants related to cnb protocols
"""

#Labels which define the type of parameters written
SetChoices = ['Unknown input protocol', 'Number of movies', 'CTF parameters']

#Type of sets included
UNKNOWNSET = 0
SETOFMOVIES = 1
SETOFCTF = 2

#Defines the parameters which will be written for each kind of set.
#In 'item', includes the list of parameters of each ITEM of the set (e.g: phaseshift of each ctf)
#In 'set', includes the list of parameters found in the set (e.g: number of movies)
paramatersDic = {SETOFCTF: {'item': ['_objId', '_fitQuality', '_resolution', '_phaseShift',
                                     '_defocusRatio', '_defocusAngle', '_defocusU', '_defocusV'],
                            'set': []},
                 SETOFMOVIES: {'item': [],
                               'set': ['_size']}}
