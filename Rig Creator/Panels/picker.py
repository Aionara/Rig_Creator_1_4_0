
import bpy
from .general import *
from ..generaldata import GeneralArmatureData

def RGC_Piker(self, context) : 
    layout = self.layout
    layout.operator("rgc.piker", text="", icon="ARMATURE_DATA")

class RGC_Panel_Picker(GeneralArmatureData, bpy.types.Panel):
    bl_idname = "RGC_Panel_Picker"
    bl_label = "Picker"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "DATA"
    
    
    @classmethod
    def poll(cls, context):  
        Self = GeneralArmatureData()
        return Self.GetArmature() and Self.GetObjMode() == 'POSE'
    
    
    def Button(self, layout, type: str, name: str = "", size: tuple = (1, 1), aligment: str = "CENTER"):
        
        if self.GetBone(type, mode="POSE") is None:
            return
        row = layout.row(align=True)
        row.alignment = aligment
        row.scale_x = size[0]
        row.scale_y = size[1]

        row.operator(
            "rgc.piker",
            text=name,
            depress=self.GetBone(type, mode="POSE").bone.select,
        ).type = type
    
    def Fingers(self, layout, finger:str = "thumb", type: str = "R") :
        props = self.Props()
        layout = layout.grid_flow(row_major=True, columns=1, even_columns=True,align=False)
        
        name = finger.replace(" ", "_")
        
        if props.piker == {"GENERAL"} :
            self.Button(layout, f"root_{name.lower()}_{type}", f"", (1, 1))
            self.Button(layout, f"rot_{name.lower()}_{type}", f"", (1, 1.5))
        elif props.piker == {"DEF"} :
            for i in range(4):
                self.Button(layout, f"cont_{name.lower()}_{type}.00{i+2}", "", (1, 1))
        elif props.piker == {"FK"} :
            for i in range(3):
                self.Button(layout, f"fk_{name.lower()}_{type}.00{i+1}", "", (1, 1))
        elif props.piker == {"IK"} :
            self.Button(layout, f"ik_{name.lower()}_{type}.004", f"", (1, 1))   
             
    def Arm(self, layout, type:str = "L") : 
        props = self.Props()
        layout = layout.grid_flow(row_major=True, columns=1, even_columns=True,align=False)
        
        if props.piker == {"GENERAL"} :
            self.Button(layout, f"root_arm_{type}", f"Arm 1 {type}", (0.8, 3))
            self.Button(layout, f"cont_subarm_{type}.002", f"Arm 2 {type}", (0.8, 3))
            self.Button(layout, f"cont_subarm_{type}.003", f"Arm 3 {type}", (0.8, 3))
        
        elif props.piker == {"DEF"} :
            self.Button(layout, f"cont_arm_UP_{type}.002", f"Def 1 {type}", (1, 3))
            self.Button(layout, f"cont_arm_DOWN_{type}.002", f"Def 2 {type}", (1, 3))
            self.Button(layout, f"cont_hand_{type}.002", f"Def 3 {type}", (1, 3))
        elif props.piker == {"FK"} :
            for i in range(3) :
                self.Button(layout, f"fk_arm_{type}.00{i+1}", f"Fk {i+1} {type}", (1, 3))
        elif props.piker == {"IK"} :
            self.Button(layout, f"ik_arm_{type}.001", f"Ik 1 {type}", (1, 5))
            self.Button(layout, f"polearm_{type}", f"Ik 2 {type}", (1, 2))
            self.Button(layout, f"ik_arm_{type}.003", f"Ik 3 {type}", (1, 3))
            
        row = layout.row(align=True)
        for f in self.ListFinger() if type == "L" else reversed(self.ListFinger()) :
            self.Fingers(row, f, type)
    
    def Leg(self, layout, type : str = "L"): 
        
        props = self.Props()
        layout = layout.grid_flow(row_major=True, columns=1, even_columns=True,align=False)
        
        if props.piker == {"GENERAL"} :
            self.Button(layout, f"root_leg_{type}", f"Leg 1 {type}", (1.2, 2.5))
            self.Button(layout, f"cont_subleg_{type}.002", f"Leg 2 {type}", (1.2, 1))
            self.Button(layout, f"cont_subleg_{type}.003", f"Leg 3 {type}", (1.2, 1))
            self.Button(layout, f"rot_feet_{type}", f"Leg 4 {type}", (1.2, 1))
        
        elif props.piker == {"DEF"} :
            self.Button(layout, f"cont_leg_UP_{type}.002", f"Def 1 {type}", (1.2, 2))
            self.Button(layout, f"cont_leg_DOWN_{type}.002", f"Def 2 {type}", (1.2, 2))
            self.Button(layout, f"cont_feet_{type}.002", f"Def 3 {type}", (1.2, 1))
            self.Button(layout, f"cont_feet_{type}.003", f"Def 4 {type}", (1.2, 1))
            
        elif props.piker == {"FK"} :
            for i in range(4) : 
                self.Button(layout, f"fk_leg_{type}.00{i+1}", f"Fk {i+1} {type}", (1.2, 2))
        
        elif props.piker == {"IK"} :
            self.Button(layout, f"ik_leg_{type}.001", f"Ik 1 {type}", (1.2, 4))
            self.Button(layout, f"poleleg_{type}", f"Ik 2 {type}", (1.2, 2))
            row = layout.row(align=True)
            if type == "R" :
                self.Button(row, f"rot_ik_leg_{type}", f"", (1, 3))
            self.Button(row, f"ik_leg_{type}", f"Ik 4 {type}", (1.2, 3))
            if type == "L" :
                self.Button(row, f"rot_ik_leg_{type}", f"", (1, 3))
            
    def Head(self, layout) :
        props = self.Props()
        layout = layout.grid_flow(row_major=True, columns=1, even_columns=True,align=False)
        row = layout.row(align=True)
        row.alignment = 'CENTER'
        self.Button(row, "eye_R", "R", (0.9, 1))
        self.Button(row, "eyes", "Eyes", (0.95, 1))
        self.Button(row, "eye_L", "L", (0.9, 1))
        if props.piker == {"GENERAL"} or props.piker == {"IK"}:
            row = layout.row(align=True)
            row.alignment = 'CENTER'
            
            self.Button(row, "head", "Head", (1.5, 4))
            if props.piker == {"IK"} :
                self.Button(layout, "ik_tongue.004", "Ik Tongue", (1.2, 1))
            

            self.Button(layout, "jaw", " Jaw ", (1.5, 1))
            
        elif props.piker == {"DEF"} :
            self.Button(layout, "head", "Head", (1.5, 1))
            def DefFace(layout, type : str = "R") :
                grip = layout.grid_flow(row_major=True, columns=1, even_columns=True,align=False)
                row = grip.row(align=True)
                row.alignment = 'CENTER'
                if type == "R" :
                    self.Button(row, f"cont_cheekbone_DOWN_{type}.004", f"", (1, 1))
                    self.Button(row, f"cont_eyebrows_{type}.002", f"", (1, 1))
                    self.Button(row, f"cont_eyebrows_{type}.003", f"", (1, 1))
                    self.Button(row, f"cont_eyebrows_{type}.004", f"", (1, 1))
                if type == "L" :
                    self.Button(row, f"cont_eyebrows_{type}.004", f"", (1, 1))
                    self.Button(row, f"cont_eyebrows_{type}.003", f"", (1, 1))
                    self.Button(row, f"cont_eyebrows_{type}.002", f"", (1, 1)) 
                    self.Button(row, f"cont_cheekbone_DOWN_{type}.004", f"", (1, 1))
                    
                list = [1, 2, 3, 4, 5]
                row = grip.row(align=True)
                row.alignment = 'CENTER'
                for i in list if type == "R" else reversed(list) :
                    self.Button(row, f"cont_subeyelids_UP_{type}.00{i}", f"", (1,1))
                    
                list = [2, 3, 4]
                row = grip.row(align=True)
                row.alignment = 'CENTER'
                for i in list if type == "R" else reversed(list) :
                    self.Button(row, f"cont_eyelids_UP_{type}.00{i}", f"", (1, 0.8))

                
                row = grip.row(align=True)
                row.alignment = 'CENTER'
                
                if type == "R" :
                    self.Button(row, f"cont_subeye_{type}.00{1}", f"", (1, 2))
                    self.Button(row, f"cont_eye_{type}", f"Eye", (1, 2))
                    self.Button(row, f"cont_subeye_{type}.00{2}", f"", (1, 2))
                    
                else :
                    self.Button(row, f"cont_subeye_{type}.00{2}", f"", (1, 2))
                    self.Button(row, f"cont_eye_{type}", f"Eye", (1, 2))
                    self.Button(row, f"cont_subeye_{type}.00{1}", f"", (1, 2))
                
                list = [2, 3, 4]
                row = grip.row(align=True)
                row.alignment = 'CENTER'
                for i in list if type == "L" else reversed(list) :
                    self.Button(row, f"cont_eyelids_DOWN_{type}.00{i}", f"", (1, 0.8))

                list = [2, 3, 4]
                row = grip.row(align=True)
                row.alignment = 'CENTER'
                for i in list if type == "R" else reversed(list) :
                    self.Button(row, f"cont_cheekbone_UP_{type}.00{i}", f"", (1,0.8))

                row = grip.row(align=True)
                row.alignment = 'RIGHT' if type == "R" else 'LEFT'
                self.Button(row, f"cont_nose_{type}.002", f"", (1,1))

                for dir in ["UP", "DOWN"] :
                    row = grip.row(align=True)
                    row.alignment = 'RIGHT' if type == "R" else 'LEFT'
                    list = [1, 2, 3]
                    for i in list if type == "L" else reversed(list) :
                        self.Button(row, f"cont_submouth_{dir}_{type}.00{i}", f"", (1,1))
                
                row = grip.row(align=True)
                row.alignment = 'RIGHT' if type == "R" else 'LEFT'
                if type == "L" :
                    self.Button(row, f"cont_nose_{type}.003", f"", (1,1))
                    self.Button(row, f"cont_cheekbone_DOWN_{type}.003", f"", (1,1))
                else:
                    self.Button(row, f"cont_cheekbone_DOWN_{type}.003", f"", (1,1))
                    self.Button(row, f"cont_nose_{type}.003", f"", (1,1))
                
                list = [1, 2, 3, 4]
                row = grip.row(align=True)
                row.alignment = 'CENTER'
                for i in list if type == "R" else reversed(list) :
                    self.Button(row, f"cont_jaw_{type}.00{i}", f"", (1,0.8))
                
                
            def DefEar(layout, type : str = "R") :
                grip = layout.grid_flow(row_major=True, columns=1, even_columns=True,align=True)
                list = [2, 3, 4, 5, 6]
                for i in list if type == "R" else reversed(list) :
                    self.Button(grip, f"cont_ear_{type}.00{i}", f"", (1, 1))
                
            
            row = layout.row(align=True)
            row.alignment = 'CENTER'
            DefEar(row, "R")
            DefFace(row, "R")
            grip = row.grid_flow(row_major=True, columns=1, even_columns=True,align=True)
            for i in range(5) :
                self.Button(grip, f"cont_medface_UP.00{i+1}", "     " if i != 4 else "Nose", (1.2, 1.5))
                
            self.Button(grip, f"cont_submouth_UP", "Mauth", (1.2, 1))
            
            self.Button(grip, f"cont_submouth_DOWN", "Mauth", (1.2, 1))
            
            for i in [3,2,1]:
                self.Button(grip, f"cont_medface_DOWN.00{i}", "     " if i != 2 else "Jaw", (1.2, 1))
            DefFace(row, "L")
            DefEar(row, "L")
            
            def DefTooth(layout, type : str = "R") :
                grip = layout.grid_flow(row_major=True, columns=1, even_columns=True,align=True)
                for dir in ["UP", "DOWN"] :
                    row = grip.row(align=True)
                    row.alignment = 'RIGHT' if type == "R" else 'LEFT'
                    list = [2, 3, 4]
                    for i in list if type == "L" else reversed(list) :
                        self.Button(row, f"cont_tooth_{dir}_{type}.00{i}", f"", (1,1))
            
            
            row = layout.row(align=False)
            row.alignment = 'CENTER'
            DefTooth(row, "R")
            grip = row.grid_flow(row_major=True, columns=1, even_columns=True,align=True)
            self.Button(grip, f"cont_tooth_UP", " Tooth UP ", (1.3, 1))
            self.Button(grip, f"cont_tooth_DOWN", "Tooth DOWN", (1.2, 1))
            DefTooth(row, "L")
        
        elif props.piker == {"FK"} :
            
            grow = layout.row(align=False)
            grow.alignment = 'EXPAND'
            grip = grow.grid_flow(row_major=True, columns=1, even_columns=True,align=False)
            self.Button(grip, "tooth_UP", "Tooth UP", (1, 1))
            self.Button(grip, "tooth_DOWN", "Tooth DOWN", (0.8, 1))
            
            grip_ = grow.grid_flow(row_major=True, columns=1, even_columns=True,align=False)
            row = grip_.row(align=True)
            row.alignment = 'CENTER'
            grip = row.grid_flow(row_major=True, columns=1, even_columns=True,align=False)
            self.Button(grip, "cont_ear_R", " ", (1.2, 0.8))
            self.Button(grip, "ear_R", "ear R", (0.8, 1.5))
            self.Button(row, "head", "Head", (1.5, 2.5))
            grip = row.grid_flow(row_major=True, columns=1, even_columns=True,align=False)
            self.Button(grip, "cont_ear_L", " ", (1.2, 0.8))
            self.Button(grip, "ear_L", "ear L", (0.8, 1.5))
            
            row = grip_.row(align=True)
            row.alignment = 'CENTER'
            self.Button(row, "mov_eyebrows_R", "R", (0.9, 1))
            self.Button(row, "eyebrows", "Eyebrows", (0.95, 1))
            self.Button(row, "mov_eyebrows_L", "L", (0.9, 1))
            
            def Eye(layout, type : str = "R") :
                grip = layout.grid_flow(row_major=True, columns=1, even_columns=True,align=False)
                self.Button(grip, f"mov_subeyelids_UP_{type}", f"       ", (1, 1))
                self.Button(grip, f"mov_eyelids_UP_{type}", f"Eyelids UP ", (1, 1))
                self.Button(grip, f"mov_eyelids_DOWN_{type}", f"Eyelids DOWN", (1, 1))
            
            row = grip_.row(align=True)
            row.alignment = 'CENTER'
            Eye(row, "R")
            grip = row.grid_flow(row_major=True, columns=1, even_columns=True,align=False)
            self.Button(grip, "cont_subnose_R", "", (1, 0.8))
            self.Button(grip, "cont_nose_R", "R", (0.8, 2.5))
            self.Button(row, "nose", "Nose", (1, 3.5))
            grip = row.grid_flow(row_major=True, columns=1, even_columns=True,align=False)
            self.Button(grip, "cont_subnose_L", "", (1, 0.8))
            self.Button(grip, "cont_nose_L", "L", (0.8, 2.5))
            Eye(row, "L")
            
            row = grip_.row(align=False)
            row.alignment = 'CENTER'
            self.Button(row, "mouth_R", "R", (1.2, 4.4 / 2))
            grip = row.grid_flow(row_major=True, columns=1, even_columns=True,align=False)
            row_ = grip.row(align=True)
            row_.alignment = 'CENTER'
            self.Button(row_, "submouth_UP", "", (1.2, 1.2 / 2))
            self.Button(row_, "mouth_UP", "  ", (1.2, 1.2 / 2))
            self.Button(grip, "mouth", "Mouth", (1.2, 2 / 2))
            row_ = grip.row(align=True)
            row_.alignment = 'CENTER'
            self.Button(row_, "submouth_DOWN", "", (1.2, 1.2 / 2))
            self.Button(row_, "mouth_DOWN", "  ", (1.2, 1.2 / 2))
            self.Button(row, "mouth_L", "L", (1.2, 4.4 / 2))
            

            grip = grow.grid_flow(row_major=True, columns=1, even_columns=True,align=False)
            self.Button(grip, "root_tongue", "Root Tongue", (1, 1))
            for i in range(3) :
                self.Button(grip, f"fk_tongue.00{i+1}", f"FK {i+1}", (1, 1))
            self.Button(grip, "rotfk_tongue", "Tongue", (1, 1))
            
            
            
        self.Button(layout, "neck", "Neck", (1.2, 1))
        
    
    def Torzo(self, layout) : 
        props = self.Props()
        layout = layout.grid_flow(row_major=True, columns=1, even_columns=True,align=False)
        row = layout.row(align=True)
        row.alignment = 'CENTER'

        if props.piker == {"GENERAL"} or props.piker == {"IK"}:
            
            scale_y = 5.9 if props.piker == {"GENERAL"} else 5.5
            
            self.Button(row, "shoulder_R", "R", (1,scale_y))
            self.Button(row, "shoulders", "Shoulders", (1.5,scale_y))
            self.Button(row, "shoulder_L", "L", (1,scale_y))
            self.Button(layout, "hips", "     Hips     ", (1.5,scale_y))
        
        if props.piker == {"FK"} :
            row = layout.row(align=True)
            row.alignment = 'CENTER'
            self.Button(row, "rot_spine_UP.002", "Spine UP 2", (1.5, 2))
            row = layout.row(align=True)
            row.alignment = 'CENTER'
            self.Button(row, "rot_spine_UP.001", "Spine UP 1", (1.5, 4))
            row = layout.row(align=True)
            row.alignment = 'CENTER'
            self.Button(row, "rot_spine_DOWN.001", "Spine DOWN 1", (1.5, 4))
            row = layout.row(align=True)
            row.alignment = 'CENTER'
            self.Button(row, "rot_spine_DOWN.002", "Spine DOWN 2", (1.5, 2))
        
        if props.piker == {"DEF"} :
            self.Button(layout, "cont_spine.006", "Spine 6", (1.5,2.2))
            row = layout.row(align=True)
            row.alignment = 'CENTER'
            self.Button(row, "cont_shoulder_R.001", "L", (1.5,2.2))
            self.Button(row, "cont_shoulder_L.001", "R", (1.5,2.2))
            
            self.Button(layout, "cont_spine.004", "Spine 4", (1.5,2.2))
            self.Button(layout, "cont_spine.003", "Spine 3", (1.5,2.2))
            
            row = layout.row(align=True)
            row.alignment = 'CENTER'
            self.Button(row, "cont_hip_R", "L", (1.5,2.2))
            self.Button(row, "cont_spine.002", "Spine 2", (1.5,2.2))
            self.Button(row, "cont_hip_L", "R", (1.5,2.2))
            
            self.Button(layout, "cont_spine.001", "Spine 1", (1.5,2.2))
    
    def draw(self, context):
        layout = self.layout
        props = self.Props()
        
        split = layout.split(factor=0.3)
        layout.prop(props, "piker", text="1")
        layout = layout.grid_flow(row_major=True, columns=1, even_columns=True,align=False)
        
  
        self.Head(layout)
        med_row = layout.row(align=True)
        self.Arm(med_row, "R")
        self.Torzo(med_row)
        self.Arm(med_row, "L")
        self.Button(layout, "Root_hip", "Root Hip", (1.9, 2))
        down_row = layout.row(align=True)
        down_row.alignment = "CENTER"
        self.Leg(down_row, "R")
        self.Leg(down_row, "L")
        self.Button(layout, "Root_move", "Root Move", (1.8, 2))