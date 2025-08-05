
class Config (object):
    def __init__ (self, fp):
        with open(fp, 'r') as cfg:
            lines = cfg.readlines()

        for line in lines:
            entries = line.split('=', 1)
            k = entries[0].strip()
            try:
                v = entries[1].strip()
                v = self.__validate(v)
            except IndexError:
                v = None
            self.__dict__[k] = v

    def __validate (self, item):
        cast = [int, float]
        for cls in cast:
            try:
                return cls(item)
            except ValueError:
                pass
        return item

