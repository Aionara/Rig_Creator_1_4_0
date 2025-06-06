
from ...generaldata import *
from bpy.props import (
    BoolProperty,
    BoolVectorProperty,
    IntProperty,
    FloatProperty,
    StringProperty,
    EnumProperty,
    PointerProperty,
    CollectionProperty,
    FloatVectorProperty,
    IntVectorProperty,
)


class GeneralSocketData(GeneralArmatureData):

    bl_idname = 'RGC_Socket'
    bl_label = 'Socket'

    def __init__(self):
        super().__init__()
        self.default_value : StringProperty()
        self.base_color = (0.0, 0.0, 0.0, 1.0)
    
    
    def draw(self, context, layout, node, text):
        layout.label(text=text)
    
    def draw_color(self, context, node):
        for i in range(len(self.links)):
            if self.is_linked and self.links[i].from_socket.bl_idname == self.bl_idname:
                return (self.base_color)
            else:
                return (1.0, 0, 0, 1.1)
        if not self.is_linked:
            return (self.base_color)
