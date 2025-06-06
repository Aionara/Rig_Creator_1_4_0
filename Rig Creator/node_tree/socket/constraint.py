
import bpy
from bpy.types import NodeTree, Node, PropertyGroup, NodeSocket
from .general import *

class RGC_Socket_Constraint(GeneralSocketData, NodeSocket) :
    bl_idname = "RGC_Socket_Constraint"
    bl_label = "Constraint"
    
    def __init__(self):
        super().__init__()
        self.base_color = (0, 1, 1, 1)
    