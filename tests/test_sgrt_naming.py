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


import os
import unittest
from datetime import datetime

import logging

from geopathfinder.sgrt_naming import SgrtFilename
from geopathfinder.sgrt_naming import sgrt_tree
from geopathfinder.sgrt_naming import sgrt_path

logging.basicConfig(level=logging.INFO)


class TestSgrtFilename(unittest.TestCase):


    def setUp(self):
        self.start_time = datetime(2008, 1, 1, 12, 23, 33)
        self.end_time = datetime(2008, 1, 1, 13, 23, 33)

        fields = {'start_time': self.start_time, 'end_time': self.end_time,
                  'var_name': 'SSM'}

        self.sgrt_fn = SgrtFilename(fields)


    def test_build_sgrt_filename(self):
        """
        Test building SGRT file name.
        """

        fn = ('-_20080101_122333_20080101_132333_SSM------_---_--_---_-_-_--_'
              '----_----_-----_---.tif')

        self.assertEqual(self.sgrt_fn.__repr__(), fn)


    def test_set_and_get_datetime(self):
        """
        Test set and get start and end time.
        """

        self.assertEqual(self.sgrt_fn['start_time'], self.start_time)
        self.assertEqual(self.sgrt_fn['end_time'], self.end_time)

        new_start_time = datetime(2009, 1, 1, 12, 23, 33)
        self.sgrt_fn['start_time'] = new_start_time

        self.assertEqual(self.sgrt_fn['start_time'], new_start_time)


class TestSgrtPath(unittest.TestCase):
    """
    Tests checking if a SGRT path is correctly reflected by sgrt_tree.
    """

    def setUp(self):
        """
        Setting up the test sgrt_tree.
        """

        self.test_dir = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'test_data', 'Sentinel-1_CSAR')


    def test_full_path(self):
        """
        Tests the SmartPath() for the SGRT naming conventions
        """

        should = os.path.join(self.test_dir, 'IWGRDH', 'products', 'datasets',
                              'ssm', 'C1003', 'EQUI7_EU500M', 'E048N012T6',
                              'ssm', 'qlooks')

        stp1 = sgrt_path(self.test_dir,
                         mode='IWGRDH', group='products', datalog='datasets',
                         product='ssm', wflow='C1003', grid='EQUI7_EU500M',
                         tile='E048N012T6', var='ssm',
                         qlook=True, make_dir=False)

        self.assertEqual(stp1.directory, should)

        # giving no specifications on group and datalog levels
        stp2 = sgrt_path(self.test_dir,
                         mode='IWGRDH', product='ssm', wflow='C1003',
                         grid='EQUI7_EU500M', tile='E048N012T6', var='ssm',
                         qlook=True, make_dir=False)

        self.assertEqual(stp2.directory, should)

        pass



class TestSgrtTree(unittest.TestCase):
    """
    Tests checking if a SGRT tree is correctly reflected by sgrt_tree.
    """

    def setUp(self):
        """
        Setting up the test sgrt_tree.
        """

        self.test_dir = os.path.join(os.path.dirname(
            os.path.abspath(__file__)), 'test_data', 'Sentinel-1_CSAR')
        self.hierarchy_should = ['root', 'mode', 'group', 'datalog', 'product',
                                 'wflow', 'grid', 'tile', 'var', 'qlook']
        self.stt = sgrt_tree(self.test_dir, register_file_pattern='.tif')


    def test_tree_hierarchy(self):
        """
        Tests if a correct SGRT hierarchy was built.
        """

        self.assertEqual(self.stt.hierarchy, self.hierarchy_should)

        self.assertEqual(self.stt.root, self.test_dir)


    def test_tree_depth(self):
        """
        Checks if maximum depth is not violated.
        """

        max_depth_allowed = len(self.stt.root.split(os.sep)) + \
                            len(self.hierarchy_should) - 1

        self.assertTrue(all([len(x.split(os.sep)) <= max_depth_allowed
                             for x in self.stt.get_all_dirs()]))


if __name__ == "__main__":
    unittest.main()
