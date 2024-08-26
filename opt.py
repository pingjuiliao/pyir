#!/usr/bin/env python3

import argparse
import json
import logging
import os
import sys

from pyir import ir_pass
from pyir.interface import bril

logger = logging.getLogger("opt.py")
logging.basicConfig(level=logging.INFO)

PASS_MAP = {
    "tdce": "pyir.redundancy.tdce.TrivialDeadCodeElimination",
}


def list_all_passes():
    logger.info("All passes")
    logger.info("--- End of the list of passes")

def optimize(module, passes):
    pass_manager = ir_pass.PassManager()
    for pass_name in passes:
        if pass_name not in PASS_MAP:
            logger.error(f"Cannot find pass {pass_name}")
            quit()
        pass_module_name = PASS_MAP[pass_name]
        module_name, class_name = pass_module.rsplit(".", 1)
        module = __import__(module_name, fromlist=[class_name])
        PassClass = getattr(module, class_name)
        pass_manager.add_pass(PassClass())

    pass_manager.transform(module)
    return module


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--list", action="store_true")
    parser.add_argument("-c", "--source", type=str)
    parser.add_argument("-p", "--passes", nargs="+")

    args = parser.parse_args()
    if args.list:
        list_all_passes()
        quit()

    if not os.path.exists(args.source):
        logger.error(f"{args.source} does not exists")
        quit()

    # compile & optimize
    interface = bril.BrilInterface()
    module = interface.parse(args.source)
    passes = [] if args.passes is None else args.passes
    optimize(module, passes)
    module_json = interface.dump_json(module)
    #fs = json.dumps(module_json, indent=2)
    # print(fs)
    json.dump(module_json, sys.stdout)

if __name__ == '__main__':
    main()
