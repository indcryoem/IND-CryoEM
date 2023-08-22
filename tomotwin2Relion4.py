#!usr/bin/env python3
  

# ===================================================================
# Name:		tomotwin2relion
# Purpose:	Converts ".coords" file from tomotwin particle picker to ".star" file for Relion 
#		More information: Check reference folder
# Author:	Arthur Melo & Eric Tse
# Created:	2023/04/12
# Version:	alpha_v3
# Last Change:	
# ===================================================================    
        

# =============
# Importing libraries    
# Observation: starfile needs to be installed on local machine. Run command 'pip install starfile'
# =============

import os
import sys
import subprocess
import argparse
import starfile
import pandas as pd
from get_tomo_name import get_tomo_name as gtn

parser = argparse.ArgumentParser("tomotwin2relion_batch.py")
parser.add_argument("input", help="folder with scipion project' format.", type=str)
parser.add_argument("-s",dest="scale", help="binning factor during AreTomo reconstruction", type=int, default=7)
args = parser.parse_args()

scipion_project = args.input
scale_factor = args.scale
scipion_str = gtn(scipion_project)



#Function for getting '.coords' files
def get_coords():
    res = []
    # Iterate directory
    for file in os.listdir(coords_folder):
        # check only text files
        if file.endswith('.coords'):
            res.append(file)         
    return res


star_item = []
for n,tomo in enumerate(scipion_str['tomo_name']):
    coords_folder = scipion_str['aretomo_path'][n] + '/' + tomo + '/out/coords/'
    res = get_coords()
    for j,coords_item in enumerate(res):
        coords_file = scipion_str['aretomo_path'][n] + '/' + tomo + '/out/coords/' + coords_item
        out_star = scipion_str['aretomo_path'][n] + '/' + tomo + '/out/coords/' + coords_item[0:-7] + '.star'
        if os.path.isfile(coords_file):
            coords = pd.read_csv(coords_file,sep=' ', header=None, names=["rlnCoordinateX","rlnCoordinateY","rlnCoordinateZ"])
            coords['rlnTomoName'] = tomo
            coords['rlnCoordinateX'] = coords['rlnCoordinateX']*scale_factor
            coords['rlnCoordinateY'] = coords['rlnCoordinateY']*scale_factor
            coords['rlnCoordinateZ'] = coords['rlnCoordinateZ']*scale_factor
            star_item.append(out_star)
            starfile.write(coords,out_star,overwrite=True)
            print('Done with file',coords_item[0:-7],'!')
        else:
            print(coords_file + ' is not a file')
            
            
#Merge starfiles
file_string = ""
for i in star_item:
    file_string += i + " "
print('####################################################\n')    
print('Copy and execute this command to merge all starfiles\n')
print('relion_star_handler --combine --i',repr(file_string),'--o combined.star --ignore_optics true')