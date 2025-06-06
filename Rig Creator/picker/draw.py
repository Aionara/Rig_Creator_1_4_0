
import bpy
import gpu
from gpu_extras.batch import batch_for_shader
import blf




class Draw : 
    
    def DrawQuare(self, x=0, y=0, width=100, height=100, color=(1.0, 0.0, 0.0, 1.0)):

        # Asegurarse de que 'x' sea un número (float o int)
        if not isinstance(x, (int, float)):
            x = 0  # Establecer un valor predeterminado si 'x' no es válido

        # Ubicación y dimensiones del nodo
        vertices = [
            (x - (width / 2), y),
            (x + (width / 2), y),
            (x + (width / 2), y - height),
            (x - (width / 2), y - height),
        ]

        shader = gpu.shader.from_builtin('UNIFORM_COLOR')
        batch = batch_for_shader(
                shader, 'TRI_FAN',  # Usa TRI_FAN para dibujar un rectángulo lleno
                {"pos": vertices}
            )

        shader.bind()
        shader.uniform_float("color", color)  # Color del cuadro: Gris semitransparente
        batch.draw(shader)
    

    def DrawText(self, x=0, y=0, width=100, height=100, text="Texto", text_size = 1, color=(1.0, 0.0, 0.0, 1.0)):


        # Asegurarse de que 'x' y 'y' sean números (float o int)
        if not isinstance(x, (int, float)):
            x = 0  # Establecer un valor predeterminado si 'x' no es válido

        if not isinstance(y, (int, float)):
            y = 0  # Establecer un valor predeterminado si 'y' no es válido
        
        # Calcular el tamaño del texto para que se ajuste dentro del ancho y la altura proporcionados
        scale_factor = 0.5  # Este valor se puede ajustar para cambiar la escala del texto
        size = min(height*text_size, width) * scale_factor  # Ajustar el tamaño al área

        
        font_id = 0  # Fuente por defecto
        blf.size(font_id, int(size))

        # Medir dimensiones del texto
        text_width, text_height = blf.dimensions(font_id, text)
        # Calcular posición centrada
        pos_x = x - (text_width / 2)
        pos_y = y - (height/2+text_size/2+text_height/2)

        # Posicionar y dibujar
        blf.position(font_id, int(pos_x), int(pos_y), 0)
        
        blf.size(font_id, size)  # Tamaño del texto
        blf.color(font_id, color[0], color[1], color[2], color[3])  # Establecer el color del texto (RGBA)
        blf.draw(font_id, text)  # Dibujar el texto
    
    def DrawImage(self,image, x=0, y=0, width=100, height=100, color=(0.0, 0.0, 0.0, 1)):

        if not image : return
        
        # Verificar que la imagen tenga un buffer de píxeles cargado
        if not image.has_data:
            image.reload()


        shader = gpu.shader.from_builtin('IMAGE')
       
        vertices = [
            (x - (width / 2), y),
            (x + (width / 2), y),
            (x + (width / 2), y - height),
            (x - (width / 2), y - height),
        ]

        tex_coords = [
            (0.0, 1.0),
            (1.0, 1.0),
            (1.0, 0.0),
            (0.0, 0.0),
        ]

        batch = batch_for_shader(shader, 'TRI_FAN', {"pos": vertices, "texCoord": tex_coords})

        shader.bind()

        texture = gpu.texture.from_image(image)
        shader.uniform_sampler("image", texture) 
        batch.draw(shader)
    
    def DrawIcon(self, icon_name, x=0, y=0, width=50, height=50):
        # Obtener el ID del icono
        icon_id = bpy.types.UILayout.bl_rna.functions["prop"].parameters["icon"].enum_items[icon_name].value

        if icon_id == 0:
            return  # Icono no encontrado
        
        return
        icon_id = bpy.types.UILayout.icon(icon_id)

        if icon_id == 0:
            print("Icono no encontrado")
            return  # Icono no encontrado
        
        # Usamos el ID del icono para obtener la textura asociada al icono
        texture = gpu.texture.from_builtin(icon_id)

        if texture is None:
            print("No se pudo obtener la textura del icono")
            return

        # Crear un shader 2D para dibujar la imagen
        shader = gpu.shader.from_builtin('2D_IMAGE')
        shader.bind()
        shader.uniform_sampler("image", texture)

        # Coordenadas de los vértices del cuadro en pantalla
        vertices = [
            (x - (width / 2), y),
            (x + (width / 2), y),
            (x + (width / 2), y - height),
            (x - (width / 2), y - height),
        ]

        # Coordenadas de textura (la textura se mapea de 0 a 1)
        tex_coords = [
            (0.0, 1.0),
            (1.0, 1.0),
            (1.0, 0.0),
            (0.0, 0.0),
        ]

        # Crear el batch de dibujo
        batch = batch_for_shader(shader, 'TRI_FAN', {"pos": vertices, "texCoord": tex_coords})

        # Dibujar el icono
        batch.draw(shader)