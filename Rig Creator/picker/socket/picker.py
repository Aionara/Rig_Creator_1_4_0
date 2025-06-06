import bpy
from bpy.types import NodeTree, Node, PropertyGroup, NodeSocket
from .general import *

class RGC_Socket_Picker(RGC_GeneralSocket, NodeSocket) :
    bl_idname = "RGC_Socket_Picker"
    bl_label = "Draw"
    
    base_color = (1, 1, 0, 1)
    def init(self, context):
        self.display_shape = "DIAMOND"
    
    def draw(self, context, layout, node, text):
        super().draw(context, layout, node, text)
        layout.label(text=text)