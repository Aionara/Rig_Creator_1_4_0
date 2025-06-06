from .bone import *
from .vector2d import *
from .picker import *
from .properties import *
from .scene import *
from .constraint import *
classes = (
    #Sockets
    RGC_Socket_Bone,
    RGC_Socket_Vector2d,
    RGC_Socket_Picker,
    RGC_Socket_Properties,
    RGC_Socket_Scene,
    RGC_Socket_Constraint,
    
    #operator
    RGC_Operator_AddInput,
)

def PickerSocketRegister():
    for cls in classes:
        bpy.utils.register_class(cls)

def PickerSocketUnregister():
    for cls in classes :
        bpy.utils.unregister_class(cls)

