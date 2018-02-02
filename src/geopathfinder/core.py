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
import re
import glob
import errno

from datetime import datetime

import numpy as np
import pandas as pd


class SmartPath(object):
    '''
    Base class for the single path structure to a data set.
    - allows building a path,
    - searching files with temporal slicing,
    - creating a pandas.DataFrame from a folder
    '''

    def __init__(self, levels, hierarchy, make_dir=False):
        '''
        Parameters
        ----------
        levels : str
            name of level in hierarchy
        hierarchy : list of str
            list defining the order of the levels
        make_dir : bool, optional
            if set to True, then the full path of
            the SmartPath is created in the filesystem
        '''

        self.levels = levels
        self.hierarchy = hierarchy

        directory = self.build_levels()

        self.directory = directory

        if make_dir:
            self.make_dir()

    def __getitem__(self, level):
        '''
        short link for path, down to 'level'.
        Usage: path2level = your_smart_path[level]

        Parameters
        ----------
        level : str
            name of level in hierarchy

        Returns
        -------
        str
            path from root to level

        '''
        return self.get_level(level)


    def get_dir(self, make_dir=False):
        '''

        Parameters
        ----------
        make_dir : bool, optional

        Returns
        -------
        str
            full path of the SmartPath

        '''

        if make_dir:
            self.make_dir()

        return self.directory

    def make_dir(self):
        '''
        Creates directory from root to deepest level

        '''
        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def build_levels(self, level=''):
        '''

        Parameters
        ----------
        level : str, optional
            name of level in hierarchy

        Returns
        -------
        str
            full path of the SmartPath

        '''

        directory = ''

        for h in self.hierarchy:
            if self.levels[h] is None:
                break
            else:
                directory = os.path.join(directory, self.levels[h])
                if h == level:
                    break

        return directory

    def get_level(self, level):
        '''

        Parameters
        ----------
        level : str
            name of level in hierarchy

        Returns
        -------
        str
            path from root to level

        '''

        if level in self.hierarchy:
            return self.build_levels(level=level)
        else:
            print('\'{}\' is not part of the path\'s hierarchy. '
                  'Try on of {}.'.format(level, self.hierarchy))


    def expand_full_path(self, level, files):
        '''
        Joins the path at level with given filenames

        Parameters
        ----------
        level : str
            name of level in hierarchy
        files : list of str
            fileanames

        Returns
        -------
        str
            joined filepaths

        '''

        return [os.path.join(self[level], x) for x in files]


    def search_files(self, level, pattern='.*', full_paths=False):
        '''
        Searches files meeting the regex pattern at level in the SmartPath

        Parameters
        ----------
        level : str
            name of level in hierarchy
        pattern : str, optional
            regex search pattern for file search
        full_paths : bool, optional
            should full paths be in the dataframe? if not set: False

        Returns
        -------
        list of str
            filenames at the level

        '''

        paths = glob.glob(os.path.join(self.build_levels(level), '*.*'))
        basenames = reduce_2_basename(paths)

        regex = re.compile(pattern)
        files = [x for x in basenames if regex.match(x)]

        if full_paths:
            files = self.expand_full_path(level, files)

        return files


    def search_files_ts(self, level, pattern='.*',
                        date_position=1, date_format='%Y%m%d_%H%M%S',
                        starttime=None, endtime=None, full_paths=False):
        '''
        Function searching files at a level in the SmartPath, returning the filenames
        and the datetimes as pd.DataFrame

        Parameters
        ----------
        level : str
            name of level in hierarchy
        pattern : str, optional
            regex search pattern for file search
        date_position : int
            position of first character of date string in name of files
        date_format : str
            string with the datetime format in the filenames.
            e.g. '%Y%m%d_%H%M%S' reflects '20161224_000000'
        starttime : str or datetime, optional
            earliest date and time, if str must follow "date_format"
        endtime : str or datetime, optional
            latest date and time, if str must follow "date_format"
        full_paths : bool, optional
            should full paths be in the dataframe? if not set: False

        Returns
        -------
        df : pd.DataFrame
            dataframe holding the filenames and the datetimes
        '''


        files = self.search_files(level, pattern=pattern)
        times = extract_times(files, date_position=date_position, date_format=date_format)

        if full_paths:
            files = self.expand_full_path(level, files)

        df = pd.DataFrame({'Files': files}, index=times)
        df.sort_index(inplace=True)

        if (starttime is not None) or (endtime is not None):
            if not isinstance(starttime, datetime):
                starttime = datetime.strptime(starttime, date_format)
            if not isinstance(endtime, datetime):
                endtime = datetime.strptime(endtime, date_format)
            df = df[starttime:endtime]

        return df

def reduce_2_basename(files):
    '''
    Converts full file paths to file basenames.

    Parameters
    ----------
    files : list of str
        list of filepaths

    Returns
    -------
    list of str
        list of basenames

    '''

    return [os.path.basename(f) for f in files]


def extract_times(files, date_position=1, date_format='%Y%m%d_%H%M%S'):
    '''
    Extracts the datetimes from filenames.

    Parameters
    ----------
    files: list of str
        list of strings with filenames or filepaths
    date_position: int
        position of first character of date string in name of files
    date_format: str
        string with the datetime format in the filenames.
        '%Y%m%d_%H%M%S' reflects eg. '20161224_000000'

    Return
    ------
    list of datetime
        list of datetime.datetime objects extracted from the filenames,

    '''

    if any([os.path.isdir(x) for x in files]):
        files = reduce_2_basename(files)

    return [datetime.strptime(x[date_position:date_position + len(date_format) + 2], date_format) for x in files]
