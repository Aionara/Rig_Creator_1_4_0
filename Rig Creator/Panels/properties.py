import bpy
from .general import *
from ..generaldata import GeneralArmatureData

class RGC_Panel_Properties(GN_RigCreatorViewPort, bpy.types.Panel):
    bl_idname = "RGC_Panel_Properties"
    bl_label = "Properties"

    
    @classmethod
    def poll(cls, context):  
        Self = GeneralArmatureData()
        if Self == None : return False
        return Self.GetArmature() and Self.PanelType([{"ALL"}, {"ANIMATION"}])
    
    def draw(self, context):
        layout = self.layout
        layout.label(text="Properties")
        props = self.Props()
        if props == None : return
        col = layout.column(align=True)
        if self.Panel(col, "edit", "Edit", "GREASEPENCIL", Default_Closed=True):
            col.prop(props, "use_old_prop", text="Old Properties")
            props = self.PropsToArmature()
            if props : 
                col.operator("rgc.properties", text="Set Drive New to Old Properties").type = "SET"
                col.operator("rgc.general", text="Get Constraint Armature To Ik").type = "GET_CONST_ARMATURE"
        


        
class ID : 
    bl_parent_id = "RGC_Panel_Properties"


class Draw_Properties_To_RigCreator : 
    
    def GlobalLocal(self, layout, props, use_panel : bool = True):
        # Global Local
        if use_panel == True:
            if  not self.Panel(layout, "global_local", "Global Local", "", False) : return
        
        row = layout.row(align=True)
        row.prop(props, "head", text="Head")
        row.prop(props, "eyes", text="Eyes")
        layout = layout.column(align=True)
    
    def Face(self, layout, props):
        # Boca
        if self.Panel(layout, "face", "Face", "") : 
            if self.Panel(layout, "mouth", "Mouth", "") : 
                row = layout.row(align=True)
                for type in ["R", "L"] : 
                    row.prop(props, f"corner_mouth_{type}", text=f"Normal a Cartoon {type}")
                row = layout.row(align=True)
                for type in ["R", "L"] : 
                    row.prop(props, f"arc_{type}", text=f"Arc {type}")
            
            if self.Panel(layout, "tongue", "Tongue", "") : 
                layout.prop(props, "tongue_ik_fk", text="IK a FK")
                layout.prop(props, "tongue_stretch_to", text="Stretch To", toggle=1)
    
    def HowFace(self, layout, props):
        
        layout.label(text="Mouth")
        row = layout.row(align=True)
        for type in ["R", "L"] : 
            row.prop(props, f"corner_mouth_{type}", text=f"Normal a Cartoon {type}")
        row = layout.row(align=True)
        for type in ["R", "L"] : 
            row.prop(props, f"arc_{type}", text=f"Arc {type}")
        layout.label(text="Tongue")
        layout.prop(props, "tongue_ik_fk", text="IK a FK")
        layout.prop(props, "tongue_stretch_to", text="Stretch To", toggle=1)
    
    def Arm(self, layout, props, use_panel : bool = True):
        # Arms
        col = layout.column(align=True)
        if self.Panel(col, "arms", "Arms", "", False) :
            row = col.row(align=True)
            row.prop(props, "arm_ik_fk_R", text="FK a IK R")
            row.prop(props, "arm_ik_fk_L", text="FK a IK L")
            row = col.row(align=True)
            row.prop(props, "elbow_cartoon_R", text="Elbow Cartoon R")
            row.prop(props, "elbow_cartoon_L", text="Elbow Cartoon L")
            
            grid = col.grid_flow(
            row_major=False, columns=4, 
            even_columns=True, even_rows=False, 
            align=True
            )
            
            grid.prop(props, "arm_rot_L", text="R", icon="CON_CLAMPTO", toggle=1)
            grid.prop(props, "arm_stretch_to_L", text="R", icon="CON_STRETCHTO", toggle=1)
            grid.prop(props, "arm_rot_R", text="L", icon="CON_CLAMPTO", toggle=1)
            grid.prop(props, "arm_stretch_to_R", text="L", icon="CON_STRETCHTO", toggle=1)
            
            
            row = col.row(align=True)
            row.prop(props, "arm_followed_R", text="Followed R", toggle=1)
            row.prop(props, "arm_followed_enum_R", text="", icon="CON_FOLLOWTRACK", toggle=1, icon_only=True)
            row.prop(props, "arm_followed_L", text="Followed L", toggle=1)
            row.prop(props, "arm_followed_enum_L", text="", icon="CON_FOLLOWTRACK", toggle=1, icon_only=True)
            
            row = col.row(align=True)
            row.operator(
                "rgc.properties", 
                text="FK a IK R"if props.arm_invert_ik_fk_R else "IK a FK R", 
                icon="SNAP_ON"
                ).type = "ARMS_IKAFK_R"
            row.prop(props, "arm_invert_ik_fk_R", text="", icon="ARROW_LEFTRIGHT", toggle=1)
            row.operator(
                "rgc.properties", 
                text="FK a IK L" if props.arm_invert_ik_fk_L else "IK a FK L", 
                icon="SNAP_ON"
                ).type = "ARMS_IKAFK_L"
            row.prop(props, "arm_invert_ik_fk_L", text="", icon="ARROW_LEFTRIGHT", toggle=1)
    
    def HowArm(self, layout, props, type : str = "R",):
        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(props, f"arm_ik_fk_{type}", text=f"FK a IK {type}")
        row = col.row(align=True)
        row.prop(props, f"elbow_cartoon_{type}", text=f"Elbow Cartoon {type}")
        
        grid = col.grid_flow(
        row_major=False, columns=4, 
        even_columns=True, even_rows=False, 
        align=True
        )
        
        if type == "R" : 
            grid.prop(props, "arm_rot_L", text="R", icon="CON_CLAMPTO", toggle=1)
            grid.prop(props, "arm_stretch_to_L", text="R", icon="CON_STRETCHTO", toggle=1)
        else:
            grid.prop(props, "arm_rot_R", text="L", icon="CON_CLAMPTO", toggle=1)
            grid.prop(props, "arm_stretch_to_R", text="L", icon="CON_STRETCHTO", toggle=1)
        
        
        row = col.row(align=True)
        row.prop(props, f"arm_followed_{type}", text=f"Followed {type}", toggle=1)
        row.prop(props, f"arm_followed_enum_{type}", text="", icon="CON_FOLLOWTRACK", toggle=1, icon_only=True)

        
        row = col.row(align=True)
        row.operator(
            "rgc.properties", 
            text=f"FK a IK {type}"if props.arm_invert_ik_fk_R else f"IK a FK {type}", 
            icon="SNAP_ON"
            ).type = f"ARMS_IKAFK_{type}"
        row.prop(props, f"arm_invert_ik_fk_{type}", text="", icon="ARROW_LEFTRIGHT", toggle=1)

    
    def Fingers(self, layout, props, use_panel : bool = True):   
        
        col = layout.column(align=True) 
        if self.Panel(col, "fingers", "Fingers", "", True) :
            grid = col.grid_flow(
            row_major=False, columns=2, 
            even_columns=True, even_rows=False, 
            align=True
            )
            for type in ["R", "L"] :
                
                grid.prop(props, f"fingers_fk_a_ik_{type}", text=f"Fk a Ik {type}")
                grid.prop(props, f"fingers_stretch_to_{type}", text=f"Stratch To {type}", toggle=1, icon_only=True)
                grid_1 = grid.grid_flow(
                    row_major=False, columns=2, 
                    even_columns=False, even_rows=False, 
                    align=True
                )
                #grid_1.prop(props, f"fingers_followed_{type}", text=f"FolloWed {type}")
                grid_1.prop(props, f"fingers_enum_{type}", text=f"", icon="CON_FOLLOWTRACK", toggle=1, icon_only=False)
        
            if self.Panel(col, "by_the_finger", "By The Finger", "", True) :
                grid = col.grid_flow(
                row_major=False, columns=2, 
                even_columns=True, even_rows=False, 
                align=True
                )
                for type in ["R", "L"] :
                    for prop in self.ListFinger() :
                        clean_name = prop.replace(" ", "").lower()
                        FK_a_IK = f"{clean_name}_fk_a_ik_{type}"
                        Stretch_To = f"{clean_name}_stretch_t_{type}"
                        Rot = f"{clean_name}_rot_{type}"
                        Followed = f"{clean_name}_followed_{type}"
                        Enum = f"{clean_name}_enum_{type}"
                
                        if type == "R":
                            grid.label(text=f"{prop}")
                        else:
                            grid.label(text="")
                        grid.prop(props, FK_a_IK, text=f"FK a IK {type}")
                        col_1 = grid.column(align=True)
                        col_1.active =  True if getattr(props, FK_a_IK, None) > 0 else False 
                        col_1.prop(props, Stretch_To, text=f"Stretch To {type}", toggle=1)
                        #col_1.prop(props, Rot, text=f"Rot {type}", toggle=1)
                        grid_1 = col_1.grid_flow(
                            row_major=False, columns=2, 
                            even_columns=False, even_rows=False, 
                            align=True
                            )
                        grid_1.prop(props, Followed, text=f"Followed {type}", toggle=1)
                        grid_1.prop(props, Enum, text="", icon="CON_FOLLOWTRACK", toggle=1, icon_only=True)

    def HowFinger(self, layout, props, type : str = "R", finger = "Thumb") :
        
        col = layout

        clean_name = finger.replace(" ", "").lower()
        FK_a_IK = f"{clean_name}_fk_a_ik_{type}"
        Stretch_To = f"{clean_name}_stretch_t_{type}"
        Rot = f"{clean_name}_rot_{type}"
        Followed = f"{clean_name}_followed_{type}"
        Enum = f"{clean_name}_enum_{type}"

        col.prop(props, FK_a_IK, text=f"FK a IK {type}")
        col_1 = col.column(align=True)
        col_1.active =  True if getattr(props, FK_a_IK, None) > 0 else False 
        col_1.prop(props, Stretch_To, text=f"Stretch To {type}", toggle=1)
        #col_1.prop(props, Rot, text=f"Rot {type}", toggle=1)
        grid_1 = col_1.grid_flow(
            row_major=False, columns=2, 
            even_columns=False, even_rows=False, 
            align=True
            )
        grid_1.prop(props, Followed, text=f"Followed {type}", toggle=1)
        grid_1.prop(props, Enum, text="", icon="CON_FOLLOWTRACK", toggle=1, icon_only=True)


    def Leg(self, layout, props, use_panel : bool = True):
        col = layout.column(align=True) 
        if self.Panel(col, "legs", "Legs", "", False) :
            row = col.row(align=True)
            row.prop(props, "leg_ik_fk_R", text="FK a IK R")
            row.prop(props, "leg_ik_fk_L", text="FK a IK L")
            
            row = col.row(align=True)
            row.prop(props, "leg_elbow_cartoon_R", text="Elbow Cartoon R")
            row.prop(props, "leg_elbow_cartoon_L", text="Elbow Cartoon L")
            
            grid = col.grid_flow(
            row_major=False, columns=4, 
            even_columns=True, even_rows=False, 
            align=True
            )
            
            grid.prop(props, "leg_rot_R", text="R", icon="CON_CLAMPTO", toggle=1)
            grid.prop(props, "leg_stretch_to_R", text="R", icon="CON_STRETCHTO", toggle=1)
            grid.prop(props, "leg_rot_L", text="L", icon="CON_CLAMPTO", toggle=1)
            grid.prop(props, "leg_stretch_to_L", text="L", icon="CON_STRETCHTO", toggle=1)
            
            row = col.row(align=True)
            row.prop(props, "leg_followed_R", text="Followed R", toggle=1)
            row.prop(props, "leg_followed_enum_R", text="", icon="CON_FOLLOWTRACK", toggle=1, icon_only=True)
            row.prop(props, "leg_followed_L", text="Followed L", toggle=1)
            row.prop(props, "leg_followed_enum_L", text="", icon="CON_FOLLOWTRACK", toggle=1, icon_only=True)
            

            row = col.row(align=True)
            row.operator(
                "rgc.properties", 
                text="FK a IK R"if props.leg_invert_ik_fk_R else "IK a FK R", 
                icon="SNAP_ON"
                ).type = "LEGS_IKAFK_R"
            row.prop(props, "leg_invert_ik_fk_R", text="", icon="ARROW_LEFTRIGHT", toggle=1)
            row.operator(
                "rgc.properties", 
                text="FK a IK L" if props.leg_invert_ik_fk_L else "IK a FK L", 
                icon="SNAP_ON"
                ).type = "LEGS_IKAFK_L"
            row.prop(props, "leg_invert_ik_fk_L", text="", icon="ARROW_LEFTRIGHT", toggle=1)

    def HowLeg(self, layout, props, type : str = "R",):
        col = layout
        col.prop(props, f"leg_ik_fk_{type}", text=f"FK a IK {type}")
        col.prop(props, f"leg_elbow_cartoon_{type}", text=f"Elbow Cartoon {type}")
        row = col.row(align=True)
        row.prop(props, f"leg_rot_{type}", text=f"{type}", icon="CON_CLAMPTO", toggle=1)
        row.prop(props, f"leg_stretch_to_{type}", text=f"{type}", icon="CON_STRETCHTO", toggle=1)
        
        row = col.row(align=True)
        row.prop(props, f"leg_followed_{type}", text=f"Followed {type}", toggle=1)
        row.prop(props, f"leg_followed_enum_{type}", text="", icon="CON_FOLLOWTRACK", toggle=1, icon_only=True)
        
        row = col.row(align=True)
        row.operator(
            "rgc.properties", 
            text=f"FK a IK {type}"if props.leg_invert_ik_fk_R else f"IK a FK {type}", 
            icon="SNAP_ON"
            ).type = f"LEGS_IKAFK_{type}"
        row.prop(props, f"leg_invert_ik_fk_{type}", text="", icon="ARROW_LEFTRIGHT", toggle=1)

    
class RGC_Panel_Proterties_RigCreator(ID, GN_RigCreatorViewPort, Draw_Properties_To_RigCreator, bpy.types.Panel):
    bl_idname = "RGC_Panel_Proterties_RigCreator"
    bl_label = "Properties RigCreator"

    @classmethod
    def poll(cls, context):        
        Self = GeneralArmatureData()
        return Self.GetArmature()
        
    def draw(self, context):
        layout = self.layout
        props = self.PropsToArmature()
        if not props : 
            layout.operator("rgc.properties", text="Add Properties").type = "ADD"
            return
        props = props[0]
        
        col = layout.column(align=True)
        self.GlobalLocal(col, props)
        self.Face(col, props)
        self.Arm(col, props)
        self.Fingers(col, props)
        self.Leg(col, props)
        
class RGC_Panel_Call_Proterties_RigCreator(GeneralArmatureData, Draw_Properties_To_RigCreator, bpy.types.Panel):
    bl_idname = "RGC_Panel_Call_Proterties_RigCreator"
    bl_label = "Properties RigCreator"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Item"
    

    
    @classmethod
    def poll(cls, context):        
        Self = GeneralArmatureData()
        return Self.GetArmature() and Self.GetObjMode() == "POSE"
        
    def draw(self, context):
        layout = self.layout
        props = self.PropsToArmature()
        if not props : 
            layout.operator("rgc.properties", text="Add Properties").type = "ADD"
            return
        props = props[0]
        
        col = layout.column(align=True)
        
        ABN = self.GetActiveBone().name
        
        if ABN in {"head", "eyes", "eye_L", "eye_R"}:
            col.label(text="Global Local")
            self.GlobalLocal(col, props, use_panel=False)
            
        if ABN in {"mouth", "mouth_UP", "mouth_DOWN", "mouth_DOWN", "mouth_L", "mouth_R"}:
            col.label(text="Face")
            self.HowFace(col, props)
  
        for type in ["R", "L"]:
            
            if ABN in {f"ik_leg_{type}", f"ik_leg_{type}.001", f"poleleg_{type}"} : 
                col.label(text="Leg")
                self.HowLeg(col, props, type)
                
            elif ABN in {f"ik_arm_{type}.001", f"ik_arm_{type}.003", f"polearm_{type}"} : 
                col.label(text="Arm")
                self.HowArm(col, props, type)
                
            for finger in self.ListFinger():
                clean_name = finger.replace(" ", "_").lower()
                if ABN == f"ik_{clean_name}_{type}.004" : 
                    col.label(text=f"{finger}_{type}")
                    self.HowFinger(col, props, type, finger)
        

         
class RGC_Panel_Properties_Armature(ID, GN_RigCreatorViewPort, bpy.types.Panel):
    bl_idname = "RGC_Panel_Properties_Armature"
    bl_label = "Properties Armature"
    bl_options = {"DEFAULT_CLOSED"}
    
    
    @classmethod
    def poll(cls, context):        
        Self = GeneralArmatureData()
        return Self.GetArmature()
    
    def draw(self, context):
        layout = self.layout
        props = self.Props()
        
        
        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(props, "search_armature", text="", icon="VIEWZOOM")
        if self.Panel(col, "edit", "Edit", "GREASEPENCIL", True) : 
            row = col.row(align=True)
            row.prop(props, "armature_column", text="Columns",)
            row = col.row(align=True)
            row.prop(props, "armature_use_specific_name", text="", icon="KEY_HLT", toggle=1)
            row.scale_x = 1.8
            row.prop(props, "armature_key", text="")
        
        grid_1 = layout.grid_flow(
            row_major=False, columns=props.armature_column, 
            even_columns=True, even_rows=False, 
            align=True
            )
        
        if not self.GetArmature() : return
        
        for prop_name, prop_value in self.GetPropertiesToObject(self.GetArmature(), filter={}, filter_base={"active_constraint"}, type="items"):
            if not self.SearchInList(props.search_armature, prop_name) : continue
            if props.armature_use_specific_name : 
                prop_name : str = prop_name
                text = prop_name.replace(props.armature_key, "")
                if props.armature_key.lower() in prop_name.lower() :
                    if isinstance(prop_value, bool):
                        grid_1.prop(self.GetArmature(), f'["{prop_name}"]', text=text, toggle=1)
                    else : 
                        grid_1.prop(self.GetArmature(), f'["{prop_name}"]', text=text)
            else :
                if isinstance(prop_value, bool):
                    grid_1.prop(self.GetArmature(), f'["{prop_name}"]', text=f"{prop_name}", toggle=1)
                else : 
                    grid_1.prop(self.GetArmature(), f'["{prop_name}"]', text=f"{prop_name}")

class RGC_Panel_Properties_Bones(ID, GN_RigCreatorViewPort, bpy.types.Panel):
    bl_idname = "RGC_Panel_Properties_Bones"
    bl_label = "Properties Bones"
    bl_options = {"DEFAULT_CLOSED"}

    
    @classmethod
    def poll(cls, context):        
        Self = GeneralArmatureData()
        return Self.GetArmature() and Self.GetObjMode() == "POSE"
    
    def draw(self, context):
        layout = self.layout
        props = self.Props()
        
        
        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(props, "search_bone", text="", icon="VIEWZOOM")
        
        if self.Panel(col, "edit", "Edit", "GREASEPENCIL", True) : 
            row = col.row(align=True)
            #row.prop(props, "bone_column", text="Columns",)
            row.prop(props, "bone_subcolumn", text="SudColumns",)
            row = col.row(align=True)
            row.prop(props, "bone_use_specific_name", text="", icon="KEY_HLT", toggle=1)
            row.scale_x = 1.8
            row.prop(props, "bone_key", text="")
        
        
        grid_1 = layout.grid_flow(
            row_major=False, columns=props.bone_column, 
            even_columns=True, even_rows=False, 
            align=True
            )

        for bone in self.GetActiveObject().pose.bones : 
            if not self.SearchInList(props.search_bone, bone.name) : continue
            
            if not bone.keys() : continue
            if len(bone.keys()) == 1:
                if "active_constraint" in bone.keys() or "Bone_Constraint_list_index" in bone.keys(): 
                    continue
            
            
            
            def is_have() -> bool:
                for prop_name, prop_value in self.GetPropertiesToObject(bone, filter={}, type="items"):
                    if props.bone_use_specific_name : 
                        if props.bone_key.lower() in prop_name.lower():
                            return True
                return False
            
            if props.bone_use_specific_name :
                if is_have() : 
                    box = grid_1.box()
                    col = box.column(align=True)
                    if not self.Panel(col, bone.name.lower(), bone.name, "", False) : continue
                    
                    grid_2 = col.grid_flow(
                            row_major=False, columns=props.bone_subcolumn, 
                            even_columns=True, even_rows=False, 
                            align=True
                            )
                    
                    for prop_name, prop_value in self.GetPropertiesToObject(bone, filter={}, filter_base={"active_constraint", "Bone_Constraint_list_index"}, type="items"):
                        prop_name : str = prop_name
                        text = prop_name.replace(props.bone_key, "")
                        if props.bone_use_specific_name : 
                            if props.bone_key.lower() in prop_name.lower() :
                                if isinstance(prop_value, bool):
                                    grid_2.prop(bone, f'["{prop_name}"]', text=text, toggle=1)
                                else :
                                    grid_2.prop(bone, f'["{prop_name}"]', text=text)
                    
            else:
                
                box = grid_1.box()
                col = box.column(align=True)
                if not self.Panel(col, bone.name.lower(), bone.name, "", False) : continue
                    
                
                grid_2 = col.grid_flow(
                        row_major=False, columns=props.bone_subcolumn, 
                        even_columns=True, even_rows=False, 
                        align=True
                        )
                for prop_name, prop_value in self.GetPropertiesToObject(bone, filter={}, filter_base={"active_constraint", "Bone_Constraint_list_index"}, type="items"):
                    if isinstance(prop_value, bool):
                        grid_2.prop(bone, f'["{prop_name}"]', text=prop_name,toggle=1)
                    else :
                        grid_2.prop(bone, f'["{prop_name}"]', text=prop_name)


# Old Properties
class RGC_Panel_OldProperties(ID, GN_RigCreatorViewPort,bpy.types.Panel):
    bl_idname = "Panel_rig_creator_props"
    bl_label = " Old Properties Rig Creator"
    bl_order = 1
    
    @classmethod
    def poll(cls, context):
        # Verificar si el objeto seleccionado es una armadura
        data = GeneralArmatureData()
        return data.GetActiveObject() and data.Props().use_old_prop
    
    def draw(self, context):
        layout = self.layout
        obj = context.active_object
        if obj and obj.type == 'ARMATURE':
            armature = obj.data

            Scale_x = 1
            Scale_y = 1.5

            prop = {
                'Cabeza_Global_Local': "Cabeza_Global_Local",
                'Ojos_Global_Local': "Ojos_Global_Local",
                'Brazo_IK_FK_L': "Brazo_IK_FK_L",
                'Brazo_IK_FK_R': "Brazo_IK_FK_R",
                'Brazo_IK_Stretch_L': "Brazo_IK_Stretch_L",
                'Brazo_IK_Stretch_R': "Brazo_IK_Stretch_R",
                'Brazo_Rot_Mov_L': "Brazo_Rot_Mov_L",
                'Brazo_Rot_Mov_R': "Brazo_Rot_Mov_R",
                'Global_Local_Brazo_L': "Global_Local_Brazo_L",
                'Global_Local_Brazo_R': "Global_Local_Brazo_R",
                'Pierna_IK_Fk_L': "Pierna_IK_Fk_L",
                'Pierna_IK_Fk_R': "Pierna_IK_Fk_R",
                'Pierna_IK_Stretch_L': "Pierna_IK_Stretch_L",
                'Pierna_IK_Stretch_R': "Pierna_IK_Stretch_R",
                'Pierna_Rot_Mov_L': "Pierna_Rot_Mov_L",
                'Pierna_Rot_Mov_R': "Pierna_Rot_Mov_R",
            }

            # Define un diccionario para almacenar los valores de las propiedades
            prop_valor = {}

            # Verifica si cada propiedad existe y agrega su valor al diccionario si es así
            for nombre, propiedad in prop.items():
                if propiedad in armature:
                    prop_valor[nombre] = armature[propiedad]

            def Column(row, prop_A, text_A, use_facto = False,): 
                for p in range(len(prop_A)):
                    if prop_A[p]:
                        if prop_A[p] in armature:
                            row.prop(armature, f'["{prop_A[p]}"]', text=text_A[p], slider = use_facto)
                
            def existe(prop):
                if prop:
                    if prop in armature:
                        return prop
                    else:
                        return None
                else:
                    return None    
            row = layout.row(align=False, translate=False)
            
            if existe(prop['Cabeza_Global_Local']):
                row.label(text = "Cabeza")
            if existe(prop['Ojos_Global_Local']):
                row.label(text = "Ojos")

            row = layout.row(align=False, translate=False)
            row.scale_x = Scale_x
            row.scale_y = Scale_y

            #cabeza Properties
            Column(
                row, 
                prop_A = [
                    existe(prop['Cabeza_Global_Local']),
                    existe(prop['Ojos_Global_Local']),
                ], 
                text_A = [
                    "GLobal Local",
                    "GLobal Local",    
                ],
                use_facto = True,
                   )
            
            
            def Ik_Fk(row, 
                      properties_a = [], label_a = "", Text_a = [], use_Factor_a = [],
                      properties_b = [], label_b = "", Text_b = [], use_Factor_b = [],
                      use_columns = False,
                      ):

                col_B = row.column(align=True)
                col_A = row.column(align=True)
                
                if use_columns == False:
                    existe=None
                    for i in properties_a:
                        existe=i
                    if existe != None:
                        col_A.label(text = label_a)

                    for i in range(len(properties_a)):
                        if properties_a[i]:
                            if properties_a[i] in armature:  
                                col_A.prop(armature, f'["{properties_a[i]}"]', text=Text_a[i], slider = use_Factor_a[i], toggle = use_Factor_a[i])
                else:
                    
                    existe=None
                    
                    for i in properties_a:
                        existe=i
                        
                    if existe != None:
                        col_A.label(text = label_a)
                        
                    for i in properties_b:
                      existe=i  
                      
                    if existe != None:
                        col_B.label(text = label_b)

                    for i in range(len(properties_a)):
                        if properties_a[i]:
                            if properties_a[i] in armature:  
                                col_A.prop(armature, f'["{properties_a[i]}"]', text=Text_a[i], slider = use_Factor_a[i], toggle = use_Factor_a[i])

                    for i in range(len(properties_b)):
                        if properties_a[i]:
                            if properties_b[i] in armature:  
                                col_B.prop(armature, f'["{properties_b[i]}"]', text=Text_b[i], slider = use_Factor_b[i], toggle = use_Factor_b[i])



            row = layout.row(align=False, translate=False)
            row.scale_x = Scale_x
            row.scale_y = Scale_y / 1.5

            Ik_Fk(row, 
                  
                #L
                  properties_a = [
                    existe(prop["Brazo_IK_FK_L"]), 
                    existe(prop["Brazo_IK_Stretch_L"]), 
                    existe(prop["Brazo_Rot_Mov_L"]),
                    ], 
                  label_a = "Brazo L", 
                  Text_a = [
                      "IK FK", "Streth", "Rot Mov"
                      ], 
                  use_Factor_a = [
                      True, True, True
                      ],

                #R
                  properties_b = [
                    existe(prop["Brazo_IK_FK_R"]), 
                    existe(prop["Brazo_IK_Stretch_R"]), 
                    existe(prop["Brazo_Rot_Mov_R"]),
                    ], 
                  label_b = "Brazo R", 
                  Text_b = [
                      "IK FK", "Streth", "Rot Mov"
                      ], 
                  use_Factor_b = [
                      True, True, True
                      ],

                use_columns = True

                  )
            
            
            #Menu de cambio de follow 
            if prop_valor.get("Global_Local_Brazo_L") is not None and prop_valor.get("Global_Local_Brazo_R") is not None:
                if isinstance(prop_valor["Global_Local_Brazo_L"], int) and isinstance(prop_valor["Global_Local_Brazo_R"], int):
                    row = layout.row(align=False, translate=False)
                    row_a = row.row(align=True, translate=False)
                    row_b = row.row(align=True, translate=False)
                    row.scale_x = Scale_x
                    row.scale_y = Scale_y / 1.5
                    
                    if "Global_Local_Brazo_R" in armature:
                        row_a.prop(armature, f'["{prop["Global_Local_Brazo_R"]}"]', text="Follow", slider = False)
                        #row_a.menu(Enum_Follow_R.bl_idname,text='', icon='CON_FOLLOWPATH')
                        #row_a.prop_menu_enum(obj, "follow_emun_R", text="", icon = 'CON_FOLLOWPATH')
                    if "Global_Local_Brazo_L" in armature:
                        row_b.prop(armature, f'["{prop["Global_Local_Brazo_L"]}"]', text="Follow", slider = False)
                        #row_b.menu(Enum_Follow_L.bl_idname,text='', icon='CON_FOLLOWPATH')
                        #row_b.prop_menu_enum(obj, "follow_emun_L", text="", icon = 'CON_FOLLOWPATH')
    
                    
                else:
                    row = layout.row(align=False, translate=False)
                    row.scale_x = Scale_x
                    row.scale_y = Scale_y / 1.5
                    if "Global_Local_Brazo_R" in armature:
                        row.prop(armature, f'["{prop["Global_Local_Brazo_R"]}"]', text="GLobal Local", slider = True)
                    if "Global_Local_Brazo_L" in armature:
                        row.prop(armature, f'["{prop["Global_Local_Brazo_L"]}"]', text="GLobal Local", slider = True)
            
            
            row = layout.row(align=False, translate=False)
            row.scale_x = Scale_x
            row.scale_y = Scale_y / 1.5
            
            def Bono_existe(IK_exite):
                for Bone in armature.bones:
                    if Bone.name in IK_exite:
                        return True
                    
                return False
            
            
            
            
            
            #IK_exite = [
            #"Control_FK_Brazo_R.001",
            #"Control_FK_Brazo_R.002",
            #"Control_FK_Brazo_R.003", 
            #]
            #if Bono_existe(IK_exite):
            #    row_ = row.row(align=True)
            #    row_.operator("gen.oper_h", text = "FK->IK", 
            #                 emboss=True, icon='SNAP_ON').type = "IMAN_BRAZO_R"
            #    row_1 = row_.row(align=True)
            #    row_1.enabled = armature["Brazo_Rot_Mov_R"]
            #    new = row_1.operator("gen.oper_h", text = "IK->FK", 
            #                     emboss=True, icon='SNAP_ON')
            #    new.type = "IK_IMAN_BRAZO_R"
            #    
            #IK_exite = [
            #"Control_FK_Brazo_L.001",
            #"Control_FK_Brazo_L.002",
            #"Control_FK_Brazo_L.003", 
            #]
            #if Bono_existe(IK_exite):
            #    row_ = row.row(align=True)
            #    row_.operator("gen.oper_h", text = "FK->IK", 
            #                 emboss=True, icon='SNAP_ON').type = "IMAN_BRAZO_L"
            #    row_1 = row_.row(align=True)
            #    row_1.enabled = armature["Brazo_Rot_Mov_L"]
            #    new = row_1.operator("gen.oper_h", text = "IK->FK", 
            #                     emboss=True, icon='SNAP_ON')
            #    new.type = "IK_IMAN_BRAZO_L"
                
                          
            row = layout.row(align=False, translate=False)
            row.scale_x = Scale_x
            row.scale_y = Scale_y / 1.5

            Ik_Fk(row, 
                  
                #L
                  properties_a = [
                    existe(prop["Pierna_IK_Fk_L"]), 
                    existe(prop["Pierna_IK_Stretch_L"]), 
                    existe(prop["Pierna_Rot_Mov_L"]),
                    ], 
                  label_a = "Pierna L", 
                  Text_a = [
                      "IK FK", "Streth", "Rot Mov"
                      ], 
                  use_Factor_a = [
                      True, True, True
                      ],

                #R
                  properties_b = [
                    existe(prop["Pierna_IK_Fk_R"]), 
                    existe(prop["Pierna_IK_Stretch_R"]), 
                    existe(prop["Pierna_Rot_Mov_R"]),
                    ], 
                  label_b = "Pierna R", 
                  Text_b = [
                      "IK FK", "Streth", "Rot Mov"
                      ], 
                  use_Factor_b = [
                      True, True, True
                      ],

                use_columns = True

                  )
            
            #row = layout.row(align=False, translate=False)
            #row.scale_x = Scale_x
            #row.scale_y = Scale_y / 1.5
            #
            #IK_exite = [
            #"FK_Pierna_R.001",
            #"FK_Pierna_R.002",
            #"FK_Pierna_R.003", 
            #"FK_Pierna_R.004", 
            #]
            #if Bono_existe(IK_exite):
            #    row_ = row.row(align=True)
            #    row_.operator("gen.oper_h", text = "FK->IK", 
            #                 emboss=True, icon='SNAP_ON').type = "IMAN_PIERNA_R"
            #    row_1 = row_.row(align=True)
            #    row_1.enabled =armature["Pierna_Rot_Mov_R"]
            #    new = row_1.operator("gen.oper_h", text = "IK->FK", 
            #                     emboss=True, icon='SNAP_ON')
            #    new.type = "IK_IMAN_PIERNA_R"
            #    
            #IK_exite = [
            #"FK_Pierna_L.001",
            #"FK_Pierna_L.002",
            #"FK_Pierna_L.003", 
            #"FK_Pierna_L.004", 
            #]
            #if Bono_existe(IK_exite):
            #    row_ = row.row(align=True)
            #    row_.operator("gen.oper_h", text = "FK->IK", 
            #                 emboss=True, icon='SNAP_ON').type = "IMAN_PIERNA_L"
            #    row_1 = row_.row(align=True)
            #    row_1.enabled = armature["Pierna_Rot_Mov_L"]
            #    new = row_1.operator("gen.oper_h", text = "IK->FK", 
            #                     emboss=True, icon='SNAP_ON')
            #    new.type = "IK_IMAN_PIERNA_L"
                
   
        