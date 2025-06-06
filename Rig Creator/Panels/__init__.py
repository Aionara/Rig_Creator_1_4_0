from .general import *
from .generators import *
from .collections import *
from .properties import *
from .rst_armature import *
from .app_armature import * 
from .constraint_bone import *
from .constraint_object import *
from .draw_constraints import * 
from .animation import *
from .picker import *
from .mesh_bone import *
from .curve_bone import *
from .set_animation import *
from .edit_bone import *



classes = (
    
    RGC_Panel_Viewport,
    
    RGC_Panel_Collections,
    RGC_Menu_Collections,
    
    RGC_Panel_Properties,
    RGC_Panel_Proterties_RigCreator,
    RGC_Panel_Properties_Armature,
    RGC_Panel_Properties_Bones,
    RGC_Panel_Call_Proterties_RigCreator,
    RGC_Panel_OldProperties,
    RGC_Panel_Picker,
    RGC_Panel_SetAnimation,
    
    RGC_Panel_RelationShip,
    #RGC_Menu_CopyXformRelationShip,
    
    RGC_Panel_MeshToBone,
    RGC_Panel_CurveToBone,
    
    ## Generators
    RGC_Generators_List,
    RGC_Panel_Generators,
    RGC_Panel_Physics,
    RGC_Panel_ResetArmature,
    
    RGC_Menu_AddArmature,
    RGC_Menu_ForGames,
    RGC_Menu_AddExtras,
    RGC_Menu_AddBodyParts,
    RGC_Menu_AddGenerators,
    RGC_Menu_AddBone,
    RGC_Menu_UnionBone,
    RGC_Menu_Parent,
    RGC_Menu_EditBone,
    RGC_Operator_Call_AddGenerators,
    RGC_Panel_Call_AddGenerators,
    #RGC_Menu_AddBodyParts,
    
    # Constraints
    RGC_List_ConstraintsBone,
    BONE_PT_constraints,
    RGC_Panel_Bone_Constraint,
    RGC_Panel_Object_Constraint,
    RGC_Menu_Constraints,
    
    #view select
    #RGC_List_ViewSelect, 
    #RGC_Panel_ViewSelect,
)

def ApplyArmatureScale(self, context):
    
    layout = self.layout
    layout.separator()
    layout.operator("rgc.aplicarscale", text="Transform To Armature")


def PanelRegister():
    
    for c in classes :
        bpy.utils.register_class(c)
    bpy.types.VIEW3D_MT_armature_add.append(AddArmature)
    bpy.types.VIEW3D_MT_editor_menus.append(RGC_DrawButtonAnimation)
    bpy.types.BONE_PT_curved.append(RGC_DrawSetControlBendyBone)
    bpy.types.VIEW3D_MT_editor_menus.append(Pose_AddGenerators)
    bpy.types.VIEW3D_MT_editor_menus.append(Pose_EditBone)
    bpy.types.TOPBAR_MT_edit_armature_add.append(Edit_AddGenerators)
    #bpy.types.VIEW3D_HT_tool_header.append(RGC_Annotate_PoseBone)
    RegDrawConstraint()
    
def PanelUnregister():
    for c in classes :
        bpy.utils.unregister_class(c)
    
    bpy.types.VIEW3D_MT_armature_add.remove(AddArmature)
    bpy.types.VIEW3D_MT_editor_menus.remove(RGC_DrawButtonAnimation)
    bpy.types.VIEW3D_MT_object_apply.remove(ApplyArmatureScale)
    bpy.types.BONE_PT_curved.remove(RGC_DrawSetControlBendyBone)
    bpy.types.VIEW3D_MT_editor_menus.remove(Pose_AddGenerators)
    bpy.types.VIEW3D_MT_editor_menus.remove(Pose_EditBone)
    bpy.types.TOPBAR_MT_edit_armature_add.remove(Edit_AddGenerators)
    #bpy.types.VIEW3D_HT_tool_header.remove(RGC_Annotate_PoseBone)
    UnreDrawConstraint()