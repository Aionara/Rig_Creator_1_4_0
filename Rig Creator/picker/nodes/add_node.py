import bpy

class RGC_Operator_AddPickerNode(bpy.types.Operator):
    """Add a Picker Node"""
    bl_idname = "node.add_picker_node"
    bl_label = "Add Picker Node"
    bl_options = {'REGISTER', 'UNDO'}
    
    type: bpy.props.StringProperty()

    def execute(self, context):
        node_tree = context.space_data.node_tree
        if node_tree.bl_idname == 'RGC_NodeTree_Picker':
            bpy.ops.node.add_node(use_transform=True, type=self.type)

        return {'FINISHED'}


def AddNodes(self, context):
    layout = self.layout
    node_tree = context.space_data.node_tree
    if node_tree.bl_idname == 'RGC_NodeTree_Picker' and node_tree.type_mode == "EDIT":
        
        layout.menu("RGC_Menu_Inputs")
        layout.menu("RGC_Menu_DrawNode")
        layout.menu("RGC_Menu_Value")

class RGC_Menu_DrawNode(bpy.types.Menu):
    """Menu for adding Picker Nodes"""
    bl_idname = "RGC_Menu_DrawNode"
    bl_label = "Draw"
    
    def draw(self, context):
        layout = self.layout
        layout.operator("node.add_picker_node", text="Draw Picker",).type = "P-OutPicker"
        layout.separator()
        layout.operator("node.add_picker_node", text="Select Bone",).type = "P-SelectBone"
        layout.operator("node.add_picker_node", text="Menu Properties",).type = 'P-CallProperties'
        layout.operator("node.add_picker_node", text="Draw Image",).type = "P-Image"
        layout.operator("node.add_picker_node", text="Draw Label",).type = "P-Label"
        #layout.operator("node.add_picker_node", text="Icon",).type = "P-Icon"
        layout.separator()
        layout.operator("node.add_picker_node", text="Join Picker",).type = "P-JoinPicker"
        layout.operator("node.add_picker_node", text="If Draw",).type = "P-IfDraw"

class RGC_Menu_Picker(bpy.types.Menu):
    """Menu for adding Picker Nodes"""
    bl_idname = "RGC_Menu_Picker"
    bl_label = "Picker"
    
    def draw(self, context):
        layout = self.layout
        
        
class RGC_Menu_Outputs(bpy.types.Menu):
    """Menu for adding Picker Nodes"""
    bl_idname = "RGC_Menu_Outputs"
    bl_label = "Outputs"
    
    def draw(self, context):
        layout = self.layout
        

class RGC_Menu_Inputs(bpy.types.Menu):
    """Menu for adding Picker Nodes"""
    bl_idname = "RGC_Menu_Inputs"
    bl_label = "Inputs"
    
    def draw(self, context):
        layout = self.layout
        
        layout.operator("node.add_picker_node", text="Bone",).type = "P-Bone"
        layout.operator("node.add_picker_node", text="Image",).type = "P-GetImage"
        layout.operator("node.add_picker_node", text="Propertie",).type = "P-GetPropertie"

class RGC_Menu_Value(bpy.types.Menu):
    """Menu for adding Picker Nodes"""
    bl_idname = "RGC_Menu_Value"
    bl_label = "Value"
    
    def draw(self, context):
        layout = self.layout
        Nodes = [
            "Print",
            "String",
            "Float",
            "Int",
            "Vector",
            "Vector Acceleration",
            "Vector Direction",
            "Vector Euler",
            "Vector Translation",
            "Vector Velocity",
            "Vector xyz",
            "Color",
        ]
        for node in Nodes:
            layout.operator("node.add_picker_node", text=node).type = f"P-{node}"