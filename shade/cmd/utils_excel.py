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

import xlwt
from datetime import datetime
import json


def create_workbook(inventory_dict, output_file='inventory.xls'):            
    wb = xlwt.Workbook()
    sheet = wb.add_sheet("servers")
            
    create_sheet(sheet, inventory_dict)
    wb.save(output_file)


def create_sheet(sheet, itemlist):    
    style0 = xlwt.easyxf('font: name Times New Roman, color-index black, bold on',num_format_str='D-MMM-YY' )
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = xlwt.Style.colour_map['gray25']
    style0.pattern = pattern
    
    style1 = xlwt.easyxf(num_format_str='D-MMM-YY')

    if isinstance(itemlist, list):
        rowc = 1
        for item in itemlist:            
            if isinstance(item, dict):
                colc = 0
                for k,v in item.items():
                    # here this is a dict of the keys
                    v2 = v
                    if isinstance(v, dict):                     
                        v2 = json.dumps( v ) 
                    if rowc == 1:
                        sheet.write(rowc-1, colc, k,style0)
                    sheet.write(rowc, colc, str(v2))
                    colc = colc + 1
            else :
                raise  KeyError ("not support embeded list")
            rowc= rowc + 1  
        
        
    

def create_output(inventory_dict, output_file='inventory.xls'):        
    if not output_file: 
        raise KeyError( "Output File Mandatory!")
    create_workbook( inventory_dict, output_file )