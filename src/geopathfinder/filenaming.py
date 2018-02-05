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

from collections import OrderedDict
from datetime import datetime


class SmartFilename():

    """
    Class handling file name following pre-defined rules.
    """

    def __init__(self, fields, fields_def, pad='-', delimiter='_'):
        """
        Define name of fields, length, pad and delimiter symbol.

        Parameters
        ----------
        fields : dict
            Name of fields (keys) and  (values).
        field_def : OrderedDict
            Name of fields (keys) in right order and length (values).
        pad : str, optional
            Padding symbol (default: '-').
        delimiter : str, optional
            Delimiter (default: '_')
        """
        self.fields = fields
        self.fields_def = fields_def
        self.delimiter = delimiter
        self.pad = pad

    def _build_fn(self):
        """
        Build file name based on fields, padding and length.

        Returns
        -------
        filename : str
            Filled file name.
        """
        filename = ''
        for name, length in self.fields_def.items():
            if name in self.fields:
                if filename == '':
                    filename = self.fields[name]
                else:
                    filename += self.delimiter + self.fields[name]
            else:
                if filename == '':
                    filename = self.pad * length
                else:
                    filename += self.delimiter + self.pad * length

        return filename

    def __getitem__(self, key):
        return self.fields[key]

    def __setitem__(self, key, value):
        self.fields[key] = value

    def __repr__(self):
        return self._build_fn()


def sgrt_ssm_fn(start_time, end_time, pol):
    """
    Test function.

    Parameters
    ----------
    start_time : datetime
        Start time.
    end_time : datetime
        End time.
    pol : str
        Polarization

    Returns
    -------
    smart_fn : SmartFilename object
        Smart file name object.
    """
    fields_def = OrderedDict(
        [('pflag', 1), ('start_time', 15), ('end_time', 15),
            ('var_name', 9), ('sensor_id', 3), ('mode_id', 2),
            ('product_type', 3), ('res_class', 1), ('level', 1),
            ('pol', 2), ('direction', 4), ('relative_orbit', 4),
            ('workflow_id', 5), ('ftile_name', 3), ('ext', 4)])

    names = {'start_time': start_time.strftime("%Y%m%d_%H%M%S"),
             'end_time': end_time.strftime("%Y%m%d_%H%M%S"),
             'product_type': 'SSM', 'pol': pol, 'ext': '.tif'}

    return SmartFilename(names, fields_def)


class SgrtFilename(SmartFilename):

    def __init__(self, fields):

        self.date_format = "%Y%m%d%H%M%SZ"

        fields_def = OrderedDict(
            [('pflag', 1), ('start_time', 15), ('end_time', 15),
             ('var_name', 9), ('sensor_id', 3), ('mode_id', 2),
             ('product_type', 3), ('res_class', 1), ('level', 1),
             ('pol', 2), ('direction', 4), ('relative_orbit', 4),
             ('workflow_id', 5), ('ftile_name', 3), ('ext', 4)])

        for v in ['start_time', 'end_time']:
            if v in fields:
                fields[v] = fields[v].strftime(self.date_format)

        fields['ext'] = '.tif'

        super(SgrtFilename, self).__init__(fields, fields_def)

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
        if key in ['start_time', 'end_time']:
            item = datetime.strptime(self.fields[key], self.date_format)
        else:
            item = self.fields[key]

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
            self.fields[key] = value.strftime(self.date_format)
        else:
            self.fields[key] = value


def test_sgrt_filename_times():
    """
    Test file name dates.
    """
    start_time = datetime(2008, 1, 1, 12, 23, 33)
    end_time = datetime(2008, 1, 1, 13, 23, 33)
    fields = {'start_time': start_time, 'end_time': end_time}
    fn = SgrtFilename(fields)

    assert fn['start_time'] == start_time
    assert fn['end_time'] == end_time

    new_start_time = datetime(2008, 3, 1, 12, 23, 33)
    fn['start_time'] = new_start_time

    assert fn['start_time'] == new_start_time


def example():
    """
    Example.
    """
    start_time = datetime(2008, 1, 1, 12, 23, 33)
    end_time = datetime(2008, 1, 1, 13, 23, 33)
    pol = 'VV'
    fn = sgrt_ssm_fn(start_time, end_time, pol)
    print(fn)

    fields = {'start_time': start_time, 'end_time': end_time}
    fn = SgrtFilename(fields)
    print(fn)
    print(fn['start_time'], fn['end_time'])

if __name__ == '__main__':
    example()
    test_sgrt_filename_times()
