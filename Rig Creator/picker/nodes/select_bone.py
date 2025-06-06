import bpy 
from .general_nodes import *





class RGC_PNode_SelectBone(RGC_PickerNodes, bpy.types.Node):
    """Select a Bone"""
    bl_idname = 'P-SelectBone'
    bl_label = 'Select Bone'
    bl_icon = 'BONE_DATA'
   
    active : bpy.props.BoolProperty()
    
    save_color : bpy.props.FloatVectorProperty(default=(0.0, 0.0, 0.0, 1.0), size=4)
    save_mirror_color : bpy.props.FloatVectorProperty(default=(0.0, 0.0, 0.0, 1.0), size=4)
    def IsActive(self, bones_list) -> bool:
        for bone_name in bones_list:
            bone = self.GetBone(bone_name, "POSE")
            if bone :
                return bone.bone.select
        return False
    
    def init(self, context):
        
        self.index = 1
        self.use_collider = True
        self.width = 250
        # Configura el valor por defecto de "Bone" si es necesario
        self.inputs.new(type="RGC_Socket_Picker", name="Draw")
        self.outputs.new(type="RGC_Socket_Picker", name="Draw")
        self.inputs.new(type="NodeSocketBool", name="Use Text").default_value = True
        self.inputs.new(type="NodeSocketString", name="Text").default_value = "Bone"
        self.inputs.new(type="NodeSocketFloat", name="Text Size").default_value = 1
        self.inputs.new(type="NodeSocketColor", name="Text Color").default_value = (1, 1, 1, 1)
        self.inputs.new(type="NodeSocketColor", name="Normal Color").default_value = (0, 1, 0, 1)
        self.inputs.new(type="NodeSocketColor", name="Active Color").default_value = (0, 1, 1, 1)
        self.size_x = 85
        self.size_y = 50
        self.inputs.new(type="NodeSocketBool", name="Only Selected").default_value = True
        self.inputs.new(type="NodeSocketBool", name="Selected and Deselected").default_value = True
        self.inputs.new(type="NodeSocketBool", name="Mirror").default_value = False
        self.inputs.new(type="NodeSocketInt", name="Range").default_value = -1
        new = self.inputs.new(type="RGC_Socket_Bone", name="Bone")
        new.use_addinputs = True

        self.ColorActive()
        
    def ColorActive(self):
        color = self.InputLink("Normal Color")
        mirror_color = self.InputLink("Normal Color")
        if self.IsActive(self.CreateList()):
            color = self.InputLink("Active Color")
        if self.IsActive(self.CreateList(use_mirror=True)):
            mirror_color = self.InputLink("Active Color")
        self.save_color = color 
        self.save_mirror_color = mirror_color
        
    
    
    def SelectBone(self, use_names=False) -> list:
        bones = []
        names = []
        armature = self.GetArmature()

        if armature and self.GetObjMode() == 'POSE':
            for input in self.inputs:
                if input.bl_idname == "RGC_Socket_Bone":
                    # Obtiene el nombre del hueso desde el input
                    bone_name = self.InputLink(obj_socket=input)
                    if not bone_name:
                        continue  # Si está vacío, saltamos

                    # Evita duplicados
                    if bone_name in names:
                        continue
                    names.append(bone_name)

                    # Verifica si el hueso existe en el armature
                    bone = self.GetBone(bone_name, "POSE")
                    if bone:
                        bones.append(bone)

        # Devuelve según el parámetro solicitado
        return names if use_names else bones
        
    def bone_label(self) :
        bones, names = [self.SelectBone(), self.SelectBone(use_names=True)]
        if bones :
            if len(bones) != 1:
                return "Group Bones"
            return bones[0].name
        return self.bl_label
    
    def draw_buttons(self, context, layout):
        super().draw_buttons(context, layout)
        
    def draw_piker(self, x, y, size_x, size_y):
        super().draw_piker(x, y, size_x, size_y)
        self.DrawBoxToBone(x, y, size_x, size_y)

    def DrawBoxToBone(self, x, y, size_x, size_y):
        
        
        for i in range(2 if self.InputLink(socket="Mirror") else 1):
            m = self.save_x
            if i == 1:
                if self.InputLink(socket="Mirror") :
                    m = self.save_mirror_x

            self.DrawQuare(
                x=m, 
                y=self.save_y,
                width=self.save_size_x,
                height=self.save_size_y, 
                color=self.save_color if i == 0 else self.save_mirror_color,
            )
            
            if self.InputLink(socket="Use Text"):
                self.DrawText(
                    x=m,
                    y=self.save_y,
                    width=self.save_size_x,
                    height=self.save_size_y, 
                    text=self.InputLink("Text"),
                    text_size=self.InputLink("Text Size"),
                    color=self.InputLink("Text Color"),
                )
        

    def update(self):
        self.label = self.bone_label()
        super().update()
    
    def SetOperator(self, x, y, size_x, size_y):
        
        self.SetSaveOperator(x, y, size_x, size_y)
        for inp in self.inputs :
            if inp.bl_idname == "RGC_Socket_Picker":
                node = self.GetInputNode(obj_socket=inp)
                if node :
                    node.SetOperator(x, y, size_x, size_y)
           
        normal_x = x + self.x * size_x
        mirror_x = x + (self.x*-1) * size_x
        y = y + self.y * size_y
        size_x = self.size_x * size_x
        size_y = self.size_y * size_y
        
        for i in range(2 if self.InputLink(socket="Mirror") else 1):
            m = normal_x
            if i == 1:
                if self.InputLink(socket="Mirror") :
                    m = mirror_x
            if self.DetectCollision(m,y,size_x,size_y) == "CLICK" :
                if i == 1:
                    self.execute(use_mirror=True)
                else:
                    self.execute(use_mirror=False)

        self.ColorActive()
        
    def CreateList(self, use_mirror : bool = False):
        get_bones = []
        bones, names = [self.SelectBone(), self.SelectBone(use_names=True)]
        
        def collect_bones_to_select(bone, name):
            bones_to_select = []
            if bone:
                if self.InputLink("Range") <= -1:
                    # Single bone selection
                    bones_to_select.append(name)
                else:
                    # Range selection
                    base_name = bone.name[:-4]
                    bones_to_select.extend(f"{base_name}.{i+1:03}" 
                                    for i in range(self.InputLink("Range")))
            return bones_to_select
        
        # First collect all bones that need to be selected
        for bone, name in zip(bones, names):
            if use_mirror:
                # Handle mirror bones
                mirror_name = ""
                if ".L" in name:
                    mirror_name = name.replace(".L", ".R")
                elif ".R" in name:
                    mirror_name = name.replace(".R", ".L")
                elif "_L" in name:
                    mirror_name = name.replace("_L", "_R")
                elif "_R" in name:
                    mirror_name = name.replace("_R", "_L")
                elif ",L" in name:
                    mirror_name = name.replace(",L", ",R")
                elif ",R" in name:
                    mirror_name = name.replace(",R", ",L")
                
                if mirror_name:
                    mirror_bone = self.GetBone(mirror_name, "POSE")
                    get_bones.extend(collect_bones_to_select(mirror_bone, mirror_name))
            else:
                get_bones.extend(collect_bones_to_select(bone, name))
        return get_bones
    

    def execute(self, use_mirror : bool = False):

        # Now process the selection/deselection
        # Now process the selection/deselection
        get_bones = self.CreateList(use_mirror)
        active = self.IsActive(get_bones)
        
        if get_bones:
            
            # Deselect all bones first if Only Selected is enabled
            if self.InputLink("Only Selected"):
                armature = self.GetActiveObject()
                if armature and armature.pose:
                    for bone in armature.pose.bones:
                        bone.bone.select = False
            
            # Apply selection to all collected bones
            for bone_name in get_bones:
                if self.InputLink("Selected and Deselected"):
                    self.ActiveBone(bone_name, "POSE", use_deselect=active)
                else:
                    self.ActiveBone(bone_name, "POSE")
                    
class RGC_Operator_PickerSelectBone(GeneralArmatureData, bpy.types.Operator):
    """Select a Bone"""
    bl_idname = "picker.select_bone"
    bl_label = "Select Bone"
    node_name : bpy.props.StringProperty(name="Node Name", default="P-SelcetBone")
    
    @classmethod
    def poll(cls, context):  
        return context.active_object and context.active_object.type == 'ARMATURE'
    
    def execute(self, context):
        space = context.space_data
        if not space or not hasattr(space, 'edit_tree') or not space.edit_tree:
            self.report({'ERROR'}, "No Node Tree found in context")
            return {'CANCELLED'}

        node_tree = space.edit_tree
        node = node_tree.nodes.get(self.node_name)

        if not node:
            self.report({'ERROR'}, f"Node '{self.node_name}' not found")
            return {'CANCELLED'}

        if node.bl_idname == 'P-SelcetBone':
            node.execute()

        return {'FINISHED'}