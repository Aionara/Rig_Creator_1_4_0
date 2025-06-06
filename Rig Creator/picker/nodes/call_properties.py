import bpy 
from .general_nodes import *
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


Menu = []
Node = None

class RGC_PNode_CallProperties(RGC_PickerNodes, bpy.types.Node):
    """CallProperties"""
    bl_idname = 'P-CallProperties'
    bl_label = 'Menu Properties'
    bl_icon = 'PROPERTIES'
    
    
    use_active : bpy.props.BoolProperty()
    
    def init(self, context):
        self.index = 1

        self.use_collider = True
        self.width = 250
        # Configura el valor por defecto de "Bone" si es necesario
        self.inputs.new(type="RGC_Socket_Picker", name="Draw")
        self.outputs.new(type="RGC_Socket_Picker", name="Draw")
        self.inputs.new(type="NodeSocketBool", name="Use Text").default_value = True
        self.inputs.new(type="NodeSocketString", name="Text").default_value = "Menu "
        self.inputs.new(type="NodeSocketFloat", name="Text Size").default_value = 1
        self.inputs.new(type="NodeSocketColor", name="Text Color").default_value = (1, 1, 1, 1)
        self.inputs.new(type="NodeSocketColor", name="Normal Color").default_value = (0, 1, 0, 1)
        self.size_x = 100
        new = self.inputs.new(type="RGC_Socket_Properties", name="Propertie")
        new.use_addinputs = True
        
    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        
    
    def DrawProperties(self, context, layout):
        return super().DrawProperties(context, layout)
        
    
    def draw_piker(self, x, y, size_x, size_y):
        super().draw_piker(x, y, size_x, size_y)
        
        text = ""
        if self.InputLink(socket="Use Text") : 
            text = self.InputLink("Text")
            
        self.DrawButton(
            self.save_x,self.save_y,
            self.save_size_x,self.save_size_y,
            normal_color=self.InputLink("Normal Color"),
            text=text, 
            text_color=self.InputLink("Text Color"),
            text_size= self.InputLink("Text Size"),
            value_bool=self.use_active,
        )
    
    def execute(self):
        
        global Node
        Node = self
        bpy.ops.wm.call_menu(name=RGC_Menu_CallProperties.bl_idname)


        
                            
class RGC_Menu_CallProperties(GeneralArmatureData, bpy.types.Menu):
    bl_idname = 'Menu_CallProperties'
    bl_label = ''
    
    def draw(self, context):
        layout = self.layout
        
        global Node 
        if Node :
            layout.alignment = "RIGHT"
            col = layout.column()
            
            Node.DrawProperties(context, col)

        