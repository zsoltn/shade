#! /usr/bin/env python
from os import listdir, sep
from os.path import abspath, basename, isdir


tree_text = ""
def dict_tree(d, indent=0 ):
    global tree_text
    
    for key, value in d.iteritems():    
        tree_text = tree_text + "  " * (indent+1)  + str(key) + "\n"  
        tree_text = tree_text +  ("  " * (indent+1))  + '|' + "\n"
        if isinstance(value, dict):
            dict_tree(value, indent+1)
        elif isinstance(value, list):
            for v2 in value:
                if isinstance(v2, dict):
                    dict_tree(v2, indent+1)
                elif isinstance(v2, list):
                    for v3 in v2:
                        dict_tree(v3, indent+1)
                else:
                    tree_text = tree_text +  ('  ' * (indent+1))+ '+-' + str(v2) + "\n"
                    #raise  KeyError ("not support embeded list")  
        else:
            tree_text = tree_text +  ('  ' * (indent+1))+ '+-' + str(value) + "\n" 


def create_output(inventory_dict, output_file=None):
    if isinstance(inventory_dict, list):
        for item in inventory_dict:    
            dict_tree( item )
    if not output_file: 
        print tree_text
    else:
        with open(output_file, 'w') as f:                
            f.write(tree_text)


