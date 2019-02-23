# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####
# <pep8 compliant>

bl_info = {
    "name": "Batch import OBJ files",
    "author": "poor + entropy_phi",
    "version": (0, 2, 1),
    "blender": (2, 79, 0),
    "location": "File > Import-Export",
    "description": "Batch import multiple OBJ files with specified settings",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Import-Export"}

import bpy
import os

from bpy_extras.io_utils import ImportHelper
from bpy.props import (BoolProperty,
                       FloatProperty,
                       StringProperty,
                       EnumProperty,
                       CollectionProperty
                       )

class ImportMultipleObjs(bpy.types.Operator, ImportHelper):
    """Load multiple OBJ files at once"""
    bl_idname = "import_scene.multiple_objs"
    bl_label = "Import multiple OBJ's"
    bl_options = {'PRESET', 'UNDO'}
    filename_ext = ".obj"
    filter_glob = StringProperty(
            default="*.obj",
            options={'HIDDEN'},
            )
    files = CollectionProperty(type=bpy.types.PropertyGroup)

    # Properties shown in the editor
    ngons_setting = BoolProperty(
            name="NGons",
            description="Import faces with more than 4 verts as n-gons",
            default=True,
            )
			
    edges_setting = BoolProperty(
            name="Lines",
            description="Import lines and faces with 2 verts as edges",
            default=True,
            )
			
    smooth_groups_setting = BoolProperty(
            name="Smooth Groups",
            description="Surround smooth groups by sharp edges",
            default=True,
            )

    split_objects_setting = BoolProperty(
            name="Object",
            description="Import OBJ Objects into Blender Objects",
            default=True,
            )

    split_groups_setting = BoolProperty(
            name="Group",
            description="Import OBJ Groups into Blender Objects",
            default=True,
            )

    groups_as_vgroups_setting = BoolProperty(
            name="Poly Groups",
            description="Import OBJ groups as vertex groups",
            default=False,
            )

    image_search_setting = BoolProperty(
            name="Image Search",
            description="Search subdirs for any associated images "
                        "(Warning, may be slow)",
            default=True,
            )
			
    use_file_name_setting = BoolProperty(
            name="Use File Name",
            description="Use the file name as the object name",
            default=True,
            )

    split_mode_setting = EnumProperty(
            name="Split",
            items=(('ON', "Split", "Split geometry and omit unused verts"),
                   ('OFF', "Keep Vert Order", "Keep vertex order from file"),
                   ),
            )

    reset_location_setting = BoolProperty(
            name="Location",
            description="Reset Location to (0, 0, 0)",
            default=False,
            )

    reset_rotation_setting = BoolProperty(
            name="Rotation",
            description="Reset Rotation to (0, 0, 0)",
            default=False,
            )

    reset_scale_setting = BoolProperty(
            name="Scale",
            description="Reset Scale to (1, 1, 1)",
            default=False,
            )

    clamp_size_setting = FloatProperty(
            name="Clamp Size",
            description="Clamp bounds under this value (zero to disable)",
            min=0.0, max=1000.0,
            soft_min=0.0, soft_max=1000.0,
            default=0.0,
            )
			
    axis_forward_setting = EnumProperty(
            name="Forward",
            items=(('X', "X Forward", ""),
                   ('Y', "Y Forward", ""),
                   ('Z', "Z Forward", ""),
                   ('-X', "-X Forward", ""),
                   ('-Y', "-Y Forward", ""),
                   ('-Z', "-Z Forward", ""),
                   ),
            default='-Z',
            )

    axis_up_setting = EnumProperty(
            name="Up",
            items=(('X', "X Up", ""),
                   ('Y', "Y Up", ""),
                   ('Z', "Z Up", ""),
                   ('-X', "-X Up", ""),
                   ('-Y', "-Y Up", ""),
                   ('-Z', "-Z Up", ""),
                   ),
            default='Y',
            )

    def draw(self, context):
        layout = self.layout
        row = layout.row(align=True)
        row.prop(self, "ngons_setting")
        row.prop(self, "edges_setting")
        layout.prop(self, "smooth_groups_setting")
        box = layout.box()
        row = box.row()
        row.prop(self, "split_mode_setting", expand=True)
        row = box.row()
        # Split objects/groups if enabled
        if self.split_mode_setting == 'ON':
            row.label(text="Split by:")
            row.prop(self, "split_objects_setting")
            row.prop(self, "split_groups_setting")
        else:
            row.prop(self, "groups_as_vgroups_setting")
        row = layout.split(percentage=0.67)
        row.prop(self, "clamp_size_setting")
        layout.prop(self, "axis_forward_setting")
        layout.prop(self, "axis_up_setting")
        layout.prop(self, "image_search_setting")
        layout.prop(self, "use_file_name_setting")
        row = box.row()
        row.label(text="Reset orientation")
        row = box.row()
        row.prop(self, "reset_location_setting")
        row.prop(self, "reset_rotation_setting")
        row.prop(self, "reset_scale_setting")

    def execute(self, context):
        folder = (os.path.dirname(self.filepath))
        for i in self.files:
            path_to_file = (os.path.join(folder, i.name))
            # Import object using default importer with custom settings                  
            bpy.ops.import_scene.obj(filepath = path_to_file,
                                axis_forward = self.axis_forward_setting,
                                axis_up = self.axis_up_setting, 
                                use_edges = self.edges_setting,
                                use_smooth_groups = self.smooth_groups_setting, 
                                use_split_objects = self.split_objects_setting,
                                use_split_groups = self.split_groups_setting,
                                use_groups_as_vgroups = self.groups_as_vgroups_setting,
                                use_image_search = self.image_search_setting,
                                split_mode = self.split_mode_setting,
                                global_clamp_size = self.clamp_size_setting)
            # Get loaded object for operations
            loaded_obj = bpy.data.objects[len(bpy.data.objects)-1]
            # Reset orientation values if enabled
            if self.reset_location_setting:
                loaded_obj.location = Vector((0,0,0))
            if self.reset_rotation_setting:
                loaded_obj.rotation_euler = Euler((0,0,0), 'XYZ')
            if self.reset_scale_setting:
                loaded_obj.scale = Vector((1,1,1))
            # Use file name as object name if enabled
            if self.use_file_name_setting:
                loaded_obj.name = i.name.split('.obj')[0]
        return {'FINISHED'}

def menu_func_import(self, context):
    self.layout.operator(ImportMultipleObjs.bl_idname, text="Wavefront Batch (.obj)")

def register():
    bpy.utils.register_class(ImportMultipleObjs)
    bpy.types.INFO_MT_file_import.append(menu_func_import)

def unregister():
    bpy.utils.unregister_class(ImportMultipleObjs)
    bpy.types.INFO_MT_file_import.remove(menu_func_import)


if __name__ == "__main__":
    register()