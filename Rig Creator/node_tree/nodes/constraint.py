import bpy
from .general import *
from bpy.types import Node


class RGC_Node_OutConstraint(GeneralNodeData, Node):
    bl_idname = 'RGC_Node_OutConstraint'
    bl_label = 'Outputs Constraint'

    def init(self, context,):
        self.CreateSocket(self.ListNodeSocket()["constraint"], "Constraint", use_outputs=True)
        
    def draw_buttons(self, context, layout):
        pass
    
    def update(self):
        pass
    
    def execute(self):
        
        pass 

class RGC_Node_InpConstraint(GeneralNodeData, Node):
    bl_idname = 'RGC_Node_InpConstraint'
    bl_label = 'Inputs Constraint'

    def init(self, context,):
        self.CreateSocket(self.ListNodeSocket()["constraint"], "Constraint")
        
    def draw_buttons(self, context, layout):
        pass
        
    def update(self):
        pass
    
    def execute(self):
        pass 
