from .general import *
from .grups import *
from .windowdraw import *
from ..generaldata import *
classes = (
    RGC_Save_Bones_Have_Select_View,
    RGC_Armature_GrupsProps,
    RGC_GrupsProps,
    RGC_ViewSelect_Grups,
    RGC_PoseBone_GrupsProps,
    
)

@bpy.app.handlers.persistent   
def _init_blender(dummy):
    ...

@bpy.app.handlers.persistent   
def _update_blender(dummy):
    
    data : GeneralArmatureData = GeneralArmatureData()
    Props = data.Props()

    if Props.rot_to_cursor == True and data.GetObjMode() == "POSE": 
        scene = bpy.context.scene
        obj = data.GetActiveObject()
        bone = data.GetActiveBone(mode="POSE")
        if bone : 
            bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'
            matrix = bone.matrix 
            loc, rot, scale = matrix.decompose()
            scene.cursor.location = loc + obj.location


def GeneralRegister():
    for c in classes :
        bpy.utils.register_class(c)
    
    bpy.types.Scene.RGC_GrupsProps = bpy.props.PointerProperty(
        type=RGC_GrupsProps
    )
    bpy.types.Object.RGC_Armature_GrupsProps = bpy.props.CollectionProperty(
        type=RGC_Armature_GrupsProps
    )

    
    bpy.types.PoseBone.active_constraint = bpy.props.IntProperty(min=0,options={'HIDDEN'},)
    bpy.types.Object.active_constraint = bpy.props.IntProperty(min=0, options={'HIDDEN'},)
    
    bpy.app.handlers.load_post.append(_init_blender)
    bpy.app.handlers.depsgraph_update_pre.append(_update_blender)

def GeneralUnregister():
    for c in classes :
        bpy.utils.unregister_class(c)
        
    del bpy.types.Scene.RGC_GrupsProps
    del bpy.types.Object.RGC_Armature_GrupsProps
    del bpy.types.PoseBone.active_constraint
    del bpy.types.Object.active_constraint
    
    bpy.app.handlers.load_post.remove(_init_blender)
    bpy.app.handlers.depsgraph_update_pre.remove(_update_blender)

