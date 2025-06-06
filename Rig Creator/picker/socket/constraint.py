
import bpy
from bpy.types import NodeTree, Node, PropertyGroup, NodeSocket
from .general import *

class RGC_Socket_Constraint(RGC_GeneralSocket, NodeSocket) :
    bl_idname = "RGC_Socket_Constraint"
    bl_label = "Constraint"
    
    base_color = (0.5, 1, 0.5, 1)
    def draw(self, context, layout, node, text):
        super().draw(context, layout, node, text)
        if not self.is_output:
            layout.prop(self, "default_value", text="")
        else:
            layout.label(text=text)
    