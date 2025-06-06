import bpy 
from .general_nodes import *
from bpy.types import Node

data = GeneralArmatureData()

class NodeValue:
    @staticmethod
    def Init(node):
        def init(self, context):
            self.use_custom_color = True
            self.color = (0.153017, 0.191266, 0.202444)
            self.CreateSocket(node[2], node[1], use_outputs=node[3])
        return init

    @staticmethod
    def DrawButtons(node):
        def draw_buttons(self, context, layout):
            if self.GetTypeMode() == "EDIT":
                if node[3] == False:
                    inp = self.outputs[0]
                    if inp is list:
                        layout.label(text=node[1])
                        for i in range(3):
                            layout.prop(inp, "default_value", text="", index=i)
                    layout.prop(inp, "default_value", text=node[1])
        return draw_buttons

    @staticmethod
    def Update(node):
        def update(self):
            ...
        return update

    @staticmethod
    def Execute(node):
        def execute(self):
            ...
        return execute


Nodes = [
    ("Print", "Print", data.ListNodeSocket()["string"], True),
    ("String", "String", data.ListNodeSocket()["string"], False),
    ("Float", "Float", data.ListNodeSocket()["float"], False),
    ("Int", "Intager", data.ListNodeSocket()["int"], False),
    ("Vector", "Vector", data.ListNodeSocket()["vector"], False),
    ("Vector Acceleration", "Vector Acceleration", data.ListNodeSocket()["vector_acceleration"], False),
    ("Vector Direction", "Vector Direction", data.ListNodeSocket()["vector_direction"], False),
    ("Vector Euler", "Vector Euler", data.ListNodeSocket()["vector_euler"], False),
    ("Vector Translation", "Vector Translation", data.ListNodeSocket()["vector_translation"], False),
    ("Vector Velocity", "Vector Velocity", data.ListNodeSocket()["vector_velocity"], False),
    ("Vector xyz", "Vector xyz", data.ListNodeSocket()["vector_xyz"], False),
    ("Color", "Color", data.ListNodeSocket()["color"], False),
]

Nodes_Value = {}

for node in Nodes:
    class_name = f"RGC_PNode_{node[0]}"
    bl_idname = f"P-{node[0]}"
    bl_label = f"{node[1]}"

    class_operator = type(class_name, (RGC_PickerNodes, Node), {
        "bl_idname": bl_idname,
        "bl_label": bl_label,
        "init": NodeValue.Init(node),
        "draw_buttons": NodeValue.DrawButtons(node),
        "update": NodeValue.Update(node),
        "execute": NodeValue.Execute(node)
    })

    Nodes_Value[class_name] = class_operator

                
