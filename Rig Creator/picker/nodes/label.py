import bpy 
from .general_nodes import *
import os

class RGC_PNode_Label(RGC_PickerNodes, bpy.types.Node):
    """Node for displaying an image in the Node Editor"""
    bl_idname = 'P-Label'
    bl_label = 'Draw Label'
    bl_icon = 'SORTALPHA'

    def init(self, context):
        self.width = 250
        self.inputs.new(type="RGC_Socket_Picker", name="Draw")
        self.outputs.new(type="RGC_Socket_Picker", name="Draw")
        self.inputs.new(type="NodeSocketBool", name="Use Text").default_value = True
        self.inputs.new(type="NodeSocketString", name="Text").default_value = "Label"
        self.inputs.new(type="NodeSocketFloat", name="Text Size").default_value = 1
        self.inputs.new(type="NodeSocketColor", name="Text Color").default_value = (1, 1, 1, 1)
        self.inputs.new(type="NodeSocketColor", name="Normal Color").default_value = (0.2, 0.2, 0.2, 1)
        self.size_x = 100
        
    def draw_piker(self, x, y, size_x, size_y):
        super().draw_piker(x, y, size_x, size_y)
        text = ""
        if self.InputLink(socket="Use Text") : 
            text = self.InputLink("Text")

        self.DrawButton(
            self.save_x,self.save_y,
            self.save_size_x,self.save_size_y,
            normal_color=self.InputLink("Normal Color"),
            text=text, 
            text_color=self.InputLink("Text Color"),
            text_size= self.InputLink("Text Size"),
        )
        
        
    def draw_buttons(self, context, layout):
       #if self.GetTypeMode() == "EDIT":
       #    layout.prop(self, "image_path", text="Image")
        super().draw_buttons( context, layout)
            
        
        
