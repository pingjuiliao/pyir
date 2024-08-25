#!/usr/bin/env python3

import logging

class PYIRComponent(object):
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)


class PYIRComposite(PYIRComponent):
    def __init__(self):
        raise NotImplementedError

    def get_components(self):
        raise NotImplementedError
