class Config (object):
    def __init__ (self, fp):
        self.fp = fp
        self.__load(fp)

    def __load (self, fp):
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

    def force_reload (self):
        self.__load(self.fp)

    def __validate (self, item):
        cast = [int, float]
        for cls in cast:
            try:
                return cls(item)
            except ValueError:
                pass
        return item

