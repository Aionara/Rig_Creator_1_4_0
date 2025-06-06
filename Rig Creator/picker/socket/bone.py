
import bpy
from bpy.types import NodeTree, Node, PropertyGroup, NodeSocket
from .general import *

class RGC_Socket_Bone(RGC_GeneralSocket, NodeSocket) :
    bl_idname = "RGC_Socket_Bone"
    bl_label = "Bone"
    
    base_color = (0, 1, 0.5, 1)
    
    def draw(self, context, layout, node, text):
        super().draw(context, layout, node, text)
        if self.GetArmature() is not None:
            if self.id_data.type_mode == "EDIT":
                if not self.is_output:
                    if not self.is_linked:
                        layout.prop_search(self, "default_value", self.GetArmature(), "bones", text="")
                    else:
                        if self.GetBone(self.InputLink(), "POSE"):
                            layout.label(text=self.GetBone(self.InputLink(), "POSE").name)
                        else:
                            layout.label(text=self.bl_label)
                else :
                    layout.prop_search(self, "default_value", self.GetArmature(), "bones", text="")
            else : 
                if self.GetBone(self.InputLink(), "POSE"):
                    layout.label(text=self.GetBone(self.InputLink(), "POSE").name)
                else:
                    layout.label(text=self.bl_label)
    