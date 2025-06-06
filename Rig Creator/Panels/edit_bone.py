from .general import *
from ..generaldata import GeneralArmatureData
import bmesh
from .generators import *


def Pose_EditBone(self, context) : 
    layout = self.layout
    RGC = GeneralArmatureData()
    if RGC.GetActiveObject() and RGC.GetActiveObject().type == "ARMATURE":
        layout.menu("rgc.editbone", text="Edit Bone")
            

class RGC_Menu_EditBone(GeneralArmatureData, bpy.types.Menu):
    bl_idname = "rgc.editbone"
    bl_label = ""

    def draw(self, context):
        layout = self.layout
        props = self.Props()
        if self.GetObjMode() == "EDIT":
            layout.prop(props, "ebone_curve_in_out", text="Normal Curve")