
from .general import *
from ..generaldata import GeneralArmatureData
import bmesh
from .generators import *

class RGC_Panel_MeshToBone(GeneralArmatureData, bpy.types.Panel):
    bl_idname = "RGC_Panel_MeshToBone"
    bl_label = "Mesh To Bone"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Item"
    
    @classmethod
    def poll(cls, context):        
        Self = GeneralArmatureData()
        return Self.GetActiveObject() and Self.GetActiveObject().type == "MESH" and Self.GetObjMode() == "EDIT"

    def draw(self, context):
        layout = self.layout
        props = self.Props()
        
        
        #bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='VERT')

        
        obj = self.GetActiveObject()
        bm = bmesh.from_edit_mesh(obj.data)
        view : bool = False
        select_objects = self.GetSelectableObjects()
        have_armature = False
        for o in select_objects:
            if o != obj : 
                if o.type == "ARMATURE" : 
                    have_armature = True
                    break
        layout.label(text="Set To Armature" if have_armature else "Add Armature",)
        for v in bm.verts:
            if v.select : view = True
        if view == False :
            layout.label(text="Select Vertex", icon="ERROR")
            return
        
        layout = layout.column(align=True)
        layout.scale_y = 1.2
        layout.prop(props, "mesh_bone_name", text="Bone Name")
        
        # bone Reference
        row = layout.row(align=True)
        row.prop(props, "mesh_use_bone_reference", text="Bone Reference", expand=False, slider=False, toggle=1)
        rrow = row.row(align=True)
        rrow.enabled = props.mesh_use_bone_reference
        rrow.prop(props, "mesh_bone_reference_name", text="")
        
        layout.separator()
        layout.prop(props, "mesh_use_aling_roll_normal", text="Aling Roll Normal", expand=False, slider=False, toggle=1)
        layout.prop(props, "mesh_keep_object", text="Keep Object", expand=False, slider=False, toggle=1)
        layout.separator()
        
        # weights
        row = layout.row(align=True)
        row.prop(props, "mesh_with_automatic_weights", text="With Automatic Weights", expand=False, slider=False, toggle=1)
        rrow = row.row(align=True)
        rrow.enabled = props.mesh_with_automatic_weights
        rrow.prop(props, "mesh_with_by_distance_of_vertex", text="With By Distance Of Vertex", expand=False, slider=False, toggle=1)
        
        layout.separator()
        
        
        if self.GetMeshSelectMode("EDGE") or self.GetMeshSelectMode("VERT"):
            
            clayout = layout.column(align = True)
            clayout.enabled = self.GetMeshSelectMode("VERT")
            clayout.prop(props, "mesh_use_vertcurve", text="Vert Curve", expand=False, slider=False, toggle=1)
            clayout = layout.column(align = True)
            clayout.enabled = props.mesh_use_vertcurve
            clayout.prop(props, "mesh_vertcurve_power", text="Curve Power", expand=False, slider=False, toggle=1)

            clayout = layout.column(align = True)
            if self.GetMeshSelectMode("VERT"):
                clayout.enabled = not props.mesh_use_vertcurve
                
            clayout.prop(props, "mesh_use_tail", text="Use Tail", expand=False, slider=False, toggle=1)
            col = clayout.column(align=True)
            col.enabled = props.mesh_use_tail
            
            col = clayout.column(align=True)
            col.enabled = not props.mesh_use_tail
            col.prop(props, "mesh_normal_global", text="")
            if props.mesh_normal_global  == "GLOBAL":
                row = col.row(align=True)
                row.prop(props, "mesh_direction", text="X")
        else :
            layout.prop(props, "mesh_normal_global", text="")
            if props.mesh_normal_global  == "GLOBAL":
                row = layout.row(align=True)
                row.prop(props, "mesh_direction", text="X")
            
        text = ""
        if self.GetMeshSelectMode("VERT"):
            text = "Set Bone To Selected Vert"
        elif self.GetMeshSelectMode("EDGE"):
            text = "Set Bone To Selected Edge"
        elif self.GetMeshSelectMode("FACE"):
            text = "Set Bone To Selected Face"
            
        layout.separator()
        layout.prop(props, "mesh_use_curve", text="Use Curve Grip",expand=False, slider=False, toggle=1)
        
        if props.mesh_use_curve :
            DrawGenerators().CurveGrip(layout, props, use_run=False)
            
        layout.separator()   
        #def t_diferente() -> bool : 
        #    for i in range(3) : 
        #        if obj.location[i] != 0 or obj.scale[i] != 1 or obj.rotation_euler[i] != 0 : 
        #            return True
        #    return False
        #
        #if t_diferente(): 
        #    box = layout.box()
        #    box.label(text="Object Transform is not default", icon="ERROR")
        
        layout.operator("rgc.mesh_to_bone", 
            text=text, 
            icon="BONE_DATA"
        )
        
        