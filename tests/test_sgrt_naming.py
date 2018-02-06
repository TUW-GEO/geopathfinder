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
import shutil
from datetime import date, datetime
import glob
import unittest

import numpy.testing as nptest
import numpy as np

import logging

logging.basicConfig(level=logging.INFO)

from geopathfinder.sgrt_naming import get_full_sgrt_path
from geopathfinder.sgrt_naming import SgrtFolderName
from geopathfinder.sgrt_naming import SgrtFilename

def curpath():
    # pth, _ = os.path.split(os.path.abspath(__file__))
    pth = r'R:\Projects_work\SAR_NRT_Code_Sprint\test_pathfinder'
    return pth

'''
class TestSgrt(unittest.TestCase):

    def setUp(self):
        self.path = os.path.join(curpath())

    def tearDown(self):
        #if os.path.exists(self.path):
        #    shutil.rmtree(self.path)
        pass


    def test_a_sgrt(self):

        target = r'R:\Projects_work\SAR_NRT_Code_Sprint\test_pathfinder\Sentinel-1_CSAR\IWGRDH\products\datasets\ssm' \
                 r'\C1003\EQUI7_EU500M\E048N006T6\ssm\qlooks'


        root_path = curpath()
        product_id = 'S1AIWGRDH'
        wflow_id = 'C1003'
        ptop_name = 'ssm'
        grid = 'EQUI7'
        ftile = 'EU500M_E048N006T6'
        sgrt_var_name = 'SSM--'

        sgrt_dir = get_full_sgrt_path(dir_root=root_path, product_id=product_id, wflow_id=wflow_id,
                             ptop_name=ptop_name, grid=grid, ftile=ftile, sgrt_var_name=sgrt_var_name)

        result = sgrt_dir.get_dir(make_dir=True)

        # test correct path string
        assert result == target

        # test if directory was created
        assert os.path.exists(result)


        pass


    def test_b_SgrtFolderName(self):

        root_path = curpath()
        product_id = 'S1AIWGRDH'
        wflow_id = 'C1003'
        ptop_name = 'ssm'
        grid = 'EQUI7'
        ftile = 'EU500M_E048N006T6'
        sgrt_var_name = 'SSM--'

        obj = SgrtFolderName(dir_root=root_path, product_id=product_id, wflow_id=wflow_id,
                             ptop_name=ptop_name, grid=grid, ftile=ftile, sgrt_var_name=sgrt_var_name)


        xtile = 'AF500M_E054N036T6'
        obj.build_subdirs(ptop_name=ptop_name, grid=grid, ftile=xtile, sgrt_var_name=sgrt_var_name, makedir=True)

        # test if directory was created
        assert os.path.exists(obj.level_5)
'''


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


if __name__ == "__main__":

    unittest.main()
