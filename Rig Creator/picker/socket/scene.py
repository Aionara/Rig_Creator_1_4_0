
import bpy
from bpy.types import NodeTree, Node, PropertyGroup, NodeSocket
from .general import *

class RGC_Socket_Scene(RGC_GeneralSocket, NodeSocket) :
    bl_idname = "RGC_Socket_Scene"
    bl_label = "Scene"
    
    base_color = (0, 1, 0.5, 1)
    default_value : bpy.props.PointerProperty(type=bpy.types.Scene)
    
    def draw(self, context, layout, node, text):
        super().draw(context, layout, node, text)
        layout.prop(self, "default_value", text=text)