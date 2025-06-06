import bpy 
from .general_nodes import *
import os

class RGC_PNode_Icon(RGC_PickerNodes, bpy.types.Node):
    """Node for displaying an image in the Node Editor"""
    bl_idname = 'P-Icon'
    bl_label = 'Icon'
    bl_icon = 'BLENDER_LOGO_LARGE'
    

    items = []
    for index, icon in enumerate(bpy.types.UILayout.bl_rna.functions["prop"].parameters["icon"].enum_items.keys()):
        items.append((icon, icon.replace("_", " ").title(), "", icon, index))
        
    icon_enum : bpy.props.EnumProperty(
        name="Icon Selector",description="Select an icon",items=items
        )

    def init(self, context):
        
        
        self.inputs.new(type="RGC_Socket_Picker", name="Draw")
        self.outputs.new(type="RGC_Socket_Picker", name="Draw")
        
        
    def draw_piker(self):
        super().draw_piker()
        # Dibuja la imagen sobre el nodo
        self.DrawIcon(
            icon_name=self.icon_enum,
            x=self.x, 
            y=self.y,
            width=self.size_x,
            height=self.size_y, 
            )
        
        
    def draw_buttons(self, context, layout):
        if self.GetTypeMode() == "EDIT":
            layout.prop(self, "icon_enum", text="Image")
        super().draw_buttons( context, layout)
            
        
        
