import bpy
import mathutils
import math

#Funcition Generales Pasa usar durante la creacion del acuto rig
class GeneralArmatureData : 
    
    
    def AddCollection(self,):
        
        SaveObj = self.GetActiveObject()
        self.SetMode("OBJECT")
        self.Collection_Name = "RIG_CREATOR_Material"
        
        def create_empty(empty_type, collection):
            empty = bpy.data.objects.new(f"Materiales_RIG_CREATOR_{empty_type}", None)
            empty.empty_display_type = empty_type
            collection.objects.link(empty)
            return empty
        
        def get_empty(empty_type : str):
           
            return bpy.data.objects.get(f"Materiales_RIG_CREATOR_{empty_type}")
                
        if self.IsCollectionExists() :
            
            GetCollection = bpy.data.collections.get(self.Collection_Name)
            if GetCollection :
                
                self.EMPTY_Arrow = get_empty('SINGLE_ARROW')
                if self.EMPTY_Arrow == None: 
                    self.EMPTY_Arrow = create_empty('SINGLE_ARROW', GetCollection)
                self.EMPTY_Circle = get_empty('CIRCLE')
                if self.EMPTY_Circle == None: 
                    self.EMPTY_Circle = create_empty('CIRCLE', GetCollection)
                self.EMPTY_Cube = get_empty('CUBE')
                if self.EMPTY_Cube == None: 
                    self.EMPTY_Cube = create_empty('CUBE', GetCollection)
                self.EMPTY_Sphere = get_empty('SPHERE')
                if self.EMPTY_Sphere == None: 
                    self.EMPTY_Sphere = create_empty('SPHERE', GetCollection)
                self.EMPTY_Axes = get_empty('PLAIN_AXES')
                if self.EMPTY_Axes == None: 
                    self.EMPTY_Axes = create_empty('PLAIN_AXES', GetCollection)
                self.EMPTY_Arrows = get_empty('ARROWS') 
                if self.EMPTY_Arrows == None: 
                    self.EMPTY_Arrows = create_empty('ARROWS', GetCollection)
        else :

            if self.Collection_Name not in bpy.data.collections:
                
                nueva_coleccion = bpy.data.collections.new(self.Collection_Name)
                bpy.context.scene.collection.children.link(nueva_coleccion)
                colección_op = bpy.data.collections.get(self.Collection_Name)

                
                
                if colección_op:
                    for i in range(6):

                        if i == 0:
                            self.EMPTY_Arrow = create_empty('SINGLE_ARROW', colección_op)
                        elif i == 1:
                            self.EMPTY_Circle = create_empty('CIRCLE', colección_op)
                        elif i == 2:
                            self.EMPTY_Cube = create_empty('CUBE', colección_op)
                        elif i == 3:
                            self.EMPTY_Sphere = create_empty('SPHERE', colección_op)
                        elif i == 4:
                            self.EMPTY_Axes = create_empty('PLAIN_AXES', colección_op)
                        elif i == 5:
                            self.EMPTY_Arrows = create_empty('ARROWS', colección_op)

  
                colección_op.hide_viewport = True
                colección_op.hide_render = True

        self.ActiveObj(SaveObj)
    
    
    def AlingBboneToNormal(self, bone_edit, normal, influence=1.0):
        
        # Normaliza el vector normal
        normal = normal.normalized()
        
        y_axis = bone_edit.y_axis
        x_axis = bone_edit.x_axis
        z_axis = bone_edit.z_axis
        
        # Calcula la dirección local del hueso (eje Y, que es hacia adelante en el hueso)
        bone_dir = y_axis.normalized()

        # Proyectamos la normal en el plano perpendicular a la dirección del hueso
        # (Para evitar que la normal afecte la dirección longitudinal del B-Bone)
        tangent = normal - (normal.dot(bone_dir)) * bone_dir
        tangent.normalize()

        # Calculamos los componentes X y Z en el espacio local del hueso
        x_component = tangent.dot(x_axis) * influence
        z_component = tangent.dot(z_axis) * influence

        # Aplicamos los valores a las propiedades de curva del B-Bone
        bone_edit.bbone_curveinx = x_component 
        bone_edit.bbone_curveinz = z_component 
        bone_edit.bbone_curveoutx = x_component
        bone_edit.bbone_curveoutz = z_component 

    def AlignBboneToLocalAxis(self, bone_edit, axis='Z', influence=1.0):
        # Ejes locales del hueso
        y_axis = bone_edit.y_axis  # dirección del hueso
        x_axis = bone_edit.x_axis
        z_axis = bone_edit.z_axis

        # Escoge el eje objetivo
        if axis.upper() == 'Z':
            target_dir = z_axis
        elif axis.upper() == 'X':
            target_dir = x_axis
        else:
            return

        # Calculamos el vector tangente: la parte del eje objetivo que es perpendicular al eje Y del hueso
        tangent = (target_dir - target_dir.project(y_axis)).normalized()

        # Proyectamos esa dirección en los ejes X y Z locales del hueso
        x_component = tangent.dot(x_axis) * influence
        z_component = tangent.dot(z_axis) * influence

        # Aplicamos las curvas B-Bone
        bone_edit.bbone_curveinx = x_component
        bone_edit.bbone_curveinz = z_component
        bone_edit.bbone_curveoutx = x_component
        bone_edit.bbone_curveoutz = z_component


# Ejemplo de uso:
# align_bbone_to_normal("Bone", (1, 0, 0))  # Alinea el B-Bone a la normal (1, 0, 0)
    
    def ChangeIcon(self, Icon_a : str, Icon_b : str, Value : bool) -> str:
        return Icon_a if Value == True else Icon_b
    
    def ActiveObj(self, Obj, use_deselect = True) : 
        if Obj:
            if use_deselect :
                bpy.ops.object.select_all(action='DESELECT')
            Obj.select_set(True)
            bpy.context.view_layer.objects.active = Obj
    
    def ActiveBone(self, Bone_Name, mode="EDIT", use_deselect : bool = False):
        armature = self.GetArmature()
        """
        Mode = EDIT and POSE
        """
        if mode == "EDIT":
            # Obtener el hueso en modo edición
            bone = self.GetBone(Bone_Name, mode=mode)
            if bone:
                if not use_deselect:
                    # Seleccionar y activar el hueso
                    bone.select = True
                    armature.edit_bones.active = bone
                else:
                    bone.select = False
                    armature.edit_bones.active = None
                    
        elif mode == "POSE":
            # Obtener el hueso en modo pose
            bone = self.GetBone(Bone_Name, mode=mode)
            if bone:
                # Seleccionar y activar el hueso
                if not  use_deselect:
                    bone.bone.select = True
                    armature.bones.active = bone.bone
                else:
                    bone.bone.select = False
                    armature.bones.active = None
    
    def SelectBones(self, Bones, mode ="EDIT") : 
        bones = self.GetSelectBones(mode=mode)
        for bone in bones : 
            if mode == "EDIT" : 
                bone.select = False
            else :
                bone.bone.select = False
        for bone in Bones : 
            if mode == "EDIT" : 
                bone.select = True
            else :
                bone.bone.select = True
        self.ActiveBone(Bones[-1].name, mode=mode)
    
    def NIndexList(self, i, List : list):
        return i if i <= len(List)-1 else -1
    
    
    def BoneCollectionAssing(self, collection_name : str, bone : object) : 
        col = self.GetActiveObject().data.collections.get(collection_name)
        if col :
            col.assign(bone)
    
    # IS
    def IsCollectionExists(self) -> bool:
        return True if bpy.data.collections.get(self.Collection_Name) else False
    
    def IsArmatureExists(self) -> bool:
        return self.GetActiveObject() and self.GetActiveObject().type == "ARMATURE"
    
    def IsCollectionToRigCreatorExists(self):
        if self.GetCollectionsNames() == self.ListCollectionToArmature() : return True
        return False
    
    def isBonesExists(self, Bones_name : list) -> bool :
        for name in Bones_name :
            if self.IsBoneExists(name) : return True
        return False
    
    def IsBoneExists(self, Bone_Name : str) -> bool: 
        Bone = self.GetActiveObject().data.bones.get(Bone_Name)
        return True if Bone else False
    
    # LIST
    
    def ListIconConstraint(self) -> list:
        return {
            'CAMERA_SOLVER': 'CON_CAMERASOLVER',
            'FOLLOW_TRACK': 'CON_FOLLOWTRACK',
            'OBJECT_SOLVER': 'CON_OBJECTSOLVER',
            'COPY_LOCATION': 'CON_LOCLIKE',
            'COPY_ROTATION': 'CON_ROTLIKE',
            'COPY_SCALE': 'CON_SIZELIKE',
            'COPY_TRANSFORMS': 'CON_TRANSLIKE',
            'LIMIT_DISTANCE': 'CON_DISTLIMIT',
            'LIMIT_LOCATION': 'CON_LOCLIMIT',
            'LIMIT_ROTATION': 'CON_ROTLIMIT',
            'LIMIT_SCALE': 'CON_SIZELIMIT',
            'MAINTAIN_VOLUME': 'CON_SAMEVOL',
            'TRANSFORM': 'CON_TRANSFORM',
            'TRANSFORM_CACHE': 'CON_TRANSFORM_CACHE',
            'CLAMP_TO': 'CON_CLAMPTO',
            'DAMPED_TRACK': 'CON_TRACKTO',
            'IK': 'CON_KINEMATIC',
            'LOCKED_TRACK': 'CON_LOCKTRACK',
            'SPLINE_IK': 'CON_SPLINEIK',
            'STRETCH_TO': 'CON_STRETCHTO',
            'TRACK_TO': 'CON_TRACKTO',
            'ACTION': 'ACTION',
            'ARMATURE': 'CON_ARMATURE',
            'CHILD_OF': 'CON_CHILDOF',
            'FLOOR': 'CON_FLOOR',
            'FOLLOW_PATH': 'CON_FOLLOWPATH',
            'PIVOT': 'CON_PIVOT',
            'SHRINKWRAP': 'CON_SHRINKWRAP',
        }
    
    def ListNodeSocket(self) -> list : 
        return {
            
            "bool": "NodeSocketBool",
            "collection": "NodeSocketCollection",
            "color": "NodeSocketColor",
            "float": "NodeSocketFloat",
            "float_angle": "NodeSocketFloatAngle",
            "float_distance": "NodeSocketFloatDistance",
            "float_factor": "NodeSocketCCFloatFactor",
            "float_percentage": "NodeSocketFloatPercentage",
            "float_time": "NodeSocketFloatTime",
            "float_time_absolute": "NodeSocketFloatTimeAbsolute",
            "float_unsigned": "NodeSocketFloatUnsigned",
            "geometry": "NodeSocketGeometry",
            "image": "NodeSocketImage",
            "int": "NodeSocketInt",
            "int_factor": "NodeSocketIntFactor",
            "int_percentage": "NodeSocketIntPercentage",
            "int_unsigned": "NodeSocketIntUnsigned",
            "material": "NodeSocketMaterial",
            "object": "NodeSocketObject",
            "rotation": "NodeSocketRotation",
            "shader": "NodeSocketShader",
            "string": "NodeSocketString",
            "texture": "NodeSocketTexture",
            "vector": "NodeSocketVector",
            "vector_acceleration": "NodeSocketVectorAcceleration",
            "vector_direction": "NodeSocketVectorDirection",
            "vector_euler": "NodeSocketVectorEuler",
            "vector_translation": "NodeSocketVectorTranslation",
            "vector_velocity": "NodeSocketVectorVelocity",
            "vector_xyz": "NodeSocketVectorXYZ",
            "virtual": "NodeSocketVirtual",
            
            "constraint" : "RGC_Socket_Constraint"
        }
    

    def ListFinger(self) -> list:
        return [
            "Thumb",
            "Index Finger",
            "Middle Finger",
            "Ring Finger",
            "Pinky",
        ]
    
    def ListGenerators(self) -> list:
        return [
            "Physics",
            "Fingers",
            "Ik",
            "Fk",
            "Bones",
            "Curve",
            "Auto_Root",
            "Add_Collection_Of_Material",
        ]
        
    def ListCollectionToArmature(self,) -> list[str]:
        return [
            "Head", 
            "torso", 
            "Arm_R",
            "Arm_DEF_R",
            "Arm_FK_R",
            "Arm_IK_R",
            "Hands_R",
            "Hands_DEF_R",
            "Hands_FK_R",
            "Hands_IK_R",
            "Leg_R",
            "Leg_DEF_R",
            "Leg_FK_R",
            "leg_IK_R",
            "Roots",
            "Deformation_Bone",
            "Base_Body",
            
            "Head_Def",
            "torso_Def",
            "Arm_L", 
            "Arm_DEF_L",
            "Arm_FK_L",
            "Arm_IK_L", 
            "Hands_L",
            "Hands_DEF_L",
            "Hands_FK_L",
            "Hands_IK_L", 
            "Leg_L",
            "Leg_DEF_L",
            "Leg_FK_L",
            "leg_IK_L",
            "SubRoots",
            "Control_Bone",
            "Base_Face"
        ]
    
    # Function GET
    def GetNode(self, context, name) -> object: 
        space = context.space_data
        if not space or not hasattr(space, 'edit_tree') or not space.edit_tree:
            self.report({'ERROR'}, "No Node Tree found in context")
            return {'CANCELLED'}

        node_tree = space.edit_tree
        node = node_tree.nodes.get(name)
        return node
    
    def get_constraint(self, context):
        if context.space_data.context == 'BONE_CONSTRAINT' and context.mode == 'POSE':
            # Check for bone constraints in pose mode
            bone = context.active_pose_bone
            if bone:
                return bone.constraints[bone.active_constraint]
        else:
            # Check for bone constraints in pose mode
            object = context.active_object
            if object:
                return object.constraints[object.active_constraint]
        return None
    
    def GetConstraintActive(self, Obj : object) -> object:
        if not Obj.constraints : return None
        if Obj.active_constraint > len(Obj.constraints)-1 or Obj.active_constraint < 0: return None
        return Obj.constraints[Obj.active_constraint]
        
    
    def GetWorldNormal(self, Eje: str = "z") -> mathutils.Vector:
        eje_dict = {
            "x": (1, 0, 0),
            "-x": (-1, 0, 0),
            "y": (0, 1, 0),
            "-y": (0, -1, 0),
            "z": (0, 0, 1),
            "-z": (0, 0, -1)
        }

        return mathutils.Vector(eje_dict.get(Eje, (0, 0, 0)))
    
    
    
    def GetScene(self) -> object:
        return bpy.context.scene
    
    def GetOnlyOneSelectableObject(self) -> object:
        for obj in self.GetSelectableObjects():
            return obj
        return None
    
    def GetActiveObject(self) -> object:
        return bpy.context.active_object
    
    
    def GetArmature(self) -> object:
        return self.GetActiveObject().data if self.GetActiveObject() and self.GetActiveObject().type == "ARMATURE" else None
    
    def GetSelectableObjects(self) -> list:
        return bpy.context.selected_objects
        
    def GetNameToBones(self, Bones : list) -> list:
        
        bones = []
        for bone in Bones:
            if bone : bones.append(bone.name)
        return bones

    def GetObjMode(self) -> str:
        return self.GetActiveObject().mode
    
    def GetSelectBones(self, mode : str = "EDIT", only_select : bool = False) -> list:
        bones = []
        if mode == "EDIT":
            for bone in bpy.context.selected_editable_bones :
                if only_select : 
                    if bone != bpy.context.active_bone:
                        bones.append(bone)
                else : 
                    bones.append(bone)
            
        elif mode == "POSE":
            for bone in bpy.context.selected_pose_bones :
                if only_select : 
                    if bone != bpy.context.active_pose_bone:
                        bones.append(bone)
                else : 
                    bones.append(bone)
        return bones
    def GetActiveBone(self, mode : str = "POSE") -> object:
        if mode == "POSE": 
            return bpy.context.active_pose_bone
        elif mode == "EDIT" : 
            return bpy.context.active_bone
        else : 
            return None
    
    # Emproseso 
    def ChangeTheBonesMode(self, Bones : list, mode : str = "OBJECT"):
        
        bones = []
        bones_names = []
        
        if not Bones : return 
        
        for b in Bones : 
            bones_names.append(b.name)
        
        if mode == 'OBJECT':
            bone_source = self.GetActiveObject().data.bones
        elif mode == 'POSE':
            bone_source = self.GetActiveObject().pose.bones
        elif mode == 'EDIT':
            bone_source = self.GetActiveObject().data.edit_bones
            
        self.SetMode(mode)
        for b in bones_names : 
            bone = bone_source.get(b)
            bones.append(bone)
            
        return bones 
    
    
    def GetBonesToRange(self, Bone_Name : str, Range : int = 0, mode : str = "OBJECT") -> list:
        Range_Bones = [f"{Bone_Name}.{i+1:003}" for i in range(Range)]
        Bones = self.GetBones(Range_Bones, mode=mode)
        return Bones
    
    def GetBone(self, Bone_Name : str, mode: str = 'OBJECT') -> object:
        bones = []
        
        if mode == 'OBJECT':
            bone_source = self.GetActiveObject().data.bones
        elif mode == 'POSE':
            bone_source = self.GetActiveObject().pose.bones
        elif mode == 'EDIT':
            bone_source = self.GetActiveObject().data.edit_bones
        else:
            raise ValueError("Modo no válido. Usa 'object', 'pose' o 'edit'.")

        return bone_source.get(Bone_Name)
    
    def GetBones(self, Bones_Names: list[str], mode: str = 'OBJECT') -> list:
        bones = []
        
        if mode == 'OBJECT':
            bone_source = self.GetActiveObject().data.bones
        elif mode == 'POSE':
            bone_source = self.GetActiveObject().pose.bones
        elif mode == 'EDIT':
            bone_source = self.GetActiveObject().data.edit_bones
        else:
            raise ValueError("Modo no válido. Usa 'object', 'pose' o 'edit'.")

        for name in Bones_Names:
            bone = bone_source.get(name)
            if bone:
                bones.append(bone)
        
        return bones

    def GetBonesNamesInCollection(self, Col_Name : str) -> list[str]:
        bones_name = []
        for bone in self.GetCollectionToName(Col_Name).bones:
            bones_name.append(bone.name)
        return bones_name
    
    def GetBonesInCollection(self, Col_Name : str) -> list:
        bones = []
        for bone in self.GetCollectionToName(Col_Name).bones:
            bones.append(bone)
        return bones
    

    def GetCollectionToName(self, Col_Name : str) :
        return self.GetActiveObject().data.collections_all.get(Col_Name)
    
    def GetCollectionsNames(self) -> list[str]:
        Col = []
        for c in self.GetCollections():
            Col.append(c.name)
        return Col

    
    def GetCollections(self) -> list:
        if  not self.IsArmatureExists() : return []
        if hasattr(self.GetActiveObject().data, "collections_all"):
            return self.GetActiveObject().data.collections_all
        else:
            return self.GetActiveObject().data.collections

    def GetPropertiesToObject(self, Obj, filter = {},  filter_base = {},  invert_filter : bool = False, type = "keys") -> list:
        p = []
        if type == "keys" :
            for k in Obj.keys():
                if k in filter_base : continue
                if invert_filter == False:
                    if k not in filter:
                        p.append(k)
                else:
                    if k in filter:
                        p.append(k)
        elif type == "items":
            for k in Obj.items():
                if k[0] in filter_base : continue
                if invert_filter == False:
                    if k[0] not in filter:
                        p.append(k)
                else:
                    if k[0] not in filter:
                        p.append(k)
        return p
    
    
    def GetDistancia3d(self, v1, v2):
        # v1 y v2 son tuplas o listas de tres elementos (x, y, z)
        return math.sqrt((v2[0] - v1[0])**2 + (v2[1] - v1[1])**2 + (v2[2] - v1[2])**2)

    def GetMatrixToSave(self):
        return self.Matrix
    
    def GetMeshSelectMode(self, mode : str = "VERT") -> bool:
        """
        mode : str = "VERT", "EDGE", "FACE"
        """
        list_mode = {
            "VERT" : 0,
            "EDGE" : 1,
            "FACE" : 2
        }
        return bpy.context.tool_settings.mesh_select_mode[list_mode[mode]]
    
    # Function SET
    
    def SetMode(self, mode : str):
        if self.GetActiveObject() : 
            bpy.ops.object.mode_set(mode=mode)
    

    # Para Igualar el Displat Size de los Huesos
    def SetDisplaySize(
        self,
        Bone_A, Bone_B,  
        Display_size_x = 1, Display_size_y = 1):
        Bone_A.bbone_x = Bone_B.bbone_x * Display_size_x
        Bone_A.bbone_z = Bone_B.bbone_z * Display_size_y


    def SetTransformToAxis(self, Bone_A : object, Bone_B : object, How_Axis : str = "z", length_value = 1, roll_value = 1):
        
        axis = getattr(Bone_B, f"{How_Axis}_axis")
        if not axis : return
        Bone_A.tail = axis
        self.SetTransform(
            Bone_A, Bone_B, use_tail=False, length_value=length_value,
            roll_value=roll_value
        )

    def SetTransformToBones(
        self, Bones_A : list, Bones_B : list, 
        use_head = True, head_value = 1, use_tail = True, tail_value = 1, 
        use_roll = True, roll_value = 1, use_length = True, length_value = 1,
        only_tail = False
        ) :
        for i in range(len(Bones_A)):
            self.SetTransform(Bones_A[i], Bones_B[i],
            use_head = use_head, head_value = head_value, use_tail = use_tail, tail_value = tail_value, 
            use_roll = use_roll, roll_value = roll_value, use_length = use_length, length_value = length_value,
            only_tail = only_tail
            )

        
    def SetTransform(
        self, Bone_A, Bone_B, 
        use_head = True, head_value = 1, use_tail = True, tail_value = 1, 
        use_roll = True, roll_value = 1, use_length = True, length_value = 1,
        only_tail = False, invert_head_tail : bool = False
        ) : 
        if only_tail :
            Bone_A.head = Bone_B.head 
            Bone_A.tail = Bone_B.tail 
            Bone_A.length *= 2
            Bone_A.head = Bone_B.tail
            if use_roll : Bone_A.roll = Bone_B.roll * roll_value
            if use_length : Bone_A.length = Bone_B.length * length_value
            return
        if invert_head_tail == False :
            if use_head : Bone_A.head = Bone_B.head * head_value
            if use_tail : Bone_A.tail = Bone_B.tail * tail_value
        else:
            if use_head : Bone_A.head = Bone_B.tail * head_value
            if use_tail : Bone_A.tail = Bone_B.head * tail_value
        if use_roll : Bone_A.roll = Bone_B.roll * roll_value
        if use_length : Bone_A.length = Bone_B.length * length_value

    def SetPoleTransform(self, Bone_A, Bones_B: list, Distance : float = 1):
        Z_axis = mathutils.Vector((0, 0, 0))
        Head = mathutils.Vector((0, 0, 0))
        Tail = mathutils.Vector((0, 0, 0))
        
        Save_Length = Bone_A.length
        for bone in Bones_B:
            Z_axis += bone.z_axis.normalized()
            Head += bone.head
            Tail += bone.tail

        Bone_A.head = ((Head+Tail)/2) / len(Bones_B)
        Bone_A.tail = Bone_A.head + (Z_axis / len(Bones_B))*-1
        Save_Head = Bone_A.tail
        direction = (Bone_A.tail - Bone_A.head).normalized()
        Bone_A.tail = Bone_A.head + direction * (Distance)
        Save_Tail = Bone_A.tail
        Bone_A.head = Save_Head
        Bone_A.tail = Save_Tail
        Bone_A.length = Save_Length
  
        
    def SetReDrawViewPort(self, iterarions : int = 1):
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=iterarions)
    
    def SetColorBone(self, Bone, type_palette : str = 'THEME01'):
        Bone.color.palette = type_palette

    def SetDeform(self, Bones : list, Value : bool = False):
        for bone in Bones :
            bone.use_deform = Value
    
    def SetRelationsOnlyOneList(self, Bones : list, Use_connect : bool = False):
        for i in range(len(Bones)-1) :
            self.SetRelations(Bones[i+1], Bones[i], Use_connect=Use_connect)
            
    def SetRelations(self, Bone_A, Bone_B, Use_connect : bool = False) :
        Bone_A.parent = Bone_B
        Bone_A.use_connect = Use_connect

    def RemoveBones(self, Bones_Names : list[str]):
        if self.GetActiveObject().mode != "EDIT" : self.SetMode(mode="EDIT")
        for name in Bones_Names:
            bone = self.GetActiveObject().data.edit_bones.get(name)
            self.GetActiveObject().data.edit_bones.remove(bone)


    # Create
    
    def CreateConstraint(self, bone : object, type : str, name : str, target : object, subtarget : object, owner_space : str, target_space : str) -> object:
        # Crear un nuevo constraint en el objeto
        constraint = bone.constraints.new(type=type)
        constraint.name = name
        constraint.target = target
        if target.type == "ARMATURE":
            constraint.subtarget = subtarget.name
        else :
            constraint.subtarget = subtarget
        constraint.owner_space = owner_space
        constraint.target_space = target_space
        
        return constraint
        

    def CreateVector(self, x, y, z) :
        return mathutils.Vector((x, y, z))
    
    def CreatreDrive(
        self, Obj : object, Propertie : str, Control_Obj : object, Control_Propertie : str,  Use_Bone : bool = False, 
        Use_Expression : bool = False, Expression : str = "-1", index: int = -1):
        # Agregar un controlador (driver) a la propiedad del objeto
        if index >= 0:
            driver = Obj.driver_add(Propertie, index).driver
        else:
            driver = Obj.driver_add(Propertie).driver

        driver.type = 'SCRIPTED'
        
        # Crear una nueva variable para el driver
        var = driver.variables.new()
        var.name = "var"
        var.targets[0].id_type = "OBJECT"
        var.targets[0].id = self.GetActiveObject()
        
        # Si se está usando un hueso, agregar la ruta correspondiente
        if Use_Bone:
            var.targets[0].data_path = f'pose.bones["{Control_Obj.name}"].{Control_Propertie}'
        else:
            # Si no es un hueso, asignar la propiedad directamente
            var.targets[0].data_path = Control_Propertie
        

        if Use_Expression : driver.expression = "var" + Expression
        else : driver.expression = "var"
       
    
    def CreateSocket(self, type : str, name : str, use_outputs : bool = False) -> object: 
        if not use_outputs : return self.outputs.new(type, name)
        else : return self.inputs.new(type, name)
    
    def CreateBonesName(self, Base_Name : str, Range : int) -> list:
        bone_name = []
        for i in range(Range):
            bone_name.append(f"{bone_name}.{i+1:003}")
        return bone_name
    
    def CreateBonesRange(self, Bone_Name : str, Range : int) -> list:
        bones = []
        if self.GetActiveObject().mode != "EDIT":
            self.SetMode(mode="EDIT")
        for i in range(Range) :
            bpy.ops.armature.bone_primitive_add(name=f"{Bone_Name}.{i+1:003}")
            bones.append(list(self.GetActiveObject().data.edit_bones)[-1])
        return bones

    def CreateBones(self, Bones_Names : list[str]) -> list:
        bones = []
        if self.GetActiveObject().mode != "EDIT":
            self.SetMode(mode="EDIT")
        for name in Bones_Names :
            bpy.ops.armature.bone_primitive_add(name=name)
            bones.append(list(self.GetActiveObject().data.edit_bones)[-1])
        return bones

    

    def CreateMatrix(self, location : mathutils, rotation_euler, scale : mathutils):
        # Valores de ejemplo para la ubicación, rotación y escala
        location = location  # Posición del hueso
        rotation_euler = mathutils.Euler(rotation_euler, 'XYZ')  # Rotación en ángulos Euler
        scale = scale  # Escala del hueso

        # Crear matrices individuales
        translation_matrix = mathutils.Matrix.Translation(location)
        rotation_matrix = rotation_euler.to_matrix().to_4x4()
        scale_matrix = mathutils.Matrix.Diagonal(scale).to_4x4()

        # Combinar las matrices (traslación * rotación * escala)
        transform_matrix = translation_matrix @ rotation_matrix @ scale_matrix
        return transform_matrix

    def MatrixMedFor(self, matrix1, matrix2):
        # Obtener componentes de traslación, rotación y escala de cada matriz
        loc1, rot1, scale1 = matrix1.decompose()
        loc2, rot2, scale2 = matrix2.decompose()
        
        # Promediar las ubicaciones (Vector)
        avg_loc = (loc1 + loc2) / 2
        
        # Promediar las rotaciones (Quaternion)
        avg_rot = rot1.slerp(rot2, 0.5)
        
        # Promediar las escalas (Vector)
        avg_scale = (scale1 + scale2) / 2
        
        # Crear una nueva matriz a partir de los componentes promediados
        new_matrix = (
            mathutils.Matrix.Translation(avg_loc) @  # Traslación
            avg_rot.to_matrix().to_4x4() @           # Rotación
            mathutils.Matrix.Diagonal(avg_scale).to_4x4()  # Escala
        )
        
        return new_matrix
    
    def PropsToArmature(self):
        return bpy.context.active_object.RGC_Armature_GrupsProps
    
    def Props(self):
        return bpy.context.scene.RGC_GrupsProps
    
   #def PoseBoneProps(self):
   #    return self.GetActiveBone("POSE").rgc_props
    
    def UseMirror(self, use : bool) : 
        self.GetActiveObject().data.use_mirror_x = use
    
    def SearchInList(self, Name_A, Name_B,) -> bool:
        return bool(Name_A.lower() in Name_B.lower() or Name_A.lower() in "")


    def UpdateViewLayer(self):
        bpy.context.view_layer.update()


    # Draw Function 
    
    def Panel(self,layout, Type : str,  Label : str, Icon : str, Default_Closed : bool = False) -> bool:
        
        col = layout.column(align=True) 
        layout_header, layout_body = col.panel(Type, default_closed=Default_Closed)
        if Icon != "":
            layout_header.label(text=Label,icon=Icon)
        else :
            layout_header.label(text=Label)
        col.column(align=True)
        return True if layout_body else False
    
    def LabelParagraph(self, layout , texts : list = []) : 
        for t in texts :
            layout.label(text=t)
    
    def ShadowBox(self, layout, size_x : float = 1, size_y : float = 1):
        box = layout.box()
        [box.scale_x, box.scale_y] = [size_x, size_y]
        

    def SplitBonesForParent(self, list_Bones: list) -> list:
        # Lista para almacenar las partes divididas
        partes_bones = []
        
        # Lista para mantener un seguimiento de los huesos ya agrupados
        huesos_vistos = set()

        # Función recursiva para agrupar huesos por jerarquía de padres
        def agrupar_bones_por_parent(bone):
            # Esta función recursiva encuentra todos los huesos que tienen el mismo parent
            grupo_bones = [bone]
            for other_bone in list_Bones:
                if other_bone.parent == bone and other_bone not in huesos_vistos:
                    huesos_vistos.add(other_bone)
                    grupo_bones.extend(agrupar_bones_por_parent(other_bone))  # Llamada recursiva
            return grupo_bones

        # Recorrer todos los huesos seleccionados
        for bone in list_Bones:
            if bone not in huesos_vistos:
                huesos_vistos.add(bone)
                grupo = agrupar_bones_por_parent(bone)
                partes_bones.append(grupo)

        # Devolver las partes de huesos divididos en un arreglo
        return partes_bones
    
    def PanelType(self, type : list = []):
        props = self.Props()
        return props.panel_type in type
    
    def GN_Name(self, new_name , bone_name : str) -> str : 
        get_name = bone_name[-4:]
        list_name = (f".{i:003}" for i in range(100))
        t_name : str = bone_name
        if get_name in list_name:
            t_name = bone_name[:-4]
        return new_name + t_name
    
    
    def WithDistanceWeights(self, object : object, armature_obj: object):
        def get_global_vertex_position(obj, vertex):
            """Devuelve la posición global de un vértice"""
            return obj.matrix_world @ vertex.co

        def get_global_bone_position(armature_obj, bone_name):
            """Devuelve la posición global de un hueso en modo pose"""
            bone = armature_obj.pose.bones.get(bone_name)
            if bone:
                return armature_obj.matrix_world @ bone.head
            return None

        def create_vertex_group(obj, bone_name):
            """Crea un grupo de vértices basado en el nombre del hueso si no existe"""
            if bone_name not in obj.vertex_groups:
                obj.vertex_groups.new(name=bone_name)

        def move_vertex_to_nearest_bone(obj, armature_obj):
            """Mueve los vértices del objeto hacia los huesos más cercanos y asigna vértices a grupos"""
            # Asegúrate de estar en modo de edición
            if obj.mode != 'EDIT':
                bpy.ops.object.mode_set(mode='EDIT')

            # Cambiar a modo objeto temporalmente para acceder a la malla y los vértices
            bpy.ops.object.mode_set(mode='OBJECT')
            
            # Recorrer los vértices del objeto
            for vertex in obj.data.vertices:
                vertex_global_pos = get_global_vertex_position(obj, vertex)
                min_distance = float('inf')
                closest_bone = None

                # Recorrer los huesos del armature para encontrar el más cercano
                for bone in armature_obj.pose.bones:
                    bone_global_pos = get_global_bone_position(armature_obj, bone.name)
                    if bone_global_pos:
                        distance = (bone_global_pos - vertex_global_pos).length
                        if distance < min_distance:
                            min_distance = distance
                            closest_bone = bone

                # Si encontramos un hueso cercano, movemos el vértice a su posición y lo asignamos a su grupo
                if closest_bone:
                    # Crear el grupo de vértices si no existe
                    create_vertex_group(obj, closest_bone.name)
                    
                    # Asignar el vértice al grupo del hueso más cercano con peso 1.0
                    group = obj.vertex_groups[closest_bone.name]
                    group.add([vertex.index], 1.0, 'REPLACE')

            # Volver al modo objeto al final
            bpy.ops.object.mode_set(mode='OBJECT')

        # Ejecutar la función para mover los vértices al hueso más cercano
        move_vertex_to_nearest_bone(object, armature_obj)

class CreateFakeBone : 
    
    def __init__(self, head, tail, roll, length):
        self.head = head
        self.tail = tail 
        self.roll = roll
        self.length = length
        
        
