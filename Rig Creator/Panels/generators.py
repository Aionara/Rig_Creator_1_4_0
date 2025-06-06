import bpy

from .general import *
from ..generaldata import GeneralArmatureData


class RGC_Generators_List(GeneralArmatureData, bpy.types.UIList):
    

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row = layout.row()
            row_1 = row.row()
            row_1.enabled = len(self.GetSelectBones(self.GetObjMode())) > 0
            if item.name == "Physics":
                row_1.enabled = self.GetObjMode() == "POSE" 
                row_1.operator(f"rgc.{item.name.lower()}", text="",  emboss=False, icon="PLAY")
            elif item.name == "Ik":
                col_1 = row_1.row()
                col_1.enabled = len(self.GetSelectBones(self.GetObjMode())) > 1
                col_1.operator(f"rgc.{item.name.lower()}", text="",  emboss=False, icon="PLAY")
            else:
                row_1.enabled = not self.GetObjMode() == "OBJECT"
                row_1.operator(f"rgc.{item.name.lower()}", text="",  emboss=False, icon="PLAY")
            layout.label(text=item.name)
            
                
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon=item.icon)


class DrawGenerators(GeneralArmatureData): 
    
    def PanelList(self) -> list: 
        return {
            "Annotate_Bone" : self.AnnotateBone, 
            #"Physics" : self.Physics, 
            "Fingers" : self.Fingers, 
            "Ik" : self.Ik, 
            "Fk" : self.Fk, 
            "Bones" : self.Bones, 
            "Curve": self.Curve,
            "Curve_Grip" : self.CurveGrip,
            "Auto_Root" : self.AutoRoot,
            
        }     
    
    
    def AnnotateBone(self, layout, props):
        
        if self.GetObjMode() == "POSE" :
            
            layout.prop(props, "annotate_type_mode", text="" ,expand=False, slider=False, toggle=1)
            layout.separator()
            layout.prop(props, "annotate_use_deform", text="Deform" ,expand=False, slider=False, toggle=1)
            row = layout.row(align=True)
            row.prop(props, "annotate_use_parent", text="Parent" ,expand=False, slider=False, toggle=1)
            srow = row.row(align=True)
            srow.enabled = props.annotate_use_parent
            srow.prop(props, "annotate_use_connect", text="Connected" ,expand=False, slider=False, toggle=1)
            layout.prop(props, "annotate_size_bbone", text="Bbone Size" ,expand=False, slider=False, toggle=1)
            
            layout.label(text="Align Mirror", icon="MOD_MIRROR")
            row = layout.row(align=True)
            row.prop(props, "annotate_use_align_mirror_x", text="X" ,expand=False, slider=False, toggle=1)
            row.prop(props, "annotate_use_align_mirror_y", text="Y" ,expand=False, slider=False, toggle=1)
            row.prop(props, "annotate_use_align_mirror_z", text="Z" ,expand=False, slider=False, toggle=1)
            row = layout.row(align=True)
            row.prop(props, "annotate_use_align_mirror_negative_x", text="-X" ,expand=False, slider=False, toggle=1)
            row.prop(props, "annotate_use_align_mirror_negative_y", text="-Y" ,expand=False, slider=False, toggle=1)
            row.prop(props, "annotate_use_align_mirror_negative_z", text="-Z" ,expand=False, slider=False, toggle=1)
            
            layout.separator()
            row = layout.column(align=True)
            row.prop(props, "annotate_use_join_bones", text="Join Bones" ,expand=False, slider=False, toggle=1)
            srow = row.column(align=True)
            srow.enabled = props.annotate_use_join_bones
            srow.prop(props, "annotate_join_same_name", text="Same Name" ,expand=False, slider=False, toggle=1)
            srow.prop(props, "annotate_proximity_join", text="Proximity To Join" ,expand=False, slider=False, toggle=1)
            layout.separator()
            layout.label(text="Target Normal")
            layout.prop(props, "annotate_global_normal", text="Only Global Normals" ,expand=False, slider=False, toggle=1)
            col = layout.column(align=True)
            col.enabled = not props.annotate_global_normal
            row = col.row(align=True)
            row.prop(props, "annotate_use_select_target", text="Select Object",expand=False, slider=False, toggle=1)
            srow = row.row(align=True)
            srow.enabled = not props.annotate_use_select_target
            srow.prop(props, "annotate_target", text="")
            #if props.annotate_target or props.annotate_use_select_target :
            #    layout.separator()
            #    layout.prop(props, "annotate_use_vertbone", text="Vert Bone" ,expand=False, slider=False, toggle=1)
            #    srow = layout.column(align=True)
            #    srow.enabled = props.annotate_use_vertbone
            #    srow.prop(props, "annotate_use_vertbone_deform", text="Vert Bone Deform" ,expand=False, slider=False, toggle=1)
            #    srow.prop(props, "annotate_name_vertbone", text="" ,expand=False, slider=False, toggle=1)
            layout.separator()
            
            row = layout.row(align=True)
            row.enabled = (not(props.annotate_target or props.annotate_use_select_target)) or props.annotate_global_normal
            row.prop(props, "annotate_direction", text="Normal Direction" ,expand=False, slider=False, toggle=1)
            layout.prop(props, "annotate_aling_roll_normal", text="Roll to Normal" ,expand=False, slider=False, toggle=1)
            layout.separator()
            row = layout.column(align=True)
            row.prop(props, "annotate_use_curve", text="Curve" ,expand=False, slider=False, toggle=1)
            srow = row.column(align=True)
            srow.enabled = props.annotate_use_curve
            srow.prop(props, "annotate_curve_power", text="Curve Power" ,expand=False, slider=False, toggle=1)
            srow.prop(props, "annotate_segments", text="Segments" ,expand=False, slider=False, toggle=1)
            
            layout.separator()
            
            layout.label(text="Names")
            layout.prop(props, "annotate_name", text="")
            layout.separator()
            layout.prop(props, "annotate_auto_bone", text="Auto Bone", icon="AUTO" ,expand=False, slider=False, toggle=1)
            if not props.annotate_auto_bone:
                layout.operator(f"rgc.generatorsbones", text="Run",  icon="PLAY").type = "Annotate_Bone"
            
        else:
            layout.operator(
                "rgc.setmode", text="Correct Mode"
            ).mode = "POSE"
    
    
    def Physics(self, layout, props):
        if self.GetObjMode() == "POSE" :
            layout.prop(
                props, "use_stretch_to", text="Stretch To", 
                icon="CON_STRETCHTO"
                )
            if props.use_stretch_to : 
                layout.prop(
                    props, "power_stretch", text="Power Stretch"
                )
            layout.prop(
                props, "power_overlapping", text="Power Overlapping"
            )
            layout.prop(
                props, "frame_step", text="Frame Step"
            )
            row = layout.row(align=True)
            row.prop(
                props, "frame_start", text="Frame Start"
            )
            row.prop(
                props, "frame_end", text="Frame End"
            )
            layout.operator(f"rgc.generatorsbones", text="Run",  icon="PLAY").type = "Physics"
        else:
            layout.operator(
                "rgc.setmode", text="Correct Mode"
            ).mode = "POSE"
        self.ShadowBox(layout, size_y=1.5)
    
    def Fingers(self, layout, props) : 
        row = layout.row(align=True)
        row.prop(props, "use_parent", text="", icon="FILE_PARENT" ,expand=False, slider=False, toggle=1)
        row.prop(props, "use_fk", text="FK", expand=False, slider=False, toggle=1)
        row.prop(props, "use_fingers", text="Fingers", expand=False, slider=False, toggle=1)
        row = layout.row(align=True)
        row.prop(props, "use_segments", text="Segments", icon="MOD_ARRAY", expand=False, slider=False, toggle=1)
        row.scale_x = 0.4
        srow = row.row(align=True)
        srow.enabled = props.use_segments
        srow.prop(props, "int_segments", text="")
        
        #layout.prop(props, "use_limit_rot_fingers", icon="CON_ROTLIMIT", text="Limit Rotation Fingers", expand=False, slider=False, toggle=1)
        #if props.use_limit_rot_fingers :
        #    row = layout.row(align=True)
        #    row.prop(props, "limit_rot_fingers" , text="Range Bones")
        #    row.prop(props, "limit_rot_fingers_invert", text="", icon = "ARROW_LEFTRIGHT", expand=False, slider=False, toggle=1)
        #    value = len(self.GetSelectBones(self.GetObjMode()))
        #    if props.limit_rot_fingers > value:
        #        box = layout.box()
        #        box.label(text="Out of the limit of selected bones", icon="ERROR")
        layout.label(text="Names")
        row = layout.row(align=True)
        row.prop(props, "name_def", text="")
        frow = layout.row(align=True)
        frow.enabled = props.use_fk 
        frow.prop(props, "name_fk", text="")
        frow = layout.row(align=True)
        frow.enabled = props.use_fingers
        frow.prop(props, "name_fingers", text="")
        layout.operator(f"rgc.generatorsbones", text="Run",  icon="PLAY").type = "Fingers"
        self.ShadowBox(layout, size_y=1.5)
        ...
    
    def Ik(self, layout, props) : 
        row = layout.row(align=True)
        row.prop(props, "use_stretch_to_ik", text="Stretch To", icon="CON_STRETCHTO", expand=False, slider=False, toggle=1)
        row.prop(props, "use_ik_as", text="", icon="EMPTY_DATA", expand=False, slider=False, toggle=1)
        row = layout.row(align=True)
        row.prop(props, "use_copy_transforms_ik", text="Copy Transforms", icon="CON_TRANSLIKE", expand=False, slider=False, toggle=1)
        layout.prop(props, "distance_pole_target", text="Distence Pole Target", icon="CON_TRACKTO")
        layout.prop(props, "pole_angle", text="Pole Angle", icon="ORIENTATION_GIMBAL")
        layout.label(text="Names")
        layout.prop(props, "name_ik", text="")
        col_1 = layout.column(align=True)
        col_1.enabled = len(self.GetSelectBones(self.GetObjMode())) > 1
        col_1.operator(f"rgc.generatorsbones", text="Run",  icon="PLAY").type = "Ik"
        self.ShadowBox(layout, size_y=1.5)
    
    def Fk(self, layout, props):
        row = layout.row(align=True)
        row.prop(props, "use_view_object", text="View Object", icon="OBJECT_DATA", expand=False, slider=False, toggle=1)
        row.prop(props, "use_copy_transforms_fk", text="Copy Transforms", icon="CON_TRANSLIKE", expand=False, slider=False, toggle=1)
        layout.label(text="Names")
        layout.prop(props, "name_fk1", text="")
        layout.operator(f"rgc.generatorsbones", text="Run",  icon="PLAY").type = "Fk"
        self.ShadowBox(layout, size_y=1.5)
    
    def Bones(self, layout, props):
        row = layout.row(align=True)
        row.prop(props, "look_bone", text="X", icon="NORMALS_FACE", expand=False, slider=False, toggle=1)
        row = layout.row(align=True)
        row.prop(props, "add_orientation", text="", icon="ORIENTATION_GIMBAL", expand=False, slider=False, toggle=1)
        row = layout.row(align=True)
        row.prop(props, "use_viewport_display", text="Viewport Display", icon="SHADING_TEXTURE", expand=False, slider=False, toggle=1)
        
        srow = row.row(align=True)
        srow.active = props.use_viewport_display
        srow.prop(props, "viewport_display_type", text="", icon="SHADING_BBOX", expand=False, slider=False, toggle=1)
        row = layout.row(align=True)
        row.prop(props, "use_parent_bone", text="", icon="FILE_PARENT", expand=False, slider=False, toggle=1)
        row.prop(props, "use_bone_in_tail",text="Bone In Tail", expand=False, slider=False, toggle=1)
        
        srow = row.row(align=True)
        srow.active = props.use_bone_in_tail
        srow.prop(props, "use_stretch_to_bone", text="Stretch To", icon="CON_STRETCHTO", expand=False, slider=False, toggle=1)
        
        layout.label(text="Names")
        layout.prop(props, "name_bone", text="")
        layout.operator(f"rgc.generatorsbones", text="Run",  icon="PLAY").type = "Bones"
        ...
    
    def Curve(self, layout, props) :
        row = layout.row(align=True)
        row.prop(props, "use_curve_root", text="Root Curve", expand=False, slider=False, toggle=1)
        row.prop(props, "curve_int_segments", text="Segments", expand=False, slider=False, toggle=1)
        layout.prop(props, "use_curve_subbone", text="Sub Bone", expand=False, slider=False, toggle=1)
        Sublayout = layout.column(align=True)
        Sublayout.active = props.use_curve_subbone
        Sublayout.prop(props, "curve_subbone_howmuch", text="How Much Bones")
        
        #layout.prop(props, "use_curve_drive", text="Drive", expand=False, slider=False, toggle=1)
        layout.label(text="Names")
        layout.prop(props, "name_curve_free", text="")
        layout.prop(props, "name_curve_cont", text="")
        Nlayout = layout.column(align=True)
        Nlayout.active = props.use_curve_root
        Nlayout.prop(props, "name_curve_root", text="")
        layout.operator(f"rgc.generatorsbones", text="Run",  icon="PLAY").type = "Curve"
        ...
    
    def CurveGrip(self, layout, props, use_run : bool = True) :
        row = layout.row(align=True)
        row.prop(props, "grip_use_target", text="Target", expand=False, slider=False, toggle=1)
        row.prop(props, "grip_use_target_scale", text="Target Scale", expand=False, slider=False, toggle=1)
        layout.label(text="Align")
        layout.prop(props, "grip_align_to_normal", text="Root To Normal", expand=False, slider=False, toggle=1)
        tlayout = layout.column(align=True)
        tlayout.active = props.grip_use_target
        tlayout.prop(props, "grip_align_target", text="Target To Root", expand=False, slider=False, toggle=1)
        layout.separator()
        layout.prop(props, "grip_bulge", text="Bulge", expand=False, slider=False, toggle=1)
        layout.prop(props, "grip_proximity_join", text="Join Proximity", expand=False, slider=False, toggle=1)
        layout.label(text="Names")
        layout.prop(props, "name_grip_root", text="")
        tlayout = layout.column(align=True)
        tlayout.active = props.grip_use_target
        tlayout.prop(props, "name_grip_target", text="")
        slayuot = layout.column(align=True)
        slayuot.active = props.grip_use_target_scale
        slayuot.prop(props, "name_grip_target_scale", text="")  
        if use_run :
            layout.operator(f"rgc.generatorsbones", text="Run",  icon="PLAY").type = "Curve_Grip"
        
    def AutoRoot(self, layout, props) :
        row = layout.row(align=True)
        row.prop(props, "use_active_bone", text="Active Bone", expand=False, slider=False, toggle=1)
        row.prop(props, "bones_parent", text="Bones Parent", expand=False, slider=False, toggle=1)
        layout.label(text="Names")
        layout.prop(props, "name_auto_root", text="")
        layout.operator(f"rgc.generatorsbones", text="Run",  icon="PLAY").type = "Auto_Root"


class RGC_Panel_Generators(GN_RigCreatorViewPort, DrawGenerators, bpy.types.Panel):
    bl_idname = "RC_Panel_Generators"
    bl_label = "Generators"
    
    @classmethod
    def poll(cls, context):
        Self = GeneralArmatureData()        
        return context.active_object and context.active_object.type == "ARMATURE"\
            and Self.PanelType([{"ALL"}, {"RIG"}])
    
    def draw(self, context):
        layout = self.layout
        scena = self.GetScene()
        props = self.Props()
        
        col = layout.column()
        col.scale_y = 1
        col = layout.column(align=True)
        col.scale_y = 1.2
        
        if not self.GetObjMode() == "OBJECT" :
            col.prop(props, "generators_browser", text="", icon="VIEWZOOM")
            def is_select(type : str) -> bool:
                if type.lower() in props.generators_browser.lower() or props.generators_browser == "":
                    return True
                return False
            panels = self.PanelList()
            for type in panels :
                if is_select(type) and self.Panel(col, type, type.replace("_", " "), "", True):
                    panels[type](col, props)
                
def Pose_AddGenerators(self, context) : 
    layout = self.layout
    RGC = GeneralArmatureData()
    if RGC.GetActiveObject() and RGC.GetActiveObject().type == "ARMATURE":
        if RGC.GetObjMode() == "POSE":
            layout.menu("rgc.addbone", text="Add")

def Edit_AddGenerators(self, context) :
     
    layout = self.layout
    
class RGC_Menu_AddBone(GeneralArmatureData, bpy.types.Menu):
    bl_idname = "rgc.addbone"
    bl_label = "Add"

    
    def draw(self, context):
        layout = self.layout
        layout.operator("rgc.generatorsbones", text="Add Bone").type = "AddBone"
        layout.menu("rgc.parent")
        layout.menu("rgc.unionbone")
        layout.menu("rgc.addgenerators")

class RGC_Menu_Parent(GeneralArmatureData, bpy.types.Menu):
    bl_idname = "rgc.parent"
    bl_label = "Parent"

    def draw(self, context):
        layout = self.layout
        layout.operator("rgc.generatorsbones", text="Keep Offset").type = "ParentOffSet"
        layout.operator("rgc.generatorsbones", text="Connected").type = "ParentConnected"
        layout.separator()
        layout.operator("rgc.generatorsbones", text="Select Bones To Active Bendy-Bones").type = "ParentBendyBones"
        layout.operator("rgc.generatorsbones", text="Active Bone To Bendy-Bones").type = "ParentActiveBendyBones"
        layout.separator()
        layout.operator("rgc.generatorsbones", text="Damped Track Parent").type = "DampedTrackParent"

        
class RGC_Menu_UnionBone(GeneralArmatureData, bpy.types.Menu):
    bl_idname = "rgc.unionbone"
    bl_label = "Union Bone"

    def draw(self, context):
        layout = self.layout
        
        layout.operator("rgc.generatorsbones", text="Base").type = "UnionBase"
        layout.operator("rgc.generatorsbones", text="Active Bone").type = "UnionActiveBone"


class RGC_Menu_AddGenerators(DrawGenerators, bpy.types.Menu):
    bl_idname = "rgc.addgenerators"
    bl_label = "Generators"

    
    def draw(self, context):
        layout = self.layout
        for op in self.PanelList():
            layout.operator("rgc.call_menu_generators", text=op.replace("_"," ")).type = op
            
How_Menu = ""
class RGC_Operator_Call_AddGenerators(bpy.types.Operator):
    bl_idname = "rgc.call_menu_generators"
    bl_label = ""


    type : StringProperty()
    
    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        global How_Menu
        How_Menu = self.type
        bpy.ops.wm.call_panel(name="rgc.call_addgenerators")

        return {"FINISHED"}



class RGC_Panel_Call_AddGenerators(DrawGenerators, bpy.types.Panel):
    bl_idname = "rgc.call_addgenerators"
    bl_label = "Generators"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
   
    
    @classmethod
    def poll(cls, context):
        return True
    

    def draw(self, context):
        layout = self.layout
        props = self.Props()
        global How_Menu
        panels = self.PanelList()
        if How_Menu in panels :
            panels[How_Menu](layout, props)
        

class RGC_Panel_Physics(DrawGenerators, GN_RigCreatorViewPort, bpy.types.Panel) : 
    bl_idname = "RGC_Panel_Physics"
    bl_label = "Physics"

    @classmethod
    def poll(cls, context):
        Self = GeneralArmatureData()        
        return context.active_object and context.active_object.type == "ARMATURE"\
            and Self.PanelType([{"ANIMATION"}])
    
    def draw(self, context):
        layout = self.layout
        props = self.Props()
        
        col = layout.column(align=True)
        col.scale_y = 1.2
        self.Physics(col, props)




def RGC_DrawSetControlBendyBone(self, context) : 
    RGC = GeneralArmatureData()
    if RGC.GetObjMode() != "POSE" : return
    L = self.layout
    props = RGC.Props()
    if RGC.Panel(L, "set_control_bendy", "Set Control BendyBone", "BONE_DATA", True) :
        L.prop(props, "bendybone_type", text="Type", icon="BONE_DATA", expand=True)
        UIop = L.column(align=True)
        if props.bendybone_type != {"PARENT"}:
            UIop.enabled = not len(RGC.GetSelectBones(mode="POSE")) < 3 
        else :
            UIop.enabled = not len(RGC.GetSelectBones(mode="POSE")) < 2 
        row = L.row(align=True)
        row.operator("rgc.general", text="Set Control BendyBone").type = "SET_CONT_BENDYBONE"
        if props.bendybone_type != {"PARENT"}:
            row.prop(props, "bendy_bone_invest", text="", icon="ARROW_LEFTRIGHT", expand=False, slider=False, toggle=1)