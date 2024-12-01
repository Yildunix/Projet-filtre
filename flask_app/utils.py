#####################################################################
####################### Modules standards############################
#####################################################################
import os 

#####################################################################
#################### Modules exportes ###############################
#####################################################################
import pandas as pd 




def get_file_extension(filename):
    """Retourne l'extension du fichier en minuscules."""
    return os.path.splitext(filename)[1].lower()

def load_csv(filepath):
    """Charge un fichier CSV et retourne un DataFrame pandas."""
    return pd.read_csv(filepath)

def is_csv(filename):
    """Vérifie si le fichier est un CSV."""
    return get_file_extension(filename) == '.csv'


