import unreal


class ControlRig(object):
    """
    The primary rig object that we operate on.
    """
    def __init__(self):
        self._rig = None

    @property
    def rig(self):
        return self._rig

    @rig.setter
    def rig(self, value):
        pass
