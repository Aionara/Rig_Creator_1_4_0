
import bpy
from bpy.props import (
    BoolProperty,
    IntProperty,
    FloatProperty,
    StringProperty,
    EnumProperty,
    PointerProperty,
    CollectionProperty,
    FloatVectorProperty,
    IntVectorProperty,
    BoolVectorProperty,
)


def set_index(nodes):
    # Ordena los nodos por su índice
    nodes = sorted(nodes, key=lambda x: x.index)
    
    # Marca todos los nodos como seleccionados
    for node in nodes:
        
        node.select = True


@bpy.app.handlers.persistent
def update_nodos(dummy):
    
    
    return
    nodes = set() 
    
    for tree in bpy.data.node_groups:
        if tree.bl_idname == RGC_NodeTree_Picker.bl_idname:
            for node in tree.nodes:
                if node.bl_idname == 'P-OutPicker':
                    nodes.add(node) 
    for node in nodes:
        if hasattr(node, 'update'):  
            node.update()     
    
    nodes = set() 
    
    for tree in bpy.data.node_groups:
        if tree.bl_idname == RGC_NodeTree_Picker.bl_idname:
            for node in tree.nodes:
                if hasattr(node, 'update'):  
                    nodes.add(node) 
                    
    for node in nodes:
        if node.inputs or node.outputs:
            node.update() 
            
     
    
    
def update_enum(self, context):
    nodes = set() 
    
    for tree in bpy.data.node_groups:
        if tree.bl_idname == RGC_NodeTree_Picker.bl_idname:
            for node in tree.nodes:
                if hasattr(node, 'swich_mode'):  
                    nodes.add(node) 
                    
    for node in nodes:
        node.swich_mode()
    

class RGC_NodeTree_Picker(bpy.types.NodeTree):
    bl_idname = 'RGC_NodeTree_Picker'
    bl_label = 'Picker Bones'
    bl_icon = "RESTRICT_SELECT_OFF"
    
    type_mode : EnumProperty(
        name = "Type",
        items = [
            ('EDIT', 'Edit', ''),
            ('PICKER', 'Picker', ''),
            
        ],
        default = 'EDIT',
        update = update_enum,
    )
    
    lock_pocition : BoolProperty(
        name = "Lock Position",
        default = True,
        description = "Lock position of nodes",
    )
    
    Colliders : list = []

def DrawPicker(self, context):
    layout = self.layout
    node_tree = context.space_data.node_tree
    
    if node_tree and node_tree.bl_idname == 'RGC_NodeTree_Picker':
        layout.prop(node_tree, "type_mode", text="")
        if node_tree.type_mode == 'PICKER': ...
            #layout.prop(node_tree, "lock_pocition", text="", icon='DECORATE_LOCKED', emboss=True)



# Definir el operador modal
class RGC_ClickButton(bpy.types.Operator):
    bl_idname = "rgc.click_button"
    bl_label = ""

    def execute(self, context):
        # Buscar nodos válidos
        nodes = set()

        for tree in bpy.data.node_groups:
            if tree.bl_idname == "RGC_NodeTree_Picker":
                for node in tree.nodes:
                    if node.bl_idname == 'P-OutPicker':
                        nodes.add(node)
                    
        if nodes:
            # Si hay nodos, ejecutar SetOperator directamente
            for node in nodes:
                if hasattr(node, 'SetOperator'):
                    node.SetOperator()
        
            
        return {'FINISHED'}
    
class RGC_MoveButton(bpy.types.Operator):
    bl_idname = "rgc.move_button"
    bl_label = "Detectar Clic en Node Editor"

    def execute(self, context):
        # Buscar nodos válidos
        nodes = set()

        for tree in bpy.data.node_groups:
            if tree.bl_idname == "RGC_NodeTree_Picker":
                for node in tree.nodes:
                    if node.bl_idname == 'P-OutPicker':
                        nodes.add(node)

        if nodes:
            for node in nodes:
                # Obtener posición del cursor
                mouse_x, mouse_y = context.space_data.cursor_location

                # Bordes de la caja del nodo
                left = node.x - (node.size_x / 2)
                right = node.x + (node.size_x / 2)
                top = node.y
                bottom = node.y - node.size_y

                # Verificar si el mouse está dentro de la caja
                inside = left <= mouse_x <= right and bottom <= mouse_y <= top
                if inside: pass
                    # Mover el nodo a la posición del cursor
                node.x += mouse_x
                node.y += mouse_y
                

        return {'FINISHED'}

# Función para registrar el keymap
addon_keymaps = []

def register_keymap():
    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps.new(name='Node Editor', space_type='NODE_EDITOR')
    kmi = km.keymap_items.new("rgc.click_button", 'LEFTMOUSE', 'RELEASE',
        ctrl=False, alt=False, shift=True, repeat=False)
    addon_keymaps.append((km, kmi))
    #kmi = km.keymap_items.new("rgc.move_button", 'G', 'PRESS',
    #    ctrl=False, alt=False, shift=True, repeat=True)
    #addon_keymaps.append((km, kmi))
    
# Función para eliminar el keymap al desregistrar el addon
def unregister_keymap():
    wm = bpy.context.window_manager
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

