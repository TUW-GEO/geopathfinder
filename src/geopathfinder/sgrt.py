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
Base class for the SGRT folder structure

'''

import os
from geopathfinder.base import GeoTree







def sgrt_tree(root_path=None, product_id=None, wflow_id=None,
              ptop_name=None, grid='EQUI7', ftile=None, sgrt_var_name=None):


    '''
    levels = {'root_level': root_level,
              'main_level': main_level,
              'grid_level': grid_level,
              'data_level': data_level}
    '''

    '''
    levels = {'level_1': root_level,
              'level_2': main_level,
              'level_3': grid_level,
              'level_4': data_level,
              'level_5': data_level}}
    '''


    # function for the sensor and prodcut folders
    if product_id[0:2].lower() == 's1':
        sensor = "Sentinel-1_CSAR"
        product = product_id[3:9].upper()
    elif product_id[0:3].lower() == 'asa':
        sensor = "Envisat_ASAR"
        product = product_id[3:5].upper()
    elif product_id[0:3].lower() == 'asc':
        sensor = 'METOP_ASCAT'
        product = product_id[3:9].upper()
    elif product_id[0:3].lower() == 'sss':
        sensor = 'SCATSAR'
        product = product_id[3:8].upper()
    else:
        raise ValueError('product_id is unknown!')

    # function for the wflow_folder_names
    wflow_folder_names = {"A": "preprocessed", "B": "parameters", "C": "products", "N": "nrt"}
    wflow_group = wflow_folder_names[wflow_id[0].upper()]

    # function for the ptop_name
    top_folder = ptop_name

    # function for grid_folder, tile_folder
    grid_folder, tile_folder = "_".join([grid.upper(), ftile.split('_')[0]]), ftile.split('_')[1]

    # function for the sgrt_var_name
    var_folder = sgrt_var_name.lower().rstrip('-')


    # defining the levels in the directory tree (order could become shuffled around)
    levels = {'root': root_path,
              'sensor': sensor,
              'product': product,
              'group': wflow_group,
              'ptop': top_folder,
              'grid': grid_folder,
              'tile': tile_folder,
              'var': var_folder}

    # defining the hierarchy
    hierarchy = ['root', 'sensor', 'product', 'group',
                 'ptop', 'grid', 'tile', 'var']


    sgrt_struct = GeoTree(levels, hierarchy)


    return sgrt_struct

