import bpy 
from .general_nodes import *
import time

def set_save_operator(self, context):
        for input in self.inputs:
            node = self.GetInputNode(obj_socket=input)
            if node :
                node.SetSaveOperator(self.x, self.y, self.size_x, self.size_y)
                
class RGC_PNode_OutPicker(RGC_PickerNodes, bpy.types.Node):
    """Select a Bone"""
    bl_idname = 'P-OutPicker'
    bl_label = 'Draw Picker'
    bl_icon = 'SHADING_RENDERED'
   
    draw : bpy.props.BoolProperty(
        name = "",
        default = True,
        description = "",
    )
    
    x: bpy.props.FloatProperty(
            default=0,
            update = set_save_operator,
        )
    y: bpy.props.FloatProperty(
            default=0,
            update = set_save_operator,
        )
    size_x: bpy.props.FloatProperty(
            default=50,
            update = set_save_operator,
        )
    size_y: bpy.props.FloatProperty(
            default=50,
            update = set_save_operator,
        )
    def init(self, context):
        self.index = 1

        # Configura el valor por defecto de "Bone" si es necesario
        new = self.inputs.new(type="RGC_Socket_Picker", name="Draw")
        new.use_addinputs = True
        self.size_x = 1
        self.size_y = 1
        
    def draw_buttons(self, context, layout):
        self.draw_piker()
                
        super().draw_buttons(context, layout)
        
    def draw_piker(self):
        for input in self.inputs:
            node = self.GetInputNode(obj_socket=input)
            if node :
                node.draw_piker(self.x, self.y, self.size_x, self.size_y)
    
    def SetOperator(self,):
        for input in self.inputs:
            node = self.GetInputNode(obj_socket=input)
            if node :
                node.SetOperator(self.x, self.y, self.size_x, self.size_y)
    
    def update(self):
        
        pass
    
    def execute(self):
        pass