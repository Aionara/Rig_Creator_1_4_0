import gpu
from gpu_extras.batch import batch_for_shader
from bpy_extras import view3d_utils  # Importamos view3d_utils para las conversiones de coordenadas





class Draw : 
    
    def __init__(self) -> None:
        pass
    
    def Box(self, vertices, color):
        """Dibuja un cuadro en el viewport 3D"""
        shader = gpu.shader.from_builtin('UNIFORM_COLOR')
        batch = batch_for_shader(shader, 'TRI_FAN', {"pos": vertices})
        
        shader.bind()
        shader.uniform_float("color", color)
        batch.draw(shader)

    def GetCameraOretation(context, box_size=0.2):
        """Obtiene los vértices de un cuadro centrado en la cámara en el espacio de la vista 3D"""
        region = context.region
        rv3d = context.space_data.region_3d
        mid_x = region.width / 2
        mid_y = region.height / 2

        # Coordenadas de 4 vértices en el centro del viewport en 2D
        vertices_2d = [
            (mid_x - box_size * region.width, mid_y - box_size * region.height),
            (mid_x + box_size * region.width, mid_y - box_size * region.height),
            (mid_x + box_size * region.width, mid_y + box_size * region.height),
            (mid_x - box_size * region.width, mid_y + box_size * region.height),
        ]

        # Convertir las coordenadas 2D a 3D
        vertices_3d = [view3d_utils.region_2d_to_location_3d(region, rv3d, coord, (0, 0, 0)) for coord in vertices_2d]
        
        return vertices_3d

class Window(Draw):
    
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.vertices = [(x, y), (x, y + height), (x + width, y + height), (x + width, y)]
    
    def DrawWindow(self):
        self.Box(self.vertices, self.color)
    
    def MoveWindow(self, x, y):
        self.x = x
        self.y = y
        self.vertices = [(x, y), (x, y + self.height), (x + self.width, y + self.height), (x + self.width, y)]
        self.DrawWindow()

class button(Draw):
    
    def __init__(self, parent : Window,  x, y, width, height, text, color, text_color):
        self.parent = parent
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.color = color
        self.text_color = text_color
        self.vertices = [(x * parent.x, y * parent.y), (x , y + height), (x + width, y + height), (x + width, y)]
    
    
    
    
    def DrawButton(self):
        self.Box(self.vertices, self.color)
    
