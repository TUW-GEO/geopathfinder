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
import glob

from datetime import datetime
from collections import OrderedDict

from geopathfinder.folder_naming import SmartPath
from geopathfinder.file_naming import SmartFilename
from geopathfinder.folder_naming import build_smarttree


# Please add here new sensors if they follow the SGRT naming convention.
allowed_sensor_dirs = ['Sentinel-1_CSAR',
                       'SCATSAR',
                       'METOP_ASCAT',
                       'Envisat_ASAR']


class SgrtFilename(SmartFilename):

    """
    SGRT file name definition using SmartFilename class.
    """

    def __init__(self, fields):

        self.date_format = "%Y%m%d_%H%M%S"

        fields_def = OrderedDict(
            [('pflag', 1), ('start_time', 15), ('end_time', 15),
             ('var_name', 9), ('sensor_id', 3), ('mode_id', 2),
             ('product_type', 3), ('res_class', 1), ('level', 1),
             ('pol', 2), ('direction', 4), ('relative_orbit', 4),
             ('workflow_id', 5), ('ftile_name', 3)])

        for v in ['start_time', 'end_time']:
            if v in fields:
                fields[v] = fields[v].strftime(self.date_format)

        super(SgrtFilename, self).__init__(fields, fields_def, ext='.tif')

    def __getitem__(self, key):
        """
        Get field content.

        Parameters
        ----------
        key : str
            Field name.

        Returns
        -------
        item : str
            Item value.
        """
        item = super(SgrtFilename, self).__getitem__(key)

        if key in ['start_time', 'end_time']:
            item = datetime.strptime(item, self.date_format)

        return item

    def __setitem__(self, key, value):
        """
        Set field content.

        Parameters
        ----------
        key : str
            Field name.
        value : str or datetime
            Field value.
        """
        if key in ['start_time', 'end_time'] and isinstance(value, datetime):
            value = value.strftime(self.date_format)

        super(SgrtFilename, self).__setitem__(key, value)



def sgrt_path(root, sensor=None, mode=None, group=None, datalog=None,
              product=None, wflow=None, grid=None, tile=None, var=None,
              qlook=True, make_dir=False):
    '''
    Realisation of the full SGRT folder naming convention, yielding a single
    SmartPath.

    Parameters
    ----------
    root : str
        e.g. "R:\Datapool_processed"
    sensor : str
        e.g. "Sentinel-1_CSAR"
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
    '''

    # check the sensor folder name
    if sensor not in allowed_sensor_dirs:
        raise ValueError('Wrong input for "sensor" level!')

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
    levels = {'root': root, 'sensor': sensor, 'mode': mode, 'group': group,
              'datalog': datalog, 'product': product, 'wflow': wflow,
              'grid': grid, 'tile': tile, 'var': var, 'qlook': 'qlooks'}

    # defining the hierarchy
    hierarchy = ['root', 'sensor', 'mode', 'group',
                 'datalog', 'product', 'wflow', 'grid',
                 'tile', 'var', 'qlook']

    return SmartPath(levels, hierarchy, make_dir=make_dir)


def sgrt_tree(root, target_level=None, register_file_pattern=None):

    '''
    Realisation of the full SGRT folder naming convention, yielding a
    SmartTree(), reflecting all subfolders as SmartPath()

    Parameters
    ----------
    root : str
        top level directory of the SGRT dataset, which is the sensor name in
        the SGRT naming convention.
        E.g.: "R:\Datapool_processed\Sentinel-1_CSAR"
    target_level : str, optional
        Can speed up things: Level name of target tree-depth.
        The SmartTree is only built from directories reaching this level,
        and only built down to this level. If not set, all directories are
        built down to deepest depth.
    register_file_pattern : str tuple, optional
        strings defining search pattern for file search for file_register
        e.g. ('C1003', 'E048N012T6').
        No asterisk is needed ('*')!
        Sequence of strings in given tuple is crucial!
        Be careful: If the tree is large, this can take a while!

    Returns
    -------
    SmartTree
        Object for the SGRT tree.
    '''

    # defining the hierarchy
    hierarchy = ['mode', 'group','datalog',
                 'product', 'wflow', 'grid',
                 'tile', 'var', 'qlook']

    # Check for allowed directory topnames for "root".
    if root.split(os.sep)[-1] in allowed_sensor_dirs:
        sgrt_tree = build_smarttree(root, hierarchy,
                                    target_level=target_level,
                                    register_file_pattern=register_file_pattern)
    else:
        raise ValueError('Root-directory "{}" does is '
                         'not a valid SGRT folder!'.format(root))

    return sgrt_tree



if __name__ == '__main__':
    pass
