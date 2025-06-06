

from .node_tree import *
from .nodes import *
from .socket import *


def AddNodes(self, context) : 

    if context.space_data.tree_type == RGC_Node_Tree.bl_idname:
            layout = self.layout
            layout.menu("rgc.menuconstraints", text="Constraints")
            layout.menu("rgc.menuvalue", text="Value")
            #input menu
            #layout.separator()
            #valores menu
            
class RGC_Menu_Constraints(bpy.types.Menu):
    bl_idname = "rgc.menuconstraints"
    bl_label = "Constraints"

    def draw(self, context):
        layout = self.layout
        nodes_constraints = (
            RGC_Node_OutConstraint,
            RGC_Node_InpConstraint,
        )
        for node in nodes_constraints:
            layout.operator("rgc.addnode", text=node.bl_label,).type = node.bl_idname

class RGC_Menu_Value(bpy.types.Menu):
    bl_idname = "rgc.menuvalue"
    bl_label = "Value"

    def draw(self, context):
        layout = self.layout
        for node in Nodes_Value.values():
            layout.operator("rgc.addnode", text=node.bl_label,).type = node.bl_idname


classes = (
    RGC_Node_Tree, 
    
    # Memu
    RGC_Menu_Constraints,
    RGC_Menu_Value,
    
    # Socket
    RGC_Socket_Constraint,

)

classes_node = (
    # Nodes 
    RGC_Node_OutConstraint,
    RGC_Node_InpConstraint,
)



def NodeTreeRegister() : 
    for cls in classes:
        bpy.utils.register_class(cls)
        
    for cls in classes_node:
        bpy.utils.register_class(cls)
    
    
    for cls in Nodes_Value.values():
        bpy.utils.register_class(cls)
    
    bpy.types.NODE_MT_add.append(AddNodes)    
    
def NodeTreeUnregister() : 
    
    for cls in classes:
        bpy.utils.unregister_class(cls)
    for cls in classes_node:
        bpy.utils.unregister_class(cls)
        
    bpy.types.NODE_MT_add.remove(AddNodes)    
    