import bpy
from ..generaldata import *
from .node_tree import *
from .nodes import *
from .socket import *
from .copy_properties import *
from .check_selected_bones import *

classes = (
    RGC_NodeTree_Picker,
    RGC_ClickButton,
    RGC_MoveButton,
    RGC_CopyPropertie,
    #RGC_NodeTree_DrawPicker,
    
    
    )




def PickerRegister():
    for c in classes:
        bpy.utils.register_class(c)
    PickerNodeRegister()
    PickerSocketRegister()
    bpy.types.NODE_MT_editor_menus.prepend(DrawPicker)
    bpy.app.handlers.depsgraph_update_pre.append(update_nodos)
    bpy.types.WM_MT_button_context.append(DrawButton)
    bpy.app.timers.register(CheckSelectedBones, persistent=True)
    register_keymap()
    
def PickerUnregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    PickerNodeUnregister()
    PickerSocketUnregister()
    bpy.types.NODE_MT_editor_menus.remove(DrawPicker)
    bpy.app.handlers.depsgraph_update_pre.remove(update_nodos)
    bpy.types.WM_MT_button_context.remove(DrawButton)
    unregister_keymap()
