
import bpy
from bpy.types import NodeTree, Node, PropertyGroup, NodeSocket
from .general import *

class RGC_Socket_Properties(RGC_GeneralSocket, NodeSocket) :
    bl_idname = "RGC_Socket_Properties"
    bl_label = "Properties"
    
    base_color = (0, 0.8, 1, 1)
    
    def draw(self, context, layout, node, text):
        super().draw(context, layout, node, text)
        layout.label(text= text)
    