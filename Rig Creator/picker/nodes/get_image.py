import bpy 
from .general_nodes import *
import os

class RGC_PNode_GetImage(RGC_PickerNodes, bpy.types.Node):
    """Node for displaying an image in the Node Editor"""
    bl_idname = 'P-GetImage'
    bl_label = 'Get Image'
    bl_icon = 'OUTLINER_OB_IMAGE'
    
    def ImagePath(self, context):
        if self.image_path:
            image = bpy.data.images.get(self.image_path)
            if not image:
                try:
                    image = bpy.data.images.load(self.image_path)
                except Exception as e:
                    print(f"Error al cargar la imagen: {e}")
                    return
            self.outputs["Image"].default_value = image

    image_path: bpy.props.StringProperty(
        name="Image Path",
        subtype='FILE_PATH',
        update=ImagePath,
    )


    def init(self, context):
        self.outputs.new(type="NodeSocketImage", name="Image")

    def draw_buttons(self, context, layout):
       if self.GetTypeMode() == "EDIT":
           layout.prop(self, "image_path", text="Image")
            
        
        
