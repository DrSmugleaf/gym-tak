def read_only_properties(*args):

    def class_rebuilder(cls):

        def __setattr__(self, key, value):
            if key in args and key in self.__dict__:
                raise AttributeError("Can't modify %s" % key)
            else:
                super().__setattr__(key, value)

        cls.__setattr__ = __setattr__
        return cls

    return class_rebuilder
