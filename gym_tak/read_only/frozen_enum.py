from enum import EnumMeta


class FrozenEnum(EnumMeta):
    def __getattr__(cls, name):
        if name not in cls._member_map_:
            raise AttributeError('%s %r has no attribute %r' % (cls.__class__.__name__, cls.__name__, name))
        return super().__getattr__(name)

    def __setattr__(cls, name, value):
        if name in cls.__dict__ or name in cls._member_map_:
            return super().__setattr__(name, value)
        raise AttributeError('Cannot create new members for %s %r' % (cls.__class__.__name__, cls.__name__))


def frozen_enum(enum_class):
    enum_class.__class__ = FrozenEnum
    return enum_class
