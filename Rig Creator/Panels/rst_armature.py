import bpy
from .general import *
from ..generaldata import GeneralArmatureData



class RGC_Panel_ResetArmature(GN_RigCreatorViewPort, bpy.types.Panel):
    bl_idname = "RGC_Panel_ResetArmature"
    bl_label = "Reset Armature"
    
    
    @classmethod
    def poll(cls, context):  
        Self = GeneralArmatureData()
        return Self.GetArmature() and Self.PanelType([{"ALL"}, {"RIG"}])
    
    def draw(self, context):
        
        layout = self.layout
        props = self.Props()
        
        col = layout.column(align=True)
        col.scale_y = 1.5
        col.operator("rgc.rstarmature", text="Armature").type = "RESET_ALL"
        self.ShadowBox(col, size_y=1.5) 
        col = layout.column(align=True)
        
        if self.Panel(col, "Body parts", "body_parts", "RIGID_BODY_CONSTRAINT", True):
            col.operator("rgc.rstarmature", text="Face").type = "RESET_FACE"
            col.operator("rgc.rstarmature", text="Cartoon Face").type = "RESET_CARTOON_FACE"
            col.operator("rgc.rstarmature", text="Spine").type = "RESET_SPINE"
            grid = col.grid_flow(
                row_major=False, columns=2, 
                even_columns=False, even_rows=False, 
                align=True,
            )
            for type in ["R", "L"]:
                grid.operator("rgc.rstarmature", text=f"Arm {type}").type = f"RESET_ARM_{type}"
                for finger in self.ListFinger():
                    grid.operator("rgc.rstarmature", text=f"{finger} {type}").type = f"RESET_{finger.upper()}_{type}"
                
                grid.operator("rgc.rstarmature", text=f"Leg {type}").type = f"RESET_LEG_{type}"
                #grid.operator("rgc.rstarmature", text=f"Feet {type}").type = f"RESET_FEET_{type}"
                
            col.operator("rgc.rstarmature", text="Root").type = "RESET_ROOT"
            self.ShadowBox(col, size_y=1.5)
        
        col = layout.column(align=True)
        col.operator("rgc.rstarmature", text="All Bone Stretch To").type = "RESET_ALLSTRETCH_TO"
        col.operator("rgc.rstarmature", text="Select Bone Stretch To").type = "RESET_STRETCH_TO"
        self.ShadowBox(col, size_y=1.5) 
            