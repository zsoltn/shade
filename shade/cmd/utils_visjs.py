# Copyright (c) 2016 T-systems Zsolt Nagy
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from jinja2 import Environment, FileSystemLoader
import base64
from os import listdir, sep
from os.path import basename
import json

PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.join(PATH, 'templates')),
    trim_blocks=False)

TEMPLATE_ENVIRONMENT.filters['b64encode'] = base64.b64encode

file_list = { }


def render_template(template_filename, context):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)

#https://github.com/nathangrigg/dayone_export/blob/master/dayone_export/filters.py
def get_content( filename ):
    fn, ext = os.path.splitext(filename)
    with open(filename, 'rb') as content_file:
        content = base64.b64encode(content_file.read() ) 
    return "data:image/%s;base64,%s" % (ext[1:], content)
    return content



def init_image_file_list():
    imgdir = os.path.join(PATH, 'templates/img/') #PATH + '/templates/img/' 
    files = listdir(imgdir)
    for mfile in files:        
        file_list.update({basename(mfile): get_content(imgdir + mfile )})


def conv_dict_to_node_and_edges( dict ):
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


    nodes = []
    
    # add computer nodes  
    for data in dict:
        nodes.append({"id": data.get("id"), "label": data.get("name"),  "image": file_list['db.jpg'], "shape": 'image'})        
    
    # add networks 
    
    for data in dict:
        for k in data.get("addresses").keys():
            if k not in [ n["id"] for n in nodes ]: 
                nodes.append({"id": k, "label": k,  "image": file_list['Network-Pipe-icon.png'], "shape": 'image'} )  
         
    # add public net
    nodes.append( {"id": 1, "label": "PUBLIC NET" , "image": file_list['System-Firewall-3-icon.png'], "shape": 'image'} )
    
    
    #print nodes
    # add edges  
    edges = [ ]
    # add computer - network connections 
    for data in dict:
        edges.append({"from": data.get("id"), "to": data.get("addresses").keys()[0]  })        

    # add computer - eip connections 
    for data in dict:
        if data.get("public_v4"):
            edges.append({"from": data.get("id"), "to": 1,"label": 'EIP:('+ data.get("public_v4") + ')' ,"length": 250 })        
    
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    return nodes, edges 

def create_output(inventory_dict, output_file='inventory.html'):
    init_image_file_list()
    nodes, edges = conv_dict_to_node_and_edges(inventory_dict)
        
    context = {
        'file_list': file_list,
        'nodes': json.dumps( nodes ), 
        'edges': json.dumps( edges )
    }
    #
    with open(output_file, 'w') as f:
        html = render_template('visjs.html.template', context)
        htmlutf8 = html.encode('utf-8')
        f.write(htmlutf8)


def main():
    create_output({})

#############################################################################

if __name__ == "__main__":
    main()
