import os
import pandas as pd

def get_tomo_name(scipion_folder):
     
    scipion_abs_path = os.path.abspath(scipion_folder)
    scipion_runs = scipion_abs_path + '/Runs'
        
    in_runs= [name for name in os.listdir(scipion_runs) if os.path.isdir(os.path.join(scipion_runs, name))]
    process_dir=sorted(in_runs)
    
    movie_subfolder = scipion_runs + '/' + process_dir[0] + '/extra'
    mcor2_subfolder = scipion_runs + '/' + process_dir[1] + '/extra'
    ts_subfolder = scipion_runs + '/' + process_dir[2] + '/extra'
    aretomo_subfolder = scipion_runs + '/' + process_dir[-1] + '/extra'
    
    tomo_name = sorted([name for name in os.listdir(aretomo_subfolder) if os.path.isdir(os.path.join(aretomo_subfolder, name))])
    
    scipion_stru = pd.DataFrame((),columns=["import_movie_path","motioncor_path","ts_path","aretomo_path","tomo_name"])
    scipion_stru["tomo_name"]=tomo_name
    scipion_stru["ts_path"]=ts_subfolder
    scipion_stru["import_movie_path"]=movie_subfolder
    scipion_stru["motioncor_path"]=mcor2_subfolder
    scipion_stru["aretomo_path"]=aretomo_subfolder
    
    return scipion_stru    
