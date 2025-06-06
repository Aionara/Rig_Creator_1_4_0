import bpy
from .general import *
from ..generaldata import GeneralArmatureData



class RGC_Panel_SetAnimation(GN_RigCreatorViewPort, bpy.types.Panel):
    bl_idname = "RGC_Panel_SetAnimation"
    bl_label = "Set Animation"
    

    
    @classmethod
    def poll(cls, context):  
        return False
        Self = GeneralArmatureData()
        return Self.GetArmature() and Self.PanelType([{"ALL"}, {"RIG"}])
    
    def draw(self, context):
        layout = self.layout
        props = self.Props()
        
