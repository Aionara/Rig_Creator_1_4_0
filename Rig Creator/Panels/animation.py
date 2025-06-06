
import bpy

from ..generaldata import *

data = GeneralArmatureData()

def RGC_DrawButtonAnimation(self, context) : 
    layout = self.layout
    
    #row = layout.row(align=True)
    #if data.GetObjMode() != "POSE" : return
    #layout.menu("rgc.copyxformrelationship", text="RelationShip", icon="LIBRARY_DATA_DIRECT")


class RGC_Panel_RelationShip(GeneralArmatureData, bpy.types.Panel):
    bl_idname = "RGC_Panel_RelationShip"
    bl_label = "RelationShip"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Animation"
    
    @classmethod
    def poll(cls, context):        
        Self = GeneralArmatureData()
        return Self.GetArmature() and Self.GetObjMode() == "POSE"

    def draw(self, context):
        layout = self.layout
        props = self.Props()
        
        col = layout.column(align=True)
        col.operator("rgc.animation", text="Copy To Relation", icon="COPYDOWN").type = "COPY"
        col_1 = col.column()
        col_1.enabled = props.is_save_matrix
        col_1.operator("rgc.animation", text="Paste To Relation", icon="PASTEDOWN").type = "PASTE"
        
        col = layout.column(align=True)
        col.operator("rgc.animation", text="Baking RelationShip by Frame", icon="NEXT_KEYFRAME").type = "BAKE_FOR_FRAME"
        
        col_2 = layout.column(align=True)
        col_2.prop(props, "use_local_space", text="Take Local Space", toggle=1)
        row = col_2.row(align=True)
        row.prop(props, "use_rotation", text="Rotation", toggle=1)
        row.prop(props, "use_scale", text="Scale", toggle=1)
        
        col = layout.column(align=True)
        col.prop(props, "rot_to_cursor", text="Select Bone: Rot to Activate", icon="BONE_DATA", toggle=1)
        

class RGC_Menu_CopyXformRelationShip(GeneralArmatureData, bpy.types.Menu):
    bl_idname = "rgc.copyxformrelationship"
    bl_label = "Edit Copy Xform Relation Ship"

    def draw(self, context):
        layout = self.layout
        props = self.Props()
        
        layout.operator("rgc.animation", text="Copy To Relation", icon="COPYDOWN").type = "COPY"
        
        col_1 = layout.column()
        col_1.enabled = props.is_save_matrix
        col_1.operator("rgc.animation", text="Paste To Relation", icon="PASTEDOWN").type = "PASTE"
        
        col_2 = layout.column(align=True)
        col_2.prop(props, "use_local_space", text="Take Local Space", toggle=1)
        col_2.prop(props, "use_rotation", text="Rotation", toggle=1)
        col_2.prop(props, "use_scale", text="Scale", toggle=1)

GN = GeneralArmatureData()
def RGC_Annotate_PoseBone(self, context):
    if GN.IsArmatureExists() : 
        layout = self.layout
        props = GN.Props()
        layout.prop(props, "annotate_posebone", text="Draw Pose", icon="GREASEPENCIL", toggle=1)