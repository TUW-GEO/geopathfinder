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
import os
import shutil
from datetime import date, datetime
import glob
import numpy.testing as nptest
import numpy as np

from geopathfinder.sgrt import sgrt_tree

def curpath():
    # pth, _ = os.path.split(os.path.abspath(__file__))
    pth = r'R:\Projects_work\SAR_NRT_Code_Sprint\test_pathfinder'
    return pth


class TestSgrt(unittest.TestCase):

    def setUp(self):
        self.path = os.path.join(curpath())

    def tearDown(self):
        shutil.rmtree(self.path)


    def test_sgrt(self):

        target = r'R:\Projects_work\SAR_NRT_Code_Sprint\test_pathfinder\Sentinel-1_CSAR\IWGRDH\products\ssm\EQUI7_EU500M\E048N006T6\ssm'

        root_path = curpath()
        product_id = 'S1AIWGRDH'
        wflow_id = 'C1003'
        ptop_name = 'ssm'
        grid = 'EQUI7'
        ftile = 'EU500M_E048N006T6'
        sgrt_var_name = 'SSM--'

        sgrt_dir = sgrt_tree(root_path=root_path, product_id=product_id, wflow_id=wflow_id,
                      ptop_name=ptop_name, grid=grid, ftile=ftile, sgrt_var_name=sgrt_var_name)

        result = sgrt_dir.get_dir(make_dir=True)

        # test correct path string
        assert result == target

        # test if directory was created
        assert os.path.exists(result)


        pass



if __name__ == "__main__":

    unittest.main()
