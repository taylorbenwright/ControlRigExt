import unreal

'''
Non UFUNCTION functions as we cannot call ufunctions within ufunctions unless if nested
'''

def cast_key_to_type(rig, rig_key):
    """
    Given an element key and its parent hierarchy modifier, returns the object of the correct type
    :param rig: The rig we are looking at
    :type rig: unreal.ControlRigBlueprint
    :param rig_key: The key to query
    :type rig_key: unreal.RigElementKey
    :return: The casted type for the key
    :rtype: unreal.RigBone | unreal.RigControl | unreal.RigSpace | unreal.RigCurve
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

def get_selected_controls(rig):
    """
    Returns the controls that are selected in the hierarchy panel. These return in a first-in/last-out manner
    :param rig: The rig we are looking at
    :type rig: unreal.ControlRigBlueprint
    :return: A list of the selected object
    :rtype: list[unreal.RigElementKey]
    """
    return rig.get_hierarchy_modifier().get_selection()

def create_rig_element_key(rig, key_type):

    """
    Given a RigElementType, add desired rig element to the rig with specific identifier.
    If there are selected rig elements, this will add desired rig element with selected transforms and name attached.
    :param rig: The rig we are looking at
    :type rig: unreal.ControlRigBlueprint
    :param key_type: enum value of Rig Element Type
    :type key_type: unreal.RigElementType value
    :return: A list of the selected object
    :rtype: list[unreal.RigElementKey] | list[]
    """

    element_list = []

    if key_type == unreal.RigElementType.BONE:

        type_name = "bone"

    elif key_type == unreal.RigElementType.SPACE:
    
        type_name = "space"

    elif key_type == unreal.RigElementType.CONTROL:

        type_name = "ctrl"
    
    elif key_type == unreal.RigElementType.CURVE:
        
        type_name = "curve"

    elif key_type == unreal.RigElementType.NONE or key_type == unreal.RigElementType.ALL:
        
        return element_list

    hierarchy_mod = rig.get_hierarchy_modifier()
    selection = hierarchy_mod.get_selection()

    if not selection:

        global_xform = unreal.Transform()

        element_name = type_name

        element = add_element_with_init_transform(hierarchy_mod, element_name, key_type, global_xform)

        element_list.append(element)

    for item in selection:

        global_xform = hierarchy_mod.get_global_transform(item)

        element_name = "{0}_{1}".format(item.get_editor_property("Name"), type_name)

        element = add_element_with_init_transform(hierarchy_mod, element_name, key_type, global_xform)

        element_list.append(element)
        
    return element_list

def add_element_with_init_transform(hierarchy_mod, element_name, key_type, global_xform):
    """
    Create a new element to the control rig hiearchy with a given name, element type, and initial transform
    :param hierarchy_mod: The control rig hierarchy object
    :type hierarchy_mod: unreal.ControlRigHierarchyModifier
    :param element_name: name of the new element
    :type element_name: str
    :param key_type: what RigElementType it will be
    :type key_type: unreal.RigElementType value
    :param global_xform: the initial transform
    :type global_xform: unreal.Transform
    :return: Nothing
    :rtype: None
    """

    element = add_element_to_hierarchy_mod(hierarchy_mod, element_name, key_type)

    if key_type != unreal.RigElementType.CURVE:
        
        hierarchy_mod.set_initial_global_transform(element, global_xform)

    return element

def add_element_to_hierarchy_mod(hierarchy_mod, element_name, key_type):
    """
    Create a new element to the control rig hiearchy with a given name and element type
    :param hierarchy_mod: The control rig hierarchy object
    :type hierarchy_mod: unreal.ControlRigHierarchyModifier
    :param element_name: name of the new element
    :type element_name: str
    :param key_type: what RigElementType it will be
    :type key_type: unreal.RigElementType value
    :return: Nothing
    :rtype: None
    """

    if key_type == unreal.RigElementType.BONE:

        element = hierarchy_mod.add_bone(element_name)

    elif key_type == unreal.RigElementType.SPACE:

        element = hierarchy_mod.add_space(element_name)

    elif key_type == unreal.RigElementType.CONTROL:

        element = hierarchy_mod.add_control(element_name)

    elif key_type == unreal.RigElementType.CURVE:
        
        element = hierarchy_mod.add_curve(element_name)

    else:

        element = None

    return element

def edit_element_property(hierarchy_mod, rig_element, property, value):
    """
    Given a rig element, edit the given property with the given value
    :param hierarchy_mod: The control rig hierarchy object
    :type hierarchy_mod: unreal.ControlRigHierarchyModifier
    :param rig_element: The rig element key object
    :type rig: unreal.RigElementKey
    :param property: property name 
    :type property: string
    :param value: value for the property
    :type value: object
    :return: Nothing
    :rtype: None
    """

    rig_element.set_editor_property(property, value)
    hierarchy_mod.set_control(rig_element)

def get_elements_by_rig_type(rig, selection, rig_element_type):
    """
    Given a boolean, set selected controls' gizmo to that color
    :param rig: The control rig object
    :type rig: unreal.ControlRigBlueprint
    :param selection: list of RigElementKeys
    :type selection: list[unreal.RigElementKey]
    :param rig_element_type: class type of desired rig type
    :type rig_element_type: unreal.uclass
    :return: return_list 
    :rtype: list[rig_element_type] | list[]
    """

    return_list = []

    if not selection:
    
        return return_list

    for item in selection:

        rig_element = cast_key_to_type(rig, item)

        if type(rig_element) != rig_element_type:

            continue

        return_list.append(rig_element)

    return return_list