import bpy 
from .general_nodes import *
import os

class RGC_PNode_Image(RGC_PickerNodes, bpy.types.Node):
    """Node for displaying an image in the Node Editor"""
    bl_idname = 'P-Image'
    bl_label = 'Draw Image'
    bl_icon = 'OUTLINER_OB_IMAGE'
    
    def ImagePath(self, context):
        if self.image_path:
            image = bpy.data.images.get(self.image_path)
            if not image:
                try:
                    image = bpy.data.images.load(self.image_path)
                except Exception as e:
                    return
            self.image = image
    
    
    image: bpy.props.PointerProperty(
        name="Image",
        type=bpy.types.Image,
        description="Imagen que se mostrará sobre el nodo"
    )
    image_path: bpy.props.StringProperty(
        name="Image Path",
        subtype='FILE_PATH',
        update=ImagePath,
    )


    def init(self, context):
        self.inputs.new(type="RGC_Socket_Picker", name="Draw")
        self.outputs.new(type="RGC_Socket_Picker", name="Draw")
        self.inputs.new(type="NodeSocketImage", name="Image")
        
    def draw_piker(self,x, y, size_x, size_y):
        super().draw_piker(x, y, size_x, size_y)

        if self.InputLink(socket="Image"):
            self.DrawImage(
                image=self.InputLink(socket="Image"),
                x=self.save_x, 
                y=self.save_y,
                width=self.save_size_x,
                height=self.save_size_y, 
                )
        
        
    def draw_buttons(self, context, layout):
       #if self.GetTypeMode() == "EDIT":
       #    layout.prop(self, "image_path", text="Image")
        super().draw_buttons( context, layout)
            
        
        
