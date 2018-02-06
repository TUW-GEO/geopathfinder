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

import unittest
from collections import OrderedDict

from geopathfinder.file_naming import SmartFilename


class TestSmartFilename(unittest.TestCase):

    def setUp(self):
        self.fields_def = OrderedDict([('pflag', 1), ('start_time', 14)])

    def test_build_filename_wihout_ext(self):
        """
        Test building file naming without extension.
        """
        fields = {'pflag': 'M', 'start_time': '20180101120000'}
        smrtf = SmartFilename(fields, self.fields_def)

        self.assertTrue(smrtf.__repr__() == 'M_20180101120000')

    def test_build_filename_with_ext(self):
        """
        Test building file naming with extension.
        """
        fields = {'pflag': 'M', 'start_time': '20180101120000'}
        smrtf = SmartFilename(fields, self.fields_def, ext='.tif')

        self.assertTrue(smrtf.__repr__() == 'M_20180101120000.tif')

    def test_set_and_get_fields(self):
        """
        Test set and get file name fields.
        """
        fields = {'pflag': 'M', 'start_time': '20180101120000'}
        smrtf = SmartFilename(fields, self.fields_def, ext='.tif')
        
        self.assertTrue(smrtf['pflag'] == 'M')
        self.assertTrue(smrtf['start_time'] == '20180101120000')

        smrtf['pflag'] = 'D'
        smrtf['start_time'] = '20180101130000'

        self.assertTrue(smrtf['pflag'] == 'D')
        self.assertTrue(smrtf['start_time'] == '20180101130000')

    def test_set_nonexisting_fields(self):
        """
        Test setting field which is non-existing in definition.
        """
        fields = {'pflag': 'M', 'start_time': '20180101120000'}
        smrtf = SmartFilename(fields, self.fields_def, ext='.tif')

        with self.assertRaises(KeyError) as context: 
            smrtf['new_field'] = 'test'

if __name__ == '__main__':
    unittest.main()
