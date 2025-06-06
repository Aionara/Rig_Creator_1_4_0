import bpy
from ...generaldata import GeneralArmatureData
import gpu
from gpu_extras.batch import batch_for_shader
import blf

from ..check_selected_bones import *
from ..draw import *

def set_save_operator(self, context):
        node = None
        outputs = self.outputs.get("Draw")
        if outputs:
                if outputs.links:
                    node = outputs.links[0].to_node
        if node :
            self.SetSaveOperator(node.x, node.y, node.size_x, node.size_y)

class RGC_PickerNodes(GeneralArmatureData, Draw):
    
    save_position : bpy.props.FloatVectorProperty(name="Position", default=(0,0),size=2, subtype='XYZ')
    index : bpy.props.IntProperty(name="Index", default=0)
    use_collider : bpy.props.BoolProperty(name="Use Collider", default=False)
    
    
    x: bpy.props.FloatProperty(
            default=0,
            update = set_save_operator,
        )
    y: bpy.props.FloatProperty(
            default=0,
            update = set_save_operator,
        )
    size_x: bpy.props.FloatProperty(
            default=50,
            update = set_save_operator,
        )
    size_y: bpy.props.FloatProperty(
            default=50,
            update = set_save_operator,
        )
    
    
    save_x: bpy.props.FloatProperty(
            default=0,
        )
    save_mirror_x: bpy.props.FloatProperty(
            default=0,
        )
    save_y: bpy.props.FloatProperty(
            default=0,
        )
    save_size_x: bpy.props.FloatProperty(
            default=50,
        )
    save_size_y: bpy.props.FloatProperty(
            default=50,
        )
    
    
    is_move : bpy.props.BoolProperty(name="Use Collider", default=False)
    

    def SetSaveOperator(self, x, y, size_x, size_y):
        self.save_x = x + self.x * size_x
        self.save_mirror_x = x + (self.x*-1) * size_x
        self.save_y = y + self.y * size_y
        self.save_size_x = self.size_x * size_x
        self.save_size_y = self.size_y * size_y
    
    
    def init(self, context):
        global Set_FSB
        Set_FSB.append(self.CheckSelectBone)
        
    def draw_buttons(self, context, layout):
        if self.GetTypeMode() != "PICKER": 
            layout.prop(self, "x", text="X")
            layout.prop(self, "y", text="Y")
            layout.prop(self, "size_x", text="Size X")
            layout.prop(self, "size_y", text="Size Y")
        
    
    def update(self):
        pass

    def draw_piker(self, x, y, size_x, size_y):
        for input in self.inputs:
            if input.bl_idname == "RGC_Socket_Picker":
                node = self.GetInputNode(obj_socket=input)
                if node :
                    node.draw_piker(x, y, size_x, size_y)

        
    HIDDEN_POSITION = (-500000, -500000)
    
    def swich_mode(self):
        
        if self.GetTypeMode() == "PICKER": 
            self.save_position = self.location
            self.is_visible = False 
            self.location = self.HIDDEN_POSITION
            self.select = False
            
        else:
            self.location = self.save_position
            self.is_visible = True
            
    
    def CheckSelectBone(self, select_bone):
        ...
    
    def GetNodeTree(self):
        if self:
            return self.id_data
        return None
    def GetTypeMode(self):
        if self.GetNodeTree():
            return self.GetNodeTree().type_mode
        return "None"
    def GetTypeModeIsEdit(self) -> bool:
        return self.GetNodeTree().type_mode == "EDIT"
    
    def InputLink(self, socket="", index=-1, obj_socket=None):
        def get_input_value(input_socket):
            if input_socket:
                if input_socket.links:
                    return input_socket.links[0].from_socket.default_value
                else:
                    return input_socket.default_value
            return None

        if obj_socket is not None:
            return get_input_value(obj_socket)
        elif index >= 0 and index < len(self.inputs):
            return get_input_value(self.inputs[index])
        elif socket:
            input_socket = self.inputs.get(socket)
            return get_input_value(input_socket)

        return None
    
    def NormalizeColor(self, color : list) -> list:
        return(color[0], color[1], color[2])
    
    def GetInputNode(self, socket="", index=-1, obj_socket=None):
        def get_input_value(input_socket):
            if input_socket:
                if input_socket.links:
                    return input_socket.links[0].from_node
            return None
        if obj_socket :
            return get_input_value(obj_socket)
        elif index >= 0 and index < len(self.inputs):
            return  get_input_value(self.inputs[index])
        elif socket:
            input = self.inputs.get(socket)
            if input: 
                return get_input_value(input)
        return None
    
    def SetOperator(self, x, y, size_x, size_y):
        self.SetSaveOperator(x, y, size_x, size_y)
        for input in self.inputs:
            if input.bl_idname == "RGC_Socket_Picker":
                node = self.GetInputNode(obj_socket=input)
                
                if node :
                    node.SetOperator(x, y, size_x, size_y)
        
        x = x + self.x * size_x
        y = y + self.y * size_y
        size_x = self.size_x * size_x
        size_y = self.size_y * size_y
        
        if self.DetectCollision(
            x,
            y,
            size_x,
            size_y
            ) == "CLICK" :
            print(self.name)
            self.execute()
                    
        
                    
    def execute(self) : ... 
    
    def DrawProperties(self, context, layout):
        for inp in self.inputs :
            if inp.bl_idname == "RGC_Socket_Properties":
                node = self.GetInputNode(obj_socket=inp)
                if node :
                    node.DrawProperties(context, layout)
                 
    def DetectCollision(self, box_x, box_y, width, height):
        # Obtener contexto de la ventana y área
        mouse_x, mouse_y = bpy.context.space_data.cursor_location

        # Bordes de la caja
        left = box_x - (width / 2)
        right = box_x + (width / 2)
        top = box_y
        bottom = box_y - height
        
        
        # Verificar si el mouse está dentro de la caja
        inside = left <= mouse_x <= right and bottom <= mouse_y <= top
        if inside:
                return "CLICK"
        return "OUT"

    def SetMove(self):
        if self.is_move :
            self.x, self.y = bpy.context.space_data.cursor_location
    
    def DrawButton(
        self, x, y, width, height, 
        desactive_color : list = (0.5, 0.5, 0.5, 1), 
        use_shadow : bool = False,
        shadow_width = 0, shadow_height= 0,
        shadow_color : list = (1, 1, 1, 1),
        normal_color : list = (0.8,0.8, 0.8, 1), active_color : list = (0, 0, 1, 1), 
        is_bool : bool = True, value_bool : bool = False,
        text : str = "", text_size = 1, text_color = (1, 1, 1, 1)
        
        ):
        
        color = desactive_color
        if is_bool :
            color = normal_color if not value_bool else active_color
        else: 
            color = normal_color
            
        if use_shadow :
            self.DrawQuare(
                x=x, 
                y=y+shadow_height/2,
                width=width+shadow_width,
                height=height+shadow_height, 
                color=shadow_color,
            )
        
        self.DrawQuare(
            x=x, 
            y=y,
            width=width,
            height=height, 
            color=color,
        )
        
        self.DrawText(
            x=x,
            y=y,
            width=width,
            height=height, 
            text=text,
            text_size=text_size,
            color=text_color,
        )
    
    
