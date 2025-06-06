
import bpy
from bpy.types import NodeTree, Node, PropertyGroup, NodeSocket
from .general import *

class RGC_Socket_Vector2d(RGC_GeneralSocket, NodeSocket) :
    bl_idname = "RGC_Socket_Vector2d"
    bl_label = "Vector2d"
    
    base_color = (0, 1, 0.5, 1)
    # Definir la propiedad correctamente
    default_value: bpy.props.IntVectorProperty(
        name="Vector2D", 
        size=2,  # El tamaño debe ser 2 para representar un vector 2D
        default=(0, 0),  # Proporcionar un valor por defecto compatible con el tipo
    )
    def draw(self, context, layout, node, text):
        if self.GetArmature() is not None:
            if self.id_data.type_mode == "EDIT":
                if not self.is_output:
                    layout.prop(self, "default_value", text="")
            layout.label(text=text)
    