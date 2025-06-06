
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


class RGC_GeneralSocket(GeneralArmatureData):

    bl_idname = 'RGC_Socket'
    bl_label = 'Socket'
    
    default_value : StringProperty()
    base_color = (0.0, 0.0, 0.0, 1.0)
    primitive_color = (0.8, 0.8, 0.8, 1)
    use_addinputs : BoolProperty(
        name="Use Add Inputs",
        description="Add inputs to the node",
        default=False,
    )

    def InputLink(self):

        if self.links:
            return self.links[0].from_socket.default_value
        else:
            return self.default_value
            
    def draw(self, context, layout, node, text):
        if node.inputs:
            if self.use_addinputs:
               
                # Botón para añadir socket
                add_op = layout.operator("node.add_input", text="", icon='ADD')
                add_op.type = "ADD"
                add_op.socker = self.bl_idname
                add_op.node_name = node.name
                add_op.text = text
                # Contar cuántos sockets hay del mismo tipo
                same_type_sockets = [i for i in node.inputs if i.bl_idname == self.bl_idname]
                col = layout.column(align=True)
                col.enabled = len(same_type_sockets) > 1
                
                # Encontrar el índice del socket actual dentro de la lista de mismos tipos
                current_index = same_type_sockets.index(self)

                remove_op = col.operator("node.add_input", text="", icon='REMOVE')
                remove_op.type = "REMOVE"
                remove_op.socker = self.bl_idname
                remove_op.index = current_index
                remove_op.node_name = node.name
                remove_op.text = text
                
                
                
    def draw_color(self, context, node):
        for i in range(len(self.links)):
            if self.is_linked and self.links[i].from_socket.bl_idname == self.bl_idname:
                
                return (self.base_color)
            else:
                return (1.0, 0, 0, 1.1)
        if not self.is_linked:
            
            return (self.base_color)


class RGC_Operator_AddInput(GeneralArmatureData, bpy.types.Operator):
    bl_idname = "node.add_input"
    bl_label = "Add Input"
    bl_description = "Add Input"
    bl_options = {'REGISTER', 'UNDO'}

    node_name : StringProperty()

    type : StringProperty(
        name="Type",
        description="Type of the input",
        default="RGC_Socket",
    )
    socker : StringProperty(
        name="Socket",
        description="Socket type",
        default="RGC_Socket",
    )
    index : IntProperty(
        name="Index",
        description="Index of the input",
        default=0,
    )
    text : StringProperty()
    def execute(self, context):
        node = self.GetNode(context, self.node_name)
        if node:
            if self.type == "ADD":
                new = node.inputs.new(self.socker, self.text)
                new.use_addinputs = True
            elif self.type == "REMOVE":
                if node.inputs:
                    node.inputs.remove(node.inputs[-1])
        return {'CANCELLED'}