#!/usr/bin/env python3

import sys
import json
import logging

from pyir.interface import bril

def main():
    bril_file = "./clobber.bril"
    if len(sys.argv) >= 2:
        bril_file = sys.argv[1]

    logging.basicConfig(level=logging.INFO)
    interface = bril.BrilInterface()
    module = interface.parse(bril_file)
    module_json = interface.dump_json(module)
    #fs = json.dumps(module_json, indent=2)
    # print(fs)
    json.dump(module_json, sys.stdout)

if __name__ == '__main__':
    main()
