
# Package import
import unreal

# Utility import
import control_rig_utils

@unreal.uclass()
class ControlRigBPExt(unreal.BlueprintFunctionLibrary):

    @unreal.ufunction(params = [unreal.ControlRigBlueprint], ret=unreal.Array(unreal.RigElementKey), static = True, meta=dict(Category="Control Rig Blueprint Ext"))
    def GetSelectedControls(rig):
        """
        Returns the controls that are selected in the hierarchy panel. These return in a first-in/last-out manner
        :param rig: The rig we are looking at
        :type rig: unreal.ControlRigBlueprint
        :return: A list of the selected object
        :rtype: list[unreal.RigElementKey]
        """

        return rig.get_hierarchy_modifier().get_selection()

    @unreal.ufunction(params=[unreal.ControlRigBlueprint, unreal.Name], ret=unreal.RigElementKey, static = True, meta=dict(Category="Control Rig Blueprint Ext"))
    def GetIndexByControlName(rig, control_name):
        """
        Given a name, returns the associated RigElementKey.
        :param rig: The control rig object
        :type rig: unreal.ControlRigBlueprint
        :param control_name: The path of the key to query
        :type control_name: str
        :return: The RigElementKeys with the given name, if any
        :rtype: unreal.RigElementKey
        """

        hierarchy_mod = rig.get_hierarchy_modifier()
        indexes = hierarchy_mod.get_elements()
        for ind in indexes:
            if ind.name == control_name:
                return ind
        return None

    @unreal.ufunction(params=[unreal.ControlRigBlueprint], static = True, meta=dict(Category="Control Rig Blueprint Ext"))
    def CopyPasteSelectedGlobalXform(rig):
        """
        Given a selection, copy the global transform from the first control into the initial transform of the second
        control
        :param rig: The control rig object
        :type rig: unreal.ControlRigBlueprint
        :return: Nothing
        :rtype: None
        """

        hierarchy_mod = rig.get_hierarchy_modifier()
        selection = hierarchy_mod.get_selection()

        if not len(selection) == 2:

            unreal.log("Not enough Control Rig controls selected")

            return

        global_xform = hierarchy_mod.get_global_transform(selection[1])
        hierarchy_mod.set_initial_global_transform(selection[0], global_xform)

    @unreal.ufunction(params = [unreal.ControlRigBlueprint, unreal.RigElementType], ret=unreal.Array(unreal.RigElementKey), static = True, meta=dict(Category="Control Rig Blueprint Ext"))
    def CreateRigElement(rig, element_type):
        """
        Given an element type, create a RigElement of that type. If any RigElement is selected, the new element will have the selected element's global transform as initial.
        :param rig: The control rig object
        :type rig: unreal.ControlRigBlueprint
        :return: elements
        :rtype: list[unreal.RigElementKey]
        """

        elements = control_rig_utils.create_rig_element_key(rig, element_type)

        return elements

    @unreal.ufunction(params = [unreal.ControlRigBlueprint, unreal.RigElementKey, unreal.RigElementKey], static = True, meta=dict(Category="Control Rig Blueprint Ext"))
    def ParentRigElements(rig, parent, child):
        """
        Given 2 rig elements, parent one to the other in the rig hierarchy
        :param rig: The control rig object
        :type rig: unreal.ControlRigBlueprint
        :param parent: The parent element
        :type parent: unreal.RigElementKey
        :param child: The child element
        :type child: unreal.RigElementKey
        :return: elements
        :rtype: list[unreal.RigElementKey]
        """

        hierarchy_mod = rig.get_hierarchy_modifier()

        hierarchy_mod.reparent_element(child, parent)

    @unreal.ufunction(params = [unreal.ControlRigBlueprint], static = True, meta=dict(Category="Control Rig Blueprint Ext"))
    def UpdateSelectedElementsInitialTransfromFromCurrentGlobal(rig):
        """
        Get selected rig elements, take the current transforms as the initial transforms
        :param rig: The control rig object
        :type rig: unreal.ControlRigBlueprint
        :return: Nothing
        :rtype: None
        """

        hierarchy_mod = rig.get_hierarchy_modifier()
        selection = hierarchy_mod.get_selection()

        for item in selection:
    
            updated_xform = hierarchy_mod.get_global_transform(item)

            hierarchy_mod.set_initial_global_transform(item, updated_xform)

    @unreal.ufunction(params = [unreal.ControlRigBlueprint], static = True, meta=dict(Category="Control Rig Blueprint Ext"))
    def ZeroSelectedElementsInitialTransfrom(rig):
        """
        Set selected rig elements' intial transform to default
        :param rig: The control rig object
        :type rig: unreal.ControlRigBlueprint
        :return: Nothing
        :rtype: None
        """

        hierarchy_mod = rig.get_hierarchy_modifier()
        selection = hierarchy_mod.get_selection()

        for item in selection:
    
            updated_xform = unreal.Transform(location = [0,0,0], rotation = [0,0,0], scale = [1,1,1])

            hierarchy_mod.set_initial_global_transform(item, updated_xform)

    @unreal.ufunction(params=[unreal.ControlRigBlueprint], static = True, meta=dict(Category="Control Rig Blueprint Ext"))
    def CopyPasteSelectedGizmos(rig):
        """
        Copy the first selected control gizmo attributes and paste it to the second control.
        :param rig: The control rig object
        :type rig: unreal.ControlRigBlueprint
        :return: Nothing
        :rtype: None
        """

        hierarchy_mod = rig.get_hierarchy_modifier()
        selection = hierarchy_mod.get_selection()
        
        if not len(selection) == 2:
            
            return

        src_element = control_rig_utils.cast_key_to_type(rig, selection[1])
        dst_element = control_rig_utils.cast_key_to_type(rig, selection[0])

        if type(src_element) != unreal.RigControl and type(dst_element) != unreal.RigControl:

            return
        
        gizmo_name = src_element.get_editor_property("gizmo_name")
        gizmo_color = src_element.get_editor_property("gizmo_color")
        gizmo_transform = src_element.get_editor_property("gizmo_transform")
        gizmo_enabled = src_element.get_editor_property("gizmo_enabled")

        dst_element.set_editor_property("gizmo_name", gizmo_name)
        dst_element.set_editor_property("gizmo_color", gizmo_color)
        dst_element.set_editor_property("gizmo_transform", gizmo_transform)
        dst_element.set_editor_property("gizmo_enabled", gizmo_enabled)

        hierarchy_mod.set_control(dst_element)

    @unreal.ufunction(params=[unreal.ControlRigBlueprint, unreal.LinearColor], static = True, meta=dict(Category="Control Rig Blueprint Ext"))
    def EditGizmoColor(rig, color):
        """
        Given a color, set selected controls' gizmo to that color
        :param rig: The control rig object
        :type rig: unreal.ControlRigBlueprint
        :param color: The color object
        :type color: unreal.LinearColor
        :return: Nothing
        :rtype: None
        """

        hierarchy_mod = rig.get_hierarchy_modifier()
        selection = hierarchy_mod.get_selection()

        rig_elements = control_rig_utils.get_elements_by_rig_type(rig, selection, unreal.RigControl)

        for rig_element in rig_elements:

            rig_element.set_editor_property("gizmo_color", color)
            hierarchy_mod.set_control(rig_element)
    
    @unreal.ufunction(params=[unreal.ControlRigBlueprint, unreal.Transform()], static = True, meta=dict(Category="Control Rig Blueprint Ext"))
    def EditGizmoTransform(rig, transform):
        """
        Given a transform, set selected controls' gizmo to that color
        :param rig: The control rig object
        :type rig: unreal.ControlRigBlueprint
        :param transform: The transform object
        :type transform: unreal.Transform
        :return: Nothing
        :rtype: None
        """

        hierarchy_mod = rig.get_hierarchy_modifier()
        selection = hierarchy_mod.get_selection()

        rig_elements = control_rig_utils.get_elements_by_rig_type(rig, selection, unreal.RigControl)

        for rig_element in rig_elements:
    
            rig_element.set_editor_property("gizmo_transform", transform)
            hierarchy_mod.set_control(rig_element)

    @unreal.ufunction(params=[unreal.ControlRigBlueprint, bool], static = True, meta=dict(Category="Control Rig Blueprint Ext"))
    def EditGizmoEnabled(rig, is_enabled):
        """
        Given a boolean, set selected controls' gizmo to that color
        :param rig: The control rig object
        :type rig: unreal.ControlRigBlueprint
        :param is_enabled: is gizmo enabled
        :type is_enabled: bool
        :return: Nothing
        :rtype: None
        """

        hierarchy_mod = rig.get_hierarchy_modifier()
        selection = hierarchy_mod.get_selection()

        rig_elements = control_rig_utils.get_elements_by_rig_type(rig, selection, unreal.RigControl)

        for rig_element in rig_elements:
    
            rig_element.set_editor_property("gizmo_enabled", is_enabled)
            hierarchy_mod.set_control(rig_element)

    @unreal.ufunction(params=[unreal.ControlRigBlueprint, str, str], static = True, meta=dict(Category="Control Rig Blueprint Ext"))
    def SearchAndReplaceRigElementNames(rig, search_string, replace_string):
        """
        Given a string, search for it in the selected rig elements' name 
        and replace it with another string in the selected rig elements' name
        :param rig: The control rig object
        :type rig: unreal.ControlRigBlueprint
        :param search_string: search for string
        :type search_string: string
        :param replace_string: string for replace
        :type replace_string: string
        :return: Nothing
        :rtype: None
        """

        hierarchy_mod = rig.get_hierarchy_modifier()
        selection = hierarchy_mod.get_selection()

        if not selection:

            return

        for item in selection:

            src_name = str(item.get_editor_property("name"))

            new_name = src_name.replace(search_string, replace_string)

            hierarchy_mod.rename_element(item, new_name)

    @unreal.ufunction(params=[unreal.ControlRigBlueprint, str, bool], static = True, meta=dict(Category="Control Rig Blueprint Ext"))
    def AddStringPrefixOrSuffixToSelected(rig, insert_text, is_suffix):
        """
        Given a string, insert it at the start or end of the selected rig elements' name
        :param rig: The control rig object
        :type rig: unreal.ControlRigBlueprint
        :param insert_text: the insert string
        :type insert_text: string
        :param is_suffix: adding it to the end or start?
        :type is_suffix: bool
        :return: Nothing
        :rtype: None
        """

        hierarchy_mod = rig.get_hierarchy_modifier()
        selection = hierarchy_mod.get_selection()

        if not selection:

            return

        for item in selection:

            src_name = str(item.get_editor_property("name"))

            new_name = "{0}_{1}".format(insert_text, src_name)

            if is_suffix:
                
                new_name = "{0}_{1}".format(src_name, insert_text)

            hierarchy_mod.rename_element(item, new_name)

    @unreal.ufunction(params=[unreal.ControlRigBlueprint, str, int, int], static = True, meta=dict(Category="Control Rig Blueprint Ext"))
    def RenameAndNumberSelectedControls(rig, name, start_number, number_padding):
        """
        Given a name, start number, and number padding, set selected rig elements' name to a newly created name
        :param rig: The control rig object
        :type rig: unreal.ControlRigBlueprint
        :param name: replacement name
        :type name: string
        :param start_number: start number for numberring items
        :type start_number: int
        :param number_padding: this many digits padded for text
        :type number_padding: int
        :return: Nothing
        :rtype: None
        """
        
        hierarchy_mod = rig.get_hierarchy_modifier()
        selection = hierarchy_mod.get_selection()

        if not selection:

            return

        x = start_number

        for item in selection:

            new_name = "{0}_{1}".format(name, str(x).zfill(number_padding))

            hierarchy_mod.rename_element(item, new_name)

            x+=1

print("Control Rig Ext Loaded")