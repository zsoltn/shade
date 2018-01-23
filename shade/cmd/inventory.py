# Copyright (c) 2015 Hewlett-Packard Development Company, L.P.
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

import argparse
import json
import sys
import yaml

import shade
import shade.inventory


from utils_excel import create_output as create_output_excel  # @UnusedImport
from utils_visjs import create_output as create_output_graph  # @UnusedImport
from utils_tree import create_output as create_output_tree  # @UnusedImport


def output_format_dict(data, use_yaml, use_tree, use_graph, use_excel):
    if use_yaml:
        return yaml.safe_dump(data, default_flow_style=False)
    if use_graph: 
        create_output_graph(data, output_file="inventory.html")
        return "Graph report created!"            
    elif use_tree:
         
        small = filter_dict(data)
        create_output_tree(small)        
    elif use_excel:
        small = filter_dict(data)             
        create_output_excel(small,output_file="inventory.xls")        
        return "Excel report created!"
    else:
        return json.dumps(data, sort_keys=True, indent=2)

def filter_dict( datas ):
    small_datas = []
    for data in datas:
        vols = []
        for v in data["volumes"] :
            vol = {   "bootable": v.get("bootable"),
                       "device": v.get("device"),
                       "display_name": v.get("display_name"),
                       "size": v.get("metadata").get("quantityGB"),
                   }
            vols.append(vol)
        small_data = { "name": data.get("name"),
                      #"id": data.get("id"),
                       "key_name": data.get("key_name"),
                       "az": data.get("az"),
                       "interface_ip": data.get("interface_ip"),
                       "interface_v6": data.get("interface_v6"),
                       "net": data.get("addresses"),
                       "state": data.get("OS-EXT-STS:vm_state"),
                       "LaunchedAt": data.get("OS-SRV-USG:launched_at"),
                       "flavor": data.get("flavor"),
                       "image": data.get("image"),
                       "volumes": vols,                                              
                       }        
        small_datas.append(small_data)
    
    #print small_datas
    return small_datas



def parse_args():
    parser = argparse.ArgumentParser(description='OpenStack Inventory Module')
    parser.add_argument('--refresh', action='store_true',
                        help='Refresh cached information')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--list', action='store_true',
                       help='List active servers')
    group.add_argument('--host', help='List details about the specific host')
    parser.add_argument('--private', action='store_true', default=False,
                        help='Use private IPs for interface_ip')
    parser.add_argument('--cloud', default=None,
                        help='Return data for one cloud only')
    parser.add_argument('--excel', action='store_true', default=False,
                        help='Output data in excel format')
    parser.add_argument('--graph', action='store_true', default=False,
                        help='Output data in Visual Graph')
    parser.add_argument('--tree', action='store_true', default=False,
                        help='Output data in text tree format')
    parser.add_argument('--yaml', action='store_true', default=False,
                        help='Output data in nicely readable yaml')

    parser.add_argument('--debug', action='store_true', default=False,
                        help='Enable debug output')
    return parser.parse_args()


def main():
    args = parse_args()
    try:
        shade.simple_logging(debug=args.debug)
        inventory = shade.inventory.OpenStackInventory(
            refresh=args.refresh, private=args.private,
            cloud=args.cloud)
        if args.list:
            output = inventory.list_hosts()
        elif args.host:
            output = inventory.get_host(args.host)
                    
        print(output_format_dict(output, args.yaml, args.tree, args.graph, args.excel))
    except shade.OpenStackCloudException as e:
        sys.stderr.write(e.message + '\n')
        sys.exit(1)
    sys.exit(0)


if __name__ == '__main__':
    main()
