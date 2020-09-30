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

"""
SGRT folder and file name definition.

"""

import os
import copy

import datetime as dt
from datetime import datetime
from collections import OrderedDict

from geopathfinder.folder_naming import SmartPath
from geopathfinder.folder_naming import build_smarttree
from geopathfinder.folder_naming import create_smartpath
from geopathfinder.file_naming import SmartFilename


class YeodaFilename(SmartFilename):

    """
    yeoda file name definition using SmartFilename class.
    """

    fields_def = OrderedDict([
        ('var_name', {'len': 0}),
        ('datetime_1', {'len': 0, 'delim': ''}),
        ('datetime_letter', {'len': 1, 'delim': ''}),
        ('datetime_2', {'len': 0}),
        ('band', {'len': 0}),
        ('extra_field', {'len': 0}),
        ('grid_name', {'len': 6}),
        ('tile_name', {'len': 10}),
        ('version_run_id', {'len': 6}),
        ('sensor_field', {'len': 0})
    ])
    pad = "-"
    delimiter = "_"

    def __init__(self, fields, ext=".tif", convert=False):
        """
        Constructor of YeodaFilename class.

        Parameters
        ----------
        fields: dict
            Dictionary specifying the different parts of the filename.
        convert: bool, optional
            If true, decoding is applied to parts of the filename, where such an operation is available (default is False).
        """

        fields = fields.copy()

        # implement here the date and time options & checks
        # 20170103T130355
        # 20170103
        # 20160103-20170103
        # 20160103T130355-20170103T230355
        if 'datetime_1' in fields:
            fields['datetime_1'] = self.encode_datetime(fields['datetime_1'])

        if 'datetime_2' in fields:
            self.single_date = False
            fields['datetime_2'] = self.encode_datetime(fields['datetime_2'])
        else:
            self.single_date = True

        fields_def_ext = copy.deepcopy(YeodaFilename.fields_def)
        fields_def_ext['datetime_1']['decoder'] = lambda x: self.decode_datetime(x)
        fields_def_ext['datetime_1']['encoder'] = lambda x: self.encode_datetime(x)
        fields_def_ext['datetime_2']['decoder'] = lambda x: self.decode_datetime(x)
        fields_def_ext['datetime_2']['encoder'] = lambda x: self.encode_datetime(x)
        fields_def_ext['extra_field']['decoder'] = lambda x: self.decode_extra_field(x)
        fields_def_ext['extra_field']['encoder'] = lambda x: self.encode_extra_field(x)

        super(YeodaFilename, self).__init__(fields, fields_def_ext, ext=ext, pad=YeodaFilename.pad,
                                           delimiter=YeodaFilename.delimiter, convert=convert)

    @classmethod
    def from_filename(cls, filename_str, convert=False):
        """
        Converts a filename given as a string into an YeodaFilename class object.

        Parameters
        ----------
        filename_str : str
            Filename without any paths (e.g., "M20170725_165004--_SIG0-----_S1BIWGRDH1VVA_146_A0104_EU500M_E048N012T6.tif").
        convert: bool, optional
            If true, decoding is applied to parts of the filename, where such an operation is available (default is False).

        Returns
        -------
        YeodaFilename
            Class representing an SGRT filename.
        """

        return super().from_filename(filename_str, YeodaFilename.fields_def, pad=YeodaFilename.pad,
                                     delimiter=YeodaFilename.delimiter, convert=convert)

    @property
    def stime(self):
        """
        Start time.

        Returns
        -------
        datetime.datetime
            Start time.
        """
        try:
            return self.obj['datetime_1']
        except TypeError:
            return None

    @property
    def etime(self):
        """
        End time.

        Returns
        -------
        datetime.datetime
            End time.
        """
        try:
            return self.obj['datetime_1']
        except TypeError:
            return None

    @property
    def time(self):
        """
        Unified time.

        Returns
        -------
        datetime.datetime
            Unified time.
        """
        try:
            if self.single_date:
                return self.stime
            else:
                return self.stime + (self.etime - self.stime) / 2
        except TypeError:
            return None

    @property
    def product_id(self):
        """
        Builds product id from other filename attributes (e.g. 'S1AIWGRDH').

        Returns
        -------
        product_id: str
            Product id consisting of mission id (e.g., 'S1'), spacecraft id (e.g., 'A'), mode id (e.g., 'IW'),
            product type (e.g., 'GRD') and resolution class (e.g., 'H').
        """
        try:
            product_id = "".join([self["mission_id"], self["spacecraft_id"], self["mode_id"], self["product_type"], self["res_class"]])
        except TypeError:
            product_id = None

        return product_id

    @property
    def ftile(self):
        """
        Builds the full tile name from other filename attributes (e.g. 'EU010M_E048N015T1').

        Returns
        -------
        ftile: str
            Full tile name consisting of grid name (e.g., 'EU10M') and tile name (e.g., 'E048N015T1').
        """
        try:
            ftile = "_".join([self["grid_name"], self["tile_name"]])
        except TypeError:
            ftile = None
        return ftile

    def decode_datetime(self, string):
        """
        Decodes a string into a datetime.date object. The format is given by the class.

        Parameters
        ----------
        string: str, object
            String needed to be decoded to a datetime.date object.

        Returns
        -------
        datetime.date, object
            Original object or datetime.date object parsed from the given string.
        """
        if isinstance(string, str):
            if 'T' in string:
                return datetime.strptime(string, "%Y%m%dT%H%M%S")
            else:
                return datetime.strptime(string, "%Y%m%d")
        else:
            return string


    def decode_extra_field(self, string):
        """
        Decodes a string into an integer if possible.

        Parameters
        ----------
        string: str, object
            String needed to be decoded to an integer.

        Returns
        -------
        int, object
            Original object or integer object parsed from the given string.
        """
        # TODO: relative orbit now includes the direction - solve it (maybe add another field for input)
        if isinstance(string, str):
            try:
                decode = int(string)
            except ValueError:
                return string
            return decode
        else:
            return string

    def encode_datetime(self, datetime_obj):
        """
        Encodes a datetime.datetime/datetime.date object into a string. The format is given by the class.

        Parameters
        ----------
        time_obj: datetime.datetime, datetime.date or object
            Datetime object needed to be encoded to a string.

        Returns
        -------
        str, object
            Original object or str object parsed from the given datetime object.
        """
        if isinstance(datetime_obj, dt.datetime):
            return datetime_obj.strftime("%Y%m%dT%H%M%S")
        elif isinstance(datetime_obj, dt.date):
            return datetime_obj.strftime("%Y%m%d")
        else:
            return datetime_obj


    def encode_extra_field(self, relative_orbit):
        """
        Encodes the extra field e.g. a relative orbit number into a string.

        Parameters
        ----------
        relative_orbit: int or object
            Integer needed to be encoded to a string.

        Returns
        -------
        str, object
            Original object or str object parsed from the given integer.
        """
        if isinstance(relative_orbit, int):
            return "{:03d}".format(relative_orbit)
        else:
            return str(relative_orbit)


def yeoda_path(root, mode=None, group=None, datalog=None,
               product=None, wflow=None, grid=None, tile=None, var=None,
               qlook=True, make_dir=False):
    """
    Realisation of the full yeoda folder naming convention, yielding a single
    SmartPath.

    Parameters
    ----------
    root : str
        root directory of the path. must contain satellite sensor at toplevel.
        e.g. "R:\Datapool_processed\Sentinel-1_CSAR"
    mode : str
        e.g "IWGRDH"
    group : str, optional
        "preprocessed" or "parameters" or "products"
    datalog : str, optional
        must be "datasets" or "logfiles"
    product : str
        e.g. "ssm"
    wflow : str
        e.g. "C1003"
    grid : str
        e.g. "EQUI7_EU500M"
    tile : str
        e.g. "E048N012T6"
    var : str
        e.g. "ssm"
    qlook : bool
        if the quicklook subdir should be integrated
    make_dir : bool
        if the directory should be created on the filesystem

    Returns
    -------
    SmartPath
        Object for the path
    """

    # define the datalog folder name
    if datalog is None:
        if isinstance(wflow, str):
            datalog = 'datasets'
    elif datalog == 'logfiles':
        product = None
        wflow = None
        grid = None
        tile = None
        var = None
        qlook = False
    elif datalog == 'datasets':
        pass
    else:
        raise ValueError('Wrong input for "datalog" level!')


    # define the group folder name
    if group is None:
        if wflow.startswith('A'):
            group = 'preprocessed'
        elif wflow.startswith('B'):
            group = 'parameters'
        elif wflow.startswith('C'):
            group = 'products'
        else:
            raise ValueError('Wrong input for "wflow" level!')


    # defining the folder levels
    levels = [mode, group,
              datalog, product, wflow, grid,
              tile,  var, 'qlooks']

    # defining the hierarchy
    hierarchy = ['mode', 'group',
                 'datalog', 'product', 'wflow', 'grid',
                 'tile', 'var', 'qlook']

    if qlook is False:
        levels.remove('qlooks')
        hierarchy.remove('qlook')

    return create_smartpath(root, hierarchy=hierarchy, levels=levels,
                     make_dir=make_dir)


def yeoda_tree(root, target_level=None, register_file_pattern=None):

    """
    Realisation of the full yeoda folder naming convention, yielding a
    SmartTree(), reflecting all subfolders as SmartPath()

    Parameters
    ----------
    root : str
        top level directory of the dataset, which is the sensor name in
        the SGRT naming convention.
        E.g.: "R:\Datapool_processed\Sentinel-1_CSAR"
    target_level : str, optional
        Can speed up things: Level name of target tree-depth.
        The SmartTree is only built from directories reaching this level,
        and only built down to this level. If not set, all directories are
        built down to deepest depth.
    register_file_pattern : str tuple, optional
        strings defining search pattern for file search for file_register
        e.g. ('V01R03', 'E048N012T6').
        No asterisk is needed ('*')!
        Sequence of strings in given tuple is crucial!
        Be careful: If the tree is large, this can take a while!

    Returns
    -------
    SmartTree
        Tree object for the yeoda dataset.
    """

    # defining the hierarchy
    hierarchy = ['mode', 'group','datalog',
                 'product', 'wflow', 'grid',
                 'tile', 'var', 'qlook']

    sgrt_tree = build_smarttree(root, hierarchy,
                                target_level=target_level,
                                register_file_pattern=register_file_pattern)

    return sgrt_tree


if __name__ == '__main__':
    pass
