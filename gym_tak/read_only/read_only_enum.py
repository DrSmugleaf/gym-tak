from gym_tak.read_only.read_only_properties import read_only_properties
from gym_tak.read_only.frozen_enum import frozen_enum


def read_only_enum(*args):
    def class_rebuilder(cls):
        cls = read_only_properties(*args)(cls)
        cls = frozen_enum(cls)
        return cls

    return class_rebuilder
