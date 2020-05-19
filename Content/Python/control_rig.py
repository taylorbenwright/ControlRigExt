import unreal


class ControlRigExtension(object):
    """
    The primary rig object that we operate on.
    """
    @classmethod
    def load_rig_from_path(cls, rig_path):
        """
        Loads in a ControlRigBlueprint based on its path. Returns the resultant rig object
        :param rig_path: The relative Game path to the rig, obtained by right click->Copy Reference
        :type rig_path: str
        :return: The valid ControlRigBlueprint object
        :rtype: unreal.ControlRigBlueprint
        """
        loaded_rig = unreal.load_asset(rig_path)

        if type(loaded_rig) == unreal.ControlRigBlueprint:
            return loaded_rig
        return None

    @staticmethod
    def cast_key_to_type(rig_key, rig):
        """
        Given an element key and its parent hierarchy modifier, returns the object of the correct type
        :param rig_key: The key to query
        :type rig_key: unreal.RigElementKey
        :param rig: The rig we are looking at
        :type rig: unreal.ControlRigBlueprint
        :return: The casted type for the key
        :rtype: unreal.RigBone | unreal.RigControl | unreal.RigSpace
        """
        hierarchy_mod = rig.get_hierarchy_modifier()
        if rig_key.type == unreal.RigElementType.BONE:
            return hierarchy_mod.get_bone(rig_key)
        elif rig_key.type == unreal.RigElementType.SPACE:
            return hierarchy_mod.get_space(rig_key)
        elif rig_key.type == unreal.RigElementType.CONTROL:
            return hierarchy_mod.get_control(rig_key)
        elif rig_key.type == unreal.RigElementType.CURVE:
            return hierarchy_mod.get_curve(rig_key)
        else:
            return None

    def __init__(self):
        """
        Creates a ControlRigExtension object. Through this object we can manipulate the loaded object
        """
        self._rig = None

    @property
    def rig(self):
        return self._rig

    @rig.setter
    def rig(self, value):
        self._rig = value

    def get_selected_controls(self):
        """
        Returns the controls that are selected in the hierarchy panel. These return in a first-in/last-out manner
        :return: A list of the selected object
        :rtype: list[unreal.RigElementKey]
        """
        return self.rig.get_hierarchy_modifier().get_selection()

    def get_index_by_name(self, controller_name):
        """
        Given a name, returns the associated RigElementKey.
        :param controller_name: The path of the key to query
        :type controller_name: str
        :return: The RigElementKeys with the given name, if any
        :rtype: unreal.RigElementKey
        """
        hierarchy_mod = self.rig.get_hierarchy_modifier()
        indexes = hierarchy_mod.get_elements()
        for ind in indexes:
            if ind.name == controller_name:
                return ind
        return None

    def paste_global_xform(self):
        """
        Given a selection, copy the global transform from the first control into the initial transform of the second
        control
        :return: Nothing
        :rtype: None
        """
        hierarchy_mod = self.rig.get_hierarchy_modifier()
        selection = self.get_selected_controls()
        if not len(selection) == 2:
            return
        global_xform = hierarchy_mod.get_global_transform(selection[1])
        hierarchy_mod.set_initial_global_transform(selection[0], global_xform)
