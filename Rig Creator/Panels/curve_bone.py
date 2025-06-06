from .general import *
from ..generaldata import GeneralArmatureData
import bmesh


class RGC_Panel_CurveToBone(GeneralArmatureData, bpy.types.Panel):
    bl_idname = "RGC_Panel_CurveToBone"
    bl_label = "Curve To Bone"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Item"
    
    @classmethod
    def poll(cls, context):        
        Self = GeneralArmatureData()
        return Self.GetActiveObject() and Self.GetActiveObject().type == "CURVE" and Self.GetObjMode() == "EDIT"

    def draw(self, context):
        layout = self.layout
        props = self.Props()
        
        layout.prop(props, "curve_bone_name", text="Bone Name")
        layout.prop(props, "curve_use_reference_bone", text="Use Reference Bones")
        if props.curve_use_reference_bone :
            layout.prop(props, "curve_reference_bone_name", text="Reference Bone Name")
            box = layout.box()
            if self.Panel(box, "info", "Info", "INFO") : 
                self.LabelParagraph(box, [
                    "This will use a reference bone",
                    "for the length and display size."
                ])
                
        layout.prop(props, "curve_use_control", text="Use Control Bones")
        
        if props.curve_use_control:
            box = layout.box()
            col = box.column(align=True)
            row = col.row(align=True)
            row.prop(props, "use_parent", text="", icon="FILE_PARENT" ,expand=False, slider=False, toggle=1)
            row.prop(props, "use_fk", text="FK", expand=False, slider=False, toggle=1)
            row.prop(props, "use_fingers", text="Fingers", expand=False, slider=False, toggle=1)
            row = col.row(align=True)
            row.prop(props, "use_segments", text="Segments", icon="MOD_ARRAY", expand=False, slider=False, toggle=1)
            row.scale_x = 0.4
            if props.use_segments : 
                row.prop(props, "int_segments", text="")
            
            col.prop(props, "use_limit_rot_fingers", icon="CON_ROTLIMIT", text="Limit Rotation Fingers", expand=False, slider=False, toggle=1)
            if props.use_limit_rot_fingers :
                row = col.row(align=True)
                row.prop(props, "limit_rot_fingers" , text="Range Bones")
                row.prop(props, "limit_rot_fingers_invert", text="", icon = "ARROW_LEFTRIGHT", expand=False, slider=False, toggle=1)
                value = len(self.GetSelectBones(self.GetObjMode()))
                if props.limit_rot_fingers > value:
                    box = col.box()
                    box.label(text="Out of the limit of selected bones", icon="ERROR")
            
            row = col.row(align=True)
            if props.use_fk : 
                row.prop(props, "name_fk", text="")
            row.prop(props, "name_def", text="")
            
            if props.use_fingers :
                col.prop(props, "name_fingers", text="")
            self.ShadowBox(col, size_y=1.5)
            
        layout.operator("rgc.curve_to_bone", text="Set Bone To Curve")