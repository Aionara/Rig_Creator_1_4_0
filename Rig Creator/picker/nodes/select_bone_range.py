import bpy 
from .general_nodes import *





class RGC_PNode_SelectBoneRange(RGC_PickerNodes, bpy.types.Node):
    """Select a Bone"""
    bl_idname = 'P-SelectBoneRange'
    bl_label = 'Select Bone'
    bl_icon = 'BONE_DATA'
   


    def init(self, context):
        self.index = 1
        self.draw_handler = bpy.types.SpaceNodeEditor.draw_handler_add(
            self.DrawsQuareOverNode, (self,), 'WINDOW', 'POST_PIXEL'
        )
        self.use_collider = True
        
        # Configura el valor por defecto de "Bone" si es necesario
        self.inputs.new(type="RGC_Socket_Picker", name="Piker")
        self.outputs.new(type="RGC_Socket_Picker", name="Piker")
        self.inputs.new(type="NodeSocketString", name="Text").default_value = "Bones"
        self.inputs.new(type="NodeSocketFloat", name="Text Size").default_value = 1
        self.inputs.new(type="NodeSocketColor", name="Text Color").default_value = (1, 1, 1, 1)
        self.inputs.new(type="NodeSocketColor", name="Normal Color").default_value = (0, 1, 0, 1)
        self.inputs.new(type="NodeSocketColor", name="Active Color").default_value = (0, 1, 1, 1)
        self.inputs.new(type="NodeSocketFloat", name="X").default_value = self.location[0]
        self.inputs.new(type="NodeSocketFloat", name="Y").default_value = self.location[1]
        self.inputs.new(type="NodeSocketFloat", name="Size X").default_value = 50
        self.inputs.new(type="NodeSocketFloat", name="Size Y").default_value = 50
        self.inputs.new(type="NodeSocketBool", name="Only Selected").default_value = True
        self.inputs.new(type="NodeSocketInt", name="Range").default_value = 1
        new = self.inputs.new(type="RGC_Socket_Bone", name="Bone")
        new.use_addinputs = True

    
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
        
    def draw_piker(self):
        super().draw_piker()
        self.DrawBoxToBone()
        
    def SetOperator(self):
        if self.use_collider : 
            if self.DetectCollision(
                self.InputLink("X"),
                self.InputLink("Y"),
                self.InputLink("Size X"),
                self.InputLink("Size Y")
                ) == "CLICK" :
                self.execute()
        super().SetOperator()
    
    def update(self):
        self.label = self.bone_label()
        super().update()
    
    def execute(self):
        
        bones, names = [self.SelectBone(), self.SelectBone(use_names=True)]
        for bone, name in zip(bones, names):
            if bone :
                name = bone.name[:-4]
                get_bones = []
                for i in range(self.InputLink("Range")):
                    get_bones.append(f"{name}.{i+1:003}")
                for name in get_bones:
                    self.ActiveBone(name, "POSE")
                if self.InputLink("Only Selected"):
                    for bone in self.GetActiveObject().pose.bones:
                        if not bone.name in names and not bone.name in get_bones :
                            bone.bone.select = False
                            
