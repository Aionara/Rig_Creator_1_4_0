import bpy
from ..generaldata import *


def DrawButton(self, context):
    layout = self.layout
    layout.separator()
    layout.operator("rgc.copy_propertie", text="Copy Property", icon="COPYDOWN")

class RGC_CopyPropertie(GeneralArmatureData, bpy.types.Operator):
    bl_idname = "rgc.copy_propertie"
    bl_label = ""

    @classmethod
    def poll(cls, context):
        return (
            (context.space_data.type == "PROPERTIES") and 
            (context.object is not None) and  # Asegúrate de que haya un objeto activo
            (
                context.space_data.context == 'OBJECT' or
                context.space_data.context == 'BONE' or
                context.space_data.context == 'DATA' or
                context.space_data.context == 'BONE_CONSTRAINT'
            )
        )
    def execute(self, context):
        props = self.Props()

        if hasattr(context, "button_prop"):
            
            try :
                props.picker_object_name = context.button_pointer.name
                props.picker_object_type = context.button_pointer.bl_rna.identifier
                props.picker_propertie = context.button_prop.identifier
                
                props.picker_active_object = self.GetActiveObject().name

                if "Bone".lower() in props.picker_object_type.lower():
                    props.picker_active_bone = self.GetActiveBone("POSE").name
                if "Constraint".lower() in props.picker_object_type.lower():
                    props.picker_active_constraint = props.picker_object_name
                
                
                # Opci
                
                self.report({'INFO'}, f"Is Get Property")
                
            except :
                self.report({'WARNING'}, "Property not found ")
            
        else:
            self.report({'WARNING'}, "No property selected")

        return {"FINISHED"}
