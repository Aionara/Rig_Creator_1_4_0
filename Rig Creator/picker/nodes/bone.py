import bpy 
from .general_nodes import *
class RGC_PNode_Bone(RGC_PickerNodes, bpy.types.Node):
    """Bone"""
    bl_idname = 'P-Bone'
    bl_label = 'Bone'
    bl_icon = 'BONE_DATA'
    
    
    
    def init(self, context):
        bone = self.GetActiveBone(mode="POSE")
        new = self.outputs.new(type="RGC_Socket_Bone", name="Bone")
        if bone : 
            new.default_value = bone.name
    def bone_label(self) :
        armature = self.GetArmature()
        if armature and self.GetObjMode() == 'POSE':
            name = self.outputs["Bone"].default_value
            bone = self.GetBone(name, "POSE")
            if bone:
                return bone.name
        return self.bl_label
    
    def draw_buttons(self, context, layout):
        pass
    def update(self):
        self.label = self.bone_label()
        super().update()

                
