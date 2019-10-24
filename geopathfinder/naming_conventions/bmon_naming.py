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
BMon file name definition.

"""

import os

import datetime as dt
from datetime import datetime
from collections import OrderedDict

from geopathfinder.folder_naming import SmartPath
from geopathfinder.folder_naming import build_smarttree
from geopathfinder.folder_naming import create_smartpath
from geopathfinder.file_naming import SmartFilename


class BMonFilename(SmartFilename):

    """
    BMon file name definition using SmartFilename class.
    """

    def __init__(self, fields, convert=False):
        """
        Constructor of BMonFilename class.

        Parameters
        ----------
        fields: dict
            Dictionary specifying the different parts of the filename.
        convert: bool, optional
            If true, decoding is applied to parts of the filename, where such an operation is available (default is False).
        """

        self.timestamp_format = "%Y%m%d%H%M%S"
        self.fields = fields.copy()

        fields_def = OrderedDict([
                     ('var_name', {'len': 16, 'delim': False}),
                     ('sres', {'len': 4, 'delim': True}),
                     ('timestamp', {'len': 14, 'delim': True,
                                  'decoder': lambda x: self.decode_timestamp(x),
                                  'encoder': lambda x: self.encode_timestamp(x)}),
                    ('version', {'len': 2, 'delim': True})
                    ])

        super(BMonFilename, self).__init__(self.fields, fields_def, pad='-', ext='.nc', convert=convert)

    def decode_timestamp(self, string):
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
            return datetime.strptime(string, self.timestamp_format)
        else:
            return string

    def encode_timestamp(self, time_obj):
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

        if isinstance(time_obj, (dt.datetime, dt.date, dt.time)):
            return time_obj.strftime(self.timestamp_format)
        else:
            return time_obj


def create_bmon_filename(filename_string, convert=False):
    """
    Creates a BMonFilename() object from a given string filename

    Parameters
    ----------
    filename_string : str
        filename following the BMon filename convention.
        e.g. 'BMON_DM_ENSEMBLE_500m_20160101120000_v1.nc'
    convert: bool, optional
            If true, decoding is applied to parts of the filename, where such an operation is available (default is False).

    Returns
    -------
    BMonFilename

    """

    helper = BMonFilename({})
    filename_string = filename_string.replace(helper.ext, '')
    parts = filename_string.split(helper.delimiter)

    fields = {
              'var_name': "_".join(parts[:-3]),
              'sres': parts[-3],
              'timestamp': parts[-2],
              'version': parts[-1]
             }

    return BMonFilename(fields, convert=convert)

if __name__ == '__main__':
    pass
