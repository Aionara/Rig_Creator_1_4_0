import bpy
from .general import *
from ..generaldata import GeneralArmatureData



class RGC_Panel_Collections(GN_RigCreatorViewPort, bpy.types.Panel):
    bl_idname = "RGC_Panel_Collections"
    bl_label = "Collections"

    
    @classmethod
    def poll(cls, context):        
        Self = GeneralArmatureData()
        return Self.GetArmature() and Self.PanelType([{"ALL"}, {"ANIMATION"}])
    
    
    def draw(self, context):
        layout = self.layout
        self.Armature = self.GetArmature()
        props = self.Props()
        
        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(props, "search_collection", text="", icon="VIEWZOOM")
        
        if self.Panel(col, "edit", "Edit", "GREASEPENCIL", True) :  
            row = col.row(align=True)
            if props.columns_value > 1:
                row.prop(props, "even_columns", text="", icon="ALIGN_JUSTIFY")
            row.scale_x = 1.2
            row.prop(props, "columns_value", text="Columns",)
            row = col.row(align=True)
            if self.IsCollectionToRigCreatorExists() == False:
                row.operator("rgc.collections", text="Add Collection To Rig Creator").type="ADD_COLLECTION"
            col.prop(props, "edit_collection", text="Edit Collection", icon="GREASEPENCIL", toggle=1)
       
        
        grid = layout.grid_flow(
            row_major=False, columns=props.columns_value, 
            even_columns=props.even_columns, even_rows=False, 
            align=True
            )

        for col in self.GetCollections():
            
            if not self.SearchInList(props.search_collection, col.name) : continue
            column = grid.column(align=True)
            icon = ""
            row = column.row(align=True)
            if col.parent : 
                icon = self.ChangeIcon(
                    "RESTRICT_VIEW_ON", "RESTRICT_VIEW_OFF", not col.is_visible or not col.parent.is_visible
                    )
                column.active = col.parent.is_visible
                new = row.operator("rgc.collections", text="", icon="FILE_PARENT")
                new.type = "MENU"
                new.col_name = col.name 
                new.col_name_parent = col.parent.name
                
            else:
                icon = self.ChangeIcon(
                    "RESTRICT_VIEW_ON", "RESTRICT_VIEW_OFF", 
                    not col.is_visible
                )
            
            row.prop(
                col, "is_visible", text=col.name if props.edit_collection == False else "", toggle=1, icon=icon, 
                )
            if props.edit_collection :
                row.prop(
                    col, "name", text=""
                )
                new = row.operator("rgc.collections", text="", icon="SORT_DESC")
                new.type = "UP"
                new.col_name = col.name      
                new = row.operator("rgc.collections", text="", icon="SORT_ASC")
                new.type = "DOWN"
                new.col_name = col.name      
            
            if self.GetObjMode() == "POSE" : 
                
                # Convertir la lista get_bones_in_collections en un conjunto
                bones_in_collections_set = set(self.GetBonesNamesInCollection(col.name))
                # Comprobar si algún hueso de get_bones_select está en bones_in_collections_set
                is_select = any(sb in bones_in_collections_set for sb in self.GetNameToBones(self.GetSelectBones(self.GetObjMode())))

                new = row.operator("rgc.collections", text="", icon=self.ChangeIcon(
                    "RESTRICT_SELECT_ON", "RESTRICT_SELECT_OFF", not is_select
                ))
                new.type = "SELECT" if not is_select else "DESELECT"
                new.col_name = col.name                     
                
                new = row.operator("rgc.collections", text="", icon="INDIRECT_ONLY_ON")
                new.type = "ALL_DESELECT"
                new.col_name = col.name 
            
                

class RGC_Menu_Collections(GN_RigCreatorViewPort, bpy.types.Menu):
    bl_idname = "RGC_Menu_Collections"
    bl_label = ""

    def draw(self, context):
        layout = self.layout
        props = self.Props()
        col = self.GetCollectionToName(props.how_collection_select)
        layout.prop(
                col, "is_visible", text=col.name, toggle=1, icon=self.ChangeIcon(
                    "RESTRICT_VIEW_ON", "RESTRICT_VIEW_OFF", 
                    not col.is_visible
                ), 
                )
        