

import bpy


def AddArmature(self, context):
    layout = self.layout
    layout.menu("rgc.add_armature")
    
    ...




class RGC_Menu_AddArmature(bpy.types.Menu):
    bl_idname = "rgc.add_armature"
    bl_label = "Rig Creator"

    def draw(self, context):
        layout = self.layout
        layout.operator(
            "rgc.add_armature", text="Human", 
            icon="OUTLINER_OB_ARMATURE"
        ).type = "Human"
        
        layout.menu("rgc.add_for_games", text="For Games")
        layout.menu("rgc.add_body_parts", text="Body Parts")
        layout.separator()
        layout.menu("rgc.add_extras", text="Extras")

class RGC_Menu_ForGames(bpy.types.Menu):
    bl_idname = "rgc.add_for_games"
    bl_label = "For Games"

    def draw(self, context):
        layout = self.layout 
        layout.operator(
            "rgc.add_armature", text="Human For Games", 
            icon="OUTLINER_OB_ARMATURE"
        ).type = "Human For Games"  
        layout.operator(
            "rgc.add_armature", text="Human Flat Hierarchy", 
            icon="OUTLINER_OB_ARMATURE"
        ).type = "Human Flat Hierarchy" 

class RGC_Menu_AddExtras(bpy.types.Menu):
    bl_idname = "rgc.add_extras"
    bl_label = "Extras"

    def draw(self, context):
        layout = self.layout
        layout.operator(
            "rgc.add_armature", text="Basic Human", 
            icon="OUTLINER_OB_ARMATURE"
        ).type = "Basic Human"
        layout.operator(
            "rgc.add_armature", text="Cartoon Human", 
            icon="OUTLINER_OB_ARMATURE"
        ).type = "Cartoon Human"
        layout.operator(
            "rgc.add_armature", text="Reference Human", 
            icon="OUTLINER_OB_ARMATURE"
        ).type = "Reference Human"
        layout.operator(
            "rgc.add_armature", text="Human Sin RigCreator", 
            icon="OUTLINER_OB_ARMATURE"
        ).type = "Human Sin RigCreator"
        

class RGC_Menu_AddBodyParts(bpy.types.Menu):
    bl_idname = "rgc.add_body_parts"
    bl_label = "Body Parts"

    def draw(self, context):
        layout = self.layout
        layout.operator(
            "rgc.add_armature", text="Cartoon Face", 
            icon="OUTLINER_OB_ARMATURE"
        ).type = "Cartoon Face"
        layout.operator(
            "rgc.add_armature", text="Reference Cartoon Face", 
            icon="OUTLINER_OB_ARMATURE"
        ).type = "Reference Cartoon Face"