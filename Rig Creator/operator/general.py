
import bpy
from ..generaldata import *
from types import SimpleNamespace
import bmesh
from mathutils import Vector

"""
Operaciones Generales que utiliso en diferentes Operadores
"""

Matrix = None

class OperatorGeneral(GeneralArmatureData):
    
        
    
    def SetContBendyBone(self):
        
        try :
        
            if self.GetObjMode() != "POSE" : return
            act_bone = self.GetActiveBone(mode="POSE")
            select_bone = self.GetSelectBones(mode="POSE")
            prop = self.Props()
            
            if act_bone and select_bone: 
                for bone in select_bone[:]:
                    if bone == act_bone : 
                        select_bone.remove(bone)
                        
                if prop.bendybone_type != {"PARENT"} :
                    selct_bones_1 = select_bone[0] if not prop.bendy_bone_invest else select_bone[1]
                    selct_bones_2 = select_bone[1] if not prop.bendy_bone_invest else select_bone[0]
            
                if prop.bendybone_type == {"ROTATION"} :

                    act_bone = self.GetBone(act_bone.name, mode="OBJECT")
                    act_bone.bbone_handle_type_start = 'TANGENT'
                    act_bone.bbone_handle_type_end = 'TANGENT'
                    act_bone.bbone_handle_use_ease_start = True
                    act_bone.bbone_handle_use_ease_end  = True
                    act_bone.bbone_custom_handle_start = self.GetBone(selct_bones_1.name, mode="OBJECT")
                    act_bone.bbone_custom_handle_end = self.GetBone(selct_bones_2.name, mode="OBJECT")
                
                elif prop.bendybone_type == {"SCALE"} :
                    for i in range(3) : 
                        self.CreatreDrive(
                            act_bone, "bbone_scalein",
                            selct_bones_1, f"scale[{i}]",
                            Use_Bone=True,
                            index= i
                        )

                        self.CreatreDrive(
                            act_bone, f"bbone_scaleout",
                            selct_bones_2, f"scale[{i}]", 
                            Use_Bone=True, 
                            index= i
                        )
                        
                elif prop.bendybone_type == {"PARENT"} :
                    
                    def haveconstraint() -> bool:
                        for bone in select_bone :
                            if bone.parent and bone.parent.name == bone.name+"RGC_CONTROL" :
                                return True
                        return False
                    if not haveconstraint() : 
                        GetName = self.GetNameToBones(select_bone)
                        GetNameActBone = act_bone.name
                        self.SetMode(mode="EDIT")
                        select_bone_edit = self.GetBones(GetName, mode="EDIT")
                        act_bone_pose = self.GetBone(GetNameActBone, mode="POSE")
                        if select_bone_edit :
                            Names = []
                            for i in range(len(select_bone_edit)) :
                                Names.append(self.GN_Name(new_name=select_bone_edit[i].name, bone_name="RGC_CONTROL"))
                            cont_bones = self.CreateBones(Names)
                            if cont_bones :
                                self.SetTransformToBones(cont_bones, select_bone_edit, length_value=0.5)
                                for i, bone in enumerate(cont_bones) :
                                    self.SetDisplaySize(bone, select_bone_edit[i])
                                self.SetDeform(cont_bones, False)
                                for i in range(len(cont_bones)) :
                                    select_bone_edit[i].parent = cont_bones[i]
                        cont_bones_name = self.GetNameToBones(cont_bones)
                        self.SetMode(mode="POSE")
                        cont_bones_pose = self.GetBones(cont_bones_name, mode="POSE")
                        if cont_bones_pose : 
                            for bone in cont_bones_pose :
                                constraint = bone.constraints.new(type='ARMATURE')
                                constraint.targets.new()
                                for i, tgt in enumerate(constraint.targets):
                                    if tgt.target is None:
                                        constraint.targets[i].target = self.GetActiveObject()
                                        constraint.targets[i].subtarget = act_bone_pose.name
                                        constraint.targets[i].weight = 1.0
                    else :
                        parent_name = []
                        for bone in select_bone:
                            if bone.parent is not None:
                                parent_name.append(bone.parent.name)
                            
                        parent_bones = self.GetBones(parent_name, mode="POSE")
                        if parent_bones :
                            for bone in parent_bones :
                                if bone.constraints :
                                    for cont in bone.constraints :
                                        if cont.type == "ARMATURE" :
                                            cont.targets.new()
                                            for i, tgt in enumerate(cont.targets):
                                                if tgt.target is None:
                                                    cont.targets[i].target = self.GetActiveObject()
                                                    cont.targets[i].subtarget = act_bone.name
                                                cont.targets[i].weight = 1.0 / len(cont.targets)
        except : 
            print("Error")
        
               
    def GetConstraintArmatureToIK(self) : 
        
        self.SetMode(mode="EDIT") 
        
        get_constraint_to_armature = self.GetBones(
            ["ik_arm_L.003", "ik_arm_R.003", "ik_leg_L", "ik_leg_R"], mode="EDIT"
            )
        
        get_name_new_bone = []
        
        for bone in get_constraint_to_armature : 
            
            new_bone = self.CreateBonesRange(bone.name, 1)
            get_name_new_bone.append(new_bone[0].name)
            self.SetTransform(new_bone[0], bone)
            self.SetDeform(new_bone, False)
            self.SetDisplaySize(new_bone[0], bone)
            bone.parent = new_bone[0]
                
        self.SetMode(mode="POSE") 
        
        get_constraint_to_armature = self.GetBones(
            ["ik_arm_L.003", "ik_arm_R.003", "ik_leg_L", "ik_leg_R"], mode="POSE"
        )
        new_bones = self.GetBones(get_name_new_bone, mode="POSE")
        
        for i, bone in enumerate(get_constraint_to_armature) : 
            
            constraint = self.GetConstraintActive(bone)
            Select = new_bones[i]
            
            new_constraint = Select.constraints.new(type=constraint.type)
            
            for attr in dir(constraint):
                if not attr.startswith("_") and not callable(getattr(constraint, attr)):
                    try:
                        setattr(new_constraint, attr, getattr(constraint, attr))
                    except AttributeError:
                        pass
            
            # Handle targets for ARMATURE constraint type
            if constraint.type == 'ARMATURE':
                # Ensure the new constraint has the correct number of targets
                while len(new_constraint.targets) < len(constraint.targets):
                    new_constraint.targets.new()

                for i, tgt in enumerate(constraint.targets):
                    if tgt.target is not None:
                        new_constraint.targets[i].target = tgt.target
                        new_constraint.targets[i].subtarget = tgt.subtarget
                        new_constraint.targets[i].weight = tgt.weight
                        
                        # Verificar si el target tiene un driver y copiarlo
                        if tgt.id_data.animation_data and tgt.id_data.animation_data.drivers:
                            driver = None
                            for d in tgt.target.animation_data.drivers:
                                # Filtrar el driver que afecta específicamente el weight del target
                                if d.data_path == f'pose.bones["{bone.name}"].constraints["{constraint.name}"].targets[{i}].weight':
                                    driver = d
                            if not driver : continue
                            variables = driver.driver.variables
                            
                            def add_drive(
                                Obj : object, Propertie : str, Control_Obj : object, 
                                Control_Propertie : str,  Use_Bone : bool = False, 
                                Use_Expression : bool = False, Expression : str = "-1", ):
                                # Agregar un controlador (driver) a la propiedad del objeto
                                driver = Obj.driver_add(Propertie).driver
                                driver.type = 'SCRIPTED'
                                
                                # Crear una nueva variable para el driver
                                var = driver.variables.new()
                                var.name = variables[0].name
                                var.targets[0].id_type = "OBJECT"
                                var.targets[0].id = self.GetActiveObject()
                                
                                # Si se está usando un hueso, agregar la ruta correspondiente
                                if Use_Bone:
                                    var.targets[0].data_path = f'pose.bones["{Control_Obj.name}"].{Control_Propertie}'
                                else:
                                    # Si no es un hueso, asignar la propiedad directamente
                                    var.targets[0].data_path = Control_Propertie
                                

                                if Use_Expression : driver.expression = Expression
                                else : driver.expression = "var"
                            
                            add_drive(
                                new_constraint.targets[i], 
                                f"weight", 
                                driver, 
                                variables[0].targets[0].data_path, 
                                Use_Expression=True, 
                                Expression=driver.driver.expression
                                )
                            
            
            bone.constraints.remove(constraint)
            
            # Recorrer las colecciones
            for col in self.GetCollections():
                
                if Select.name in self.GetBonesNamesInCollection(col.name) : 
                    # Verificar si el hueso está en la colección actual
                    bpy.ops.armature.collection_unassign_named(
                        name=col.name, 
                        bone_name=Select.name
                    )

            Select.bone.select = True
            bpy.ops.armature.collection_assign(name="Control_Bone")


    def MeshToBone(self): 
        # Get the active object (assumed to be a mesh object)
        obj = self.GetActiveObject()
        select_obj = self.GetSelectableObjects()
        self.UpdateViewLayer()
        
        selected_vertex_coords = []
        selected_vertex_normal = []
        
        selected_ege_coords = []
        selected_ege_normal = []
        
        selected_face = []
        selected_face_coords = []
        selected_face_normal = []
        
        # Ensure you're in Edit Mode
        if obj.mode == 'EDIT':
            
            # Crear una representación bmesh de la malla
            bm = bmesh.from_edit_mesh(obj.data)
            
            if self.GetMeshSelectMode("VERT"):
                
                # Obtener las coordenadas de los vértices seleccionados
                selected_vertex_coords = [v.co.copy() for v in bm.verts if v.select]
                selected_vertex_normal = [v.normal.copy() for v in bm.verts if v.select]
            
            elif self.GetMeshSelectMode("EDGE"):
                
                for edge in bm.edges:
                    if edge.select:
                        
                        selected_ege_coords.append((
                            edge.verts[0].co.copy() , 
                            edge.verts[1].co.copy() ))
                        
                        selected_ege_normal.append((
                            edge.verts[0].normal.copy() , 
                            edge.verts[1].normal.copy() ))
                        
            elif self.GetMeshSelectMode("FACE"):
                
                for face in bm.faces:
                    if face.select:
                        faces = []
                        normals = []
                        for vert in face.verts:
                            faces.append(vert.co.copy())
                            normals.append(vert.normal.copy())
                        selected_face_coords.append(faces)
                        selected_face_normal.append(normals)
        armature = None
        for obj in select_obj: 
            if obj.type == "ARMATURE": 
                armature = obj
                break
        
        # Salimos del modo Edit para la malla antes de trabajar con el armature
        self.SetMode(mode="OBJECT")
        props = self.Props()
        
        
        # Función para calcular las nuevas coordenadas considerando la matriz mundial del objeto
        def n_co(co): 
            # Aplicar correctamente la matriz mundial a un Vector4 y devolver Vector3
            co_world = obj.matrix_world @ co.to_4d()  # Asegúrate de convertir a Vector4 para la multiplicación
            return co_world.to_3d()  # Convertir a Vector3 para obtener solo la parte XYZ

        
        def set_bone():
            
            
            def roll(bone, normal):
                if props.mesh_use_aling_roll_normal:
                    bone.align_roll(normal)
            
            def reference_bone(use_tail : bool = False):
                if props.mesh_use_bone_reference :
                    reference_bone = self.GetBone(props.mesh_bone_reference_name, mode="EDIT")
                    if not reference_bone : return
                    for bone in new_bones : 
                        if use_tail :
                            bone.length = reference_bone.length
                        self.SetDisplaySize(bone, reference_bone)
            
            if self.GetMeshSelectMode("VERT"):
                
                if not props.mesh_use_vertcurve or len(selected_vertex_coords) <= 1:
                    if not props.mesh_use_tail or len(selected_vertex_coords) <= 1 : 
                        new_bones = self.CreateBonesRange(props.mesh_bone_name, len(selected_vertex_coords))
                        reference_bone()
                            
                        for i, co in enumerate(selected_vertex_coords):
                            new_bones[i].head = n_co(co)
                            if props.mesh_normal_global == "GLOBAL":
                                type = str(props.mesh_direction).replace("{", "").replace("}", "").replace("'", "")
                                new_bones[i].tail = n_co(co) + self.GetWorldNormal(f"{type.lower()}")
                            else :
                                new_bones[i].tail = n_co(co) + selected_vertex_normal[i]
                            roll(new_bones[i], selected_vertex_normal[i])
                    else : 
                        new_bones = self.CreateBonesRange(props.mesh_bone_name, len(selected_vertex_coords)-1)
                        reference_bone(use_tail=True)
                        for i, bone in enumerate(new_bones):
                            bone.head =  n_co(selected_vertex_coords[i])
                            bone.tail = n_co(selected_vertex_coords[i+1])
                            roll(new_bones[i], selected_vertex_normal[i])
                else :
                    new_bones = self.CreateBonesRange(props.mesh_bone_name, 1)
                    reference_bone(use_tail=True)
                    def obtener_2_vertices_mas_lejanos(vertex_coords):
                        if len(vertex_coords) < 2:
                            return None  # Mínimo 2 vértices
                        
                        max_distance = -1
                        par_mas_lejano = (vertex_coords[0], vertex_coords[1])  # Inicialización
                        
                        # Bucle eficiente (comparación sin repeticiones)
                        for i in range(len(vertex_coords)):
                            v1 = Vector(vertex_coords[i])
                            for j in range(i + 1, len(vertex_coords)):
                                distancia = (v1 - Vector(vertex_coords[j])).length
                                if distancia > max_distance:
                                    max_distance = distancia
                                    par_mas_lejano = (vertex_coords[i], vertex_coords[j])
                        
                        return par_mas_lejano
                    verts = obtener_2_vertices_mas_lejanos(selected_vertex_coords)
                    new_bones[0].head = n_co(verts[0])
                    new_bones[0].tail = n_co(verts[-1])
                    new_bones[0].bbone_segments = 32
                    
                    normal = self.CreateVector(0, 0, 0)
                    for n in selected_vertex_normal:
                        normal += n
                    normal /= len(selected_vertex_normal)
                    roll(new_bones[0], normal)
                    influence = len(selected_vertex_coords) * props.mesh_vertcurve_power
                    self.AlingBboneToNormal(new_bones[0], normal, influence)
                    self.GetActiveObject().data.display_type = 'BBONE'
                    
                    
            
            if self.GetMeshSelectMode("EDGE") : 
                
                
                
                new_bones = self.CreateBonesRange(props.mesh_bone_name, len(selected_ege_coords))
            
                if props.mesh_use_tail : 
                    reference_bone(use_tail=True)
                    for i, co in enumerate(selected_ege_coords):
                        new_bones[i].head = n_co(co[0])
                        new_bones[i].tail = n_co(co[1])
                        normal = (selected_ege_normal[i][0] + selected_ege_normal[i][1]) / 2
                        roll(new_bones[i], normal)
                else :
                    reference_bone()
                    for i, co in enumerate(selected_ege_coords):
                        head = (n_co(co[0]) + n_co(co[1])) / 2
                        normal = (selected_ege_normal[i][0] + selected_ege_normal[i][1]) / 2
                        
                        new_bones[i].head = head
                        if props.mesh_normal_global == "GLOBAL":
                            type = str(props.mesh_direction).replace("{", "").replace("}", "").replace("'", "")
                            new_bones[i].tail = head + self.GetWorldNormal(f"{type.lower()}")
                        else :
                            new_bones[i].tail = head + normal
                        roll(new_bones[i], normal)
                            
                        if 1 > 0 : 
                            dis = self.GetDistancia3d(new_bones[i-1].tail, new_bones[i].head)
                            if dis < 0.1 :
                                bone.parent = new_bones[i-1]
                                bone.use_connect = True
                

            if self.GetMeshSelectMode("FACE") : 
                
                
                new_bones = self.CreateBonesRange(props.mesh_bone_name, len(selected_face_coords))
                reference_bone(use_tail=True)
                for i, face in enumerate(selected_face_coords):
                    
                    head = self.CreateVector(0, 0, 0)
                    for co in face : 
                        head += co
                    head = head / len(face)
                    head = n_co(head)
                    normal = self.CreateVector(0, 0, 0)
                    for n in selected_face_normal[i] : 
                        normal += n
                    normal = normal / len(selected_face_normal[i])
                    
                    new_bones[i].head = head
                    

                    if props.mesh_normal_global == "GLOBAL":
                        type = str(props.mesh_direction).replace("{", "").replace("}", "").replace("'", "")
                        new_bones[i].tail = head + self.GetWorldNormal(f"{type.lower()}")
                    else :
                        new_bones[i].tail = head + normal
                        
                    roll(new_bones[i], normal)
                    
            if props.mesh_use_curve :
                curve_bone = self.CreateBonesRange("bendy-"+props.mesh_bone_name, Range=props.mesh_bone_subdivisions)
                new_tail = self.CreateVector(0, 0, 0)
                head_cero = new_bones[0].head
                max_dist = -1  # Inicializa la distancia más grande en un valor bajo

                for bone in new_bones:
                    dis = self.GetDistancia3d(head_cero, bone.head)
                    if dis > max_dist:  # Si encontramos una distancia mayor, actualizamos
                        max_dist = dis
                        new_tail = bone.head
                
                if curve_bone :
                    for bone in curve_bone :
                        bone.head = new_bones[0].head
                        bone.tail = new_tail
                        self.SetDisplaySize(bone, new_bones[0])
                    self.SetDeform(curve_bone, False)

                self.GetActiveObject().data.display_type = 'BBONE'
                name_curve_bone = self.GetNameToBones(curve_bone)
                name_new_bones = self.GetNameToBones(new_bones)
                self.SetMode(mode="POSE")
                curve_bone_pose = self.GetBones(name_curve_bone, mode="POSE")
                new_bones_pose = self.GetBones(name_new_bones, mode="POSE")
                if curve_bone_pose and new_bones_pose :
                    self.SelectBones(curve_bone_pose, mode="POSE")
                    GeneratorsBones().GN_CurveGrip()
                    self.SelectBones(new_bones_pose, mode="POSE")
                    self.ActiveBone(curve_bone_pose[0].name, mode="POSE")
                    props.bendybone_type = {"PARENT"}
                    self.SetContBendyBone()
                
                self.SetMode(mode="EDIT")
                
                
        # Asegurarse de que el armature esté en la capa de vista activa
        if armature:
            obj = self.GetActiveObject()
            self.ActiveObj(armature)
            self.SetMode(mode="EDIT")
            set_bone()
        else:
            obj = self.GetActiveObject()
            bpy.ops.object.armature_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
            self.SetMode(mode="EDIT")
            self.RemoveBones(["Bone"])
            set_bone()
        
        
        if props.mesh_with_automatic_weights :
            self.SetMode(mode="OBJECT")
            armature = self.GetActiveObject()
            obj.select_set(True)
            bpy.ops.object.parent_set(type='ARMATURE_AUTO')
            if props.mesh_with_by_distance_of_vertex:
                self.WithDistanceWeights(obj, armature)
            self.ActiveObj(armature)
            self.SetMode(mode="EDIT")
            
        if props.mesh_keep_object : 
            self.SetMode(mode="OBJECT")
            armature = self.GetActiveObject()
            self.ActiveObj(obj)
            self.SetMode(mode="EDIT")
            armature.select_set(True)
    
    
    def CurveToBone(self): 
        # Obtener el objeto activo (suponiendo que es una curva)
        curve = self.GetActiveObject()
        select_obj = self.GetSelectableObjects()
        selected_curve = []
        hook_bones = []
        
        # Asegurarse de estar en modo edición para la curva
        if curve.mode == 'EDIT':
            # Verificar si la curva es de tipo NURBS o Bezier
            for spline in curve.data.splines:
                if spline.type == 'BEZIER':
                    for point in spline.bezier_points:
                        selected_curve.append(point.co.copy())  # Agregar coordenadas del punto Bezier
                else:
                    for point in spline.points:
                        selected_curve.append(point.co.copy())  # Agregar coordenadas del punto NURBS

        
        armature = None
        for obj in select_obj: 
            if obj.type == "ARMATURE": 
                armature = obj
                break
        
        
        
        # Salimos del modo edición para la curva antes de trabajar con el armature
        self.SetMode(mode="OBJECT")
        props = self.Props()

        # Función para calcular las nuevas coordenadas considerando la matriz mundial del objeto
        def n_co(co, curve_obj): 
            # Aplicar correctamente la matriz mundial a un Vector4 y devolver Vector3
            co_world = curve_obj.matrix_world @ co.to_4d()  # Asegúrate de convertir a Vector4 para la multiplicación
            return co_world.to_3d()  # Convertir a Vector3 para obtener solo la parte XYZ
        
        # Función para crear los huesos
        def set_bone(curve_obj):
            
            
            index = len(selected_curve)  # Número de puntos seleccionados
            # Crear huesos basados en el rango
            bones_new = self.CreateBonesRange(Bone_Name=props.curve_bone_name, Range=index)
            r_bone = None
            if props.curve_use_reference_bone :
                r_bone = self.GetBone(props.curve_reference_bone_name, mode="EDIT")
            # Configurar deformación de los huesos
            self.SetDeform(bones_new)
            
            hook_bones = self.GetNameToBones(bones_new) 
            
            # Asignar coordenadas a los huesos
            for i in range(index):
                
                # Obtener la posición del punto transformada por la matriz mundial de la curva
                head = n_co(selected_curve[i], curve_obj)  # Calcular la posición de la cabeza del hueso
                
                bones_new[i].head = head
                bones_new[i].tail = head + self.GetWorldNormal()  # Ajustar la cola para darle longitud al hueso
                if r_bone :
                    bones_new[i].length = r_bone.length
                    self.SetDisplaySize(bones_new[i], r_bone)
                
            # Ajustes adicionales si necesitas rotación o manipular más huesos
            if props.curve_use_control == True:
                bones_rot = self.CreateBonesRange(Bone_Name="rot_" + props.curve_bone_name, Range=index - 1)
                
                self.SetDeform(bones_rot)
                for i in range(index-1):
                    bones_rot[i].head = bones_new[i].head  # Si tienes otras propiedades que configurar
                    bones_rot[i].tail = bones_new[i+1].head
                    if r_bone : self.SetDisplaySize(bones_rot[i], r_bone)
                    if i != 0 : 
                        bones_rot[i].parent = bones_rot[i-1]
                        bones_rot[i].use_connect = True
                    bones_new[i].parent = bones_rot[i]
                bones_new[-1].parent = bones_rot[-1]
                self.SelectBones(bones_rot, mode="EDIT")
                GeneratorsBones().GN_Fingers()
            
            return hook_bones
        
        # Asegurarse de que la armadura esté en la capa activa y en modo edición
        if armature:
            curve = self.GetActiveObject()  # Obtener el objeto activo actual
            self.ActiveObj(armature)  # Activar el objeto armature
            self.SetMode(mode="EDIT")
            hook_bones = set_bone(curve)	
        else:
            # Si no hay armature, crear una nueva armadura
            curve = self.GetActiveObject()
            bpy.ops.object.armature_add(enter_editmode=False, align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
            armature = self.GetActiveObject()
            self.SetMode(mode="EDIT")
            self.RemoveBones(["Bone"])  # Eliminar el hueso predeterminado si es necesario
            hook_bones = set_bone(curve)
        
        self.SetMode(mode="OBJECT")
        self.ActiveObj(curve)
        Modifiers = []
        for i in range(len(selected_curve)):
            M = curve.modifiers.new(name = "", type='HOOK')
            M.object = armature
            M.subtarget = hook_bones[i]
            Modifiers.append(M)
            
        self.SetMode(mode="EDIT")
        
        def set_points(points):
            
            # Asignar cada punto de la curva a su respectivo modificador Hook
            for i, point in enumerate(points):
                # Para asegurar que no superamos el número de modificadores disponibles
                for p in points:
                     p.select = False
                     
                if i < len(Modifiers):
                    mod = Modifiers[i]
                    # Deseleccionar todos los puntos de nuevo para asegurarse de que no hay selección múltiple
                    point.select = True
                    bpy.ops.object.hook_assign(modifier=mod.name)
            
            
        if curve.mode == 'EDIT':
            # Verificar si la curva es de tipo NURBS o Bezier
            for spline in curve.data.splines:
                if spline.type == 'BEZIER':
                    set_points(spline.bezier_points)
                else:
                    set_points(spline.points)
                    
        self.ActiveObj(armature, use_deselect=False)
        bpy.ops.object.parent_set(type='ARMATURE_NAME')

    def AplicarScale(self):
        save_scale = self.GetActiveObject().scale.copy()
        self.SetMode(mode="OBJECT")
        
        for obj in self.GetSelectableObjects():
            # Asegurarse de que el objeto sea el activo y que no sea un objeto vacío
            if obj.type != 'EMPTY':  
                if obj.type == 'ARMATURE':
                    # Si el objeto no tiene múltiples usuarios, simplemente aplicar las transformaciones
                    bpy.context.view_layer.objects.active = obj
                    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
                    
                    self.SetMode(mode="POSE")
                    
                    for bone in obj.pose.bones:
                        for i in range(3):  # Normalizar cada componente de la escala, rotación y traslación
                            bone.custom_shape_translation[i] *= save_scale[i]

                        for cont in bone.constraints:
                            
                            if cont.type == "STRETCH_TO":
                                cont.rest_length = 0
                                
                            if cont.type == "LIMIT_LOCATION":
                                
                                if cont.min_x != 0 :
                                    cont.min_x *= save_scale[0]
                                if cont.min_y != 0 :
                                    cont.min_y *= save_scale[0]
                                if cont.min_z != 0 :
                                    cont.min_z *= save_scale[0]
                                    
                                if cont.max_x != 0 :
                                    cont.max_x *= save_scale[0]
                                if cont.max_y != 0 :
                                    cont.max_y *= save_scale[0]
                                if cont.max_z != 0 :
                                    cont.max_z *= save_scale[0]
                                    
                    self.SetMode(mode="OBJECT")
                
    def SetDriveToOldRigCreator(self):
        
        new_drive = [
            "head", "eyes", 
            
        ]
        old_drive = [
            "Cabeza_Global_Local", "Ojos_Global_Local", 
        ]
        for type in ["R", "L"] : 
            old_drive.append(f"Brazo_IK_FK_{type}")
            old_drive.append(f"Brazo_IK_Stretch_{type}")
            old_drive.append(f"Brazo_Rot_Mov_{type}")
            old_drive.append(f"Global_Local_Brazo_{type}")
            
            old_drive.append(f"Pierna_IK_Fk_{type}")
            old_drive.append(f"Pierna_IK_Stretch_{type}")
            old_drive.append(f"Pierna_Rot_Mov_{type}")
            
            new_drive.append(f"arm_ik_fk_{type}")
            
            mi_type = "L" if type == "R" else "R"
            new_drive.append(f"arm_stretch_to_{mi_type}")
            new_drive.append(f"arm_rot_{mi_type}")
            
            new_drive.append(f"arm_followed_{type}")
            
            new_drive.append(f"leg_ik_fk_{type}")
            new_drive.append(f"leg_stretch_to_{type}")
            new_drive.append(f"leg_rot_{type}")
            
        
        for i, old in enumerate(old_drive) : 

            if hasattr(self.GetActiveObject().data, f'["{old}"]') :
                self.GetActiveObject().data.driver_remove(f'["{old}"]')
                self.CreatreDrive(
                    self.GetActiveObject().data, f'["{old}"]', 
                    self.GetActiveObject(), f"RGC_Armature_GrupsProps[0].{new_drive[i]}", 
                    Use_Bone=False
                )

    def SetProperties(self):
        props = bpy.context.scene.RGC_GrupsProps
        
        # Para Crear la lista de Genradores Disponibles
        Generators = GeneralArmatureData().ListGenerators()
        for g in Generators:
            grups = props.Generators_List.get(g)
            if not grups:
                new = props.Generators_List.add()
                new.name = g

    def AddPropertiesRigCreator(self):
        self.PropsToArmature().add()
    
    def AddCollectionToArmature(self):
        for col in self.ListCollectionToArmature():
            if col not in self.GetCollectionsNames() :
                self.GetActiveObject().data.collections.new(col)
        
    def SelectBoneToCollection(self, Col_Name : str, Mode : str = "POSE", value : bool = True):
        if Mode == "OBJECT" : return
        if Mode == 'POSE':
            for bone in self.GetCollectionToName(Col_Name).bones:
                bone.select = value
        elif Mode == 'EDIT':
            for bone in self.GetCollectionToName(Col_Name).bones:
                bone.select = value

    def OnlySelectBonesInThesCollection(self, Col_Name : str):
        for bone in self.GetActiveObject().data.bones :
            bone.select = False
        for bone in self.GetCollectionToName(Col_Name).bones:
            bone.select = True
            
    def EditIndexCollections(self, Col_Name: str, Type: str):
        # Obtener la colección por nombre
        col = self.GetCollectionToName(Col_Name)
        collections = self.GetActiveObject().data.collections  # Obtener la colección de Armature
        
        # Encontrar el índice de la colección manualmente
        col_index = -1
        for i, c in enumerate(collections):
            if c == col:
                col_index = i
                break
        
        # Verificar si se encontró la colección
        if col_index == -1:
            print(f"Error: Colección '{Col_Name}' no encontrada.")
            return
        
        # Mover hacia arriba
        if Type == "UP":
            new_index = col_index - 1
            new_index = new_index if new_index >= 0 else 0
            collections.move(col_index, new_index)
        
        # Mover hacia abajo
        elif Type == "DOWN":
            new_index = col_index + 1
            new_index = new_index if new_index <= len(collections) - 1 else len(collections) - 1
            collections.move(col_index, new_index)

    def FkaIkoIkaFk(self, type: str = "R", body_part: str = "arm", invert: bool = False):
        index = 3 if body_part == "arm" else 4 

        IK = self.GetBonesToRange(f"ik_{body_part}_{type}", index, mode="POSE")
        FK = self.GetBonesToRange(f"fk_{body_part}_{type}", index, mode="POSE")
        POLE = self.GetBone(
            f"pole{body_part}_{type}", mode="POSE"
        )
        
        IKLEG = self.GetBone(
            f"ik_leg_{type}", mode="POSE"
        )
        ROTFEET = self.GetBone(
            f"rot_feet_{type}", mode="POSE"
        )
        
        # Verificar que tanto IK como FK existan
        if not IK or not FK and POLE:
            return

        # Aplicar transformaciones de IK a FK si invert=True
        if invert:
            for i, fk_bone in enumerate(FK):
                ik_bone = IK[i]
                
                # Aplicar la matriz de IK a FK
                fk_bone.matrix = ik_bone.matrix
                
                # Ajustar la rotación si es necesario
                if i == 1:
                    fk_bone.rotation_quaternion[2] = 0
                    fk_bone.rotation_quaternion[3] = 0
                
                # Ajustar ubicación y escala
                fk_bone.location = (0, 0, 0)
                fk_bone.scale = (1, 1, 1)
            
                # Forzar actualización de la capa de visualización
                bpy.context.view_layer.update()
            return

        # Aplicar transformaciones de FK a IK si invert=False
        for i, ik_bone in enumerate(IK):
            if i > 1 and body_part == "leg": continue
            fk_bone = FK[i]
            
            # Aplicar la matriz de FK a IK
            ik_bone.matrix = fk_bone.matrix
            
            if i == 0:
                # Ajuste cuidadoso de la rotación y transformaciones si es necesario
                ik_bone.location = (0, 0, 0)
                ik_bone.scale = (1, 1, 1)
                ik_bone.rotation_euler[0] = 0  # Ajuste rotación X si es necesario
                ik_bone.rotation_euler[2] = 0  # Ajuste rotación Z si es necesario

            if i == 1:
                # Ajuste cuidadoso para el segundo hueso
                ik_bone.location = (0, 0, 0)
                ik_bone.scale = (1, 1, 1)
                ik_bone.rotation_quaternion[0] = 1  # Solo resetea el primer componente de quaternion
                ik_bone.rotation_quaternion[1] = 0
                ik_bone.rotation_quaternion[2] = 0
                ik_bone.rotation_quaternion[3] = 0

            # Forzar actualización de la capa de visualización
            bpy.context.view_layer.update()

        if body_part == "leg" : 
            IKLEG.matrix = FK[2].matrix
            IKLEG.rotation_quaternion[0] = 1 
            IKLEG.rotation_quaternion[1] = 0 
            IKLEG.rotation_quaternion[2] = 0 
            IKLEG.rotation_quaternion[3] = 0 
            bpy.context.view_layer.update()
            ROTFEET.matrix = FK[-1].matrix
        
        position =  FK[1].z_axis*-1
        # Obtener la posición promedio de FK[0] y FK[1]
        matrix_fk0 = FK[0].matrix
        matrix_fk1 = FK[1].matrix

        # Promediar las matrices FK
        average_fk_matrix = self.MatrixMedFor(matrix_fk0, matrix_fk1)
        
        # Crear la nueva matriz (ubicación, rotación, escala)
        matrix = self.CreateMatrix(location=position, rotation_euler=(0, 0, 0), scale=(1, 1, 1))
        
        # Aplicar la transformación promedio de FK sobre la nueva matriz
        final_matrix = matrix @ average_fk_matrix
        
        # Asignar la matriz resultante a POLE
        POLE.matrix = final_matrix
        POLE.rotation_quaternion[0] = 1
        POLE.rotation_quaternion[1] = 0
        POLE.rotation_quaternion[2] = 0
        POLE.rotation_quaternion[3] = 0
    

    def CopyXformRelationShip(self):
        # Obtener el objeto activo y los objetos seleccionados
        obj = self.GetActiveObject()
        
        # Obtener el hueso activo y los huesos seleccionados
        Bone_Active = self.GetActiveBone()
        Bone_Select = self.GetSelectBones(mode="POSE")
        props = self.Props()  # Configuración de propiedades

        if not Bone_Active or not Bone_Select:
            return

        # Obtener la matriz global del objeto activo y del objeto seleccionado
        object_matrix = obj.matrix_world.copy()

        # Obtener la matriz del primer hueso seleccionado que no sea el hueso activo
        bone = None
        for b in Bone_Select:
            if b != Bone_Active:
                bone = b
                break

        if not bone:
            return

        select_object_matrix = bone.id_data.matrix_world.copy()
        
        # Obtener la matriz local del hueso seleccionado
        if bone.id_data != obj:
            select_matrix = select_object_matrix @ bone.matrix.copy()
            active_matrix = object_matrix @ Bone_Active.matrix.copy() # Matriz global del hueso seleccionado
        else:
            select_matrix = bone.matrix.copy()
            active_matrix = Bone_Active.matrix.copy() 
            
        # Descomponer la matriz del hueso seleccionado
        sloc, srot, ssca = select_matrix.decompose()

        # Obtener la localización del hueso seleccionado en el espacio del hueso activo
        temporal_matrix = active_matrix.inverted() @ select_matrix
        
        loc, rot, sca = temporal_matrix.decompose()

        # Crear una nueva matriz con las transformaciones correspondientes
        new_matrix = mathutils.Matrix.LocRotScale(
            loc , 
            rot if props.use_rotation else srot, 
            sca if props.use_scale else ssca
        )

        # Guardar la matriz descompuesta en las propiedades
        values = []
        for line in new_matrix:
            for value in line:
                values.append(value)

        for i, v in enumerate(values):
            props.save_matrix[i] = v

        props.is_save_matrix = True
        self.report({'INFO'}, f"{Bone_Active.name} Copy Relation Ship to {Bone_Select[0].name}")
        
    def PasteXformRelationShip(self):
        # Obtener el objeto activo y los objetos seleccionados
        obj = self.GetActiveObject()

        # Obtener el hueso activo y los huesos seleccionados
        Bone_Active = self.GetActiveBone()
        Bone_Select = self.GetSelectBones(mode="POSE")
        props = self.Props()  # Configuración de propiedades

        # Obtener la matriz global del objeto activo y del objeto seleccionado
        object_matrix = obj.matrix_world.copy()

        # Reconstruir la matriz a partir de los valores guardados
        values = [props.save_matrix[i] for i in range(16)]  # Suponiendo que la matriz es 4x4 (16 elementos)
        new_matrix = mathutils.Matrix()

        # Asignar los valores a la matriz
        for i in range(4):
            for j in range(4):
                new_matrix[i][j] = values[i * 4 + j]
    
        
        # Aplicar la nueva matriz a los huesos seleccionados
        for bone in Bone_Select:
            if bone != Bone_Active:
                
                loc, rot, sca = bone.matrix.copy().decompose()
                if bone.id_data != obj:
                    active_matrix = object_matrix @ Bone_Active.matrix.copy()
                else : 
                    active_matrix = Bone_Active.matrix.copy()
                new_matrix = active_matrix @ new_matrix
                nloc, nrot, nsca = new_matrix.decompose()
                new_matrix = mathutils.Matrix.LocRotScale(
                    nloc, 
                    nrot if props.use_rotation else rot, 
                    nsca if props.use_scale else sca
                )
                bone.matrix = new_matrix 

                # Insertar keyframe en la localización, rotación y escala de este hueso
                bone.keyframe_insert(data_path="location", frame=bpy.context.scene.frame_current)
                if bone.rotation_mode != 'QUATERNION' :
                    bone.keyframe_insert(data_path="rotation_euler", frame=bpy.context.scene.frame_current)
                else:
                    bone.keyframe_insert(data_path="rotation_quaternion", frame=bpy.context.scene.frame_current)
                bone.keyframe_insert(data_path="scale", frame=bpy.context.scene.frame_current) 
        
        self.report({'INFO'}, "Paste Relation Ship")
        
    def BakeByFrameXformRelationShip(self):
        # Obtener hueso activo y huesos seleccionados
        Bone_Active = self.GetActiveBone()
        Bone_Select = self.GetSelectBones(mode="POSE")
        props = self.Props()  # Configuración de propiedades

        if not Bone_Active or not Bone_Select:
            return

        # Obtener el objeto activo
        obj = self.GetActiveObject()

        # Asegurarse de que el objeto tiene datos de animación
        if obj and obj.animation_data and obj.animation_data.action:
            # Lista de frames clave (keyframes)
            keyframes = set()

            # Recorrer los huesos seleccionados y buscar sus FCurves
            for bone in Bone_Select:
                for fcurve in obj.animation_data.action.fcurves:
                    if fcurve.data_path.startswith(f'pose.bones["{bone.name}"]'):
                        # Filtrar solo los keyframes seleccionados
                        selected_keyframes = [int(kf.co[0]) for kf in fcurve.keyframe_points if kf.select_control_point]
                        keyframes.update(selected_keyframes)

           # Si se encontraron keyframes, mover el cursor a esos frames
            if keyframes:
                print(f"Keyframes encontrados: {sorted(keyframes)}")
                
                # Obtener la lista ordenada de keyframes
                keyframe_list = sorted(keyframes)

                # Iterar sobre los frames seleccionados
                for i, frame in enumerate(keyframe_list):
                    print(f"Procesando frame {frame}")
                    
                    # Establecer el cursor en el frame actual
                    bpy.context.scene.frame_set(frame)

                    # Forzar una actualización completa de la interfaz
                    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

                    # Copiar las transformaciones del hueso activo
                    self.CopyXformRelationShip()  

                    # Si hay un siguiente frame, pegar en el siguiente
                    if i < len(keyframe_list) - 1:
                        next_frame = keyframe_list[i + 1]

                        # Establecer el cursor en el siguiente frame
                        print(f"Pegar en frame {next_frame}")
                        bpy.context.scene.frame_set(next_frame)

                        # Forzar actualización antes de pegar
                        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)

                        # Pegar las transformaciones en el siguiente frame
                        self.PasteXformRelationShip()

                        # Actualizar la vista para garantizar que las animaciones se vean correctamente
                        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        
                
    # Constraints 
    def ListFunctionToConstraint(self, type : str, use_bone : bool ) :
        List_Def = {
            "REMOVE" : self.RemoveConstraints,
            "DUPLICATE_CONST" : self.DuplicateConstraints,
            "APPLY_CONST" : self.ApplyConstraints,
            "DELETE_ALL" : self.RemoveAllConstraints,
            "COPY_SEL_CONST" : self.CopyConstraints,
            "COPY_SEL_CONST_INDEX" : self.CopyConstraints,
            "UP" : self.MoveConstraints,
            "DOWN" : self.MoveConstraints,
        }
        
        How_Def = List_Def[type]
        if type in {"COPY_SEL_CONST_INDEX", "COPY_SEL_CONST"}:
            How_Def(use_bone, True if type != "COPY_SEL_CONST" else False)
        elif type in {"UP", "DOWN"}:
            How_Def(use_bone, type)
        else:
            How_Def(use_bone)
         
    def RemoveConstraints(self, use_bone : bool = False):
        X = self.GetActiveObject() if use_bone == False else self.GetActiveBone()
        if X : 
            const = self.GetConstraintActive(X)
            if not const : return
            bpy.ops.constraint.delete(constraint=const.name, owner='BONE' if use_bone else 'OBJECT')
            if X.active_constraint < 1:
                X.active_constraint = 0
            else:
                X.active_constraint = X.active_constraint-1
    
    def DuplicateConstraints(self, use_bone : bool = False) : 
        X = self.GetActiveObject() if use_bone == False else self.GetActiveBone()
        if X : 
            const = self.GetConstraintActive(X)
            if not const : return
            bpy.ops.constraint.copy(constraint=const.name, owner='BONE' if use_bone else 'OBJECT')
            X.active_constraint += 1
    
    def ApplyConstraints(self, use_bone : bool = False) : 
        X = self.GetActiveObject() if use_bone == False else self.GetActiveBone()
        if X : 
            const = self.GetConstraintActive(X)
            if not const : return
            bpy.ops.constraint.apply(constraint=const.name, owner='BONE' if use_bone else 'OBJECT')
            if len(X.constraints) > 0:
                X.active_constraint -= 1    
    
    def RemoveAllConstraints(self, use_bone : bool = False):
        X = self.GetActiveObject() if use_bone == False else self.GetActiveBone()
        if X : 
            for constraint in X.constraints:
                X.constraints.remove(constraint)
    
    def MoveConstraints(self, use_bone : bool = False, type : str = "DOWN"):
        X = self.GetActiveObject() if use_bone == False else self.GetActiveBone()
        if not X : return 
        
        const = self.GetConstraintActive(X)
        if not const : return
        
        index = X.active_constraint-1 if type == "UP" else X.active_constraint+1
        
        if 0 <= index < len(X.constraints):
            if index > -1 and index < len(X.constraints):
                bpy.ops.constraint.move_to_index(
                    constraint=const.name, 
                    owner='BONE' if use_bone else 'OBJECT', 
                    index=index,
                )
                X.active_constraint = index
        
    def CopyConstraints(self, use_bone : bool = False, use_index=True):
        
        X = self.GetActiveObject() if use_bone == False else self.GetActiveBone()
        if not X : return
        constraint = self.GetConstraintActive(X)
        if not constraint : return
        
        # Get the index of the constraint
        if use_index: 
            constraint_index = X.constraints.find(constraint.name)
        
        X_Select = self.GetSelectableObjects() if use_bone == False else self.GetSelectBones(mode="POSE")
        X_Select.remove(X)
        print(X_Select)
        # Copy the constraint to the selected bones
        for Select in X_Select:
            
            if Select != X:
                new_constraint = Select.constraints.new(type=constraint.type)
                
                for attr in dir(constraint):
                    if not attr.startswith("_") and not callable(getattr(constraint, attr)):
                        try:
                            setattr(new_constraint, attr, getattr(constraint, attr))
                        except AttributeError:
                            pass
                
                # Handle targets for ARMATURE constraint type
                if constraint.type == 'ARMATURE':
                    # Ensure the new constraint has the correct number of targets
                    while len(new_constraint.targets) < len(constraint.targets):
                        new_constraint.targets.new()

                    for i, tgt in enumerate(constraint.targets):
                        if tgt.target is not None:
                            new_constraint.targets[i].target = tgt.target
                            new_constraint.targets[i].subtarget = tgt.subtarget
                            new_constraint.targets[i].weight = tgt.weight
                
                        
                if use_index:        
                    # Move the new constraint to the correct index
                    constraints = Select.constraints
                    for i in range(len(constraints) - 1, constraint_index, -1):
                        constraints.move(i, i-1)

"""
Para Reset Todos los Hueso en la Armadura de Rig Creator
"""

class ResetArmature(GeneralArmatureData):
    
    def init(self):
        self.Armature = bpy.context.active_object
        if not self.IsArmatureExists() : return

        self.NE_Spine = []
        for i in range(6):
            self.NE_Spine.append(f"base_spine.{i+1:003}")

        Faces = [
            ("Mouth_UP", 3), ("Mouth_DOWN", 3), 
            ("Nose", 3), ("Jaw", 4), 
            ("Cheekbone_UP", 4), ("Cheekbone_DOWN", 3),
            ("Eyebrows", 4), ("Subeyebrows", 3),
            ("Subeyelids_UP", 4),
            ("Eyelids_UP", 4), ("Eyelids_DOWN", 4),
            ("Subeyelids_UP", 4), ("Ear", 5)
        ]
        
        MEdFaces = [
            ("Medface_UP", 4), ("Medface_DOWN", 2),
        ]
        
        for face in MEdFaces :
            face_name = face[0].lower()
            if "UP" in face[0]:
                face_name = face_name.replace("_up", "_UP")
            if "DOWN" in face[0]:
                face_name = face_name.replace("_down", "_DOWN")
            setattr(
                    self, f"NE_{face[0]}", [
                        f"base_{face_name}.{i+1:003}" for i in range(face[1])
                    ]
            )
            
        for type in ["R", "L"]:
            
            
            setattr(self, f"NE_Roteye_{type}", [f"base_rot_eye_{type}"])
            
            for face in Faces:
                face_name = face[0].lower()
                if "UP" in face[0]:
                    face_name = face_name.replace("_up", "_UP")
                if "DOWN" in face[0]:
                    face_name = face_name.replace("_down", "_DOWN")
                setattr(
                    self, f"NE_{face[0]}_{type}", [
                        f"base_{face_name}_{type}.{i+1:003}" for i in range(face[1])
                    ]
                )
            
            for body in ["Arm", "Leg", "Feet", "Shoulder", "Hip"] : 
               setattr(
                self, f"NE_{body}_{type}", [
                    f"base_{body.lower()}_{type}.{i+1:003}" for i in range(
                        3 if body == "Arm" else 2
                        )
                    ]
                )
            
            for finger in self.ListFinger() :
                setattr(
                    self, f"NE_{finger}_{type}", [f"base_{finger.lower()}_{type}.{i+1:003}" for i in range(4)]
                ) 
            
    
    def ResetAllArmature(self) : 
        self.init()
        self.ResetFace()
        #self.ResetCartoonFace()
        self.ResetSpine()
        self.ResetRoot()
        self.ResetArm("R"), self.ResetArm("L")
        for finger in self.ListFinger():
            name = finger.lower().replace(" ", "_").lower()
            self.ResetFingers(name, "R")
            self.ResetFingers(name, "L")
        self.ResetLeg("R"), self.ResetLeg("L")
        
    # Reseta los Huesos de la cara, el Armture selecionado
    def ResetFace(self) : 
        self.init()
        self.SetMode(mode="EDIT")

        for type in ["R", "L"] : 
            
            BS_RotEye = self.GetBones(
                    getattr(self, f"NE_Roteye_{type}"), mode="EDIT"
            )
            
            # Parpados
            for directon in ["UP", "DOWN"] : 

                BS_Eyelids = self.GetBones(
                    getattr(self, f"NE_Eyelids_{directon}_{type}"), mode="EDIT"
                )
                Df_Eyelids = self.GetBones(
                    [f"def_eyelids_{directon}_{type}.{i+1:003}" for i in range(len(BS_Eyelids))] 
                    , mode="EDIT"
                    )
                CONT_Eyelids = self.GetBones(
                    [f"cont_eyelids_{directon}_{type}.{i+1:003}" for i in range(len(BS_Eyelids)+1)] 
                    , mode="EDIT"
                    )

                ROT_Eye = self.GetBonesToRange(
                f"rot_eye_{directon}_{type}", 2, "EDIT"
                )
                
                if BS_RotEye and ROT_Eye:
                    for i in range(2):
                        if ROT_Eye[i] :
                            ROT_Eye[i].head = BS_RotEye[0].head
                            ROT_Eye[i].tail = BS_Eyelids[-2].head
                
                
                if BS_Eyelids and Df_Eyelids and CONT_Eyelids:
                    for i, bone in enumerate(Df_Eyelids) : 
                        self.SetTransform(bone, BS_Eyelids[i])
                        self.SetDisplaySize(
                            bone, BS_Eyelids[i], 
                            Display_size_x=2,
                            Display_size_y=2
                        )
                    for i in range(len(CONT_Eyelids)-1) : 
                        self.SetTransform(CONT_Eyelids[i], BS_Eyelids[i], length_value=0.2)
                    self.SetTransform(
                        CONT_Eyelids[-1], BS_Eyelids[-1], 
                        length_value=0.2, only_tail=True
                        )
                MV_Eyelids = self.GetBone(f"mov_eyelids_{directon}_{type}", "EDIT")
                if BS_Eyelids and MV_Eyelids :
                    MV_Eyelids.head = BS_Eyelids[-2].head
                    MV_Eyelids.tail = BS_Eyelids[-2].head + self.GetWorldNormal()
                    MV_Eyelids.roll = 0
                    Length : float = 0 
                    for bone in BS_Eyelids:
                        Length += bone.length
                    MV_Eyelids.length = (Length/len(BS_Eyelids))/2
                    
            CONT_SubEye = self.GetBones(
                    [f"cont_subeye_{type}.{i+1:003}" for i in range(2)] 
                    , mode="EDIT"
            )
            
            BS_Eyelids = self.GetBones(
                    getattr(self, f"NE_Eyelids_UP_{type}"), mode="EDIT"
                ) 
            
            if CONT_SubEye and BS_Eyelids:
                for i in range(2):
                    local_Head = BS_Eyelids[0].head if i == 0 else BS_Eyelids[-1].tail
                    CONT_SubEye[i].head = local_Head
                    CONT_SubEye[i].tail = local_Head
                    CONT_SubEye[i].roll = 0
                    Length : float = 0 
                    for bone in BS_Eyelids:
                        Length += bone.length
                    
                    
                    CONT_SubEye[i].length = (Length/len(BS_Eyelids))/2
            
            BS_SubEyelids = self.GetBones(
                    getattr(self, f"NE_Subeyelids_UP_{type}"), mode="EDIT"
                ) 
            Df_SubEyelids = self.GetBonesToRange(
                f"def_subeyelids_UP_{type}", len(BS_SubEyelids), "EDIT"
            )
            CONT_SubEyelids = self.GetBonesToRange(
                f"cont_subeyelids_UP_{type}", len(BS_SubEyelids)+1, "EDIT"
            )
            if BS_SubEyelids and Df_SubEyelids and CONT_SubEyelids:
                for i, bone in enumerate(Df_SubEyelids) : 
                    self.SetTransform(bone, BS_SubEyelids[i])
                    self.SetDisplaySize(
                        bone, BS_SubEyelids[i], 
                        Display_size_x=2,
                        Display_size_y=2
                    )
                for i in range(len(BS_SubEyelids)) : 
                    self.SetTransform(CONT_SubEyelids[i], BS_SubEyelids[i], length_value=0.2)
                    self.SetDisplaySize(
                        CONT_SubEyelids[i], BS_SubEyelids[i], 
                        Display_size_x=2.2,
                        Display_size_y=2.2
                    )
                self.SetTransform(CONT_SubEyelids[-1], BS_SubEyelids[-1], only_tail= True, length_value=0.2)
                self.SetDisplaySize(
                        CONT_SubEyelids[-1], BS_SubEyelids[-1], 
                        Display_size_x=2.2,
                        Display_size_y=2.2
                )                

            
            
            MV_SubEyelids = self.GetBone(f"mov_subeyelids_UP_{type}", "EDIT")
            if BS_SubEyelids and MV_SubEyelids :
                MV_SubEyelids.head = BS_SubEyelids[-2].head
                MV_SubEyelids.tail = BS_SubEyelids[-2].head + self.GetWorldNormal()
                MV_SubEyelids.roll = 0
                Length : float = 0 
                for bone in BS_SubEyelids:
                    Length += bone.length
                MV_SubEyelids.length = (Length/len(BS_SubEyelids))/2

            # Rot Eye
            ROT_Eye = self.GetBone(f"rot_eye_{type}", mode="EDIT")
            if ROT_Eye : 
                self.SetTransform(ROT_Eye, BS_RotEye[0])
            
            ROT_SubEye = self.GetBone(f"rot_subeye_{type}", mode="EDIT")
            if ROT_SubEye : 
                self.SetTransform(ROT_SubEye, BS_RotEye[0], length_value=0.5)
            
            # Control Eye 
            CONT_Eye = self.GetBone(f"cont_eye_{type}", mode="EDIT")
            if CONT_Eye : 
                self.SetTransform(CONT_Eye, BS_RotEye[0])

            # Eye
            
            Eye = self.GetBone(f"eye_{type}", mode="EDIT")
            if Eye : 
                Local_Head = (
                    BS_RotEye[0].tail[0],
                    (BS_RotEye[0].tail[1] - BS_RotEye[0].length*10),
                    BS_RotEye[0].tail[2],
                    )
                Local_Tail = (
                    BS_RotEye[0].tail[0],
                    (BS_RotEye[0].tail[1] - BS_RotEye[0].length*10),
                    BS_RotEye[0].tail[2]+1,
                    )
                Eye.head = Local_Head
                Eye.tail = Local_Tail
                Eye.length = BS_RotEye[0].length/2
            
            
            # Cejas
            BS_Eyebrows = self.GetBones(
                getattr(self, f"NE_Eyebrows_{type}"), mode="EDIT"
            )
            
            
            if BS_Eyebrows :

                # Def Cejas
                DF_Eyebrows = self.GetBonesToRange(
                    f"def_eyebrows_{type}", Range=4, mode="EDIT"
                )
                if DF_Eyebrows : 
                    for i, bone in enumerate(DF_Eyebrows) :
                        self.SetTransform(bone, BS_Eyebrows[i])
                
                
                # Control Cejas
                CONT_Eyebrows = self.GetBonesToRange(
                    f"cont_eyebrows_{type}", Range=5, mode="EDIT"
                )
                
                if CONT_Eyebrows : 
                    for i in range(len(BS_Eyebrows)) : 
                        self.SetTransform(
                            CONT_Eyebrows[i], BS_Eyebrows[i],
                            length_value=0.2
                        )
                    self.SetTransform(
                        CONT_Eyebrows[-1], DF_Eyebrows[-1], 
                        length_value=0.2, only_tail=True
                    )
                
                # Move Cejas
                MV_Eyebrows = self.GetBonesToRange(
                    f"mov_eyebrows_{type}", 4, mode="EDIT"
                )
                MV_SubEyebrows = self.GetBonesToRange(
                    f"mov_subeyebrows_{type}", 4, mode="EDIT"
                )
                if MV_Eyebrows and MV_SubEyebrows :
                    Length : float = 0 
                    for bone in BS_Eyebrows:
                        Length += bone.length
                        
                    for i in range(4) : 
                        MV_Eyebrows[i].head = BS_Eyebrows[i].head
                        MV_Eyebrows[i].tail = BS_Eyebrows[i].head
                        MV_Eyebrows[i].roll = 0
                        MV_Eyebrows[i].length = (Length/len(BS_Eyebrows))/2
                        
                        MV_SubEyebrows[i].head = BS_Eyebrows[i].head
                        MV_SubEyebrows[i].tail = BS_Eyebrows[i].head
                        MV_SubEyebrows[i].roll = 0
                        MV_SubEyebrows[i].length = (Length/len(BS_Eyebrows))/2
                
                # Mov SubCejas
                MV_Eyebrows = self.GetBone(f"mov_eyebrows_{type}", mode="EDIT")
                MV_SubEyebrows = self.GetBone(f"mov_subeyebrows_{type}", mode="EDIT")
                if MV_Eyebrows and MV_SubEyelids : 
                    
                    local_Head = (BS_Eyebrows[-2].head + BS_Eyebrows[-2].tail)/2
                    Length : float = 0 
                    for bone in BS_Eyebrows:
                        Length += bone.length
                        
                    MV_Eyebrows.head = local_Head
                    MV_Eyebrows.tail = local_Head
                    MV_Eyebrows.roll = 0
                    MV_Eyebrows.length = (Length/len(BS_Eyebrows))/2
                    
                    MV_SubEyebrows.head = local_Head
                    MV_SubEyebrows.tail = local_Head
                    MV_SubEyebrows.roll = 0
                    MV_SubEyebrows.length = (Length/len(BS_Eyebrows))/2

                Eyebrows = self.GetBone(f"eyebrows", mode="EDIT")
                if Eyebrows : 
                    Length : float = 0 
                    for bone in BS_Eyebrows:
                        Length += bone.length
                    Eyebrows.head = BS_Eyebrows[-1].tail
                    Eyebrows.tail = BS_Eyebrows[-1].tail
                    Eyebrows.roll = 0
                    Eyebrows.length = (Length/len(BS_Eyebrows))/2
                
            # SubCejas
            BS_SubEyebrows = self.GetBones(
                getattr(self, f"NE_Subeyebrows_{type}"), mode="EDIT"
            )
            
            if BS_SubEyebrows : 
                
                # Def SubCejas
                Def_SubCejas = self.GetBonesToRange(
                    f"def_subeyebrows_{type}", 3, mode="EDIT"
                )

                if Def_SubCejas : 
                    for i, bone in enumerate(Def_SubCejas) : 
                        self.SetTransform(bone, BS_SubEyebrows[i])
        
        # Eyes
        Eyes = self.GetBones(["eye_L", "eye_R"], mode="EDIT")
        Eye = self.GetBones(["eyes", "subeyes", "subeyes.001", "subeyes.002"], mode="EDIT")  
        if Eyes and Eye: 
            Local_Head = (
                    (Eyes[0].head[0] + Eyes[1].head[0]) / 2,
                    (Eyes[0].head[1] + Eyes[1].head[1]) / 2,
                    Eyes[0].head[2]
                )
            Local_Tail = (
                (Eyes[0].tail[0] + Eyes[1].tail[0]) / 2,
                (Eyes[0].tail[1] + Eyes[1].tail[1]) / 2,
                Eyes[0].tail[2]
            ) 
            for bone in Eye:
                bone.head, bone.tail = Local_Head, Local_Tail
            head = Eye[0].head.copy()
            for bone in Eyes:
                head.x , head.y, head.z = bone.head.x, head.y, bone.head.z
                bone.head = head
                bone.tail = head + self.GetWorldNormal()
                bone.roll = 0
                length : float = 0
                for b in self.GetBones(["base_rot_eye_L", "base_rot_eye_R"], mode="EDIT"):
                    length += b.length
                bone.length = length / 2
        
        # MED Face
        for direction in ["UP", "DOWN"]:
            BS_MEdFace = self.GetBones(
                getattr(self, f"NE_Medface_{direction}"), mode="EDIT"
            )
            if BS_MEdFace : 
                
                # Def MEdFace
                
                Def_MedFace = self.GetBonesToRange(
                    f"def_medface_{direction}",
                    4 if direction == "UP" else 2,
                    mode="EDIT"    
                )
                if Def_MedFace : 
                    self.SetTransformToBones(Def_MedFace, BS_MEdFace)
                
                #Control MedFace
                
                Cont_MedFace = self.GetBonesToRange(
                    f"cont_medface_{direction}", 
                    5 if direction == "UP" else 3,
                    mode="EDIT"
                )
                
                if Cont_MedFace : 
                    for i in range(4 if direction == "UP" else 2):
                        self.SetTransform(Cont_MedFace[i], BS_MEdFace[i], length_value=0.2)
                    self.SetTransform(Cont_MedFace[-1], BS_MEdFace[-1], length_value=0.2, only_tail=True)

        # Nose
        
        for type in ["R", "L"] : 
            BS_Nose = self.GetBones(
                getattr(self, f"NE_Nose_{type}"), mode="EDIT"
            )
            if BS_Nose : 
                # Def
                Def_Nose = self.GetBonesToRange(
                    f"def_nose_{type}", Range=3, mode="EDIT"
                )
                if Def_Nose : 
                    self.SetTransformToBones(Def_Nose, BS_Nose)

                # Control 
                Cont_Nose = self.GetBonesToRange(
                    f"cont_nose_{type}", Range=4, mode="EDIT"
                )
                if Cont_Nose :
                    for i in range(3) : 
                        self.SetTransform(Cont_Nose[i], BS_Nose[i], length_value=0.2)
                    self.SetTransform(Cont_Nose[-1], BS_Nose[-1], length_value=0.2, only_tail=True)

                Cont_SubNose = self.GetBone(
                    f"cont_subnose_{type}", mode="EDIT"
                ) 
                if Cont_SubNose :
                    Local_Base = self.GetBone(
                            f"base_cheekbone_UP_{type}.004", mode="EDIT"
                    )
                    Cont_SubNose.head = Local_Base.tail
                    Cont_SubNose.tail = Local_Base.head
                    Cont_SubNose.roll = 0
                    Cont_SubNose.length /= 2
                
                Cont_Nose = self.GetBone(
                    f"cont_nose_{type}", mode="EDIT"
                )
                if Cont_Nose : 
                    Local_Base = self.GetBone(
                        f"base_nose_{type}.001", mode="EDIT"
                    )
                    Cont_Nose.head = Local_Base.tail
                    Cont_Nose.tail = Local_Base.tail + self.GetWorldNormal()
                    Cont_Nose.roll = 0 
                    Cont_Nose.length = Local_Base.length/2
                
        
        Nose = self.GetBones(
            ["nose", "rot_subnose", "rot_nose"], mode="EDIT"
        )        
        
        if Nose :
            local_Base = self.GetBone(f"base_medface_UP.003", mode="EDIT")
            local_head = (self.GetBone(f"cont_nose_L", mode="EDIT").head + self.GetBone(f"cont_nose_R", mode="EDIT").head ) / 2
            local_tail = local_Base.tail
            for bone in Nose :
                bone.head, bone.tail = local_head, local_tail
                bone.roll = 0
                bone.length = local_Base.length / 2
        
        Cont_Nose = self.GetBone(
            f"cont_nose", mode="EDIT"
        )
        if Cont_Nose : 
            Local_Base = self.GetBone("base_medface_UP.003", mode="EDIT")
            Cont_Nose.head = Local_Base.tail
            Cont_Nose.tail = Local_Base.tail + self.GetWorldNormal()
            Cont_Nose.roll = 0
            Cont_Nose.length = Local_Base.length / 2
                
        # Pomulos 
        
        for type in ["R", "L"] : 
            for dir in ["UP", "DOWN"] : 
                BS_Cheekbone = self.GetBonesToRange(
                    f"base_cheekbone_{dir}_{type}", Range=4 if dir == "UP" else 3, mode="EDIT"
                )
                if BS_Cheekbone : 
                    # Def
                    Def_Cheekbone = self.GetBonesToRange(
                        f"def_cheekbone_{dir}_{type}", Range=4 if dir == "UP" else 3, mode="EDIT"
                    )
                    
                    if Def_Cheekbone : 
                        self.SetTransformToBones(Def_Cheekbone, BS_Cheekbone)
                    
                    # Control 
                    Cont_Cheekbone = self.GetBonesToRange(
                        f"cont_cheekbone_{dir}_{type}", Range=5 if dir == "UP" else 4, mode="EDIT"
                    )
                    if Cont_Cheekbone : 
                        for i in range(4 if dir == "UP" else 3):
                            self.SetTransform(Cont_Cheekbone[i], BS_Cheekbone[i], length_value=0.2)
                        self.SetTransform(
                            Cont_Cheekbone[-1], BS_Cheekbone[-1], length_value=0.2, only_tail=True
                        )  
        
        # Quijada
        
        for type in ["R", "L"] : 
            BS_Jaw = self.GetBonesToRange(
                f"base_jaw_{type}", 4, mode="EDIT"
            )
            if BS_Jaw :
                
                # DEf 
                Def_Jaw = self.GetBonesToRange(
                    f"def_jaw_{type}", 4, mode="EDIT"
                )
                if Def_Jaw : 
                    self.SetTransformToBones(Def_Jaw, BS_Jaw)
                
                # Control
                Cont_Jaw = self.GetBonesToRange(
                    f"cont_jaw_{type}", 5, mode="EDIT"
                )
                if Cont_Jaw :
                    for i in range(4) :
                        self.SetTransform(
                            Cont_Jaw[i], BS_Jaw[i], length_value=0.2
                        )
                    self.SetTransform(
                            Cont_Jaw[-1], BS_Jaw[-1], length_value=0.2, only_tail=True
                    )
        
        # Orejas

        for type in ["R", "L"] : 
            BS_Ear = self.GetBonesToRange(
                f"base_ear_{type}", 5, mode="EDIT"
            )
            if BS_Ear : 
                
                # DEF
                Def_Ear = self.GetBonesToRange(
                    f"def_ear_{type}", 5, mode="EDIT"
                )
                if Def_Ear : 
                    self.SetTransformToBones(Def_Ear, BS_Ear)
                
                # Control
                Cont_Ear = self.GetBonesToRange(
                    f"cont_ear_{type}", 6, mode="EDIT"
                )
                
                if Cont_Ear : 
                    for i in range(5) : 
                        self.SetTransform(Cont_Ear[i], BS_Ear[i], length_value=0.2)
                    self.SetTransform(Cont_Ear[-1], BS_Ear[-1], length_value=0.2, only_tail=True)
                
                Ear = self.GetBone(
                    f"ear_{type}", mode="EDIT"
                )
                if Ear : 
                    Local_Head = (BS_Ear[-1].head + BS_Ear[-1].tail) / 2
                    Ear.head = Local_Head 
                    Ear.tail = Local_Head + self.GetWorldNormal()
                    Ear.length = BS_Ear[-1].length / 2
                    Ear.roll = 0
                
                Rot_Ear = self.GetBone(
                    f"rot_ear_{type}", mode="EDIT"
                )
                if Rot_Ear : 
                    Local_Head = (BS_Ear[-1].head + BS_Ear[-1].tail) / 2
                    Local_Tail = (BS_Ear[1].head + BS_Ear[1].tail) / 2
                    Rot_Ear.head = Local_Head 
                    Rot_Ear.tail = Local_Tail
                    Rot_Ear.length = BS_Ear[-1].length / 2
                    Rot_Ear.roll = 0
                
                Cont_Ear = self.GetBone(
                    f"cont_ear_{type}", mode="EDIT"
                )
                
                if Cont_Ear : 
                    Local_Head = (BS_Ear[1].head + BS_Ear[1].tail) / 2
                    Cont_Ear.head = Local_Head 
                    Cont_Ear.tail = Local_Head + self.GetWorldNormal()
                    Cont_Ear.length = BS_Ear[2].length / 2
                    Cont_Ear.roll = 0
                
        # Boca
        for dir in ["UP", "DOWN"] : 
            for type in ["R", "L"] : 
                BS_Mouth= self.GetBonesToRange(
                    f"base_mouth_{dir}_{type}", 3, mode="EDIT"
                )
                if BS_Mouth :
                    
                    # Def 
                    Def_Mouth = self.GetBonesToRange(
                        f"def_mouth_{dir}_{type}", 3, mode="EDIT"
                    )
                    
                    if Def_Mouth :
                        self.SetTransformToBones(
                            Def_Mouth, BS_Mouth
                        )
                    
                    # Control
                    Cont_Mouth = self.GetBonesToRange(
                        f"cont_mouth_{dir}_{type}", 4, mode="EDIT"
                    )
                    if Cont_Mouth : 
                        for i in range(3) :
                            self.SetTransform(Cont_Mouth[i], BS_Mouth[i], length_value=0.2)
                        self.SetTransform(Cont_Mouth[-1], BS_Mouth[-1], length_value=0.2, only_tail=True)            
                    # Control 
                    Cont_SubMouth = self.GetBonesToRange(
                        f"cont_submouth_{dir}_{type}", 3, mode="EDIT"
                    )
                    
                    if Cont_SubMouth :
                        for i in range(2) :
                            
                            Cont_SubMouth[i].head = BS_Mouth[i+1].head 
                            Cont_SubMouth[i].tail = BS_Mouth[i+1].tail + self.GetWorldNormal()
                            Cont_SubMouth[i].roll = 0
                            Cont_SubMouth[i].length = BS_Mouth[i+1].length/1.5
                        
                        Cont_SubMouth[-1].head = BS_Mouth[-1].tail
                        Cont_SubMouth[-1].tail = BS_Mouth[-1].tail + self.GetWorldNormal()
                        Cont_SubMouth[-1].roll = 0
                        Cont_SubMouth[-1].length = BS_Mouth[-1].length/1.5
                            
            BS_Mouth = self.GetBone(
                f"base_mouth_{dir}_L.001", mode="EDIT"
            )
            if BS_Mouth :
                
                # Control 
                Cont_SubMouth = self.GetBone(
                    f"cont_submouth_{dir}", mode="EDIT"
                )
                
                if Cont_SubMouth :
                    Cont_SubMouth.head = BS_Mouth.head 
                    Cont_SubMouth.tail = BS_Mouth.tail + self.GetWorldNormal()
                    Cont_SubMouth.roll = 0
                    Cont_SubMouth.length = BS_Mouth.length/1.5
            
        # Rot
        
        Rot_Mouth = self.GetBones(
            ["rot_mouth", "rot_mouth_DOWN", "rot_mouth_UP", 
             "rot_mouth_MED", "rot_submouth_MED.001", "rot_submouth_MED.002", "rot_submouth_MED"], 
            mode="EDIT"
        )
        if Rot_Mouth : 
            if self.GetBone(f"cont_cheekbone_DOWN_{type}.003", mode="EDIT"):
                Local_Head = mathutils.Vector((0, 0, 0))
                Local_Tail = mathutils.Vector((0, 0, 0))
                for type in ["R", "L"] :
                    Local_Head += self.GetBone(f"cont_cheekbone_DOWN_{type}.003", mode="EDIT").head
                    Local_Head += self.GetBone(f"cont_jaw_{type}.003", mode="EDIT").head
                    Local_Tail += self.GetBone(f"base_mouth_UP_{type}.001", mode="EDIT").head
                    Local_Tail += self.GetBone(f"base_mouth_DOWN_{type}.001", mode="EDIT").head
                
                Local_Head /= 4
                Local_Tail /= 4
                
                for bone in Rot_Mouth :
                    bone.head = Local_Head
                    bone.tail = Local_Tail
                    bone.roll = 0
            
        
        # General Boca
        Mouth = self.GetBones(
            ["mouth", "mouth_UP", "mouth_DOWN", "submouth_UP", "submouth_DOWN", ], mode="EDIT"
        )
        
        if Mouth :
            
            Local_Head = mathutils.Vector((0, 0, 0))
            Local_Head += self.GetBone(f"base_mouth_UP_L.001", mode="EDIT").head
            Local_Head += self.GetBone(f"base_mouth_DOWN_L.001", mode="EDIT").head
            for bone in Mouth :
                bone.head = (Local_Head / 2)
                bone.tail = (Local_Head / 2) + self.GetWorldNormal()
                bone.roll = 0
                bone.length = self.GetBone(f"base_mouth_DOWN_L.001", mode="EDIT").length/2
        
        # Sub Mauth
        for type in ["R", "L"] : 
            def GetLocalHead(n : str = ".001"):
                local_Head = mathutils.Vector((0, 0, 0))
                for dir in ["UP", "DOWN"] : 
                    Local_Base = self.GetBone(f"base_mouth_{dir}_{type}{n}", mode="EDIT")
                    if local_Base :
                        local_Head += Local_Base.tail
                return local_Head/2
            
            SubMouth = self.GetBonesToRange(
                f"submouth_{type}", 3, mode="EDIT"
            )
            
            if SubMouth : 
                for i in range(3):
                    SubMouth[i].head = GetLocalHead(f".00{i+1}")
                    SubMouth[i].tail = GetLocalHead(f".00{i+1}") + self.GetWorldNormal()
                    SubMouth[i].length /= 100
            
            Mouth = self.GetBone(f"mouth_{type}", mode="EDIT")
            if Mouth :
                Mouth.head = GetLocalHead(f".003")
                Mouth.tail = GetLocalHead(f".003") + self.GetWorldNormal()
                Mouth.length = self.GetBone("base_cheekbone_DOWN_L.001", mode="EDIT").length / 3
                    
        # Quijada
        Jaw = self.GetBones(
            ["cont_subjaw", "jaw", "subjaw",], mode="EDIT"
        )
        if Jaw :
            Local_Base_1 = self.GetBones(["base_jaw_L.002", "base_jaw_R.002"], mode="EDIT")
            Local_Base_2 = self.GetBones(["base_jaw_L.004", "base_jaw_R.004"], mode="EDIT")
            if Local_Base_1 and Local_Base_2:
                Local_Head = (Local_Base_1[0].head + Local_Base_1[1].head) / 2
                Local_Tail = (Local_Base_2[0].tail + Local_Base_2[1].tail) / 2
                for bone in Jaw:
                    bone.head = Local_Head
                    bone.tail = Local_Tail
                    bone.roll = 0

            
        # Dientes 
        for dir in ["UP", "DOWN"] : 
            for type in ["R", "L"] : 
                Bs_Tooth = self.GetBonesToRange(
                    f"base_tooth_{dir}_{type}", 3, mode="EDIT"
                )
                
                if Bs_Tooth :
                    
                    # Def
                    Def_Tooth = self.GetBonesToRange(
                    f"def_tooth_{dir}_{type}", 3, mode="EDIT"
                    )
                    if Def_Tooth : 
                        self.SetTransformToBones(
                            Def_Tooth, Bs_Tooth
                        )
                        
                    # Control
                    Cont_Tooth = self.GetBonesToRange(
                    f"cont_tooth_{dir}_{type}", 4, mode="EDIT"
                    )
                    if Cont_Tooth : 
                        for i in range(3):
                            self.SetTransform(
                                Cont_Tooth[i], Bs_Tooth[i], length_value=0.2
                            )
                        self.SetTransform(
                            Cont_Tooth[-1], Bs_Tooth[-1], length_value=0.2, only_tail=True
                        )

                    Cont_Tooth = self.GetBone(
                        f"cont_tooth_{dir}", mode="EDIT"
                    )
                    if Cont_Tooth :
                        
                        Cont_Tooth.head = Bs_Tooth[0].head
                        Cont_Tooth.tail = Bs_Tooth[0].head + self.GetWorldNormal()
                        Cont_Tooth.roll = 0 
                        Cont_Tooth.length = Bs_Tooth[0].length / 4
            
            
            Bs_Tooth = self.GetBones(
                    [f"base_tooth_{dir}_L.003", f"base_tooth_{dir}_R.003"], mode="EDIT"
            )
            if Bs_Tooth :
                
                Tooth = self.GetBone(
                    f"tooth_{dir}", mode="EDIT"
                )
                if Tooth :
                    Local_Head = (Bs_Tooth[0].tail + Bs_Tooth[1].tail) / 2
                    Tooth.head = Local_Head
                    Tooth.tail = Local_Head + self.GetWorldNormal()
                    Tooth.roll = 0 
                    Local_Length = self.GetDistancia3d(Bs_Tooth[0].tail, Bs_Tooth[1].tail)
                    Tooth.length = Local_Length/2

        
        Bs_Tongue = self.GetBonesToRange(
            f"base_tongue", 3, mode="EDIT"
        )
        if Bs_Tongue :
            
            # Def 
            Def_Tongue = self.GetBonesToRange(
                f"def_tongue", 3, mode="EDIT"
            )
            if Def_Tongue : 
                self.SetTransformToBones(Def_Tongue, Bs_Tongue)
            
            # Cont 
            Cont_Tongue = self.GetBonesToRange(
                f"cont_tongue", 4, mode="EDIT"
            ) 
            if Cont_Tongue:
                for i in range(3):
                    self.SetTransform(
                        Cont_Tongue[i], Bs_Tongue[i], length_value=0.2
                    )
                self.SetTransform(
                        Cont_Tongue[-1], Bs_Tongue[-1], length_value=0.2, only_tail=True
                    )
                
            # Rot
            Rot_Tongue = self.GetBonesToRange(
                f"rot_tongue", 3, mode="EDIT"
            )
            if Rot_Tongue : 
                self.SetTransformToBones(Rot_Tongue, Bs_Tongue)
            
            # Fk 
            Fk_Tongue = self.GetBonesToRange(
                f"fk_tongue", 3, mode="EDIT"
            )
            if Fk_Tongue : 
                self.SetTransformToBones(Fk_Tongue, Bs_Tongue)
            
            RotFk_Tongue = self.GetBone(
                f"rotfk_tongue", mode="EDIT"
            )
            if RotFk_Tongue :
                RotFk_Tongue.head = Bs_Tongue[0].head
                RotFk_Tongue.tail = Bs_Tongue[-1].tail
                RotFk_Tongue.roll = Bs_Tongue[0].roll
        
            #Root
            Root_Tongue = self.GetBone(
                f"root_tongue", mode="EDIT"
            )
            if Root_Tongue :
                self.SetTransform(Root_Tongue, Bs_Tongue[0], length_value=0.5)
            
            #IK
            Ik_Tongue = self.GetBonesToRange(
                f"ik_tongue", 4, mode="EDIT"
            )
            if Ik_Tongue:
                for i in range(3) : 
                    self.SetTransform(
                        Ik_Tongue[i], Bs_Tongue[i]
                    )
                self.SetTransform(
                        Ik_Tongue[-1], Bs_Tongue[-1], only_tail=True
                    )
        
        
        
        self.SetMode(mode="POSE")
        # Fk 
        Fk_Tongue = self.GetBonesToRange(
            f"fk_tongue", 3, mode="POSE"
        )
        if Fk_Tongue : 
            for bone in Fk_Tongue:
                bone.custom_shape_translation[1] = bone.length/2

                
        self.ResetALLBoneStretchTo()
    
    def ResetCartoonFace(self) :
        
        self.SetMode(mode="EDIT")
        # Head 
        BS_Head = self.GetBone("base_head", mode="EDIT")
        if BS_Head :
            CONT_head = self.GetBonesToRange(Bone_Name="cont_def_head", Range=2, mode="EDIT")
            if CONT_head :
                self.SetTransform(CONT_head[0], BS_Head, length_value=0.2)
                self.SetTransform(CONT_head[1], BS_Head, length_value=0.2, only_tail=True)
            
            DEF_Head = self.GetBone(Bone_Name="def_head", mode="EDIT")
            if DEF_Head : 
                self.SetTransform(DEF_Head, BS_Head)
            
            HEAD = self.GetBone("head", mode="EDIT")
            if HEAD : 
                self.SetTransform(HEAD, BS_Head)
        
        # Eyes
        for type in ["R", "L"] :
            for dir in ["UP", "DOWN", "MED"] : 
                BS_Eyelid = self.GetBonesToRange(
                Bone_Name=f"base_eyelid_{dir}_{type}", Range=3 if dir != "MED" else 2, mode="EDIT"
                )
                if BS_Eyelid : 
                    DEF_Eyelid = self.GetBonesToRange(
                    Bone_Name=f"def_eyelid_{dir}_{type}", Range=3 if dir != "MED" else 2, mode="EDIT"
                    )
                    if DEF_Eyelid :
                        self.SetTransformToBones(DEF_Eyelid, BS_Eyelid)

                    if dir != "MED" :
                        CONT_Eyelid = self.GetBone(Bone_Name="cont_eyelid_{dir}_{type}", mode="EDIT")
                        if CONT_Eyelid : 
                            self.SetTransform(CONT_Eyelid, BS_Eyelid[1])
            # ROT Eye
            BASE_rot_Eye = self.GetBone(f"base_rot_eye_{type}", mode="EDIT")
            if BASE_rot_Eye :
                DEF_rot_Eye = self.GetBone(f"def_rot_eye_{type}", mode="EDIT")
                if DEF_rot_Eye :
                    self.SetTransform(DEF_rot_Eye, BASE_rot_Eye)
                    
            for dir in ["UP", "DOWN"] : 
                ROT_eyelid = self.GetBonesToRange(
                    Bone_Name=f"rot_eyelid_{dir}_{type}", Range=2, mode="EDIT"
                )
                if ROT_eyelid :
                    for i in range(2) :
                        ROT_eyelid[i].head = BASE_rot_Eye.head
                        ROT_eyelid[i].tail = self.GetBone(f"base_eyelid_{dir}_{type}.002", mode="EDIT").head
                
                # Cont Eye
                CONT_eyelid = self.GetBone(f"cont_eyelid_{dir}_{type}", mode="EDIT")
                if CONT_eyelid : 
                    self.SetTransform(CONT_eyelid, self.GetBone(f"base_eyelid_{dir}_{type}.002", mode="EDIT"), length_value=10)
        
            # Cont General Eye 

            head = self.CreateVector(0, 0, 0)
            if self.GetBone(Bone_Name="base_eyelid_UP_L.002") and self.GetBone(Bone_Name="base_eyelid_DOWN_L.002") :
                length = self.GetDistancia3d(
                    self.GetBone(Bone_Name="base_eyelid_UP_L.002").head,
                    self.GetBone(Bone_Name="base_eyelid_DOWN_L.002").head,
                )
            else :
                length = 0
            for dir in ["UP", "DOWN", "MED"] :
                BS_Eyelid = self.GetBonesToRange(
                    Bone_Name=f"base_eyelid_{dir}_{type}", Range=3 if dir != "MED" else 2, mode="EDIT"
                    )
                for bone in BS_Eyelid:
                    head += bone.head
            
            head /= 8
            CONT_Eye = self.GetBone(Bone_Name=f"cont_eye_{type}", mode="EDIT")
            if CONT_Eye : 
                CONT_Eye.head = head
                CONT_Eye.tail = head + self.GetWorldNormal()
                CONT_Eye.length = length/2
        
        for dir in ["UP", "DOWN"] : 
            #Mouth 
            BS_Mouth = self.GetBone(Bone_Name=f"base_mouth_{dir}.001", mode="EDIT")
            if BS_Mouth : 
                DEF_Mouth = self.GetBone(Bone_Name=f"def_mouth_{dir}.001", mode="EDIT")
                if DEF_Mouth : 
                    self.SetTransform(DEF_Mouth, BS_Mouth)
                    
                Mouth = self.GetBonesToRange(Bone_Name=f"mouth_{dir}", Range=2, mode="EDIT")
                print(Mouth)
                if Mouth : 
                    
                    for bone in Mouth:
                        self.SetTransform(bone, BS_Mouth, length_value=6)

            for type in ["L", "R"] : 
                BS_Mouth = self.GetBonesToRange(Bone_Name=f"base_mouth_{dir}_{type}", Range=3, mode="EDIT")
                DEF_Mouth = self.GetBonesToRange(Bone_Name=f"def_mouth_{dir}_{type}", Range=3, mode="EDIT")
                if DEF_Mouth : 
                    self.SetTransformToBones(DEF_Mouth, BS_Mouth)
                

        #Mouth MED
        for type in ["L", "R"] : 
            BS_Mouth = self.GetBone(Bone_Name=f"base_mouth_MED_{type}", mode="EDIT")
            DEF_Mouth = self.GetBone(Bone_Name=f"def_mouth_MED_{type}.001", mode="EDIT")
            if DEF_Mouth : 
                self.SetTransform(DEF_Mouth, BS_Mouth)
            Mouth = self.GetBone(Bone_Name=f"mouth_MED_{type}", mode="EDIT")
            if Mouth : 
                self.SetTransform(Mouth, BS_Mouth)
            MED_Mouth = self.GetBonesToRange(Bone_Name=f"mouth_MED_{type}", Range=3, mode="EDIT")
            if MED_Mouth : 
                Bone_UP = self.GetBonesToRange(Bone_Name=f"base_mouth_UP_{type}", Range=3, mode="EDIT")
                Bone_DOWN = self.GetBonesToRange(Bone_Name=f"base_mouth_DOWN_{type}", Range=3, mode="EDIT")
                for i in range(3):
                    head = (
                        Bone_UP[i].head +
                        Bone_DOWN[i].head
                    )/2
                    MED_Mouth[i].head = head
                    MED_Mouth[i].tail = head + self.GetWorldNormal()
                    MED_Mouth[i].length = Bone_UP[i].length
        
        head = (self.GetBone(Bone_Name="base_mouth_UP.001", mode="EDIT").head + 
                self.GetBone(Bone_Name="base_mouth_DOWN.001", mode="EDIT").head) / 2
        
        Mouth = self.GetBone(Bone_Name="mouth", mode="EDIT")
        if Mouth : 
            Mouth.head = head
            Mouth.tail = head + self.GetWorldNormal()
            Mouth.length = self.GetBone(Bone_Name="base_mouth_UP.001", mode="EDIT").length * 6
        
        BS_ROT_Mouth = self.GetBone(Bone_Name="base_rot_mouth", mode="EDIT")
        if BS_ROT_Mouth : 
            for dir in ["UP", "DOWN", "MED"] :
                ROT_Mouth = self.GetBone(Bone_Name=f"rot_mouth_{dir}", mode="EDIT")  
                if ROT_Mouth :
                    ROT_Mouth.head = BS_ROT_Mouth.head 
                    if dir != "MED" : 
                        ROT_Mouth.tail = self.GetBone(Bone_Name=f"base_mouth_{dir}.001", mode="EDIT").head 
                    else:
                        ROT_Mouth.tail = (
                            self.GetBone(Bone_Name=f"base_mouth_UP.001", mode="EDIT").head  + 
                            self.GetBone(Bone_Name=f"base_mouth_DOWN.001", mode="EDIT").head  
                        ) / 2
                    ROT_Mouth.roll = 0
        ROT_Mouth = self.GetBone(Bone_Name="rot_mouth_UP", mode="EDIT")          
        if ROT_Mouth : 
            MED_Mouth = self.GetBone(Bone_Name="rot_mouth_MED.001", mode="EDIT")
            if MED_Mouth :
                self.SetTransform(MED_Mouth, ROT_Mouth, length_value=0.5) 
        
        
        for type in ["L", "R"] : 
            BS_Rot_Eye = self.GetBone(Bone_Name=f"base_rot_eye_{type}", mode="EDIT")
            if BS_Rot_Eye :
               Eye = self.GetBone(Bone_Name=f"eye_{type}", mode="EDIT") 
               if Eye :
                   
                    head = self.CreateVector(
                        BS_Rot_Eye.tail.x, 
                        (BS_Rot_Eye.tail.y - (BS_Rot_Eye.length*3)), 
                        BS_Rot_Eye.tail.z, 
                    )
                   
                    Eye.head = head
                    Eye.tail = head + self.GetWorldNormal()
                    Eye.length = BS_Rot_Eye.length/2
        
        Eye = self.GetBone(Bone_Name="eye", mode="EDIT")
        if Eye : 
            head = (
                self.GetBone(Bone_Name=f"eye_L", mode="EDIT").head + 
                self.GetBone(Bone_Name=f"eye_R", mode="EDIT").head
            ) / 2
            tail = (
                self.GetBone(Bone_Name=f"eye_L", mode="EDIT").tail + 
                self.GetBone(Bone_Name=f"eye_R", mode="EDIT").tail
            ) / 2
            Eye.head = head 
            Eye.tail = tail
        
        #Ear
        for type in ["L", "R"] : 
        
            BS_Ear = self.GetBone(Bone_Name=f"base_ear_{type}", mode="EDIT")
            if BS_Ear : 
                DF_Ear = self.GetBone(Bone_Name=f"def_ear_{type}", mode="EDIT")
                if DF_Ear : 
                    self.SetTransform(DF_Ear, BS_Ear)
                    
            CONT_Ear = self.GetBonesToRange(Bone_Name=f"cont_ear_{type}", Range=2, mode="EDIT")
            if CONT_Ear: 
                self.SetTransform(CONT_Ear[0], BS_Ear, length_value=0.2)
                self.SetTransform(CONT_Ear[1], BS_Ear, length_value=0.2, only_tail=True)

            Ear = self.GetBone(Bone_Name=f"ear_{type}", mode="EDIT")
            if Ear :
                self.SetTransform(Ear, BS_Ear)
            
            # Tooth 
            if self.GetBone(Bone_Name="base_tooth_UP_L.001", mode="EDIT") : 
                
                for dir in ["UP", "DOWN"] : 
                    BS_Tooth = self.GetBone(Bone_Name=f"base_tooth_{dir}_L.001", mode="EDIT")
                    DF_Tooth = self.GetBone(Bone_Name=f"def_Ctooth_{dir}", mode="EDIT")
                    if DF_Tooth : 
                        DF_Tooth.head = BS_Tooth.head
                        DF_Tooth.tail = BS_Tooth.head + self.GetWorldNormal()
                        DF_Tooth.length = BS_Tooth.length
                        
                    for type in ["R", "L"] : 
                        BS_Tooth = self.GetBonesToRange(Bone_Name=f"base_tooth_{dir}_{type}", Range=3, mode="EDIT")
                        if BS_Tooth : 
                            DF_Tooth = self.GetBonesToRange(
                                Bone_Name=f"def_Ctooth_{dir}_{type}", Range=3, mode="EDIT"
                            )
                            if DF_Tooth : 
                                for i in range(3) : 
                                    
                                    DF_Tooth[i].head = BS_Tooth[i].tail
                                    DF_Tooth[i].tail = BS_Tooth[i].tail + self.GetWorldNormal()
                                    DF_Tooth[i].length = BS_Tooth[i].length
                
                    head = (
                        self.GetBone(Bone_Name=f"base_tooth_{dir}_L.003", mode="EDIT").tail + 
                        self.GetBone(Bone_Name=f"base_tooth_{dir}_R.003", mode="EDIT").tail 
                        ) / 2

                    tail = self.GetBone(Bone_Name=f"base_tooth_{dir}_L.001", mode="EDIT").head
                    
                    Tooth = self.GetBone(Bone_Name=f"tooth_{dir}", mode="EDIT")
                    if Tooth : 
                        Tooth.head, Tooth.tail = head, tail
            
            
            #Tongue
            BS_Tongue = self.GetBonesToRange(Bone_Name="base_tongue", Range=3, mode="EDIT")
            if BS_Tongue : 
                DF_Tongue = self.GetBonesToRange(Bone_Name="def_tongue", Range=4, mode="EDIT")
                if DF_Tongue : 
                    for i in range(3) : 
                        self.SetTransform(DF_Tongue[i], BS_Tongue[i], length_value=0.8)
                    self.SetTransform(DF_Tongue[-1], BS_Tongue[-1], length_value=0.8, only_tail=True)
                FK_Tongue = self.GetBonesToRange(Bone_Name="fk_tongue", Range=3, mode="EDIT")
                if FK_Tongue : 
                    self.SetTransformToBones(FK_Tongue, BS_Tongue) 
        self.ResetALLBoneStretchTo()
        
    def ResetSpine(self) : 
        
        self.SetMode(mode="EDIT")
        BS_Spine = self.GetBonesToRange(
            f"base_spine", 6, mode="EDIT"
        )
        
        
        
        if BS_Spine : 
            
            Root_P = self.GetBone(f"root_head_properties", mode="EDIT") 
            if Root_P : 
                self.SetTransform(Root_P, BS_Spine[-1], length_value=0.4)
                
            # DEF
            Def_Spine = self.GetBonesToRange(
                f"def_spine", 6, mode="EDIT"
            )
            
            if Def_Spine : 
                self.SetTransformToBones(Def_Spine, BS_Spine)
            
            # Rot
            Rot_Spine = self.GetBone("rot_subspine", mode="EDIT")
            if Rot_Spine : 
                Rot_Spine.head = BS_Spine[-2].head
                Rot_Spine.tail = BS_Spine[-2].head + self.GetWorldNormal()
                Rot_Spine.roll = 0 
                Rot_Spine.length = BS_Spine[-2].length / 2
                
            
            # Control
            Cont_Spine = self.GetBonesToRange(
                f"cont_spine", 5, mode="EDIT"
            )
            if Cont_Spine : 
                for i in range(4):
                    self.SetTransform(Cont_Spine[i], BS_Spine[i], length_value=0.2)
                self.SetTransform(Cont_Spine[-1], BS_Spine[3], length_value=0.2, only_tail=True)

            Cont_SubSpine = self.GetBonesToRange(
                f"cont_subspine", 2, mode="EDIT"
            )
            if Cont_SubSpine :
                for bone in Cont_SubSpine :
                    bone.head = BS_Spine[2].head
                    bone.tail = BS_Spine[2].head + self.GetWorldNormal()
                    bone.roll = 0 
                    bone.length = BS_Spine[2].length / 4
            
            #ROT
            Rot_Spine_DOWN = self.GetBonesToRange(
                f"rot_spine_DOWN", 2, mode="EDIT"
            ) 
            
            if Rot_Spine_DOWN :
                self.SetTransform(Rot_Spine_DOWN[0], BS_Spine[1], invert_head_tail=True)
                self.SetTransform(Rot_Spine_DOWN[1], BS_Spine[0], invert_head_tail=True)
                
            Rot_Spine_UP = self.GetBonesToRange(
                f"rot_spine_UP", 2, mode="EDIT"
            ) 
            
            if Rot_Spine_UP :
                self.SetTransform(Rot_Spine_UP[0], BS_Spine[2])
                self.SetTransform(Rot_Spine_UP[1], BS_Spine[3])

            # Hombros Caderas
            Shoulders = self.GetBone(f"shoulders", mode="EDIT")
            if Shoulders : 
                Shoulders.head = BS_Spine[2].head
                Shoulders.tail = BS_Spine[3].tail
                Shoulders.roll = 0
                
            hips = self.GetBone(f"hips", mode="EDIT")
            if hips : 
                hips.head = BS_Spine[1].tail
                hips.tail = BS_Spine[0].head
                hips.roll = 0
            
            

            #Head
            Cont_Spine = self.GetBones(
                ["cont_spine.006", "cont_spine.007", "cont_spine.008"], mode="EDIT"
            )
            if Cont_Spine :
                self.SetTransform(Cont_Spine[0], BS_Spine[4], length_value=0.2)
                self.SetTransform(Cont_Spine[1], BS_Spine[5], length_value=0.2)
                self.SetTransform(Cont_Spine[2], BS_Spine[5], length_value=0.2, only_tail=True)
            
            Head = self.GetBone(
                f"head", mode="EDIT"
            )
            if Head :
                self.SetTransform(Head, BS_Spine[5])
            Neck = self.GetBone(
                f"neck", mode="EDIT"
            )
            if Neck :
                self.SetTransform(Neck, BS_Spine[4])
            
            self.SetMode("POSE") 
            for dir in ["UP", "DOWN"]:
                Rot_Spine = self.GetBonesToRange(
                f"rot_spine_{dir}", 2, mode="POSE"
            ) 
                if Rot_Spine :
                    for bone in Rot_Spine:
                        bone.custom_shape_translation[1] = bone.length/2
        
            Shoulders = self.GetBone(f"shoulders", mode="POSE")
            if Shoulders :
                Shoulders.custom_shape_translation[1] = Shoulders.length/1.5
            hips = self.GetBone(f"hips", mode="POSE")
            if hips :
                hips.custom_shape_translation[1] = hips.length/1.5
            
            Head = self.GetBone(
                f"head", mode="POSE"
            )
            if Head : 
                Head.custom_shape_translation[1] = Head.length
            
            Neck = self.GetBone(
                f"neck", mode="POSE"
            )
            if Neck : 
                Neck.custom_shape_translation[1] = Neck.length/2
        
        self.SetMode(mode="EDIT")
        for type in ["R","L"]:
            BS_Shoulder = self.GetBonesToRange(
                f"base_shoulder_{type}", 2, mode="EDIT"
            )
            if BS_Spine : 
                
                # Def 
                Def_Shoulder = self.GetBonesToRange(
                    f"def_shoulder_{type}", 2 , mode="EDIT"
                )
                if Def_Shoulder :
                    self.SetTransformToBones(Def_Shoulder, BS_Shoulder)
                
                # Control 
                Cont_Shoulder = self.GetBonesToRange(
                    f"cont_shoulder_{type}", 2, "EDIT"
                )
                if Cont_Shoulder :
                    self.SetTransform(Cont_Shoulder[0], BS_Shoulder[1], length_value=0.2)
                    self.SetTransform(Cont_Shoulder[1], BS_Shoulder[1], length_value=0.2, only_tail=True)
                Shoulder = self.GetBone(
                    f"shoulder_{type}", "EDIT"
                )
                if Shoulder : 
                    self.SetTransform(Shoulder, BS_Shoulder[1])
              
            BS_Hip = self.GetBone(f"base_hip_{type}", mode="EDIT")
            #hip
            if BS_Hip : 
                
                # Def
                Def_Hip = self.GetBone(f"def_hip_{type}", mode="EDIT")
                if Def_Hip :
                    self.SetTransform(Def_Hip, BS_Hip)
                    
                # Control
                Cont_Hip = self.GetBone(f"cont_hip_{type}", mode="EDIT")
                if Cont_Hip :
                    self.SetTransform(Cont_Hip, BS_Hip, length_value=0.2, only_tail=True)
                
        self.ResetALLBoneStretchTo()
        
    def ResetArm(self, type : str = "R") : 
        
        self.SetMode("EDIT")
        BS_Arm = self.GetBonesToRange(
            f"base_arm_{type}", 3, mode="EDIT"
        )

        if BS_Arm :
            UPArm_1 = {
                "head" : BS_Arm[0].head,
                "tail" : (BS_Arm[0].head + BS_Arm[0].tail) / 2,
                "roll" : BS_Arm[0].roll
            }
            UPArm_2 = {
                "head" : (BS_Arm[0].head + BS_Arm[0].tail) / 2,
                "tail" : BS_Arm[0].tail,
                "roll" : BS_Arm[0].roll
            }
            
            DOWNArm_1 = {
                "head" : BS_Arm[1].head,
                "tail" : (BS_Arm[1].head + BS_Arm[1].tail) / 2,
                "roll" : BS_Arm[1].roll
            }
            DOWNArm_2 = {
                "head" : (BS_Arm[1].head + BS_Arm[1].tail) / 2,
                "tail" : BS_Arm[1].tail,
                "roll" : BS_Arm[1].roll
            }
            
            for dir in ["UP", "DOWN"] : 
                Def_Arm = self.GetBonesToRange(
                    f"def_arm_{dir}_{type}", 2, mode="EDIT"
                )
                if Def_Arm :
                    Def_Arm[0].head = UPArm_1["head"] if dir == "UP" else DOWNArm_1["head"]
                    Def_Arm[0].tail = UPArm_1["tail"] if dir == "UP" else DOWNArm_1["tail"]
                    Def_Arm[0].roll = UPArm_1["roll"] if dir == "UP" else DOWNArm_1["roll"]
            
                    Def_Arm[1].head = UPArm_2["head"] if dir == "UP" else DOWNArm_2["head"]
                    Def_Arm[1].tail = UPArm_2["tail"] if dir == "UP" else DOWNArm_2["tail"]
                    Def_Arm[1].roll = UPArm_2["roll"] if dir == "UP" else DOWNArm_2["roll"]
            
                Cont_Arm = self.GetBonesToRange(
                    f"cont_arm_{dir}_{type}", 3, mode="EDIT"
                )
                if Cont_Arm :
                    for i in range(2) : 
                        self.SetTransform(Cont_Arm[i], Def_Arm[i], length_value=0.2)
                    self.SetTransform(Cont_Arm[-1], Def_Arm[-1], length_value=0.2, only_tail=True)
            
            # Hand
            Hand = self.GetBone(
                f"def_hand_{type}", mode="EDIT"
            )
            if Hand : 
                self.SetTransform(Hand, BS_Arm[-1])
            
            Cont_Hand = self.GetBonesToRange(
                f"cont_hand_{type}", 2, mode="EDIT"
            )
            if Cont_Hand :
                self.SetTransform(Cont_Hand[0], BS_Arm[-1], length_value=0.2)
                self.SetTransform(Cont_Hand[-1], BS_Arm[-1], length_value=0.2, only_tail=True)
            
            # Sub Arms 
            SubArm = self.GetBonesToRange(
                f"subarm_{type}", 2 , mode="EDIT"
            )
            C_SubArm = self.GetBonesToRange(
                f"C_subarm_{type}", 2 , mode="EDIT"
            )
            if SubArm and C_SubArm :
                for i in range(2) : 
                    self.SetTransform(SubArm[i], BS_Arm[i])
                    self.SetTransform(C_SubArm[i], BS_Arm[i])
            
            Cont_SubArm = self.GetBonesToRange(
                f"cont_subarm_{type}", 3, mode="EDIT"
            )
            if Cont_SubArm :
                for i in range(2) : 
                    self.SetTransform(
                        Cont_SubArm[i], BS_Arm[i], length_value=0.2
                )
                self.SetTransform(
                        Cont_SubArm[-1], BS_Arm[1], length_value=0.2, only_tail=True
                )
            
            Rot_Arm = self.GetBonesToRange(
                f"rot_arm_{type}", 3, mode="EDIT"
            )
            if Rot_Arm :
                self.SetTransformToBones(Rot_Arm, BS_Arm)
            
            # Fk
            Fk_Arm = self.GetBonesToRange(
                f"fk_arm_{type}", 3, mode="EDIT"
            )
            if Fk_Arm :
                self.SetTransformToBones(Fk_Arm, BS_Arm)
            
            Root_Arm = self.GetBone(
                f"root_arm_{type}", mode="EDIT"
            )
            
            if Root_Arm :
                self.SetTransform(Root_Arm, BS_Arm[0], length_value=0.4)
            
            
            # IK
            Ik_Arm = self.GetBonesToRange(
                f"ik_arm_{type}", 3, mode="EDIT"
            )
            if Ik_Arm :
                self.SetTransformToBones(Ik_Arm, BS_Arm)
                
            PoleArm = self.GetBone(
            f"polearm_{type}", mode="EDIT"
            )
            if PoleArm :
                distance = BS_Arm[0].length + BS_Arm[1].length
                self.SetPoleTransform(PoleArm, [BS_Arm[0], BS_Arm[1]], distance)
            
            IK = self.GetBones(
                [f"rot_polearm_{type}"], mode="EDIT"
            )
            if IK :
                for bone in IK :
                    self.SetTransform(bone, BS_Arm[0], length_value=0.5)
            
            SubPoleArm = self.GetBone(
                f"subpolearm_{type}", mode="EDIT"
            )
            if SubPoleArm :
                Local_Head = self.GetBone(
                    f"cont_subarm_{type}.002", mode="EDIT"
                ).head
                Local_Tail = self.GetBone(
                    f"polearm_{type}", mode="EDIT"
                ).head
                SubPoleArm.head = Local_Head
                SubPoleArm.tail = Local_Tail
            
        Root_P = self.GetBone(f"root_arm_properties_{type}", mode="EDIT") 
        if Root_P : 
            self.SetTransform(Root_P, BS_Arm[0], length_value=0.4)
        
        Followed = self.GetBone(f"ik_arm_{type}.003.001", mode="EDIT") 
        if Followed : 
            self.SetTransform(Followed, BS_Arm[-1], length_value=0.4)
        
        self.SetMode(mode="POSE")
        Fk_Arm = self.GetBonesToRange(
            f"fk_arm_{type}", 3, mode="POSE"
        )
        if Fk_Arm :
            for bone in Fk_Arm :
                bone.custom_shape_translation[1] = bone.length / 2

        IK = self.GetBone(
                f"ik_arm_{type}.001", mode="POSE"
            )
        if IK :
            IK.custom_shape_translation[1] = IK.length/2
        
        Ik_Arm = self.GetBone(
            f"ik_arm_{type}.003", mode="POSE"
        )
        if Ik_Arm :
            Ik_Arm.custom_shape_translation[1] = Ik_Arm.length*3
        
        
        
        self.ResetALLBoneStretchTo()    
    
    def ResetFingers(self, Finger : str = "thumb", type : str = "R") : 
        
        
        self.SetMode(mode="EDIT")
        
        
        Bs_Finger = self.GetBonesToRange(
            f"base_{Finger}_{type}", 4, mode="EDIT"
        )
        index : int = len(Bs_Finger)
        if Bs_Finger and index: 
            
            # Def 
            Def_Finger = self.GetBonesToRange(
            f"def_{Finger}_{type}", index, mode="EDIT"
            )
            if Def_Finger :
                self.SetTransformToBones(Def_Finger, Bs_Finger)
            
            # Control 
            Cont_Finger = self.GetBonesToRange(
            f"cont_{Finger}_{type}", index+1, mode="EDIT"
            )
            
            if Cont_Finger : 
                for i in range(index) : 
                    self.SetTransform(
                        Cont_Finger[i], Bs_Finger[i], length_value=0.2
                    )
                self.SetTransform(
                        Cont_Finger[-1], Bs_Finger[-1], length_value=0.2, only_tail=True
                    )

            # Root
            Root_Finger = self.GetBone(
                f"root_{Finger}_{type}", mode="EDIT"
            )
            if Root_Finger :
                self.SetTransform(Root_Finger, Bs_Finger[0])
                
            
            # Fk
            Fk_Finger = self.GetBonesToRange(
                f"fk_{Finger}_{type}", index-1, mode="EDIT"
            )
            if Fk_Finger :
                for i in range(index-1):
                    self.SetTransform(Fk_Finger[i], Bs_Finger[i+1])
                self.SetRelations(Fk_Finger[0], Root_Finger)
            
            if Finger != "thumb":
                
                # Rot 
                Rot_Finger = self.GetBonesToRange(
                    f"rot_{Finger}_{type}", index-1, mode="EDIT"
                )
                if Rot_Finger :
                    for i in range(index-1):
                        self.SetTransform(Rot_Finger[i], Bs_Finger[i+1])
                
                # IK
                Ik_Finger = self.GetBonesToRange(
                    f"ik_{Finger}_{type}", index, mode="EDIT"
                )
                
                if Ik_Finger : 
                    for i in range(index-1):
                        self.SetTransform(Ik_Finger[i], Bs_Finger[i+1])
                    self.SetTransform(Ik_Finger[-1], Bs_Finger[-1], only_tail=True)

            else :
                
                # Rot 
                Rot_Finger = self.GetBonesToRange(
                    f"rot_{Finger}_{type}", index, mode="EDIT"
                )
                if Rot_Finger :
                    for i in range(index):
                        self.SetTransform(Rot_Finger[i], Bs_Finger[i])
                
                # IK
                Ik_Finger = self.GetBonesToRange(
                    f"ik_{Finger}_{type}", index+1, mode="EDIT"
                )
                
                if Ik_Finger : 
                    for i in range(index):
                        self.SetTransform(Ik_Finger[i], Bs_Finger[i])
                    self.SetTransform(Ik_Finger[-1], Bs_Finger[-1], only_tail=True)
                    
                    
            Rot_Finger = self.GetBone(
                    f"rot_{Finger}_{type}", mode="EDIT"
                )
            if Rot_Finger :
                bone = Bs_Finger[1] if Finger != "thumb" else Bs_Finger[0]
                Rot_Finger.head = bone.head
                Rot_Finger.tail = bone.tail
                Rot_Finger.roll = bone.roll
                length : float = 0 
                for bone in Bs_Finger :
                    length += bone.length
                Rot_Finger.length = length / 2 if Finger != "thumb" else length
                
                if Finger == "thumb" :
                    Rot_Finger.parent = self.GetBone(f"rot_arm_{type}.003", mode="EDIT")
                
        self.SetMode(mode="POSE")
        Fk_Finger = self.GetBonesToRange(
                f"fk_{Finger}_{type}", index-1, mode="POSE"
            )
        if Fk_Finger :
            for bone in Fk_Finger:
                bone.custom_shape_translation[1] = bone.length/2
        
        
        #def setrot(bone, bs_bone):
        #    cont = self.CreateConstraint(
        #            bone,
        #            'COPY_LOCATION', 
        #            "RGC_cont", 
        #            self.GetActiveObject(), 
        #            bs_bone, 
        #            "LOCAL", "LOCAL",
        #            )
        #    cont.use_offset = True
        #    cont = self.CreateConstraint(
        #        bone,
        #        'COPY_ROTATION', 
        #        "RGC_cont", 
        #        self.GetActiveObject(), 
        #        bs_bone,  
        #        "LOCAL", 
        #        "LOCAL", 
        #        )
        #    cont.mix_mode = 'BEFORE'
        #
        #if Finger != "thumb" : 
        #    Fk_Finger = self.GetBonesToRange(
        #            f"fk_{Finger}_{type}", index, mode="POSE"
        #        )
        #    
        #    if Fk_Finger :
        #        for cont in Fk_Finger[0].constraints:
        #            if cont.type == "COPY_SCALE": 
        #                Fk_Finger[0].constraints.remove(cont)
        #        if not Fk_Finger[0].constraints:
        #            subtarget = self.GetBone(f"rot_{Finger}_{type}", mode="POSE")
        #            setrot(Fk_Finger[0], subtarget)
        #else:    
        #    Root_Finger = self.GetBone(
        #            f"root_{Finger}_{type}", mode="POSE"
        #        )
        #    Rot_Finger = self.GetBone(
        #            f"rot_{Finger}_{type}", mode="POSE"
        #        )
        #    if Root_Finger and Rot_Finger :
        #        setrot(Root_Finger, Rot_Finger)
            
        self.ResetALLBoneStretchTo()
            
        ... 
    
    def ResetLeg(self, type : str = "R") : 
        
        
        self.SetMode(mode="EDIT")
        Bs_Leg = self.GetBonesToRange(
            f"base_leg_{type}", 2, mode="EDIT"
        )
        
        
        if Bs_Leg : 
            
            Bs_LegUp_1 = CreateFakeBone(
                Bs_Leg[0].head, (Bs_Leg[0].head+Bs_Leg[0].tail)/2,
                Bs_Leg[0].roll, Bs_Leg[0].length/2
            )
            Bs_LegUp_2 = CreateFakeBone(
                (Bs_Leg[0].head+Bs_Leg[0].tail)/2, Bs_Leg[0].tail,
                Bs_Leg[0].roll, Bs_Leg[0].length/2
            )
            Bs_LegDown_1 = CreateFakeBone(
                Bs_Leg[1].head, (Bs_Leg[1].head+Bs_Leg[1].tail)/2,
                Bs_Leg[1].roll, Bs_Leg[1].length/2
            )
            Bs_LegDown_2 = CreateFakeBone(
                (Bs_Leg[1].head+Bs_Leg[1].tail)/2, Bs_Leg[1].tail,
                Bs_Leg[1].roll, Bs_Leg[1].length/2
            )
            
            
            for dir in ["UP", "DOWN"] : 
                # Def 
                Def_Leg = self.GetBonesToRange(
                    f"def_leg_{dir}_{type}", 2, mode="EDIT"
                )
                if Def_Leg : 
                    self.SetTransform(Def_Leg[0], Bs_LegUp_1 if dir == "UP" else Bs_LegDown_1)
                    self.SetTransform(Def_Leg[1], Bs_LegUp_2 if dir == "UP" else Bs_LegDown_2)

                Cont_Leg = self.GetBonesToRange(
                    f"cont_leg_{dir}_{type}", 3, mode="EDIT"
                )
                if Cont_Leg : 
                    for i in range(2):
                        self.SetTransform(
                            Cont_Leg[i], Def_Leg[i], length_value=0.2
                        )
                    self.SetTransform(
                            Cont_Leg[-1], Def_Leg[-1], length_value=0.2, only_tail=True
                        )
            
                SubLeg = self.GetBonesToRange(
                    f"subleg_{type}", 2, mode="EDIT"
                )
                if SubLeg : 
                    self.SetTransformToBones(
                        SubLeg, Bs_Leg,
                    )
                    
                C_SubLeg = self.GetBonesToRange(
                    f"C_subleg_{type}", 2, mode="EDIT"
                )
                if C_SubLeg : 
                    self.SetTransformToBones(
                        C_SubLeg, Bs_Leg,
                    )
                
                Cont_SubLeg = self.GetBonesToRange(
                    f"cont_subleg_{type}", 3, mode="EDIT"
                )
                if Cont_SubLeg : 
                    for i in range(2):
                        self.SetTransform(Cont_SubLeg[i], Bs_Leg[i], length_value=0.2)
                    self.SetTransform(Cont_SubLeg[-1], Bs_Leg[-1], length_value=0.2, only_tail=True) 
                    
            
        Bs_Feet = self.GetBonesToRange(
            f"base_feet_{type}", 3, mode="EDIT"
        )
        
        if Bs_Feet : 
            
            # Def 
            Def_Feet = self.GetBonesToRange(
                f"def_feet_{type}", 3,  mode="EDIT"
            )
            if Def_Feet : 
                self.SetTransformToBones(Def_Feet, Bs_Feet)
            
            # Control 
            Cont_Feet = self.GetBonesToRange(
                f"cont_feet_{type}", 3,  mode="EDIT"
            )
            if Cont_Feet : 
                for i in range(2):
                    self.SetTransform(Cont_Feet[i], Bs_Feet[i], length_value=0.2)
                self.SetTransform(Cont_Feet[-1], Bs_Feet[1], length_value=0.2, only_tail=True)
        
        if Bs_Leg and Bs_Feet :
            
            # Rot 
            Rot_Leg = self.GetBonesToRange(
                f"rot_leg_{type}", 4, mode="EDIT"
            )
            if Rot_Leg : 
                for i in range(2):
                    self.SetTransform(Rot_Leg[i], Bs_Leg[i])
                for i in range(2):
                    self.SetTransform(Rot_Leg[i+2], Bs_Feet[i])
            
            # FK 
            Fk_Leg = self.GetBonesToRange(
                f"fk_leg_{type}", 4, mode="EDIT"
            )
            if Fk_Leg : 
                self.SetTransformToBones(Fk_Leg, Rot_Leg)
            
            # IK
            Ik_Leg = self.GetBonesToRange(
                f"ik_leg_{type}", 4, mode="EDIT"
            )
            if Ik_Leg : 
                self.SetTransformToBones(Ik_Leg, Rot_Leg)

            Ik_Leg = self.GetBone(
                f"ik_leg_{type}", mode="EDIT"
            )
            if Ik_Leg : 
                Ik_Leg.head = Bs_Leg[-1].tail 
                Ik_Leg.tail = (
                    Bs_Leg[-1].tail[0],
                    Bs_Feet[-2].tail[1],
                    Bs_Leg[-1].tail[2],
                    )
                Ik_Leg.roll = 0

            Ik_SubLeg = self.GetBonesToRange(
                f"ik_subleg_{type}", 2, mode="EDIT"
            )
            if Ik_SubLeg : 
                self.SetTransform(Ik_SubLeg[0], Ik_Leg, length_value=0.2)
                self.SetTransform(Ik_SubLeg[1], Bs_Feet[-2], length_value=0.5, only_tail=True)
            
            Rot_Ik_Leg = self.GetBonesToRange(
                f"rot_ik_leg_{type}", 5, mode="EDIT"
            )
            if Rot_Ik_Leg : 
                self.SetTransform(Rot_Ik_Leg[0], Bs_Feet[1], length_value=0.5)
                Local_Head_1 = Bs_Feet[-1].head
                Local_Head_2 = (Bs_Feet[-1].head + Bs_Feet[-1].tail)/ 2
                Local_Head_3 = Bs_Feet[-1].tail
                Local_Head_4 = (Bs_Feet[-1].head + Bs_Feet[-1].tail)/ 2
                Local_Head_4[1] = Bs_Feet[1].tail[1]
                
                Rot_Ik_Leg[1].head = Local_Head_1
                Rot_Ik_Leg[1].tail = Local_Head_1 + (self.GetWorldNormal("y")*-1)
                Rot_Ik_Leg[1].length = Bs_Feet[-1].length * 0.5
                
                Rot_Ik_Leg[2].head = Local_Head_2
                Rot_Ik_Leg[2].tail = Local_Head_2 + (self.GetWorldNormal("y")*-1)
                Rot_Ik_Leg[2].length = Bs_Feet[-1].length * 0.5
                
                Rot_Ik_Leg[3].head = Local_Head_3
                Rot_Ik_Leg[3].tail = Local_Head_3 + (self.GetWorldNormal("y")*-1)
                Rot_Ik_Leg[3].length = Bs_Feet[-1].length * 0.5
                
                Rot_Ik_Leg[4].head = Local_Head_4
                Rot_Ik_Leg[4].tail = Local_Head_4 + (self.GetWorldNormal("y")*-1)
                Rot_Ik_Leg[4].length = Bs_Feet[-1].length * 0.5
            
            Rot_Ik_Leg = self.GetBone(
                f"rot_ik_leg_{type}", mode="EDIT"
            )
            if Rot_Ik_Leg : 
                Local_Head_2 = (Bs_Feet[-1].head + Bs_Feet[-1].tail)/ 2
                Rot_Ik_Leg.head = Local_Head_2
                Rot_Ik_Leg.tail = Local_Head_2 + (self.GetWorldNormal("y")*-1)
                Rot_Ik_Leg.length = Bs_Feet[-1].length * 0.5
        
            # Pole
            PoleLeg = self.GetBone(
                f"poleleg_{type}", mode="EDIT"
            )
            if PoleLeg : 
                self.SetPoleTransform(PoleLeg, [Bs_Leg[0], Bs_Leg[1]],  (Bs_Leg[0].length+Bs_Leg[1].length)/1.3)
                
            SubPoleLeg_L = self.GetBone(
                f"subpoleleg_{type}", mode="EDIT"
            )
            if SubPoleLeg_L and PoleLeg : 
                SubPoleLeg_L.head = Bs_Leg[0].tail
                SubPoleLeg_L.tail = PoleLeg.head
                SubPoleLeg_L.roll = 0

            # Feet 
            Rot_Feet = self.GetBone(
                f"rot_feet_{type}", mode="EDIT"
            )
            if Rot_Feet : 
                self.SetTransform(Rot_Feet, Bs_Feet[1])
            
        #Root
        Root = self.GetBone(f"root_leg_{type}", mode="EDIT")
        if Root :
            self.SetTransform(Root, Bs_Leg[0], length_value=0.5)  
        
        Root_P = self.GetBone(f"root_leg_properties_{type}", mode="EDIT") 
        if Root_P : 
            self.SetTransform(Root_P, Bs_Leg[0], length_value=0.4)
           
           
        Ik_Leg = self.GetBone(f"ik_leg_{type}", mode="EDIT")
        Followed = self.GetBone(f"ik_leg_{type}.005", mode="EDIT")
        if Ik_Leg and Followed : 
            self.SetTransform(Followed, Ik_Leg, length_value=0.4)
        
        self.ResetALLBoneStretchTo()
        
        Bs_Leg = self.GetBonesToRange(
            f"base_leg_{type}", 2, mode="POSE"
        )
        Bs_Feet = self.GetBonesToRange(
            f"base_feet_{type}", 3, mode="POSE"
        )
        
        # FK 
        Fk_Leg = self.GetBonesToRange(
            f"fk_leg_{type}", 4, mode="POSE"
        )
        if Fk_Leg : 
            for bone in Fk_Leg:
                bone.custom_shape_translation[1] = bone.length/2
        
        Ik_Leg = self.GetBone(
            f"ik_leg_{type}", mode="POSE"
        )
        if Ik_Leg :
            Ik_Leg.custom_shape_translation[1] = Ik_Leg.length/2.5
            Distance = self.GetDistancia3d(Bs_Leg[-1].tail, (Bs_Feet[-1].head+Bs_Feet[-1].tail)/2)
            Ik_Leg.custom_shape_translation[2] = (Distance*-1)/1.1
        
        Ik_Leg = self.GetBone(
            f"ik_leg_{type}.001", mode="POSE"
        )
        if Ik_Leg : 
            Ik_Leg.custom_shape_translation[1] = Ik_Leg.length/2
        
        # Feet 
        Rot_Feet = self.GetBone(
                f"rot_feet_{type}", mode="POSE"
            )
        if Rot_Feet : 
            Rot_Feet.custom_shape_translation[1] = Rot_Feet.length

        
    
    def ResetRoot(self) : 
        
        self.SetMode("EDIT")
        BS_Spine = self.GetBone(f"base_spine.001", mode="EDIT")
        Root_Hip = self.GetBone(f"Root_hip", mode="EDIT")
        if BS_Spine and Root_Hip:
            Root_Hip.head = BS_Spine.head 
            Root_Hip.tail = BS_Spine.head + self.GetWorldNormal()
            Root_Hip.roll = 0
            Root_Hip.length = BS_Spine.length
        Root_Hip = self.GetBone(f"Root_move", mode="EDIT")
        if Root_Hip : 
            Root_Hip.head = (0, 0, 0)
            Root_Hip.tail = self.GetWorldNormal(Eje="y")*-1
            Root_Hip.roll = 0 
        self.SetMode("POSE")
        Root_Hip = self.GetBone(f"Root_hip", mode="POSE")
        if Root_Hip : 
            Root_Hip.custom_shape_translation[1] = Root_Hip.length
          
    def ResetALLBoneStretchTo(self) : 
        self.SetMode(mode="POSE")
        for bone in self.GetActiveObject().pose.bones :
            for cont in bone.constraints:
                if cont.type == "STRETCH_TO" : 
                    cont.rest_length = 0
                    
    def ResetSelectBoneStretchTo(self) : 
        self.SetMode(mode="POSE")
        for bone in self.GetSelectBones("POSE") :
            for cont in bone.constraints:
                if cont.type == "STRETCH_TO" : 
                    cont.rest_length = 0

"""
Para General Diferentes Tipos de confinaciones de en los huesos
"""

class GeneratorsBones(GeneralArmatureData):


    def GN_Name(self, new_name , bone_name : str) -> str : 
        get_name = bone_name[-4:]
        list_name = (f".{i:003}" for i in range(10000))
        t_name : str = bone_name
        if get_name in list_name:
            t_name = bone_name[:-4]
        return new_name + t_name

    def AddBone(self):
        self.SetMode("EDIT")
        bpy.ops.armature.bone_primitive_add()
        self.SetMode("POSE")
    
    def GN_Parent(self, use_connect : bool = False):
        select_bone : list = self.GetNameToBones(self.GetSelectBones(mode="POSE", only_select=True))
        active_bone = self.GetNameToBones([self.GetActiveBone()])
        if not self.GetActiveBone() : return
        self.SetMode(mode="EDIT")
        select_bone = self.GetBones(select_bone, mode="EDIT")
        active_bone= self.GetBone(active_bone[0], mode="EDIT")
        if select_bone and active_bone:
            for bone in select_bone:
                bone.parent = active_bone
                if use_connect:
                    bone.use_connect = True
        self.SetMode(mode="POSE")
    def GN_ParentOffset(self):
        self.GN_Parent()
    def GN_ParentConnected(self):
        self.GN_Parent(use_connect=True) 
    def GN_ParentBendyBone(self):
        
        def SetParent(select_bone, active_bone):
            select_bone : list = self.GetBones(select_bone, mode="POSE")
            active_bone = self.GetBone(active_bone[0], mode="POSE")
            for bone in select_bone:
                for const in bone.parent.constraints:
                    if const.type == "ARMATURE" :
                        constraint = const
                        constraint.targets.new()
                        for i, tgt in enumerate(constraint.targets):
                            if tgt.target is None:
                                constraint.targets[i].target = self.GetActiveObject()
                                constraint.targets[i].subtarget = active_bone.name
                            constraint.targets[i].weight = 1.0 / len(constraint.targets)
            
        def SetNewBone(select_bone, active_bone):
            self.SetMode(mode="EDIT")
            select_bone : list = self.GetBones(select_bone, mode="EDIT")
            active_bone = self.GetBone(active_bone[0], mode="EDIT")
            
            if select_bone :
                names = []
                for bone in select_bone:
                    names.append(f"RGC_PARENT_{bone.name}")
                new_bone = self.CreateBones(names)
                if new_bone :
                    self.SetTransformToBones(new_bone, select_bone, length_value=0.5)
                    for i, bone in enumerate(select_bone):
                        self.SetDisplaySize(new_bone[i], bone)
                        bone.parent = new_bone[i]
                    self.SetDeform(new_bone, False)

            select_bone = self.GetNameToBones(select_bone)
            active_bone = self.GetNameToBones([active_bone])
            new_bone  = self.GetNameToBones(new_bone)
            self.SetMode(mode="POSE")
            select_bone : list = self.GetBones(select_bone, mode="POSE")
            active_bone = self.GetBone(active_bone[0], mode="POSE")
            new_bone = self.GetBones(new_bone, mode="POSE")
            
            if new_bone : 
                for bone in new_bone :
                    constraint = bone.constraints.new(type='ARMATURE')
                    constraint.targets.new()
                    for i, tgt in enumerate(constraint.targets):
                        if tgt.target is None:
                            constraint.targets[i].target = self.GetActiveObject()
                            constraint.targets[i].subtarget = active_bone.name
                            constraint.targets[i].weight = 1.0
        
        parent = []
        new_bone = []
        active_bone = self.GetActiveBone(mode="POSE")
        for bone in self.GetSelectBones(mode="POSE", only_select=True) :
            if bone.name != active_bone.name:
                if bone.parent :
                    if "RGC_PARENT_".lower() in bone.parent.name.lower():
                        parent.append(bone.name)
                    else:
                        new_bone.append(bone.name)
                else:
                    new_bone.append(bone.name)
   
        if parent:
            SetParent(parent[:], [active_bone.name])
        if new_bone:
            SetNewBone(new_bone[:], [active_bone.name])
    
    def GN_ParentActiveBendyBone(self):
        
        def SetParent(select_bone, active_bone):
            select_bone : list = self.GetBones(select_bone, mode="POSE")
            active_bone = self.GetBone(active_bone[0], mode="POSE")
            if new_bone : 
                constraint = new_bone.constraints.new(type='ARMATURE')
                for bone in select_bone:
                    constraint.targets.new()
                    for i, tgt in enumerate(constraint.targets):
                        if tgt.target is None:
                            constraint.targets[i].target = self.GetActiveObject()
                            constraint.targets[i].subtarget = bone.name
                        constraint.targets[i].weight = 1 / len(select_bone)
    
    
        def SetNewBone(select_bone, active_bone):
            self.SetMode(mode="EDIT")
            select_bone : list = self.GetBones(select_bone, mode="EDIT")
            active_bone = self.GetBone(active_bone[0], mode="EDIT")
            
            if active_bone:
                new_bone = self.CreateBonesRange(f"RGC_PARENT_{active_bone.name}", 1)
                self.SetTransform(new_bone[0], active_bone, length_value=0.5)
                self.SetDisplaySize(new_bone[0], active_bone)
                self.SetDeform(new_bone, False)
                active_bone.parent = new_bone[0]
                

            select_bone = self.GetNameToBones(select_bone)
            active_bone = self.GetNameToBones([active_bone])
            new_bone  = self.GetNameToBones(new_bone)
            self.SetMode(mode="POSE")
            select_bone : list = self.GetBones(select_bone, mode="POSE")
            active_bone = self.GetBone(active_bone[0], mode="POSE")
            new_bone = self.GetBone(new_bone[0], mode="POSE")
            
            if new_bone : 
                constraint = new_bone.constraints.new(type='ARMATURE')
                for bone in select_bone:
                    constraint.targets.new()
                    for i, tgt in enumerate(constraint.targets):
                        if tgt.target is None:
                            constraint.targets[i].target = self.GetActiveObject()
                            constraint.targets[i].subtarget = bone.name
                        constraint.targets[i].weight = 1 / len(select_bone)
        
        parent = []
        new_bone = []
        active_bone = self.GetActiveBone(mode="POSE")
        for bone in self.GetSelectBones(mode="POSE") :
            if bone.name != active_bone.name:
                if bone.parent :
                    if "RGC_PARENT_".lower() in bone.parent.name.lower():
                        parent.append(bone.name)
                    else:
                        new_bone.append(bone.name)
                else:
                    new_bone.append(bone.name)
   
        if parent:
            SetParent(parent[:], [active_bone.name])
        if new_bone:
            SetNewBone(new_bone[:], [active_bone.name])
    
    
    def GN_DampedTrackParent(self):
        
        self.SetMode("EDIT")
        self.UseMirror(False)
        select_bone = self.GetNameToBones(self.GetSelectBones(mode="EDIT", only_select=True))
        active_bone = self.GetNameToBones([self.GetActiveBone(mode="EDIT")])
        new_bones = []
        for name in select_bone : 
            bone = self.GetBone(name, "EDIT")
            if bone :
                parent = bone.parent
                new_bone = self.CreateBonesRange(self.GN_Name("DampedTrack_",bone.name), 1)
                self.SetDeform(new_bone, False)
                self.SetDisplaySize(new_bone[0], bone)
                self.SetTransform(new_bone[0], bone)
                new_bone[0].tail = self.GetBone(active_bone[0], mode="EDIT").head
                new_bone[0].length = bone.length / 2
                new_bone[0].parent = parent
                bone.parent = new_bone[0]
                new_bones.append(new_bone[0].name)
        self.UseMirror(True)
        self.SetMode(mode="POSE")
        for name in new_bones:
            bone = self.GetBone(name, "POSE")
            constraint = bone.constraints.new(type='DAMPED_TRACK')
            constraint.target = self.GetActiveObject()
            constraint.subtarget = active_bone[0]
        

                
        
    def GN_UnionBone(self):
        select_bone = self.GetSelectBones(mode="POSE")
        name_select_bone = self.GetNameToBones(select_bone)
        self.SetMode("EDIT")
        select_bone = self.GetBones(name_select_bone, mode="EDIT")
        root = self.CreateBones([f"Root_{name_select_bone[0]}"])
        
        if root : 
            head = self.CreateVector(0,0,0)
            length = 0
            for bone in select_bone:
                bone.parent = root[0]
                head += bone.head
                length += bone.length
            head /= len(select_bone)
            length /= len(select_bone)
            root[0].head = head
            root[0].tail = head + self.GetWorldNormal()
            root[0].length = length * 1.5
            root[0].color.palette = select_bone[0].color.palette

            self.SetDisplaySize(root[0], select_bone[0])
            
        name_select_bone = self.GetNameToBones(select_bone)
        name_root = self.GetNameToBones(root)
        self.SetMode("POSE")
        pose_select_bone = self.GetBones(name_select_bone, mode="POSE")
        pose_root = self.GetBones(name_root, mode="POSE")
        if pose_select_bone :
            pose_root[0].custom_shape = pose_select_bone[0].custom_shape
            pose_root[0].custom_shape_scale_xyz = pose_select_bone[0].custom_shape_scale_xyz
            pose_root[0].custom_shape_translation = pose_select_bone[0].custom_shape_translation
            pose_root[0].custom_shape_rotation_euler = pose_select_bone[0].custom_shape_rotation_euler

    def GN_UnionActiveBone(self):
        
        select_bone = self.GetNameToBones(self.GetSelectBones(mode="POSE"))
        active_bone = self.GetNameToBones([self.GetActiveBone()])
        
        self.SetMode(mode="EDIT") 
        select_bone = self.GetBones(select_bone, mode="EDIT")
        active_bone = self.GetBone(active_bone[0], mode="EDIT")
        if select_bone and active_bone:
            for bone in select_bone :
                bone.parent = active_bone
        self.SetMode("POSE")
    
    
    def AddCollection(self):
        return super().AddCollection()

    def GN_Fisicas(self) : 

        props = self.Props()
 
        if self.GetObjMode() == {"OBJECT", "EDIT"} : return
        
        selects = self.SplitBonesForParent(self.GetSelectBones(mode=self.GetObjMode())).copy()
        
        
        for PB in selects:
            
            
            PBN = self.GetNameToBones(PB)
            
            self.SetMode(mode="EDIT")
            self.UseMirror(use=False)

            select_edit_bones = self.GetBones(PBN, self.GetObjMode()) 
            if not select_edit_bones : return
            
            Names_Bones = [f"FS_{bone.name}" for bone in select_edit_bones]
            Names_Bones.append(f"FS_{select_edit_bones[-1].name}")

            FBones = self.CreateBones(Names_Bones)
            
            if FBones :
                for i in range(len(select_edit_bones)) : 
                    self.SetTransform(FBones[i], select_edit_bones[i])
                
                self.SetTransform(FBones[-1], select_edit_bones[-1], only_tail=True)
                
                for bone in FBones:
                    bone.use_deform = False
                
                FBones[0].parent = select_edit_bones[0].parent
                
                for i in range(len(FBones)-1):
                    FBones[i+1].parent = FBones[i]
                    FBones[i+1].use_connect = True
            
            FBones_Name = self.GetNameToBones(FBones)
            select_edit_bones_Name = self.GetNameToBones(select_edit_bones)
            self.SetMode(mode="POSE")
            FBones_Pose = self.GetBones(FBones_Name, self.GetObjMode())
            Selecte_Bones_Pose = self.GetBones(select_edit_bones_Name, self.GetObjMode())
            obj = self.GetActiveObject()
            
            if FBones_Pose:
                
                save_frame = bpy.context.scene.frame_current
                bpy.context.scene.frame_set(1)
                
                for i, bone in enumerate(FBones_Pose) : 
                    if i < len(FBones_Pose)-1:
                        constraint = bone.constraints.new(type='COPY_TRANSFORMS')
                        constraint.name = "RIG_CREATOR_FISICAS"
                        constraint.target = self.GetActiveObject()
                        constraint.subtarget = Selecte_Bones_Pose[i].name
                        bone.bone.select = True

                bpy.ops.nla.bake(
                    frame_start=props.frame_start, 
                    frame_end=props.frame_end,
                    step=props.frame_step, 
                    only_selected=True, 
                    visual_keying=True, 
                    clear_constraints=False, 
                    clear_parents=False, 
                    use_current_action=True, 
                    clean_curves=False, 
                    bake_types={'POSE'},
                    channel_types={'LOCATION', 'ROTATION', 'SCALE'}
                )
                
                for bone in FBones_Pose:
                    bone.bone.select = True
                    for constraint in bone.constraints:
                        if constraint.type == 'COPY_TRANSFORMS':
                            if constraint.name == "RIG_CREATOR_FISICAS":
                                bone.constraints.remove(constraint)
                                
                
                for i in range(len(Selecte_Bones_Pose)):
                    
                    if not props.use_stretch_to :
                        constraint = FBones_Pose[i].constraints.new(type='DAMPED_TRACK')
                        constraint.target = self.GetActiveObject()
                        constraint.subtarget = FBones_Pose[i+1].name
                        constraint.influence = props.power_overlapping
                    else:
                        constraint = FBones_Pose[i].constraints.new(type='STRETCH_TO')
                        constraint.target = self.GetActiveObject()
                        constraint.subtarget = FBones_Pose[i+1].name
                        constraint.bulge = props.power_stretch
                        constraint.influence = props.power_overlapping
                        
                for i in range(len(Selecte_Bones_Pose)):
                    constraint = Selecte_Bones_Pose[i].constraints.new(type='COPY_TRANSFORMS')
                    constraint.name = "RIG_CREATOR_FISICAS"
                    constraint.target = self.GetActiveObject()
                    constraint.subtarget = FBones_Pose[i].name
                    Selecte_Bones_Pose[i].bone.select = True
                    
                bpy.ops.nla.bake(
                    frame_start=props.frame_start, 
                    frame_end=props.frame_end,
                    step=props.frame_step, 
                    only_selected=True, 
                    visual_keying=True, 
                    clear_constraints=False, 
                    clear_parents=False, 
                    use_current_action=True, 
                    clean_curves=False, 
                    bake_types={'POSE'},
                    channel_types={'LOCATION', 'ROTATION', 'SCALE'}
                )
                
                for bone in Selecte_Bones_Pose:
                    bone.bone.select = True
                    for constraint in bone.constraints:
                        if constraint.type == 'COPY_TRANSFORMS':
                            if constraint.name == "RIG_CREATOR_FISICAS":
                                bone.constraints.remove(constraint)
                    
                for bone in FBones_Pose:
                    for i in range(props.frame_start, props.frame_end+1, props.frame_step):
                        bone.keyframe_delete(data_path="location", frame=i)
                        if bone.rotation_mode != 'QUATERNION' :
                            bone.keyframe_delete(data_path="rotation_euler", frame=i)
                        else:
                            bone.keyframe_delete(data_path="rotation_quaternion", frame=i)
                            
                        bone.keyframe_delete(data_path="scale", frame=i)
                    
                    self.UpdateViewLayer()
                    
                FBones_Pose_Name = self.GetNameToBones(FBones_Pose)
                self.SetMode("EDIT")
                self.RemoveBones(FBones_Pose_Name)
                self.SetMode("POSE")
                bpy.context.scene.frame_set(save_frame)

    def GN_Fingers(self) : 
        
        self.AddCollection()
        
        props = self.Props()
        
        use_fk = props.use_fk
        use_def = props.use_def
        use_dedos = props.use_fingers
        use_Segments = props.use_segments
        use_Parent = props.use_parent

        if use_fk == False:
            use_dedos = False

        Armature = self.GetActiveObject()
        self.SetMode(mode="EDIT")
        self.UseMirror(use=False)
        selected_bones = self.GetSelectBones(mode="EDIT")

        to_select_bone_parent = selected_bones[0].parent

        if use_def == True:
            CONTROL = self.GN_Name(props.name_def, selected_bones[0].name)
        if use_fk == True: 
            FK = self.GN_Name(props.name_fk, selected_bones[0].name)
        if use_dedos == True:
            DEDOS = self.GN_Name(props.name_fingers, selected_bones[0].name)

        if not Armature and not Armature.type == 'ARMATURE' and not selected_bones : return

        NEWBONECANTIDA : int = len(selected_bones)
        DEDOSBONES = []
        FKBONE = []
        DEFBONE = []
        
        if use_Segments :
            for bone in selected_bones:
                bone.bbone_segments = props.int_segments
        
        
        # Set Dedos
        if use_dedos :
            DEDOSBONES = self.CreateBonesRange(DEDOS, 2)
            if DEDOSBONES :
                for bone in DEDOSBONES:
                    self.SetTransform(bone, selected_bones[0], length_value=0.5)
                    self.SetDisplaySize(bone, selected_bones[0], Display_size_x=1.2, Display_size_y=1.2)

                L : float = 0
                for bone in selected_bones: L += bone.length
                DEDOSBONES[-1].length = L
                DEDOSBONES[-1].parent = DEDOSBONES[0]
                if use_Parent : 
                    DEDOSBONES[0].parent = to_select_bone_parent
                    selected_bones[0].parent = DEDOSBONES[0]
                
                DEDOSBONES[0].color.palette = 'THEME01'
                DEDOSBONES[1].color.palette = 'THEME04'
            self.SetDeform(DEDOSBONES, False)
                
        # Set Fk
        if use_fk :
            FKBONE = self.CreateBonesRange(FK,NEWBONECANTIDA)
            if FKBONE :
                for i in range(NEWBONECANTIDA):
                    self.SetTransform(FKBONE[i], selected_bones[i])
                    self.SetDisplaySize(FKBONE[i], selected_bones[i])

                self.SetRelationsOnlyOneList(FKBONE, Use_connect=True)    
          
                for bone in FKBONE : 
                    bone.use_deform = False
                    bone.color.palette = 'THEME03'
                    if use_Segments : bone= 32
                    
                if use_Parent and not use_dedos :
                    FKBONE[0].parent = to_select_bone_parent
                else:
                    FKBONE[0].use_connect = False
                    FKBONE[0].parent = DEDOSBONES[-1]
        # Set Def
        if use_def :
            DEFBONE = self.CreateBonesRange(CONTROL, NEWBONECANTIDA+1)
            if DEFBONE :
                for i in range(NEWBONECANTIDA):
                    self.SetTransform(
                        DEFBONE[i], selected_bones[i], 
                        length_value=0.2
                    )
                    self.SetDisplaySize(DEFBONE[i], selected_bones[i], Display_size_x=0.8, Display_size_y=0.8)
                
                self.SetTransform(
                    DEFBONE[-1], selected_bones[-1], 
                    only_tail=True, length_value=0.2
                )
                self.SetDisplaySize(DEFBONE[-1], selected_bones[-1], Display_size_x=0.8, Display_size_y=0.8)
                
                for bone in DEFBONE:
                    bone.use_deform = False
                    self.SetColorBone(bone, 'THEME09')
                    
                if use_Parent and use_fk == False:
                    DEFBONE[0].parent = to_select_bone_parent
                    selected_bones[0].parent = DEFBONE[0]
                else:
                    for i, bone in enumerate(DEFBONE):
                        bone.parent = FKBONE[self.NIndexList(i, FKBONE)]
                    selected_bones[0].parent = DEFBONE[0]
                    DEFBONE[-1].parent = FKBONE[-1]
        
        SELECTBONES_NAME = self.GetNameToBones(selected_bones)
        DEDOSBONES_NAME = self.GetNameToBones(DEDOSBONES)  
        FKBONE_NAME = self.GetNameToBones(FKBONE)
        DEFBONE_NAME = self.GetNameToBones(DEFBONE)
        self.SetMode("POSE")
        DEDOSBONES_POSE = self.GetBones(DEDOSBONES_NAME, "POSE")
        FKBONE_POSE = self.GetBones(FKBONE_NAME, "POSE")
        DEFBONE_POSE = self.GetBones(DEFBONE_NAME, "POSE")
        SELECTBONES_POSE = self.GetBones(SELECTBONES_NAME, "POSE")
        
        if DEDOSBONES_POSE :
            for i in range(3):
                if i in {0, 2}:
                    DEDOSBONES_POSE[-1].lock_scale[i] = True
            DEDOSBONES_POSE[0].custom_shape = self.EMPTY_Cube
            DEDOSBONES_POSE[-1].custom_shape = self.EMPTY_Arrow
            DEDOSBONES_POSE[-1].custom_shape_rotation_euler[0] = -1.5708
            DEDOSBONES_POSE[-1].custom_shape_scale_xyz[1] = 0
            DEDOSBONES_POSE[-1].custom_shape_scale_xyz[0] = 4

        if FKBONE_POSE :
            
            def set_transforms_bone(bone, target_bone):
                const = bone.constraints.new(type='TRANSFORM')
                const.target = Armature
                const.subtarget = target_bone.name
                const.target_space = 'LOCAL'
                const.owner_space = 'LOCAL'
                const.map_from = 'SCALE'
                const.from_min_y_scale = 0.2
                const.from_max_y_scale = 1.8
                const.map_to = 'ROTATION'
                const.map_to_x_from = 'Y'
                const.to_min_x_rot = 3.141592653589793
                const.to_max_x_rot = -3.141592653589793
            
                 
            for bone in FKBONE_POSE:
                
                bone.custom_shape = self.EMPTY_Circle
                bone.custom_shape_translation[1] = bone.length/2
                    
                if use_dedos :

                    if props.use_limit_rot_fingers == False: 
                        set_transforms_bone(bone, DEDOSBONES_POSE[-1])
            
            if props.use_limit_rot_fingers : 
                value = props.limit_rot_fingers
                value = value if value <= len(FKBONE_POSE) else len(FKBONE_POSE)
                list_bones = FKBONE_POSE
                if props.limit_rot_fingers_invert : list_bones.reverse()
                for i in range(value) : 
                    set_transforms_bone(list_bones[i], DEDOSBONES_POSE[-1])
            
            if use_dedos :
                for bone in FKBONE_POSE:       
                    const = bone.constraints.new(type='COPY_SCALE')
                    const.target = Armature
                    const.subtarget = DEDOSBONES_POSE[0].name

        if DEFBONE_POSE :
            for bone in DEFBONE_POSE:
                bone.custom_shape = self.EMPTY_Sphere

        if SELECTBONES_POSE :
            for i, bone in enumerate(SELECTBONES_POSE):

                const = bone.constraints.new(type='COPY_TRANSFORMS')
                const.target = Armature
                const.subtarget = DEFBONE_POSE[i].name
                
                const = bone.constraints.new(type='STRETCH_TO')
                const.target = Armature
                const.subtarget = DEFBONE_POSE[i+1].name
                
    def GN_Ik(self) : 
        
        self.AddCollection()
        if not self.GetActiveObject() : return
        props = self.Props()
        
        self.SetMode("EDIT")
        self.UseMirror(use=False)
        Select_Bone = self.GetSelectBones("EDIT")
        if not Select_Bone : return
        
        NSB =  len(Select_Bone)
        
        if NSB == 1 : return
        
        IK_NAME = self.GN_Name(props.name_ik, Select_Bone[0].name)
        IK = self.CreateBonesRange(IK_NAME, NSB if NSB > 2 else 3)
        if NSB == 2 : 
            for i in range(NSB):
                self.SetTransform(IK[i], Select_Bone[i])
            self.SetTransform(IK[-1], Select_Bone[-1], only_tail=True)
        else:
            self.SetTransformToBones(IK, Select_Bone)
        self.SetRelationsOnlyOneList(IK, Use_connect=True)
        self.SetDeform(IK, False)
        self.SetColorBone(IK[0], "THEME04")
        
        CONTROL_IK = self.CreateBonesRange(f"cont_{IK_NAME}", 4)
        self.SetDeform(CONTROL_IK, False)
        
        self.SetTransform(CONTROL_IK[0], Select_Bone[0], length_value=0.8)
        self.SetTransform(CONTROL_IK[1], Select_Bone[0], length_value=0.4)
        DSB = [Select_Bone[-1].head, Select_Bone[-1].roll, Select_Bone[0].length * 0.4]
        [CONTROL_IK[0].tail, CONTROL_IK[0].roll, CONTROL_IK[0].length] = DSB
        [CONTROL_IK[1].tail, CONTROL_IK[1].roll, CONTROL_IK[1].length] = DSB
        
        self.SetTransform(CONTROL_IK[2], IK[-1], length_value=0.5)
        Save_List = Select_Bone[:]
        Save_List.pop()
        self.SetPoleTransform(CONTROL_IK[3], Save_List if NSB > 2 else Select_Bone , props.distance_pole_target)
        CONTROL_IK[3].length /= 2
        
        self.SetColorBone(CONTROL_IK[0])
        self.SetColorBone(CONTROL_IK[2])
        self.SetColorBone(CONTROL_IK[3], 'THEME04')
        
        self.SetRelations(CONTROL_IK[-1], CONTROL_IK[1])
        self.SetRelations(IK[0], CONTROL_IK[0])
        

        SELECT_BONE_NAME = self.GetNameToBones(Select_Bone)  
        IK_NAME = self.GetNameToBones(IK)
        CONTROL_IK_NAME = self.GetNameToBones(CONTROL_IK)
        self.SetMode("POSE")
        SELECT_BONE_POSE = self.GetBones(SELECT_BONE_NAME, "POSE")
        IK_POSE = self.GetBones(IK_NAME, "POSE")
        CONTROL_IK_POSE= self.GetBones(CONTROL_IK_NAME, "POSE")
                
        if IK_POSE and CONTROL_IK_POSE :

            IK_POSE[0].custom_shape = self.EMPTY_Cube
            IK_POSE[0].rotation_mode = 'XYZ'
            IK_POSE[0].lock_rotation[2] = True
            IK_POSE[0].lock_rotation[0] = True
            IK_POSE[0].custom_shape_scale_xyz[0] = 0.5
            IK_POSE[0].custom_shape_scale_xyz[1] = 0
            IK_POSE[0].custom_shape_scale_xyz[2] = 0.5
            IK_POSE[0].custom_shape_translation[1] = IK_POSE[0].length
            
            for bone in IK_POSE : 
                bone.ik_stretch = 0.1
            
            CONTROL_IK_POSE[0].custom_shape = self.EMPTY_Cube
            CONTROL_IK_POSE[2].custom_shape = self.EMPTY_Cube
            CONTROL_IK_POSE[2].custom_shape_translation[1] = CONTROL_IK_POSE[2].length
            
            CONTROL_IK_POSE[3].custom_shape = self.EMPTY_Sphere
            for i in range(3) :
                CONTROL_IK_POSE[3].custom_shape_scale_xyz[i] /= 2
            
            const = IK_POSE[-1].constraints.new(type='COPY_TRANSFORMS')
            const.target = self.GetActiveObject()
            const.subtarget = CONTROL_IK_POSE[2].name

            const = IK_POSE[-2].constraints.new(type='IK')
            const.target = self.GetActiveObject()
            const.subtarget = CONTROL_IK_POSE[2].name
            const.chain_count = len(SELECT_BONE_POSE)-1 if NSB > 2 else len(SELECT_BONE_POSE)
            
            if props.use_ik_as == "POLE" : 
                const.pole_target = self.GetActiveObject()
                const.pole_subtarget = CONTROL_IK_POSE[-1].name
                const.pole_angle = props.pole_angle
            
            #elif props.use_ik_as == "AllROT" : 
            #    const.use_rotation = True

            const.use_stretch = props.use_stretch_to_ik
            
            if props.use_copy_transforms_ik : 
                for i in range(len(SELECT_BONE_POSE)):
                    const = SELECT_BONE_POSE[i].constraints.new(type='COPY_TRANSFORMS')
                    const.target = self.GetActiveObject()
                    const.subtarget = IK_POSE[i].name
                            

        ...
        
    def GN_Fk(self) : 
        
        self.AddCollection()
        
        if not self.GetActiveObject() : return
        props = self.Props()
        
        self.SetMode("EDIT")
        self.UseMirror(use=False)
        Select_Bone = self.GetSelectBones("EDIT")
        if not Select_Bone : return
        
        props = self.Props()
        
        FK = self.CreateBonesRange(self.GN_Name(props.name_fk1, Select_Bone[0].name), len(Select_Bone))
        if FK : 
            self.SetTransformToBones(FK, Select_Bone)
            self.SetRelationsOnlyOneList(FK, Use_connect=True)
            self.SetDeform(FK, False)
            for fk in FK : 
                self.SetColorBone(fk, "THEME03")
            
            for i, fk in enumerate(FK) : 
                self.SetDisplaySize(fk, Select_Bone[i])
            
        
        SELECT_BONE_NAME = self.GetNameToBones(Select_Bone)
        FK_NAME = self.GetNameToBones(FK)
        self.SetMode("POSE")
        SELECT_BONE_POSE = self.GetBones(SELECT_BONE_NAME, "POSE")
        FK_POSE = self.GetBones(FK_NAME, "POSE")
        
        if FK_POSE :
            for i, fk in enumerate(FK_POSE) :
                if props.use_copy_transforms_fk :
                    const = SELECT_BONE_POSE[i].constraints.new(type='COPY_TRANSFORMS')
                    const.target = self.GetActiveObject()
                    const.subtarget = fk.name
                
                if props.use_view_object : 
                    fk.custom_shape = self.EMPTY_Circle
                    fk.custom_shape_translation[1] = fk.length/2
                        
    def GN_Bones(self) : 
        self.AddCollection()
        if not self.GetActiveObject() : return
        props = self.Props()
        
        self.SetMode("EDIT")
        self.UseMirror(use=False)
        Select_Bone = self.GetSelectBones("EDIT")
        if not Select_Bone : return
        
        props = self.Props()
        
        BONE = self.CreateBonesRange(
            self.GN_Name(props.name_bone, Select_Bone[0].name), 
            len(Select_Bone)+1 if props.use_bone_in_tail else len(Select_Bone)
        )
        self.SetDeform(BONE, False)
        for bone in BONE :
            self.SetColorBone(bone, "THEME09")
            self.SetDisplaySize(bone, Select_Bone[0])
        
        
        look_bone = str(props.look_bone).lower().replace("{", "").replace("}", "").replace("'", "")
        
        if props.add_orientation == "GLOBAL" : 
            for i in range(len(Select_Bone)) : 
                bone = BONE[i]
                bone.head = Select_Bone[i].head
                bone.tail = Select_Bone[i].head + self.GetWorldNormal(Eje=look_bone)
                world_normal = self.GetWorldNormal(Eje=look_bone)
                print(f"GetWorldNormal result for {look_bone}: {world_normal}")
                bone.roll = 0 
                bone.length = Select_Bone[i].length
                
            if props.use_bone_in_tail :
                bone = BONE[-1]
                bone.head = Select_Bone[-1].tail
                bone.tail = Select_Bone[-1].tail + self.GetWorldNormal(Eje=look_bone)
                bone.roll = 0
                bone.length = Select_Bone[-1].length
        
        elif props.add_orientation == "NORMAL" :
            
            def get_axis(bone, look_bone) :
                axis = None
                if look_bone in {"x", "y", "z"} :
                   axis = getattr(bone, f"{look_bone}_axis") 
                else :
                    name = f"{look_bone}_axis".replace("-", "")
                    axis = getattr(bone, f"{name}")*-1
                    print(axis)
                return axis
            
            for i in range(len(Select_Bone)) : 
                bone = BONE[i]
                bone.head = Select_Bone[i].head
                
                bone.tail = Select_Bone[i].head + get_axis(Select_Bone[i], look_bone)
                bone.roll = 0
                bone.length = Select_Bone[i].length
                
            if i == len(Select_Bone)-1 and props.use_bone_in_tail :
                bone = BONE[-1]
                bone.head = Select_Bone[-1].tail
                bone.tail = Select_Bone[-1].tail + get_axis(Select_Bone[-1], look_bone)
                bone.roll = 0
                bone.length = Select_Bone[-1].length
        
        if props.use_parent_bone :
            for i in range(len(Select_Bone)) : 
                Select_Bone[i].parent = BONE[i]
        
        NAME_SELECT = self.GetNameToBones(Select_Bone)
        NAME_BONE = self.GetNameToBones(BONE)
        self.SetMode("POSE")
        SELECT_BONE_POSE = self.GetBones(NAME_SELECT, "POSE")
        BONE_POSE = self.GetBones(NAME_BONE, "POSE")
        
        if BONE_POSE :
            
            list_empty = {
                "SINGLE_ARROW": self.EMPTY_Arrow,
                "CIRCLE": self.EMPTY_Circle,
                "CUBE": self.EMPTY_Cube,
                "SPHERE": self.EMPTY_Sphere,
            }
            if props.use_viewport_display :
                for bone in BONE_POSE : 
                    bone.custom_shape = list_empty[props.viewport_display_type]
                    if props.viewport_display_type == "SINGLE_ARROW" :
                        bone.custom_shape_rotation_euler[0] = -1.5708
            
            if props.use_stretch_to_bone :
                for i in range(len(SELECT_BONE_POSE)) :
                    const = SELECT_BONE_POSE[i].constraints.new(type='STRETCH_TO')
                    const.target = self.GetActiveObject()
                    const.subtarget = BONE_POSE[i+1].name
               
        ...
    
    def GN_Curve(self) : 
    
        self.AddCollection()
        if not self.GetActiveObject() : return
        props = self.Props()
        
        self.SetMode("EDIT")
        self.UseMirror(use=False)
        Select_Bone = self.GetSelectBones("EDIT")
        if not Select_Bone : return

        if props.use_curve_root :
            ROOT_BONE_CURVE = self.CreateBonesRange(self.GN_Name(props.name_curve_root, Select_Bone[0].name), 1)
            self.SetDeform(ROOT_BONE_CURVE, False)
            self.SetColorBone(ROOT_BONE_CURVE[0], "THEME01")
            self.SetTransform(ROOT_BONE_CURVE[0], Select_Bone[0])
            self.SetDisplaySize(ROOT_BONE_CURVE[0], Select_Bone[0])
            
        CURVE_CONT = self.CreateBonesRange(self.GN_Name(props.name_curve_cont, Select_Bone[0].name), len(Select_Bone)+1)
        self.SetDeform(CURVE_CONT, False)
        for i, bone in enumerate(CURVE_CONT) :
            self.SetColorBone(bone, "THEME04")
            self.SetDisplaySize(bone, Select_Bone[0])
            if i < len(Select_Bone) :
                self.SetTransform(bone, Select_Bone[i], length_value=0.5)
            else:
                self.SetTransform(bone, Select_Bone[-1], length_value=0.5, only_tail=True)

            if props.use_curve_root :
                bone.parent = ROOT_BONE_CURVE[0]
                
        CURVE_FREE = self.CreateBonesRange(self.GN_Name(props.name_curve_free, Select_Bone[0].name), len(Select_Bone)*2)
        self.SetDeform(CURVE_FREE, False)
        for i, bone in enumerate(CURVE_FREE) :
            self.SetColorBone(bone, "THEME03")
            self.SetDisplaySize(bone, Select_Bone[0])
            if i < len(Select_Bone) :
                self.SetTransform(bone, Select_Bone[i], length_value=0.5)
                bone.parent = CURVE_CONT[i]
            else:
                self.SetTransform(bone, Select_Bone[i-len(Select_Bone)], length_value=0.5, only_tail=True)
                bone.parent = CURVE_CONT[i-len(Select_Bone)+1]
            
        for i, bone in enumerate(Select_Bone) :
            bone.use_connect = False
            bone.parent = CURVE_CONT[i]
        
        LIST_DEF_BONE = [] 
        if props.use_curve_subbone : 
            for s in range(len(Select_Bone)) : 
                LIST_DEF_BONE.append(
                    self.CreateBonesRange(
                    self.GN_Name(props.name_curve_def, Select_Bone[s].name), 
                    props.curve_subbone_howmuch)
                )

            save_head = None
            for i, list_bone in enumerate(LIST_DEF_BONE) :
                for x, bone in enumerate(list_bone) :
                    self.SetColorBone(bone, "THEME09")
                    if save_head == None: 
                        bone.head = Select_Bone[i].head
                    else : 
                        bone.head = save_head
                    bone.tail = Select_Bone[i].tail
                    bone.roll = Select_Bone[i].roll
                    bone.length /= len(list_bone)-x
                    save_head = bone.tail.copy()

        SELECT_BONE_NAME = self.GetNameToBones(Select_Bone)
        CURVE_FREE_NAME = self.GetNameToBones(CURVE_FREE)
        CURVE_CONT_NAME = self.GetNameToBones(CURVE_CONT)
        SUB_LIST_DEF_BONE = []
        for list_bone in LIST_DEF_BONE : 
            SUB_LIST_DEF_BONE.append(self.GetNameToBones(list_bone))
            
        if props.use_curve_root :
            ROOT_BONE_CURVE_NAME = self.GetNameToBones(ROOT_BONE_CURVE)
        self.SetMode("POSE")
        SELECT_BONE_POSE = self.GetBones(SELECT_BONE_NAME, "POSE")
        CURVE_FREE_POSE = self.GetBones(CURVE_FREE_NAME, "POSE")
        CURVE_CONT_POSE = self.GetBones(CURVE_CONT_NAME, "POSE")
        LIST_DEF_BONE_POSE = []
        for list_bone in SUB_LIST_DEF_BONE : 
            LIST_DEF_BONE_POSE.append(self.GetBones(list_bone, "POSE"))
        
        if props.use_curve_root :
            ROOT_BONE_CURVE_POSE = self.GetBones(ROOT_BONE_CURVE_NAME, "POSE")
        
        if CURVE_FREE_POSE and SELECT_BONE_POSE and CURVE_CONT_POSE :
            for i, bone in enumerate(self.GetBones(SELECT_BONE_NAME, "OBJECT")) :
                bone.bbone_handle_type_start = 'TANGENT'
                bone.bbone_handle_type_end = 'TANGENT'
                bone.bbone_segments = props.curve_int_segments
                bone.bbone_custom_handle_start = self.GetBone(CURVE_FREE_POSE[i].name)
                bone.bbone_custom_handle_end = self.GetBone(CURVE_FREE_POSE[i+len(SELECT_BONE_POSE)].name)
                bone.bbone_handle_use_ease_start = True
                bone.bbone_handle_use_ease_end = True

            
            for i, bone in enumerate(SELECT_BONE_POSE) :
                conts = bone.constraints.new(type='STRETCH_TO')
                conts.target = self.GetActiveObject()
                conts.subtarget = CURVE_FREE_POSE[i+len(SELECT_BONE_POSE)].name

            for i, f in enumerate(CURVE_FREE_POSE) :
                f.custom_shape = self.EMPTY_Arrow
                if i < len(SELECT_BONE_POSE) :
                    f.custom_shape_rotation_euler[0] = -1.5708
                else :
                    f.custom_shape_rotation_euler[0] = 1.5708
                
                f.custom_shape_scale_xyz[0] = 10
                f.custom_shape_scale_xyz[1] = 0
                f.custom_shape_scale_xyz[2] = 1
                
                for i in range(3):
                    if i != 1 :
                        f.lock_scale[i] = True
                    f.lock_location[i] = True
            
            for c in CURVE_CONT_POSE :
                c.custom_shape = self.EMPTY_Sphere
                c.custom_shape_scale_xyz *= 0.5
                
            if props.use_curve_root :
                ROOT_BONE_CURVE_POSE[0].custom_shape = self.EMPTY_Cube
            
            def add_drive(bone, Donde, control_bone, cual, use_menos_1 = False):
                # Añadir un controlador a la propiedad de ubicación X del cubo
                
                driver = bone.driver_add(Donde).driver

                # Configurar el controlador
                driver.type = 'SCRIPTED'
                var = driver.variables.new()
                var.name = "var"
                var.targets[0].id_type = 'OBJECT'
                var.targets[0].id = self.GetActiveObject()
                #var.targets[0].bone_target = control_bone.name
                var.targets[0].data_path=f'pose.bones["{control_bone.name}"].{cual}'
                
                # Escribir la expresión del controlador
                if use_menos_1 == False:
                    driver.expression = "var-1"
                else:
                    driver.expression = "var"
                    
            if props.use_curve_drive:
                for i in range(len(CURVE_FREE_POSE)):
                    if i < len(SELECT_BONE_POSE):
                        add_drive(
                            SELECT_BONE_POSE[i],
                            "bbone_easein",
                            CURVE_FREE_POSE[i],
                            "scale[1]"
                            )
                    else : 
                        add_drive(
                            SELECT_BONE_POSE[i-len(SELECT_BONE_POSE)],
                            "bbone_easeout",
                            CURVE_FREE_POSE[i],
                            "scale[1]"
                        )
            
            if props.use_curve_subbone : 
                for i, list_bone in enumerate(LIST_DEF_BONE_POSE) :
                    for x, bone in enumerate(list_bone) :
                        
                        
                        conts = bone.constraints.new(type='ARMATURE')
                        conts.targets.new()
                        for h, tgt in enumerate(conts.targets):
                            conts.targets[h].target = self.GetActiveObject()
                            conts.targets[h].subtarget = SELECT_BONE_POSE[i].name

                        if x > 0 and x < len(list_bone)-1 : 
                            conts = bone.constraints.new(type='STRETCH_TO')
                            conts.target = self.GetActiveObject()
                            conts.subtarget = list_bone[x+1].name
    
    
    def GN_AnnotateBone(self):
        
        props = self.Props()
        
        obj = self.GetActiveObject()
        if not obj or obj.type != 'ARMATURE':
            return
        
        grease = bpy.data.grease_pencils
        if not grease:
            return

        gp = grease[0]  # Ajusta si es necesario
        if not gp : return 
        
        if not bpy.ops.gpencil.annotation_active_frame_delete.poll(): return
        self.SetMode(mode="EDIT")
        
        
        name_bone : str = props.annotate_name
        type_mode = props.annotate_type_mode
        align_bone = props.annotate_use_join_bones
        proximity_join = props.annotate_proximity_join
        aling_roll_normal = props.annotate_aling_roll_normal
        use_curve = props.annotate_use_curve 
        curve_power = props.annotate_curve_power
        target = props.annotate_target
        use_select_target = props.annotate_use_select_target
        size_bbone = props.annotate_size_bbone
        direction : str = props.annotate_direction
        use_align_mirror_x = props.annotate_use_align_mirror_x
        use_align_mirror_y = props.annotate_use_align_mirror_y
        use_align_mirror_z = props.annotate_use_align_mirror_z
        use_align_mirror_negative_x = props.annotate_use_align_mirror_negative_x
        use_align_mirror_negative_y = props.annotate_use_align_mirror_negative_y
        use_align_mirror_negative_z = props.annotate_use_align_mirror_negative_z
        global_normal = props.annotate_global_normal
        use_parent = props.annotate_use_parent
        use_connect = props.annotate_use_connect
        segments = props.annotate_segments
        use_deform = props.annotate_use_deform
        use_vertbone = props.annotate_use_vertbone
        name_vertbone = props.annotate_name_vertbone
        use_vertbone_deform = props.annotate_use_vertbone_deform
        join_same_name = props.annotate_join_same_name
        
        new_bone = self.CreateBonesRange(name_bone, 1)[0] if type_mode == "ADD" else self.GetActiveBone("EDIT") if type_mode == "MOVE" else None

        def get_normal_from_surface(obj, world_pos):
            depsgraph = bpy.context.evaluated_depsgraph_get()
            obj_eval = obj.evaluated_get(depsgraph)

            ray_origin = world_pos + mathutils.Vector((0, 0, 0.1))  # Ligeramente por encima
            ray_dir = -mathutils.Vector((0, 0, 1))  # Dirección hacia abajo

            # Transformar el rayo al espacio local del objeto evaluado
            ray_origin_local = obj_eval.matrix_world.inverted() @ ray_origin
            ray_dir_local = obj_eval.matrix_world.inverted().to_3x3() @ ray_dir

            # Usamos ray_cast directamente sobre el objeto evaluado
            result, location, normal, face_index = obj_eval.ray_cast(ray_origin_local, ray_dir_local)

            if result:
                # Devolvemos la normal en espacio mundial
                return obj_eval.matrix_world.to_3x3() @ normal
            return None
        
        vert_bone = []
        
        def get_create_bone_from_vert_object(obj, arm, points):
            
            for v in obj.data.vertices:
                for p in points:
                    vert = obj.matrix_world.inverted() @ v.co
                    point = arm.matrix_world.inverted() @ p.co
                    if self.GetDistancia3d(vert, point) < proximity_join:
                        new = self.CreateBonesRange(name_vertbone, 1)[0]
                        if use_vertbone_deform:
                            new.use_deform = True
                        new.head = vert
                        new.tail = vert + self.GetWorldNormal("z")
                        new.roll = 0
                        new.length = new_bone.length * 0.2
                        vert_bone.append(new)

        for layer in gp.layers:
            for frame in layer.frames:
                for stroke in frame.strokes:
                    points = stroke.points
                    if len(points) < 2:
                        if bpy.ops.gpencil.annotation_active_frame_delete.poll():    
                            bpy.ops.gpencil.annotation_active_frame_delete()    
                        self.SetMode(mode='POSE')
                        return # Necesitamos al menos 2 puntos para crear un hueso                    
                    # Un solo hueso por stroke
                    head = obj.matrix_world.inverted() @ points[0].co
                    tail = obj.matrix_world.inverted() @ points[-1].co
                      # usar punto inicial
                      
                    if type_mode == "REMOVE":
                        for p in points:
                            for bone in obj.data.edit_bones:
                                
                                if name_bone.lower() not in bone.name.lower():
                                    continue
                                point = obj.matrix_world.inverted() @ p.co
                                head_dis = self.GetDistancia3d(point, bone.head.copy())
                                tail_dis = self.GetDistancia3d(point, bone.tail.copy())
                                if head_dis < proximity_join or tail_dis < proximity_join :
                                    self.RemoveBones([bone.name])
                        if bpy.ops.gpencil.annotation_active_frame_delete.poll():    
                            bpy.ops.gpencil.annotation_active_frame_delete()
                        self.SetMode(mode='POSE')
                        return
                    
                    if not new_bone : 
                        if bpy.ops.gpencil.annotation_active_frame_delete.poll():    
                            bpy.ops.gpencil.annotation_active_frame_delete()
                        self.SetMode(mode='POSE')
                        return
                    
                    def use_align_mirror(value, type, is_negative = False):
                        if value :
                            if is_negative:
                                if getattr(head, type) > 0 :
                                    setattr(head, type, 0)
                                if getattr(tail, type) > 0:
                                    setattr(tail, type, 0)
                            else:
                                if getattr(head, type) < 0 :
                                    setattr(head, type, 0)
                                if getattr(tail, type) < 0:
                                    setattr(tail, type, 0)
                    
                    use_align_mirror(use_align_mirror_x, "x")
                    use_align_mirror(use_align_mirror_y, "y")
                    use_align_mirror(use_align_mirror_z, "z")
                    use_align_mirror(use_align_mirror_negative_x, "x", is_negative=True)
                    use_align_mirror(use_align_mirror_negative_y, "y", is_negative=True)
                    use_align_mirror(use_align_mirror_negative_z, "z", is_negative=True)
                    
                    new_bone.head = head
                    new_bone.tail = tail
                    if use_select_target :
                        objs = self.GetSelectableObjects()
                        for sobj in objs:
                            if sobj != obj:
                                subtarget = obj
                            else :
                                subtarget = target
                    else:
                        subtarget = target
            
                    if subtarget and not global_normal:
                        normal = self.CreateVector(0, 0, 0)
                        for p in points:
                            n = get_normal_from_surface(subtarget, p.co)
                            if not n : continue
                            normal += get_normal_from_surface(subtarget, p.co)
                        normal /= len(points)
                        
                        if use_vertbone:
                            get_create_bone_from_vert_object(subtarget, obj, points)
                        
                    else :
                        direction = str(direction).lower().replace("{'", "").replace("'}", "")
                        normal = self.GetWorldNormal(direction if direction != "" else "z")
                    
                    if normal :
                        
                        if aling_roll_normal : 
                            new_bone.align_roll(normal)
  
                        if use_curve : 
                            # Posición local del punto medio del trazo
                            Location = obj.matrix_world.inverted() @ points[int(len(points) / 2)].co
                            curve_position = Location - ((head + tail) / 2)

                            # Transformar la curva al espacio local del hueso
                            bone_matrix = new_bone.matrix.to_3x3().inverted()
                            local_curve = bone_matrix @ curve_position

                            # Aplicar curvatura en el espacio local del hueso
                            def use_align_mirror(bone, value, type, is_negative = False):
                                if value :
                                    if is_negative:
                                        if getattr(bone, type) > 0 :
                                            setattr(bone, type, 0)
                                    else:
                                        if getattr(bone, type) < 0 :
                                            setattr(bone, type, 0)
                                        
                            new_bone.bbone_curveinx = (local_curve.x / 2) * curve_power
                            new_bone.bbone_curveoutx = (local_curve.x / 2) * curve_power
                            use_align_mirror(new_bone, use_align_mirror_x, "bbone_curveinx")
                            use_align_mirror(new_bone, use_align_mirror_negative_x, "bbone_curveinx", is_negative=True)
                            use_align_mirror(new_bone, use_align_mirror_x, "bbone_curveoutx")
                            use_align_mirror(new_bone, use_align_mirror_negative_x, "bbone_curveoutx", is_negative=True)
                            
                            
                            new_bone.bbone_curveinz = (local_curve.z / 2) * curve_power
                            new_bone.bbone_curveoutz = (local_curve.z / 2) * curve_power

                            new_bone.bbone_segments = segments
                    
                    new_bone.bbone_x = size_bbone
                    new_bone.bbone_z = size_bbone
                    new_bone.use_deform = use_deform
                    
        if align_bone : 
            head_bones = []
            tail_bones = []
            head_accum = new_bone.head.copy()
            tail_accum = new_bone.tail.copy()
                        
            parent = None
            sont = None
            
            for bone in obj.data.edit_bones or join_same_name:
                name : str = bone.name.lower()
                new_name_bone : str = name_bone.lower()
                
                if new_name_bone in name or not join_same_name:
                    
                    if self.GetDistancia3d(new_bone.head, bone.head) < proximity_join:
                        head_bones.append(("head", bone))
                        head_accum += bone.head
                    if self.GetDistancia3d(new_bone.head, bone.tail) < proximity_join:
                        head_bones.append(("tail", bone))
                        parent = bone
                        head_accum += bone.tail
                    if self.GetDistancia3d(new_bone.tail, bone.tail) < proximity_join:
                        tail_bones.append(("tail", bone))
                        tail_accum += bone.tail
                    if self.GetDistancia3d(new_bone.tail, bone.head) < proximity_join:
                        tail_bones.append(("head", bone))
                        tail_accum += bone.head
                        sont = bone

            # Calcular promedios
            new_head = head_accum / (len(head_bones) + 1)
            new_tail = tail_accum / (len(tail_bones) + 1)

            # Aplicar a todos los huesos correspondientes
            for end, bone in head_bones:
                if end == "head":
                    bone.head = new_head
                else:
                    bone.tail = new_head

            for end, bone in tail_bones:
                if end == "tail":
                    bone.tail = new_tail
                else:
                    bone.head = new_tail

            new_bone.head = new_head
            new_bone.tail = new_tail
            
            if use_parent:
                if parent:
                    new_bone.parent = parent
                    new_bone.use_connect = use_connect and (new_bone.head - parent.tail).length < 1e-6

                if sont:
                    sont.parent = new_bone
                    sont.use_connect = use_connect and (sont.head - new_bone.tail).length < 1e-6

            if not new_bone.parent :
                new_bone.use_connect = False
            
        if bpy.ops.gpencil.annotation_active_frame_delete.poll():    
            bpy.ops.gpencil.annotation_active_frame_delete()
        self.SetMode(mode='POSE')

    def GN_CurveGrip(self):
        
        self.AddCollection()
        if not self.GetActiveObject() : return
        
        self.SetMode("EDIT")
        self.UseMirror(use=False)
        select_bone = self.GetSelectBones("EDIT")
        if not select_bone : return
        
        props = self.Props()
        
        use_target = props.grip_use_target
        use_target_scale = props.grip_use_target_scale
        align_to_normal = props.grip_align_to_normal
        align_target = props.grip_align_target
        root_name = props.name_grip_root
        target_name = props.name_grip_target
        target_scale_name = props.name_grip_target_scale
        proximity_join = props.grip_proximity_join
        
        
        root_bones = []
        target_bones = []
        curve_rot_target = []
        
        damped_track_bones = []
        
        points = []
        length = 0  
        for bone in select_bone : 
            length += bone.length
        length /= len(select_bone)
        
        
        collections_name = [
            "Curve", "Curve Root", "Curve Target", "Curve Controller"
        ]
        
        collections = self.GetActiveObject().data.collections
        for c in collections_name :
            if not collections.get(c):
                collections.new(c)
            
        for bone in select_bone : 
            
            points.append(bone.head)
            points.append(bone.tail)
            
            curve_rot_target.append(
                [[bone.bbone_curveinx, bone.bbone_curveinz],
                [bone.bbone_curveoutx, bone.bbone_curveoutz]]
            )
            
            tail_in = self.CreateVector(bone.bbone_curveinx, 0, bone.bbone_curveinz)
            tail_out = self.CreateVector(bone.bbone_curveoutx, 0, bone.bbone_curveoutz)
            
            bone.bbone_curveinx = 0 
            bone.bbone_curveoutx = 0 
            bone.bbone_curveinz = 0 
            bone.bbone_curveoutz = 0
            
            self.BoneCollectionAssing("Curve", bone)
            
            # Cont_
            root_bone = self.CreateBonesRange(self.GN_Name("cont_", bone.name), 2)
            root_bones.append([root_bone[0].name, root_bone[1].name])
            self.SetTransform(root_bone[0], bone, length_value=0.25)
            self.SetTransform(root_bone[1], bone, length_value=0.25, only_tail=True)
            self.SetDeform(root_bone, False)
            for i in range(2):
                self.SetDisplaySize(root_bone[i], bone)
                self.BoneCollectionAssing("Curve Controller", root_bone[i])
                self.SetColorBone(root_bone[i], type_palette="THEME04")
                root_bone[i].length = length * 0.05
            
            bone.use_connect = False
            bone.parent = root_bone[0]
            
            if use_target :
                target_bone = self.CreateBonesRange(self.GN_Name(target_name, bone.name), 2)
                target_bones.append([target_bone[0].name, target_bone[1].name])
                self.SetTransform(target_bone[0], bone, length_value=0.5)
                self.SetTransform(target_bone[1], bone, length_value=0.5, only_tail=True)
                self.SetDeform(target_bone, False)
                # Obtener matriz del hueso base para orientación
                mat = bone.matrix.to_3x3().normalized()  # Solo rotación

                # Convertir los vectores a coordenadas locales del hueso
                local_tail_in = mat @ (tail_in * 2)
                local_tail_out = mat @ (tail_out * 2)

                # Aplicarlos en el tail de los controladores
                target_bone[0].tail += local_tail_in 
                target_bone[1].tail += -local_tail_out   # igual que * -1 pero más claro

                for i in range(2):
                    self.SetDisplaySize(target_bone[i], bone)
                    self.BoneCollectionAssing("Curve Target", target_bone[i])
                    self.SetColorBone(target_bone[i], type_palette="THEME03")
                    target_bone[i].parent = root_bone[i]

                bone.bbone_custom_handle_start = target_bone[0]
                bone.bbone_custom_handle_end = target_bone[1]
            else:
                bone.bbone_custom_handle_start = root_bone[0]
                bone.bbone_custom_handle_end = root_bone[1]
                
            bone.bbone_handle_type_start = 'TANGENT'
            bone.bbone_handle_type_end = 'TANGENT'
            bone.bbone_handle_use_ease_start = True
            bone.bbone_handle_use_ease_end = True
            if bone == 1:
                bone.bbone_segments = 32
            
            if align_target and use_target: 
                damped_track_bone = self.CreateBonesRange(self.GN_Name("track_", bone.name), 2)
                damped_track_bones.append([damped_track_bone[0].name, damped_track_bone[1].name])
                self.SetTransform(damped_track_bone[0], bone, length_value=0.2)
                self.SetTransform(damped_track_bone[1], bone, length_value=0.2, only_tail=True)
                self.SetDeform(damped_track_bone, False)
                for i in range(2) : 
                    target_bone[i].parent = damped_track_bone[i]
                    damped_track_bone[i].parent = root_bone[i]
                    self.BoneCollectionAssing("Curve Controller", damped_track_bone[i])
                    self.SetDisplaySize(damped_track_bone[i], bone)
 
        new_points = []

        for a in points:
            too_close = False
            for b in new_points:
                if self.GetDistancia3d(a, b) < proximity_join:
                    too_close = True
                    break
            if not too_close:
                new_points.append(a)
        
        
        
        def CreateToPoints(name, color : str = "THEME02", value_length : float = 0.2, parents = [], get_bone_ht : bool = False):
            bones = []
            
                
            for i, head in enumerate(new_points) :
                
                bone = self.CreateBonesRange(self.GN_Name(name, select_bone[0].name), 1)
                self.BoneCollectionAssing("Curve Root", bone[0])
                bone[0].head = head 
                bone[0].tail = head + self.GetWorldNormal()
                if parents : 
                    bone[0].parent = self.GetBone(parents[i], mode="EDIT")
                self.SetDeform(bone, False)
                self.SetDisplaySize(bone[0], select_bone[0])
                self.SetColorBone(bone[0], color)

                value : int = 0
                normal = self.CreateVector(0, 0, 0)
                if get_bone_ht : 
                    head_bones = []
                    tail_bones = []
                    for sbone in select_bone:
                        
                        if self.GetDistancia3d(head, sbone.head) < proximity_join: 
                            head_bones.append(sbone.name)
                        if self.GetDistancia3d(head, sbone.tail) < proximity_join: 
                            tail_bones.append(sbone.name)
                    
                for names in root_bones : 
                    bone_a = self.GetBone(names[0], mode="EDIT")
                    bone_b = self.GetBone(names[1], mode="EDIT")
                    
                    for cbone in [bone_a, bone_b] :
                        if self.GetDistancia3d(head, cbone.head) < proximity_join: 
                            if not parents : 
                                cbone.parent = bone[0]

                            normal += cbone.z_axis
                            value += 1

                if align_to_normal :
                    normal = normal/value
                    bone[0].tail = head + normal

                bone[0].length = length * value_length
                if get_bone_ht :
                    bones.append([bone[0].name, head_bones, tail_bones])
                else:
                    bones.append(bone[0].name)
            return bones
        
        roots = CreateToPoints(root_name, value_length=0.1)
        if use_target_scale :
            target_scale_bones = CreateToPoints(target_scale_name, "THEME09", 0.12, roots, True)

        select_bone = self.GetNameToBones(select_bone)
        self.SetMode(mode="POSE")
        select_bone = self.GetBones(select_bone, mode="POSE")
        if not select_bone : return
    
        for name in roots : 
            bone = self.GetBone(name, mode="POSE")
            if bone : 
                bone.custom_shape = self.EMPTY_Sphere
                for i in range(3):
                    bone.lock_scale[i] = True
                bone.custom_shape_wire_width = 2
        
        for i, names in enumerate(root_bones) : 
            
            bone_a = self.GetBone(names[0], mode="POSE")
            bone_b = self.GetBone(names[1], mode="POSE")
            
            for bone in [bone_a, bone_b] : 
                bone.custom_shape = self.EMPTY_Sphere
                for e in range(3):
                    bone.lock_rotation[e] = True
                    bone.lock_scale[e] = True
                    bone.lock_location[e] = True
                
            conts = select_bone[i].constraints.new(type='STRETCH_TO')
            conts.target = self.GetActiveObject()
            conts.subtarget = names[1]
            conts.bulge = props.grip_bulge

        
        for i, names in enumerate(target_bones):
            
            bone_a = self.GetBone(names[0], mode="POSE")
            bone_b = self.GetBone(names[1], mode="POSE")
            
            
            cont_bone_a = root_bones[i][0]
            cont_bone_b = root_bones[i][1]
            self.CreatreDrive(
                    self.GetBone(names[0], mode="OBJECT"), "hide",
                    self.GetBone(root_bones[i][0], mode="POSE"), f"rgc_select",
                    Use_Bone=True,
                )
            if bone_a and bone_b :
                for bone in [bone_a, bone_b] :
                    bone.custom_shape = self.EMPTY_Arrow
                    if bone == bone_a :
                        bone.custom_shape_rotation_euler[0] = -1.5708
                    else :
                        bone.custom_shape_rotation_euler[0] = 1.5708
                    
                    bone.custom_shape_scale_xyz[0] = 1
                    bone.custom_shape_scale_xyz[1] = 0
                    bone.custom_shape_scale_xyz[2] = 1
                    bone.custom_shape_wire_width = 2
                    
                    
                    
                    for i in range(3):
                        if i != 1 :
                            bone.lock_scale[i] = True
                        bone.lock_location[i] = True
        
        if use_target_scale : 
            for i, list in enumerate(target_scale_bones):
                head_bones = list[1]
                tail_bones = list[2]
                
                target_bone = self.GetBone(list[0], mode="POSE")
                
                

                
                target_bone.custom_shape = self.EMPTY_Arrows
                target_bone.custom_shape_wire_width = 3
                
                target_bone.custom_shape_rotation_euler[0] = -0.459737
                target_bone.custom_shape_rotation_euler[1] = 0.417614
                target_bone.custom_shape_rotation_euler[2] = 0.685448
                

                for e in range(3):
                    target_bone.lock_rotation[e] = True
                    target_bone.lock_location[e] = True
                target_bone.lock_rotation_w = True

                for name in head_bones:
                    head_bone = self.GetBone(name, mode="POSE")
                    if head_bone:
                        for e in range(3):
                            self.CreatreDrive(
                                    head_bone, "bbone_scalein",
                                    target_bone, f"scale[{e}]",
                                    Use_Bone=True,
                                    index= e
                                )
                for name in tail_bones:
                    tail_bone = self.GetBone(name, mode="POSE")
                    if tail_bone:
                        for e in range(3):
                            self.CreatreDrive(
                                tail_bone, f"bbone_scaleout",
                                target_bone, f"scale[{e}]", 
                                Use_Bone=True, 
                                index= e
                            )
        
        if align_target and use_target : 
            
            for i, names in enumerate(damped_track_bones) :
                bone_a = self.GetBone(names[0], mode="POSE")    
                bone_b = self.GetBone(names[1], mode="POSE") 
                
                cont_bone_a = root_bones[i][0]
                cont_bone_b = root_bones[i][1]
                
                c = bone_a.constraints.new(type='DAMPED_TRACK')
                c.target = self.GetActiveObject()
                c.subtarget = cont_bone_b
                
                c = bone_b.constraints.new(type='DAMPED_TRACK')
                c.target = self.GetActiveObject()
                c.subtarget = cont_bone_a
                c.track_axis = 'TRACK_NEGATIVE_Y'

    def GN_Auto_Root(self) : 
        
        self.AddCollection()
        props = self.Props()
        
        self.SetMode("EDIT")
        self.UseMirror(use=False)
        Active_Bone = self.GetActiveBone(mode="EDIT")
        
        name = self.GN_Name(props.name_auto_root, Active_Bone.name) if props.use_active_bone else props.name_auto_root
        ROOT_BONE = self.CreateBonesRange(name, props.bones_parent)
        self.SetDeform(ROOT_BONE, False)
        if props.use_active_bone :
            for bone in ROOT_BONE :
                self.SetTransform(bone, Active_Bone)
                self.SetDisplaySize(bone, Active_Bone)
            Active_Bone.parent = ROOT_BONE[0]
        else:
            for bone in ROOT_BONE : 
                bone.head = (0, 0, 0)
                bone.tail = self.GetWorldNormal("y")
                bone.roll = 0
            
        for i, bone in enumerate(ROOT_BONE) :
            self.SetColorBone(bone, f"THEME0{i+1}")
        
        self.SetRelationsOnlyOneList(ROOT_BONE, Use_connect=False)
        
        ROOT_BONE_NAME = self.GetNameToBones(ROOT_BONE)
        ACTIVE_BONE_NAME = self.GetNameToBones([Active_Bone])
        self.SetMode("POSE")
        ROOT_BONE_POSE = self.GetBones(ROOT_BONE_NAME, "POSE")
        ACTIVE_BONE_POSE = self.GetBones(ACTIVE_BONE_NAME, "POSE")
        
        if ROOT_BONE_POSE :
            for i, bone in enumerate(ROOT_BONE_POSE) :
                if not props.use_active_bone :
                    bone.custom_shape = self.EMPTY_Cube
                    bone.custom_shape_scale_xyz *= props.bones_parent-((i+1)/2)
                    bone.custom_shape_scale_xyz[2] = 0
                else : 
                    bone.custom_shape = ACTIVE_BONE_POSE[0].custom_shape
                    bone.custom_shape_scale_xyz *= props.bones_parent-((i+1)/2)
                    bone.custom_shape_scale_xyz += ACTIVE_BONE_POSE[0].custom_shape_scale_xyz*0.5
        
        ...



                    



GN = GeneratorsBones()
import bpy
import mathutils

import bpy
import mathutils

def GN_AnnotatePoseBone():
    obj = bpy.context.active_object
    if not obj or obj.type != 'ARMATURE':
        return

    grease = bpy.data.grease_pencils
    if not grease:
        return

    gp = grease[0]  # Ajusta si tienes múltiples
    pose_bones = [b for b in obj.pose.bones if b.bone.select]

    for pbone in pose_bones:
        head_world = obj.matrix_world @ pbone.head
        tail_world = obj.matrix_world @ pbone.tail

        closest_head = None
        closest_tail = None
        min_head_dist = float("inf")
        min_tail_dist = float("inf")

        for layer in gp.layers:
            for frame in layer.frames:
                for stroke in frame.strokes:
                    for point in stroke.points:
                        pt = point.co
                        dist_head = (pt - head_world).length
                        dist_tail = (pt - tail_world).length

                        if dist_head < min_head_dist:
                            min_head_dist = dist_head
                            closest_head = pt
                        if dist_tail < min_tail_dist:
                            min_tail_dist = dist_tail
                            closest_tail = pt

        if closest_head and closest_tail:
            # Dirección del hueso
            direction = (closest_tail - closest_head).normalized()

            up = mathutils.Vector((0, 0, 1))
            if abs(direction.dot(up)) > 0.999:
                up = mathutils.Vector((0, 1, 0))  # Evitar degeneración

            right = direction.cross(up).normalized()
            up = right.cross(direction).normalized()

            rot_mat = mathutils.Matrix((
                right,
                direction,
                up
            )).transposed()

            new_matrix = rot_mat.to_4x4()
            new_matrix.translation = closest_head

            # Guardar la escala original
            original_scale = pbone.matrix.to_scale()

            
            # Asignar matriz sin escala
            pbone.matrix = obj.matrix_world.inverted() @ new_matrix

            # Restaurar la escala original
            pbone.scale = original_scale


    bpy.ops.gpencil.annotation_active_frame_delete()

@bpy.app.handlers.persistent
def GN_Update_AnnotateBone(dummy):
    props = GN.Props()
    obj = GN.GetActiveObject()
    if obj and obj.type == "ARMATURE" and GN.GetObjMode() == "POSE" :
        if props.annotate_auto_bone and GN.PanelType([{"RIG"}]):
            GN.GN_AnnotateBone()
        #else : 
        #    if props.annotate_posebone :
        #        GN_AnnotatePoseBone()