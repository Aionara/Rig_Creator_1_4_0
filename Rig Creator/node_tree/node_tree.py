import bpy
from ..generaldata import *

class RGC_Node_Tree(bpy.types.NodeTree):
    bl_idname = 'RGC_Node_Tree'
    bl_label = 'Custom Bone Constraint'
    bl_icon = "CONSTRAINT_BONE"
