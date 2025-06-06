
import bpy
from ..generaldata import GeneralArmatureData
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

ListFinger = [
            "Thumb",
            "Index Finger",
            "Middle Finger",
            "Ring Finger",
            "Pinky",
        ]

def set_annotate(self, context, value : str):
    if getattr(self, value) is True:
        # Cambiar herramienta directamente sin override
        bpy.ops.wm.tool_set_by_id(name="builtin.annotate")
    else:
        bpy.ops.wm.tool_set_by_id(name="builtin.select_box")

enum_list = {
    'EMPTY': -1,
    'ROOT_MOVE': 0,
    'ROOT_HIP': 1,
    'SHOULDERS': 2,
    'SHOULDER': 3,
    'ROOT_ARM': 4,
    'HAND': 5,
}

index_list = {
    -1: 'EMPTY',
    0: 'ROOT_MOVE',
    1: 'ROOT_HIP',
    2: 'SHOULDERS',
    3: 'SHOULDER',
    4: 'ROOT_ARM',
    5: 'HAND',
}

leg_enum_list = {
    'EMPTY': -1,
    'ROOT_MOVE': 0,
    'ROOT_HIP': 1,
    'ROOT_LEG': 2,
    
}

leg_index_list = {
    -1: 'EMPTY',
    0: 'ROOT_MOVE',
    1: 'ROOT_HIP',
    2: 'ROOT_LEG',
    
}

# Variable global para evitar recursión infinita
is_updating = False

def Index(self, context, self_property, other_property):
    global index_list, is_updating
    if is_updating:
        return  # Evita la recursión infinita
    try:
        prop = GeneralArmatureData().PropsToArmature()[0]
        value = getattr(prop, self_property)
        # Activamos la bandera antes de la actualización
        is_updating = True
        setattr(prop, other_property, index_list[value])
        # Desactivamos la bandera después de la actualización
        is_updating = False
    except (KeyError, AttributeError, IndexError) as e:
        print(f"Index Error: {e}")
        is_updating = False

def Enum(self, context, self_property, other_property):
    global enum_list, is_updating
    if is_updating:
        return  # Evita la recursión infinita
    try:
        prop = GeneralArmatureData().PropsToArmature()[0]
        # Activamos la bandera antes de la actualización
        is_updating = True
        setattr(prop, other_property, enum_list[getattr(prop, self_property)])
        # Desactivamos la bandera después de la actualización
        is_updating = False
    except (KeyError, AttributeError, IndexError) as e:
        print(f"Enum Error: {e}")
        is_updating = False

def Leg_Index(self, context, self_property, other_property):
    global leg_index_list, is_updating
    if is_updating:
        return  # Evita la recursión infinita
    try:
        prop = GeneralArmatureData().PropsToArmature()[0]
        value = getattr(prop, self_property)
        # Activamos la bandera antes de la actualización
        is_updating = True
        setattr(prop, other_property, leg_index_list[value])
        # Desactivamos la bandera después de la actualización
        is_updating = False
    except (KeyError, AttributeError, IndexError) as e:
        print(f"Index Error: {e}")
        is_updating = False

def Leg_Enum(self, context, self_property, other_property):
    global leg_enum_list, is_updating
    if is_updating:
        return  # Evita la recursión infinita
    try:
        prop = GeneralArmatureData().PropsToArmature()[0]
        # Activamos la bandera antes de la actualización
        is_updating = True
        setattr(prop, other_property, leg_enum_list[getattr(prop, self_property)])
        # Desactivamos la bandera después de la actualización
        is_updating = False
    except (KeyError, AttributeError, IndexError) as e:
        print(f"Enum Error: {e}")
        is_updating = False

def all_finger_enum(self, context, self_property):
    global enum_list, is_updating
    if is_updating:
        return  # Evita la recursión infinita
    try:
        fingers = GeneralArmatureData().ListFinger()
        for finger in fingers:
            prop = GeneralArmatureData().PropsToArmature()[0]
            name = finger.replace(" ", "").lower()
            name_property = self_property
            if 'fingers_stretch_to' in self_property:
                name_property = name_property.replace('fingers_stretch_to', 'fingers_stretch_t')
            other_property = f"{name}{name_property.replace('fingers', '')}"
            value = getattr(prop, self_property )
            setattr(prop, other_property, value)
        is_updating = False
        
    except (KeyError, AttributeError, IndexError) as e:
        print(f"Enum Error: {e}")
        is_updating = False


class RGC_Save_Bones_Have_Select_View(bpy.types.PropertyGroup):
    bone : StringProperty(default="")


class RGC_Armature_GrupsProps(bpy.types.PropertyGroup):
    
    #save_Bone
    

    #Global Local
    head : FloatProperty(default=1,min=0.0, max=1.0,subtype = "FACTOR",options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    arm_items = [
        ('EMPTY', "Empty", ""),
        ('ROOT_MOVE', "Root Move", ""),
        ('ROOT_HIP', "Root Hip", ""),
        ('SHOULDERS', "Shoulders", ""),
        ('SHOULDER', "Shoulder", ""),
        ('ROOT_ARM', "Root Arm", ""),
    ]
    eyes : FloatProperty(default=2,min=0.0, max=2.0,subtype = "FACTOR",options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    
    # Boca
    corner_mouth_L : FloatProperty(default=1,min=0.0, max=1.0,subtype = "FACTOR",options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    corner_mouth_R : FloatProperty(default=1,min=0.0, max=1.0,subtype = "FACTOR",options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    arc_L : FloatProperty(default=0.5,min=0.0, max=1.0,subtype = "FACTOR",options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    arc_R : FloatProperty(default=0.5,min=0.0, max=1.0,subtype = "FACTOR",options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    
    tongue_ik_fk : FloatProperty(default=1, min=0.0, max=1.0,subtype = "FACTOR",options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    tongue_stretch_to : BoolProperty(default=True,options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    
    # ARMS
    arm_ik_fk_L : FloatProperty(default=1, min=0.0, max=1.0,subtype = "FACTOR",options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    arm_ik_fk_R : FloatProperty(default=1, min=0.0, max=1.0,subtype = "FACTOR",options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    arm_stretch_to_L : BoolProperty(default=True,options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    arm_stretch_to_R : BoolProperty(default=True,options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    elbow_cartoon_L : FloatProperty(default=0, min=0.0, max=1.0,subtype = "FACTOR",options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    elbow_cartoon_R : FloatProperty(default=0, min=0.0, max=1.0,subtype = "FACTOR",options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    arm_rot_L : BoolProperty(default=True,options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    arm_rot_R : BoolProperty(default=True,options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    
    arm_followed_L : IntProperty(
        default=4,
        min=-1, max=4,
        update=lambda self, context: Index(self, context, "arm_followed_L", "arm_followed_enum_L"),
        options={'LIBRARY_EDITABLE', 'ANIMATABLE'}
    )
    arm_followed_R : IntProperty(
        default=4,
        min=-1, max=4,
        update=lambda self, context: Index(self, context, "arm_followed_R", "arm_followed_enum_R"),
        options={'LIBRARY_EDITABLE', 'ANIMATABLE'}
        )
    arm_items = [
        ('EMPTY', "Empty", ""),
        ('ROOT_MOVE', "Root Move", ""),
        ('ROOT_HIP', "Root Hip", ""),
        ('SHOULDERS', "Shoulders", ""),
        ('SHOULDER', "Shoulder", ""),
        ('ROOT_ARM', "Root Arm", ""),
    ]

    arm_followed_enum_L: EnumProperty(
        items=arm_items,
        name='Followed L',
        default='ROOT_ARM',
        update=lambda self, context: Enum(self,context,"arm_followed_enum_L", "arm_followed_L"),
        options={'LIBRARY_EDITABLE'}
    )
    arm_followed_enum_R: EnumProperty(
        items=arm_items,
        name='Followed R',
        default='ROOT_ARM',
        update=lambda self, context: Enum(self, context, "arm_followed_enum_R", "arm_followed_R"),
        options={'LIBRARY_EDITABLE'}
    )
    
    arm_invert_ik_fk_L : BoolProperty(options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    arm_invert_ik_fk_R : BoolProperty(options={'LIBRARY_EDITABLE', 'ANIMATABLE'})


    # FINGERS
    
    """
    for type in ["R", "L"]:
        for prop in ListFinger():
            clean_name = prop.replace(" ", "").lower()
            FK_a_IK = f"{clean_name}_fk_a_ik_{type}"
            Stretch_To = f"{clean_name}_stretch_t_{type}"
            Rot = f"{clean_name}_rot_{type}"
            Followed = f"{clean_name}_followed_{type}"
            Enum = f"{clean_name}_enum_{type}"
            
            print(f"    {FK_a_IK} : FloatProperty(default=1.0, min=0.0, max=1.0, subtype='FACTOR')")
            print(f"    {Stretch_To} : BoolProperty(default=True)")
            print(f"    {Rot} : BoolProperty(default=True)")
            print(f"    {Followed} : IntProperty(default=4,min=0, max=5, update=lambda self, context: Index(self, context, '{Followed}', '{Enum}'),)")
            print(f"    {Enum} : EnumProperty(items=arm_items,name='Followed_{type}',default='HAND',update=lambda self, context: Enum(self, context, '{Enum}', '{Followed}'),options="+"{'HIDDEN'})")
    """
    
    
    arm_items = [
        ('ROOT_MOVE', "Root Move", ""),
        ('ROOT_HIP', "Root Hip", ""),
        ('SHOULDERS', "Shoulders", ""),
        ('SHOULDER', "Shoulder", ""),
        ('ROOT_ARM', "Root Arm", ""),
        ('HAND', "Hand", ""),
    ]
    
    fingers_fk_a_ik_L : FloatProperty(
        default=1.0, min=0.0, max=1.0, subtype='FACTOR',
        update=lambda self, context: all_finger_enum(self, context, 'fingers_fk_a_ik_L'),
        options={'LIBRARY_EDITABLE',}
        )
    fingers_fk_a_ik_R : FloatProperty(
        default=1.0, min=0.0, max=1.0, subtype='FACTOR',
        update=lambda self, context: all_finger_enum(self, context, 'fingers_fk_a_ik_R'),
        options={'LIBRARY_EDITABLE', 'ANIMATABLE'}
        )
    fingers_stretch_to_L : BoolProperty(
        default=True,
        update=lambda self, context: all_finger_enum(self, context, 'fingers_stretch_to_L'),
        options={'LIBRARY_EDITABLE', 'ANIMATABLE'}
        )
    fingers_stretch_to_R : BoolProperty(
        default=True,
        update=lambda self, context: all_finger_enum(self, context, 'fingers_stretch_to_R'),
        options={'LIBRARY_EDITABLE', 'ANIMATABLE'}
        )
    fingers_followed_L : IntProperty(default=4,min=0, max=5, 
    update=lambda self, context: all_finger_enum(self, context, 'fingers_followed_L'),
    options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    fingers_followed_R : IntProperty(default=4,min=0, max=5, 
    update=lambda self, context: all_finger_enum(self, context, 'fingers_followed_R'),
    options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    fingers_enum_L : EnumProperty(items=arm_items,name='Followed_R',
    default='HAND',update=lambda self, context: all_finger_enum(self, context, 'fingers_enum_L'),
    options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    fingers_enum_R : EnumProperty(items=arm_items,name='Followed_R',
    default='HAND',update=lambda self, context: all_finger_enum(self, context, 'fingers_enum_R'),
    options={'LIBRARY_EDITABLE', 'ANIMATABLE'})

    thumb_fk_a_ik_R : FloatProperty(default=1.0, min=0.0, max=1.0, subtype='FACTOR',options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    thumb_stretch_t_R : BoolProperty(default=True,options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    thumb_rot_R : BoolProperty(default=True,options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    thumb_followed_R : IntProperty(default=4,min=-1, max=5, update=lambda self, context: Index(self, context, 'thumb_followed_R', 'thumb_enum_R'),options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    thumb_enum_R : EnumProperty(items=arm_items,name='Followed_R',default='HAND',update=lambda self, context: Enum(self, context, 'thumb_enum_R', 'thumb_followed_R'),options={'LIBRARY_EDITABLE'})
    
    indexfinger_fk_a_ik_R : FloatProperty(default=1.0, min=0.0, max=1.0, subtype='FACTOR',options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    indexfinger_stretch_t_R : BoolProperty(default=True,options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    indexfinger_rot_R : BoolProperty(default=True,options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    indexfinger_followed_R : IntProperty(default=4,min=-1, max=5, update=lambda self, context: Index(self, context, 'indexfinger_followed_R', 'indexfinger_enum_R'),options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    indexfinger_enum_R : EnumProperty(items=arm_items,name='Followed_R',default='HAND',update=lambda self, context: Enum(self, context, 'indexfinger_enum_R', 'indexfinger_followed_R'),options={'LIBRARY_EDITABLE'})
    
    middlefinger_fk_a_ik_R : FloatProperty(default=1.0, min=0.0, max=1.0, subtype='FACTOR',options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    middlefinger_stretch_t_R : BoolProperty(default=True,options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    middlefinger_rot_R : BoolProperty(default=True,options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    middlefinger_followed_R : IntProperty(default=4,min=-1, max=5, update=lambda self, context: Index(self, context, 'middlefinger_followed_R', 'middlefinger_enum_R'),options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    middlefinger_enum_R : EnumProperty(items=arm_items,name='Followed_R',default='HAND',update=lambda self, context: Enum(self, context, 'middlefinger_enum_R', 'middlefinger_followed_R'),options={'LIBRARY_EDITABLE'})
    
    ringfinger_fk_a_ik_R : FloatProperty(default=1.0, min=0.0, max=1.0, subtype='FACTOR',options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    ringfinger_stretch_t_R : BoolProperty(default=True,options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    ringfinger_rot_R : BoolProperty(default=True,options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    ringfinger_followed_R : IntProperty(default=4,min=-1, max=5, update=lambda self, context: Index(self, context, 'ringfinger_followed_R', 'ringfinger_enum_R'),options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    ringfinger_enum_R : EnumProperty(items=arm_items,name='Followed_R',default='HAND',update=lambda self, context: Enum(self, context, 'ringfinger_enum_R', 'ringfinger_followed_R'),options={'LIBRARY_EDITABLE'})
    
    pinky_fk_a_ik_R : FloatProperty(default=1.0, min=0.0, max=1.0, subtype='FACTOR',options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    pinky_stretch_t_R : BoolProperty(default=True,options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    pinky_rot_R : BoolProperty(default=True,options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    pinky_followed_R : IntProperty(default=4,min=-1, max=5, update=lambda self, context: Index(self, context, 'pinky_followed_R', 'pinky_enum_R'),options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    pinky_enum_R : EnumProperty(items=arm_items,name='Followed_R',default='HAND',update=lambda self, context: Enum(self, context, 'pinky_enum_R', 'pinky_followed_R'),options={'LIBRARY_EDITABLE'})
    
    thumb_fk_a_ik_L : FloatProperty(default=1.0, min=0.0, max=1.0, subtype='FACTOR',options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    thumb_stretch_t_L : BoolProperty(default=True,options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    thumb_rot_L : BoolProperty(default=True,options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    thumb_followed_L : IntProperty(default=4,min=-1, max=5, update=lambda self, context: Index(self, context, 'thumb_followed_L', 'thumb_enum_L'),options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    thumb_enum_L : EnumProperty(items=arm_items,name='Followed_L',default='HAND',update=lambda self, context: Enum(self, context, 'thumb_enum_L', 'thumb_followed_L'),options={'LIBRARY_EDITABLE'})
    
    indexfinger_fk_a_ik_L : FloatProperty(default=1.0, min=0.0, max=1.0, subtype='FACTOR',options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    indexfinger_stretch_t_L : BoolProperty(default=True,options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    indexfinger_rot_L : BoolProperty(default=True,options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    indexfinger_followed_L : IntProperty(default=4,min=-1, max=5, update=lambda self, context: Index(self, context, 'indexfinger_followed_L', 'indexfinger_enum_L'),options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    indexfinger_enum_L : EnumProperty(items=arm_items,name='Followed_L',default='HAND',update=lambda self, context: Enum(self, context, 'indexfinger_enum_L', 'indexfinger_followed_L'),options={'LIBRARY_EDITABLE'})
    
    middlefinger_fk_a_ik_L : FloatProperty(default=1.0, min=0.0, max=1.0, subtype='FACTOR',options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    middlefinger_stretch_t_L : BoolProperty(default=True,options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    middlefinger_rot_L : BoolProperty(default=True,options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    middlefinger_followed_L : IntProperty(default=4,min=-1, max=5, update=lambda self, context: Index(self, context, 'middlefinger_followed_L', 'middlefinger_enum_L'),options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    middlefinger_enum_L : EnumProperty(items=arm_items,name='Followed_L',default='HAND',update=lambda self, context: Enum(self, context, 'middlefinger_enum_L', 'middlefinger_followed_L'),options={'LIBRARY_EDITABLE'})
    
    ringfinger_fk_a_ik_L : FloatProperty(default=1.0, min=0.0, max=1.0, subtype='FACTOR',options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    ringfinger_stretch_t_L : BoolProperty(default=True,options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    ringfinger_rot_L : BoolProperty(default=True,options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    ringfinger_followed_L : IntProperty(default=4,min=-1, max=5, update=lambda self, context: Index(self, context, 'ringfinger_followed_L', 'ringfinger_enum_L'),options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    ringfinger_enum_L : EnumProperty(items=arm_items,name='Followed_L',default='HAND',update=lambda self, context: Enum(self, context, 'ringfinger_enum_L', 'ringfinger_followed_L'),options={'LIBRARY_EDITABLE'})
    
    pinky_fk_a_ik_L : FloatProperty(default=1.0, min=0.0, max=1.0, subtype='FACTOR',options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    pinky_stretch_t_L : BoolProperty(default=True,options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    pinky_rot_L : BoolProperty(default=True,options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    pinky_followed_L : IntProperty(default=4,min=-1, max=5, update=lambda self, context: Index(self, context, 'pinky_followed_L', 'pinky_enum_L'),options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    pinky_enum_L : EnumProperty(items=arm_items,name='Followed_L',default='HAND',update=lambda self, context: Enum(self, context, 'pinky_enum_L', 'pinky_followed_L'),options={'LIBRARY_EDITABLE'})
    
    # LEGS
    leg_ik_fk_L : FloatProperty(default=1, min=0.0, max=1.0,subtype = "FACTOR",
        options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    leg_ik_fk_R : FloatProperty(default=1, min=0.0, max=1.0,subtype = "FACTOR",
        options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    leg_stretch_to_L : BoolProperty(default=True,
        options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    leg_stretch_to_R : BoolProperty(default=True,
        options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    leg_rot_L : BoolProperty(default=True,
        options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    leg_rot_R : BoolProperty(default=True,
        options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    leg_invert_ik_fk_L : BoolProperty(
        options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    leg_invert_ik_fk_R : BoolProperty(
        options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    
    
    leg_items = [
        ('EMPTY', "Empty", ""),
        ('ROOT_MOVE', "Root Move", ""),
        ('ROOT_HIP', "Root Hip", ""),
        ('ROOT_LEG', "Root Leg", ""),
    ]
    
    leg_followed_L : IntProperty(
        default=0,min=-1, max=2, 
        update=lambda self, context: Leg_Index(self, context, 'leg_followed_L', 'leg_followed_enum_L'),
        options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    leg_followed_enum_L : EnumProperty(
        items=leg_items,name='Followed_L',default='ROOT_MOVE',
        update=lambda self, context: Leg_Enum(self, context, 'leg_followed_enum_L', 'leg_followed_L'),
        options={'LIBRARY_EDITABLE'})
    leg_followed_R : IntProperty(
        default=0,min=-1, max=2, 
        update=lambda self, context: Leg_Index(self, context, 'leg_followed_R', 'leg_followed_enum_R'),
        options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    leg_followed_enum_R : EnumProperty(
        items=leg_items,name='Followed_L',default='ROOT_MOVE',
        update=lambda self, context: Leg_Enum(self, context, 'leg_followed_enum_R', 'leg_followed_R'),
        options={'LIBRARY_EDITABLE'})
    
    leg_elbow_cartoon_L : FloatProperty(default=0, min=0.0, max=1.0,subtype = "FACTOR",options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    leg_elbow_cartoon_R : FloatProperty(default=0, min=0.0, max=1.0,subtype = "FACTOR",options={'LIBRARY_EDITABLE', 'ANIMATABLE'})
    

def UpdateType(self, context):
    GN = GeneralArmatureData()
    prop = GN.Props()
    prop.annotate_auto_bone = False

class RGC_GrupsProps(GeneralArmatureData, bpy.types.PropertyGroup):
    
    
    
    # GN 
    panel_type : EnumProperty(
        items=[
            ('ALL', "All", ""),
            ('ANIMATION', "Animation", ""),
            ('RIG', "Rigging", ""),
            
        ],
        name='Panel Type',
        default={'ANIMATION'}, 
        options={'ENUM_FLAG'},
        update=UpdateType,
    ) 
    
    
    ### Generators
    #Generators_List : CollectionProperty(type=RGC_Generators_GrupsProps)
    #Generators_index : IntProperty(options={'HIDDEN'})
    
    #browser 
    generators_browser : StringProperty()
    
    # Fisicas Props Groups
    use_stretch_to : BoolProperty()
    power_stretch : FloatProperty(min=0, max=10.0,subtype = "FACTOR",)
    power_overlapping : FloatProperty(min = 0, max = 0.8, subtype = "FACTOR")
    frame_start : IntProperty(default=1)
    frame_end : IntProperty( default=240)
    frame_step : IntProperty(default=1, min=1)
    
    # Fingers Props Groups
    use_fk : BoolProperty(default=True)
    use_def : BoolProperty(default=True)
    use_fingers : BoolProperty(default=True)
    use_fingers_rot : BoolProperty()
    use_segments : BoolProperty(default=True)
    use_parent : BoolProperty(default=True)
    name_fk : StringProperty(default="fk_")
    name_def : StringProperty(default="def_")
    name_fingers : StringProperty(default="fingers_")
    int_segments : IntProperty(min=1, max=32, default=32)
    use_limit_rot_fingers : BoolProperty()
    limit_rot_fingers : IntProperty(min=1, default=1)
    limit_rot_fingers_invert : BoolProperty()
    
    # Fk Props Groups
    use_view_object : BoolProperty(default=(True))
    use_copy_transforms_fk : BoolProperty(default=(True))
    name_fk1 : StringProperty(default="FK")
    
    # Ik Props Groups
    use_stretch_to_ik : BoolProperty(default=(True))
    use_pole_target : BoolProperty(default=(True))
    use_ik_as: EnumProperty(items=[
        ('POLE', "Pole", ""),
        ('ROT', "Rotation", ""),
        ], 
        name='Rotation IK As', 
        default='POLE', 
    )
    use_track_to : BoolProperty(default=(True))
    use_copy_transforms_ik : BoolProperty(default=(True))
    distance_pole_target : FloatProperty(subtype = "DISTANCE", default=1)
    pole_angle : FloatProperty(subtype = "ANGLE", default=-1.5708)
    name_ik : StringProperty(default="ik_")

    # Bones Props Groups
    look_bone: EnumProperty(items=[
        ('X', "X", ""),
        ('Y', "Y", ""),
        ('Z', "Z", ""),
        ('-X', "-X", ""),
        ('-Y', "-Y", ""),
        ('-Z', "-Z", ""),
        ], 
        name='LooK Bone', 
        default={'Z'}, 
        options={'ENUM_FLAG'}
        )
    add_orientation: EnumProperty(items=[
        ('GLOBAL', "Global", ""),
        ('NORMAL', "Normal", ""),
        ], 
        name='How Orientation', 
        default='GLOBAL', 
        )
    viewport_display_type: EnumProperty(items=[
        ('SINGLE_ARROW', "Arrow", "EMPTY_SINGLE_ARROW"),
        ('CIRCLE', "Circle", "MESH_CIRCLE"),
        ('CUBE', "Cube", "CUBE"),
        ('SPHERE', "Sphere", "SPHERE"),
        ], 
        name='Type', 
        default='SPHERE', 
        )
    use_parent_bone: BoolProperty(default=(True))
    use_bone_in_tail : BoolProperty(default=(True))
    use_viewport_display: BoolProperty(default=(True))
    use_stretch_to_bone : BoolProperty(default=(True))
    name_bone: StringProperty(default="bone_")

    # Curve Props Groups
    use_curve_root: bpy.props.BoolProperty(default=(False))
    use_curve_drive: bpy.props.BoolProperty(default=(False))
    use_curve_subbone: bpy.props.BoolProperty(default=(False))
    
    curve_subbone_howmuch: bpy.props.IntProperty(default=32, min=2,)
    name_curve_def: bpy.props.StringProperty(default="def_")
    name_curve_free: bpy.props.StringProperty(default="free_")
    name_curve_cont: bpy.props.StringProperty(default="cont_")
    name_curve_root: bpy.props.StringProperty(default="root_")
    curve_int_segments: bpy.props.IntProperty(default=32, min=1, max=32)
    
    # Curve Grip Props
    grip_use_target : bpy.props.BoolProperty(default=(True))
    grip_align_to_normal : bpy.props.BoolProperty(default=(False))
    grip_align_target : bpy.props.BoolProperty(default=(False))
    grip_use_target_scale : bpy.props.BoolProperty(default=(False))
    name_grip_target: bpy.props.StringProperty(default="target_")
    name_grip_target_scale: bpy.props.StringProperty(default="scale_")
    name_grip_root: bpy.props.StringProperty(default="root_")
    grip_bulge : FloatProperty( default=1, min=0, max=100)
    grip_proximity_join : FloatProperty(default=0.0001,precision=6)

    # Auto Root 
    use_active_bone : BoolProperty(default=True)
    bones_parent : IntProperty(default=2, min=1, max=4)
    name_auto_root : StringProperty(default="root_")
    
    #Collections 
    columns_value : IntProperty(default=2, min=1, max=4)
    even_columns : BoolProperty(default=True)
    how_collection_select : StringProperty()
    edit_collection : BoolProperty()
    search_collection : StringProperty()
    
    #Properties
    use_old_prop : BoolProperty(default=False)
    
    # Bone
    edit_bone : BoolProperty(default=False)
    bone_column : IntProperty(default=1, min=1, max=4)
    bone_subcolumn : IntProperty(default=1, min=1, max=4)
    bone_use_specific_name : BoolProperty(default=False)
    bone_key : StringProperty(default="View")
    search_bone : StringProperty()
    
    # Armature
    edit_armature : BoolProperty(default=False)
    armature_column : IntProperty(default=2, min=1, max=4)
    armature_use_specific_name : BoolProperty(default=True)
    armature_key : StringProperty(default="View")
    search_armature : StringProperty()
    
    # Copy Xform ReationShip
    use_local_space : BoolProperty(default=True)
    is_save : BoolProperty(default=True)
    use_rotation : BoolProperty(default=True)
    use_scale : BoolProperty(default=True)
    
    save_matrix : FloatVectorProperty(
        default=(
            0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0,
            0.0, 0.0, 0.0, 0.0,
            ),
        size = 16,
    )
    is_save_matrix : BoolProperty(default=False)
    
    rot_to_cursor : BoolProperty(default=False)
    
    # PIKER
    piker: EnumProperty(items=[
        ('GENERAL', "General", ""),
        ('FK', "Fk", ""),
        ('IK', "Ik", ""),
        ('DEF', "Def", ""),
        ], 
        name='How Piker', 
        default={'GENERAL'}, 
        options={'ENUM_FLAG'}
        )


    #Mesh 
    
    mesh_bone_name : StringProperty(default="bone")
    mesh_use_curve : BoolProperty(default=True)
    mesh_use_aling_roll_normal : BoolProperty(default=True)
    mesh_bone_subdivisions : IntProperty(default=1, min=1)
    mesh_use_bone_reference : BoolProperty(default=True)
    mesh_bone_reference_name : StringProperty(default="")
    mesh_use_tail : BoolProperty(default=True)
    mesh_use_parent : BoolProperty(default=True)
    mesh_with_automatic_weights : BoolProperty(default=False)
    mesh_with_by_distance_of_vertex : BoolProperty(default=False)
    mesh_keep_object : BoolProperty(default=True)
    
    mesh_use_vertcurve : BoolProperty(default=False)
    mesh_vertcurve_power : FloatProperty(default=0.1)
    
    mesh_normal_global: EnumProperty(items=[
        ('GLOBAL', "Global", ""),
        ('NORMAL', "Normal", ""),
        ], 
        name='How Orientation', 
        default='GLOBAL', 
        )
    
    mesh_direction: EnumProperty(items=[
        ('X', "X", ""),
        ('Y', "Y", ""),
        ('Z', "Z", ""),
        ('-X', "-X", ""),
        ('-Y', "-Y", ""),
        ('-Z', "-Z", ""),
        ], 
        name='LooK Bone', 
        default={'Z'}, 
        options={'ENUM_FLAG'}
    )
    
    #Curve
    curve_bone_name : StringProperty(default="bone")
    curve_use_reference_bone : BoolProperty(default=False)
    curve_reference_bone_name : StringProperty(default="")
    curve_use_control : BoolProperty(default=True)
    
    #BendyBone 
    bendy_bone_invest: BoolProperty(default=False)
    bendybone_type: EnumProperty(items=[
        ('SCALE', "Scale", ""),
        ('ROTATION', "Rotation", ""),
        #('PARENT', "Parent", ""),
        
        ], 
        name='BendyBone Type', 
        default={'ROTATION'}, 
        options={'ENUM_FLAG'}
        )
    
    
    # Node Picker
    #copy propertie
    picker_object_name: bpy.props.StringProperty()
    picker_object_type: bpy.props.StringProperty()
    picker_active_object: bpy.props.StringProperty()
    picker_active_bone: bpy.props.StringProperty()
    picker_active_constraint: bpy.props.StringProperty()
    picker_propertie: bpy.props.StringProperty()
    
    #edit bone
    def set_value(self, context):
        select_bones = self.GetSelectBones(mode="EDIT")
        for bone in select_bones:
            self.AlignBboneToLocalAxis(bone, influence=self.ebone_curve_in_out)
        
        # Reiniciar el valor a 0 después de usarlo
        self["ebone_curve_in_out"] = 0.0  # No dispara el update otra vez

        
    ebone_curve_in_out : FloatProperty(default=0,  update=set_value)
    
    
    
        
    #Annotate_Bone
    annotate_name : StringProperty(default="def-")
    annotate_type_mode: EnumProperty(items=[
        ('MOVE', "Move Active", ""),
        ('ADD', "Add Bone", ""),
        ('REMOVE', "Remove Bone", ""),
        ], 
        name='', 
        default='ADD', 
    )
    
    annotate_use_deform : BoolProperty(default=True)
    annotate_use_vertbone : BoolProperty(default=False)
    annotate_name_vertbone : StringProperty(default="vertex_")
    annotate_use_vertbone_deform : BoolProperty(default=True)

    annotate_segments : IntProperty(default=32, min=1, max=32)
    annotate_use_align_mirror_x: BoolProperty(default=False)
    annotate_use_align_mirror_y: BoolProperty(default=False)
    annotate_use_align_mirror_z: BoolProperty(default=False)
    annotate_use_align_mirror_negative_x: BoolProperty(default=False)
    annotate_use_align_mirror_negative_y: BoolProperty(default=False)
    annotate_use_align_mirror_negative_z: BoolProperty(default=False)
    
    annotate_use_join_bones : BoolProperty(default=True)
    annotate_join_same_name : BoolProperty(default=False)
    annotate_proximity_join : FloatProperty(default=0.01,precision=3)
    
    annotate_global_normal : BoolProperty(default=False)
    annotate_aling_roll_normal : BoolProperty(default=True)
    annotate_size_bbone : FloatProperty(default=0.001,precision=6)
    annotate_auto_bone : BoolProperty(default=False, update= lambda self, context: set_annotate(self, context, "annotate_auto_bone"))
    annotate_use_select_target : BoolProperty(default=False)
    def only_mesh_objects(self, obj) -> bool:
        return obj.type == 'MESH'
    annotate_target : PointerProperty(type=bpy.types.Object, poll=only_mesh_objects)
    annotate_direction: EnumProperty(items=[
        ('X', "X", ""),
        ('Y', "Y", ""),
        ('Z', "Z", ""),
        ('-X', "-X", ""),
        ('-Y', "-Y", ""),
        ('-Z', "-Z", ""),
        ], 
        name='LooK roll Bone', 
        default={'Z'}, 
        options={'ENUM_FLAG'}
    )
    annotate_use_curve : BoolProperty(default=True)
    annotate_curve_power : FloatProperty(default=1,precision=3)
    annotate_use_parent : BoolProperty(default=False)
    annotate_use_connect : BoolProperty(default=False)
    
    #Annotate_Animation
    annotate_posebone : BoolProperty(default=False,  update= lambda self, context: set_annotate(self, context, "annotate_posebone") ) 
    

class RGC_ViewSelect_Grups(GeneralArmatureData, bpy.types.PropertyGroup):
    bone : bpy.props.StringProperty()
    
class RGC_PoseBone_GrupsProps(GeneralArmatureData, bpy.types.PropertyGroup):
    view_select : bpy.props.CollectionProperty(type=RGC_ViewSelect_Grups)
    view_select_index : IntProperty(min=0,options={'HIDDEN'},)