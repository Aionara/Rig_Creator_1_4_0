import bpy
from .general_nodes import *
from .add_node import *
from .select_bone import *
from .bone import *
from .image import *
from .value import *
from .outpicker import *
from .select_bone_range import *
from .join_picker import *
from .call_properties import *
from .get_properties import *
from .if_draw import *
from .icon_draw import *
from .get_image import *
from .label import *
classes = (
    RGC_Operator_AddPickerNode,
    RGC_Operator_GetPropertie,
    
    RGC_Menu_Inputs,
    RGC_Menu_Outputs,
    RGC_Menu_DrawNode,
    RGC_Menu_Value,
    RGC_Menu_Picker,
    RGC_Menu_CallProperties,
    
    #Nodes
    RGC_PNode_SelectBone,
    RGC_Operator_PickerSelectBone,
    
    RGC_PNode_Bone,
    RGC_PNode_Image,
    RGC_PNode_OutPicker,
    RGC_PNode_JoinPicker,
    RGC_PNode_CallProperties,
    RGC_PNode_GetPropertie,
    RGC_PNode_IfDraw,
    #RGC_PNode_Icon,
    RGC_PNode_GetImage,
    RGC_PNode_Label,
)

def PickerNodeRegister():
    for c in classes:
        bpy.utils.register_class(c)
    for cls in Nodes_Value.values():
        bpy.utils.register_class(cls)
    bpy.types.NODE_MT_add.append(AddNodes)
def PickerNodeUnregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    for cls in Nodes_Value.values():
        bpy.utils.unregister_class(cls)
    bpy.types.NODE_MT_add.remove(AddNodes)