#Libraries

import os
import pandas as pd
import numpy as np
import matplotlib as plt

#Scripts
import exception_handeler as eh

def automatic_graph_saver(folder, name_file):
    name = eh.name(name_file)
    os.makedirs(f'{folder}', exist_ok=True)
    plt.savefig(f'{folder}/{name}.png')

def auto_name_fixer(element):
    element = element.replace('_', ' ')
    return element