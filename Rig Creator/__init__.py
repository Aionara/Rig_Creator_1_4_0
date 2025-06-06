# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name": "Rig Creator",
    "author": "Edward Ureña",
    "description": "Herramienta de creación de rigs",
    "blender": (4, 0, 0),
    "version": (1, 4, 0),
    "location": "View3D > Tool Shelf > Rig Creator",
    "warning": "",
    "category": "Rigging",
    "id": "rigcreator",  # Sin guiones ni espacios
}


from .generaldata import *
from .operator import *
from .Panels import *
from .node_tree import *
from .picker import *


def register(): 
    GeneralRegister()
    OperetorRegisnter()
    PanelRegister()
    #PickerRegister()
    #NodeTreeRegister()
    ...

def unregister(): 
    GeneralUnregister()
    OperetorUnregisnter()
    PanelUnregister()
    #PickerUnregister()
    #NodeTreeUnregister()
    ...

if __name__ == "__main__":
    register()
    # Ejecuta el operador
    