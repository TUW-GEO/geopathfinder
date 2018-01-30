# Copyright (c) 2018, Vienna University of Technology (TU Wien), Department
# of Geodesy and Geoinformation (GEO).
# All rights reserved.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL VIENNA UNIVERSITY OF TECHNOLOGY,
# DEPARTMENT OF GEODESY AND GEOINFORMATION BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''
Base class for the geopathfinder

'''

import os
import abc

class GeoTree(object):
    '''
    Base class for the structure of a geo data set
    '''

    def __init__(self, levels, hierarchy):

        self.levels = levels
        self.hierarchy = hierarchy

        directory = self._build_dir()

        self.directory = directory


    def get_dir(self, make_dir=False):

        if make_dir:
            self.make_dir()

        return self.directory

    def make_dir(self):
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    @property
    def level_1(self):
        return 'mainpath'



    def _build_dir(self, level=''):

        directory = ''

        for h in self.hierarchy:
            directory = os.path.join(directory, self.levels[h])

            if h == level:
                break

        return directory

    def search_level(self, level, pattern=None):

        directory = self._build_dir(level)

        search = 2

        return search

    def search_files(self, level, pattern):

        pass


