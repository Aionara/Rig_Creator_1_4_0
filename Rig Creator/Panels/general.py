
import bpy
from ..generaldata import *

class GN_RigCreatorViewPort(GeneralArmatureData):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Rig Creator"
    
    
    def PollArmature(self, context) -> bool:
        return context.active_object and context.active_object.type == "ARMATURE"

    def PollArmatures(self, context):
        Armatures = self.GetSelectableObjects()
        for a in Armatures :
            if a and a.type == "ARMATURE":
                return True
        return False

class RGC_Panel_Viewport(GN_RigCreatorViewPort, bpy.types.Panel):
    bl_idname = "RGC_Panel_Viewport"
    bl_label = "Rig Creator"
    
    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == "ARMATURE"
    
    def draw(self, context):
        layout = self.layout
        props = self.Props()
        
        layout.prop(props, "panel_type", text="all")
        
        

class SNA_PT_SSSSSSS_8CBB3(bpy.types.Panel):
    bl_label = 'sssssss'
    bl_idname = 'SNA_PT_SSSSSSS_8CBB3'
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = 'data'
    bl_category = 'New Category'
    bl_order = 0
    
    
    bl_ui_units_x=0
    @classmethod
    def poll(cls, context):
        return not (False)
    
    def draw_header(self, context):
        layout = self.layout
        
        
    def draw(self, context):
        layout = self.layout
        
UseBone : bool = False
class GH_RGC_DrawListConstraint(GeneralArmatureData) : 
    
    def Draw(self, context, use_bone : bool = False) : 
        layout = self.layout
        X = self.GetActiveObject() if use_bone == False else self.GetActiveBone()
        global UseBone
        UseBone = use_bone
        if not X : return
        row = layout.row(align=False)
        row.template_list(
            "RGC_List_ConstraintsBone", "",  
            X, "constraints",  
            X, "active_constraint",  
            rows=8 if X.constraints else 1,  
        )
        col = row.column(align=True)
        col.enabled = len(X.constraints) > 0 
        operator_name = "rgc.objconstraint" if use_bone == False else "rgc.boneconstraint"
        col.operator(operator_name, text="", icon="REMOVE").type = "REMOVE"
        if X.constraints :  
            col.operator(operator_name, text="" ,icon="DUPLICATE").type = "DUPLICATE_CONST"
            col.operator(operator_name, text="" ,icon="CHECKMARK").type = "APPLY_CONST"
            col.menu("rgc.editconstraint", text="", icon="DOWNARROW_HLT")
            
            col_ = col.column(align=True)
            col_.enabled = len(X.constraints) > 1
            
            col_.operator(operator_name, text= "", icon="TRIA_UP").type = "UP"
            col_.operator(operator_name, text= "", icon="TRIA_DOWN").type = "DOWN"

class RGC_Menu_Constraints(GeneralArmatureData, bpy.types.Menu):
    bl_idname = "rgc.editconstraint"
    bl_label = "Rig Creator"

    def draw(self, context):
        layout = self.layout
        operator_name = "rgc.objconstraint" if UseBone == False else "rgc.boneconstraint"
        selected_bones =  self.GetSelectableObjects() if UseBone == False else self.GetSelectBones(mode="POSE") 
        
        layout.operator(operator_name, text="Delete All", icon="PANEL_CLOSE").type = "DELETE_ALL"
        
        layout.separator(factor=1.0)
        layout_ = layout.column()
        
        Bone = self.GetActiveObject() if UseBone == False else self.GetActiveBone() 
        layout_.enabled = True if len(selected_bones) > 1 and Bone else False
        
        layout_.label(text="Copy Constraint")
        layout_.operator(operator_name, text="    To Active").type = "COPY_SEL_CONST"
        layout_.operator(operator_name, text="    To Active (Index)").type = "COPY_SEL_CONST_INDEX"
        

"""
class RGC_Panel_Properties(GN_RigCreatorViewPort, bpy.types.Panel):
    bl_idname = "RGC_Panel_Properties"
    bl_label = "Properties"
    
    def __init__(self) -> None:
        super().__init__()
        self.Armature = bpy.context.active_object
    
    @classmethod
    def poll(cls, context):        
        return context.active_object and context.active_object.type == "ARMATURE"
    
    def draw(self, context):
        layout = self.layout
        props = self.Props()"""