#!/usr/bin/env python3

#lets make a star file to take aretomo to reliontomo#
###################################
#gespannt wie en flitzebogen     ##
#pour moi en tout cas            ##
#wa ga na ha hakumen- oshitemairu##
###################################
#░░░░░░░█▐▓▓░████▄▄▄█▀▄▓▓▓▌█
#░░░░░▄█▌▀▄▓▓▄▄▄▄▀▀▀▄▓▓▓▓▓▌█
#░░░▄█▀▀▄▓█▓▓▓▓▓▓▓▓▓▓▓▓▀░▓▌█
#░░█▀▄▓▓▓███▓▓▓███▓▓▓▄░░▄▓▐█▌
#░█▌▓▓▓▀▀▓▓▓▓███▓▓▓▓▓▓▓▄▀▓▓▐█
#▐█▐██▐░▄▓▓▓▓▓▀▄░▀▓▓▓▓▓▓▓▓▓▌█▌
#█▌███▓▓▓▓▓▓▓▓▐░░▄▓▓███▓▓▓▄▀▐█
#█▐█▓▀░░▀▓▓▓▓▓▓▓▓▓██████▓▓▓▓▐█
#▌▓▄▌▀░▀░▐▀█▄▓▓██████████▓▓▓▌█▌
#▌▓▓▓▄▄▀▀▓▓▓▀▓▓▓▓▓▓▓▓█▓█▓█▓▓▌█▌
#█▐▓▓▓▓▓▓▄▄▄▓▓▓▓▓▓█▓█▓█▓█▓▓▓▐
###################################

import os
import sys
import subprocess
import argparse
from datetime import date
from get_tomo_name import get_tomo_name as gtn
from fix_aretomo_function import fix_aretomo

###########
#variables#
###########
parser = argparse.ArgumentParser("scipion-aretomo_stargen.py")
parser.add_argument("input", help="path to Scipion folder project", type=str)
args = parser.parse_args()

#User input
scipion_project=args.input

#output_file
today = date.today()
username = os.getlogin()
out_star = 'tomo_list_for_Relion4_' + str(username) + '_' + str(today) + '.star'

#Get scipion structure
scipion_str = gtn(scipion_project)

#Fix AreTomo newst and tilt files
fix_aretomo(scipion_project)

##############################
#append contents to star file#
##############################
well="""# tomograms_descr.star

data_

loop_
_rlnTomoName
_rlnTomoTiltSeriesName
_rlnTomoImportImodDir
_rlnTomoImportCtfFindFile
_rlnTomoImportCulledFile
"""
come="echo '{}' > {}".format(well,out_star)
os.system(come)

for n,tomo in enumerate(scipion_str['tomo_name']):
    ts_stack = scipion_str['ts_path'][n] + '/' + tomo + '.mrcs'
    imod_folder = scipion_str['aretomo_path'][n] + '/' + tomo +'/' + tomo +'_Imod'
    ctf= scipion_str['aretomo_path'][n] + '/' + tomo +'/' + tomo + 'ctf.txt'
    cull=scipion_str['aretomo_path'][n] + '/' + tomo +'/' + tomo +'_culled.mrc'
    command="echo '{} {} {} {} {}' >> {}".format(tomo,ts_stack,imod_folder,ctf,cull,out_star)
    os.system(command)
