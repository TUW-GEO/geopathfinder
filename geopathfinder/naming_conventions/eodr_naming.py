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

from datetime import datetime
from collections import OrderedDict


from geopathfinder.file_naming import SmartFilename


class eoDRFilename(SmartFilename):

    """
    SGRT file name definition using SmartFilename class.
    """

    def __init__(self, fields, ext='.vrt'):

        self.dt_format = "%Y%m%dT%H%M%S"
        self.fields = fields.copy()

        fields_def = OrderedDict([
                     ('id', {'len': 12, 'delim': True}),
                     ('dt_1', {'len': 15, 'delim': True,
                                  'decoder': lambda x: self.decode_datetime(x),
                                  'encoder': lambda x: self.encode_datetime(x)}),
                     ('dt_2', {'len': 15, 'delim': True,
                                  'decoder': lambda x: self.decode_datetime(x),
                                  'encoder': lambda x: self.encode_datetime(x)}),
                     ('dt', None),
                     ('band', {'len': None, 'delim': True, 'encoder': lambda x: str(x)})
                    ])

        fields_def_keys = list(fields_def.keys())
        for key in fields.keys():
            if key not in fields_def_keys:
                fields_def[key] = {'len': None, 'delim': True}

        super(eoDRFilename, self).__init__(self.fields, fields_def, pad='-', ext=ext)

    @property
    def stime(self):
        """start time"""
        if "-" not in self['dt_1']:
            return self.decode_datetime(self['dt_1'])
        else:
            return None

    @property
    def etime(self):
        """end time"""
        if "-" not in self['dt_2']:
            return self.decode_datetime(self['dt_2'])
        else:
            return None

    def decode_datetime(self, string):
        if isinstance(string, str):
            return datetime.strptime(string, self.dt_format)
        else:
            return string

    def encode_datetime(self, time_obj):
        if isinstance(time_obj, datetime):
            return time_obj.strftime(self.dt_format)
        else:
            return time_obj

    def __getitem__(self, key):

        if key == "dt":
            if self.stime and self.etime:
                return self.stime + (self.etime - self.stime) / 2
            elif self.stime:
                return self.stime  # if start and end time are given, take the mean
        else:
            return super(eoDRFilename, self).__getitem__(key)


def create_eodr_filename(filename_string):
    """
    Creates a SgrtFilename() object from a given string filename

    Parameters
    ----------
    filename_string : str
        filename following the SGRT filename convention.
        e.g. 'M20170725_165004--_SIG0-----_S1BIWGRDH1VVA_146_A0104_EU500M_E048N012T6.tif'

    Returns
    -------
    SgrtFilename

    """

    helper = eoDRFilename({})
    filename_string = filename_string.replace(helper.ext, '')
    parts = filename_string.split(helper.delimiter)

    fields = {'id': parts[0],
              'dt_1': parts[1],
              'dt_2': parts[2],
              'dt': None,
              'band': parts[3]
             }

    if len(parts) > 4:
        for i, part in enumerate(parts[4:]):
            key = 'd' + str(i+1)
            fields[key] = part

    return eoDRFilename(fields)


if __name__ == '__main__':
    pass