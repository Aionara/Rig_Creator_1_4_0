import bpy

from .general import *
from .operator import *

classes = (
    RGC_SetMode,
    RGC_OperatorCollections,
    RGC_OperatorProperties,
    RGC_OperatorResetArmature,
    RGC_OperatorAddArmature,
    RGC_OperatorAnimation,
    RGc_OperatorAplicarScale,
    
    RGC_OperatorObjectConstraint,
    RGC_OperatorBoneConstraint,
    RGC_OperatorGeneral,
    RGC_Operator_GeneratorsBones,
    
    #Constraints
    CONSTRAINT_OT_add_target,
    CONSTRAINT_OT_remove_target,
    CONSTRAINT_OT_normalize_target_weights,
    CONSTRAINT_OT_disable_keep_transform,
    
    RGC_Operador_childof_clear_inverse,
    RGC_Operador_childof_set_inverse,
    
    # Node
    RGC_OperatorAddNode,
    
    #Picker
    RGC_OperatorPiker,
    
    #Mesh
    RGC_OperatorMeshToBone,
    RGC_OperatorCurveToBone,
    
    #View Select
    RGC_Operator_Only_ViewChildBone,
)


def OperetorRegisnter():
    
    for cls in classes:
        bpy.utils.register_class(cls)
    
    for cls in GE_OP_list.values():
        bpy.utils.register_class(cls)
    
    RegisterCallMenu()
    
    bpy.app.handlers.annotation_post.append(GN_Update_AnnotateBone)

def OperetorUnregisnter():
    
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    for cls in GE_OP_list.values():
        bpy.utils.unregister_class(cls)
    
    UnregisterCallMenu()
    bpy.app.handlers.annotation_post.remove(GN_Update_AnnotateBone)