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

class RGC_PNode_GetPropertie(RGC_PickerNodes, bpy.types.Node):
    """Get Properties To Object"""
    bl_idname = 'P-GetPropertie'
    bl_label = 'Property'
    bl_icon = 'PROPERTIES'
   
    
    use_posebone : bpy.props.BoolProperty()
    use_data : bpy.props.BoolProperty()
    propertie: bpy.props.StringProperty()
    
    use_active_object : bpy.props.BoolProperty()
    use_active_bone : bpy.props.BoolProperty()
    
    def init(self, context):
        self.index = 1

        # Configura el valor por defecto de "Bone" si es necesario
        self.outputs.new(type="RGC_Socket_Properties", name="Property")
    
    def PropertyLabel(self) -> str:
        t: str = self.propertie[0]  # Primera letra
        text = self.propertie[1:] 
        t = t.upper() + text
        return t.replace("_", " ")
    
    def draw_buttons(self, context, layout):
        if self.GetTypeMode() != "PICKER":
            layout.operator("rgc.get_propertie", 
            text="Paste Propertie" if self.propertie == "" else f"Reload {self.PropertyLabel()}",
            icon="PASTEDOWN"
            ).node_name = self.name
            layout.prop(self, "use_active_object", text = "Active Object")
            layout.prop(self, "use_active_bone", text = "Active Bone")
            box = layout.box()
            self.DrawProperties(context, box)

    def GetValue(self):
        try:
            # Obtener el objeto principal
            obj = self.GetActiveObject() if self.use_active_object else self.InputLink("Object")
            inp_bone = self.InputLink("Bone")
            inp_constraint = self.InputLink("Constraint")
            inp_collection = self.InputLink("Collection")

            if inp_collection:
                collection = obj.data.collections.get(inp_collection)
                if collection :
                    return getattr(collection, self.is_custom(collection, self.propertie))

            elif inp_bone:
                bone = self.GetBone(self.GetActiveBone().name, mode="POSE" if self.use_posebone else "OBJECT") if self.use_active_bone else self.GetBone(inp_bone, mode="POSE" if self.use_posebone else "OBJECT")
                if inp_constraint:
                    constraint = bone.constraints.get(inp_constraint)
                    if constraint:
                        return getattr(constraint, self.is_custom(constraint, self.propertie))
                else:
                    return getattr(bone, self.is_custom(bone, self.propertie))
                    
            else:
                if self.use_data:
                    return getattr(obj.data, self.is_custom(obj.data, self.propertie))
                else:
                    return getattr(obj, self.is_custom(obj, self.propertie))
            return None
        except Exception as e:
            return None
    
    def is_custom(self, obj, key):
        if hasattr(obj, "keys") : 
            for k in obj.keys() :
                if key == k:
                    return f'["{key}"]'
        return key
    
    def DrawProperties(self, context, layout):
        
        try:
            # Obtener el objeto principal
            obj = self.GetActiveObject() if self.use_active_object else self.InputLink("Object")
            inp_bone = self.InputLink("Bone")
            inp_constraint = self.InputLink("Constraint")
            inp_collection = self.InputLink("Collection")

            if not obj:
                layout.label(text="Objetonot found")
                return

            if inp_collection:
                collection = obj.data.collections.get(inp_collection)
                if collection :
                    layout.prop(collection, self.is_custom(collection, self.propertie), text=self.PropertyLabel(), index=self.InputLink("Index"))

            elif inp_bone:
                bone = self.GetBone(self.GetActiveBone().name, mode="POSE" if self.use_posebone else "OBJECT") if self.use_active_bone else self.GetBone(inp_bone, mode="POSE" if self.use_posebone else "OBJECT")
                if inp_constraint:
                    constraint = bone.constraints.get(inp_constraint)
                    if constraint:
                        layout.prop(constraint, self.propertie, text=self.PropertyLabel(), index=self.InputLink("Index"))
                else:
                    layout.prop(bone, self.is_custom(bone, self.propertie), text=self.PropertyLabel(), index=self.InputLink("Index"))

            else:
                if self.use_data:
                    layout.prop(obj.data, self.is_custom(obj.data, self.propertie), text=self.PropertyLabel(), index=self.InputLink("Index"))
                else:
                    layout.prop(obj, self.is_custom(obj, self.propertie), text=self.PropertyLabel(), index=self.InputLink("Index"))

        except Exception as e:
            layout.label(text=f"Error: {str(e)}")

    def update(self):
        pass
    
    def execute(self):
        props = self.Props()
        self.propertie = props.picker_propertie
        props.picker_object_name
        for inp in self.inputs:
            self.inputs.remove(inp)
        self.inputs.new(type="NodeSocketObject", name="Object").default_value = bpy.data.objects.get(props.picker_active_object)
        self.use_data = "Armature".lower() in props.picker_object_type.lower()
        if "Collection".lower() in props.picker_object_type.lower() :
            self.inputs.new(type="NodeSocketString", name="Collection").default_value = props.picker_object_name
        elif "Bone".lower() in props.picker_object_type.lower() or "Constraint".lower() in props.picker_object_type.lower():
                self.inputs.new(type="RGC_Socket_Bone", name="Bone").default_value = props.picker_active_bone
                self.use_posebone = "Pose".lower() in props.picker_object_type.lower()
                
                if "Constraint".lower() in props.picker_object_type.lower():
                    self.inputs.new(type="NodeSocketString", name="Constraint").default_value = props.picker_active_constraint
                    self.use_posebone = True
                
        self.inputs.new(type="NodeSocketInt", name="Index").default_value = -1

        self.label = self.PropertyLabel()
        

    
class RGC_Operator_GetPropertie(GeneralArmatureData, bpy.types.Operator):
    bl_idname = "rgc.get_propertie"
    bl_label = ""

    
    node_name : StringProperty()
    
    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        
        node = self.GetNode(context, self.node_name)
        if node:
            node.execute()
        return {"FINISHED"}

