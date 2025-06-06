import bpy 
from .general_nodes import *


class RGC_PNode_IfDraw(RGC_PickerNodes, bpy.types.Node):
    bl_idname = 'P-IfDraw'
    bl_label = 'If Draw'
    bl_icon = 'OUTLINER'
   
    def mode(self, context):
        for inp in self.inputs:
            if inp.name in ["Value", "Property", "Expression"] :
                self.inputs.remove(inp)
        if self.Type == {'VALUE'} : 
            self.inputs.new("NodeSocketBool", name="Value")
        elif self.Type == {'PROPERTY'} : 
            self.inputs.new("RGC_Socket_Properties", name="Property")
            self.inputs.new("NodeSocketVirtual", name="Value")
        else:
            self.inputs.new("NodeSocketString", name="Expression")
            
    Type : bpy.props.EnumProperty(items=[
        ('VALUE', "Value", ""),
        ('EXPRESSION', "Expression", ""),
        ('PROPERTY', "Property", ""),
        ], 
        name='BendyBone Type', 
        default={'VALUE'}, 
        options={'ENUM_FLAG'},
        update=mode
        )

    enum : bpy.props.EnumProperty(items=[
        ("EQUAL", "Equal to", ""),
        ("GREATER_THAN","Greater than", ""),
        ("LESS_THAN", "Less than", ""),
        ("GREATER_THAN_OR_EQUAL", "Greater than or equal to", ""),
        ("LESS_THAN_OR_EQUAL", "Less than or equal to", ""),
        ("NOT_EQUAL", "Not equal to", ""),
        ], 
        name='', 
        default='EQUAL', 
        update=mode
        )
        
        
        
    def init(self, context):
        self.index = 1
        
        # Configura el valor por defecto de "Bone" si es necesario
        self.width = 250
        new = self.inputs.new(type="RGC_Socket_Picker", name="Draw A")
        new = self.inputs.new(type="RGC_Socket_Picker", name="Draw B")
        new = self.outputs.new(type="RGC_Socket_Picker", name="Piker")
        self.inputs.new("NodeSocketBool", name="Value")
    
    def draw_buttons(self, context, layout):
        if self.GetTypeMode() == "EDIT":
            layout.prop(self, "Type", )
            if self.Type == {'PROPERTY'} : 
                layout.prop(self, "enum", text="")
    
    def draw_piker(self, x, y, size_x, size_y):
        input_a = self.GetInputNode(socket="Draw A")
        input_b = self.GetInputNode(socket="Draw B")
        node = input_a
        if self.Type == {'VALUE'} :
            node = input_a if not self.InputLink(socket="Value") else input_b
        elif self.Type == {'PROPERTY'} :
            property = self.GetInputNode(socket="Property")
            if property : 
                property = property.GetValue()
                input_socket = self.inputs.get("Value")
                if input_socket:
                    if input_socket.links:
                        inp = input_socket.links[0].from_socket.default_value
                        if self.enum == "EQUAL" :
                            node = input_b if inp == property else input_a
                        elif self.enum == "NOT_EQUAL" :
                            node = input_b if not inp == property else input_a
                        elif self.enum == "GREATER_THAN" :
                            node = input_b if not inp > property else input_a
                        elif self.enum == "LESS_THAN" :
                            node = input_b if not inp < property else input_a
                        elif self.enum == "GREATER_THAN_OR_EQUAL" :
                            node = input_b if not inp >= property else input_a
                        elif self.enum == "LESS_THAN_OR_EQUAL" :
                            node = input_b if not inp <= property else input_a
                    else :
                        node = input_a 
                else :
                    node = input_a 
            else :
                node = input_a 
        else:
            link_value = self.InputLink(socket="Expression")
            e = eval(link_value) if link_value else None
            node = input_a if e else input_b
        if node :
            node.draw_piker( x, y, size_x, size_y)
    
    def SetOperator(self):
        input_a = self.GetInputNode(socket="Draw A")
        input_b = self.GetInputNode(socket="Draw B")
        if self.Type == {'VALUE'} :
            node = input_a if not self.InputLink(socket="Value") else input_b
        else:
            link_value = self.InputLink(socket="Expression")
            e = eval(link_value) if link_value else None
            node = input_a if e else input_b
        node.SetOperator()
    
    def update(self):
        pass
    
    def execute(self):
        pass