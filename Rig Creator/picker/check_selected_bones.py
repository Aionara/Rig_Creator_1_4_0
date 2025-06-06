import bpy

last_selected_bones = set()
last_armature = None

# Variable global para rastrear selección previa
last_selected_bones = set()

Set_FSB = [
    
]

def CheckSelectedBones():
    global last_selected_bones

    obj = bpy.context.object

    if obj and obj.type == 'ARMATURE':
        if obj.mode == 'POSE':
            selected = {bone.name for bone in obj.pose.bones if bone.bone.select}
        elif obj.mode == 'EDIT':
            selected = {bone.name for bone in obj.data.edit_bones if bone.select}
        else:
            return 0.2

        if selected != last_selected_bones:
            OnBoneSelected(selected)
            last_selected_bones = selected

    return 0.2 

def OnBoneSelected(selected_bones):
    for f in Set_FSB:
        f(selected_bones)
    


