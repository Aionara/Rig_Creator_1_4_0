import bpy
from ..generaldata import *
from .general import *

class ObjectConstraintPanel:
    bl_context = "constraint"

    @classmethod
    def poll(cls, context):
        return (context.object)

    

class RGC_List_ConstraintsObject(GeneralArmatureData, bpy.types.UIList):
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            
            
            layout.label(text="", icon=self.ListIconConstraint()[item.type])
            layout.prop(item, "name", text="",  emboss=False)
            layout.prop(item, "influence", text="", emboss=False)
            layout.prop(item, "enabled", text="",icon='HIDE_ON',  emboss=False)
            
            return
          
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon=item.icon)

class OBJECT_PT_constraints(ObjectConstraintPanel,bpy.types.Panel):
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_label = "Bone Constraints"
    bl_options = {'HIDE_HEADER'}
        
    def draw(self, context):
        layout = self.layout
        
        layout.operator_menu_enum("pose.constraint_add", "type", text="Add Bone Constraint")
        return
        #layout.template_constraints(use_bone_constraints=True)

class RGC_Panel_Object_Constraint(ObjectConstraintPanel,GH_RGC_DrawListConstraint, bpy.types.Panel):
    bl_idname = "RGC_Panel_Object_Constraint"
    bl_label = "Constraints"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_order = 0
    
    @classmethod
    def poll(cls, context):
        ob = context.object
        return (ob and context.space_data.context == 'CONSTRAINT')
    
    def draw(self, context):
        layout = self.layout
        self.Draw(context)
             
   