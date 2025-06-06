import bpy 
from .general_nodes import *


class RGC_PNode_JoinPicker(RGC_PickerNodes, bpy.types.Node):
    """Select a Bone"""
    bl_idname = 'P-JoinPicker'
    bl_label = 'Join Draw'
    bl_icon = 'NODE_INSERT_OFF'
   


    def init(self, context):
        self.index = 1
        
        
        # Configura el valor por defecto de "Bone" si es necesario
        new = self.inputs.new(type="RGC_Socket_Picker", name="Draw")
        new.use_addinputs = True
        new = self.inputs.new(type="RGC_Socket_Picker", name="Draw")
        new.use_addinputs = True
        new = self.outputs.new(type="RGC_Socket_Picker", name="Draw")

    def draw_buttons(self, context, layout):
        pass
        #return super().draw_buttons(context, layout)
    
    def SetOperator(self, x, y, size_x, size_y):
        for input in self.inputs:
            node = self.GetInputNode(obj_socket=input)
            if node :
                node.SetOperator(x, y, size_x, size_y)
    