bl_info = {
    "name": "Shape Keys in Pose Mode",
    "blender": (3, 6, 0),
    "category": "Rigging",
}

import bpy

class ShapeKeysProperties(bpy.types.PropertyGroup):
    def get_mesh_items(self, context):
        return [(obj.name, obj.name, "") for obj in bpy.data.objects if obj.type == 'MESH' and obj.data.shape_keys is not None]

    mesh_name: bpy.props.EnumProperty(items=get_mesh_items)

class ShapeKeysPanel(bpy.types.Panel):
    bl_label = "Shape Keys"
    bl_idname = "OBJECT_PT_shape_keys"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Tool"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.mode == 'POSE'

    def draw(self, context):
        layout = self.layout
        props = context.object.shape_keys_props

        layout.prop(props, "mesh_name", text="Select Mesh")

        if props.mesh_name:
            mesh = bpy.data.objects[props.mesh_name]
            for key in mesh.data.shape_keys.key_blocks:
                row = layout.row()
                row.label(text=key.name)
                row.prop(key, "value", slider=True)

def register():
    bpy.utils.register_class(ShapeKeysProperties)
    bpy.types.Object.shape_keys_props = bpy.props.PointerProperty(type=ShapeKeysProperties)
    bpy.utils.register_class(ShapeKeysPanel)

def unregister():
    bpy.utils.unregister_class(ShapeKeysPanel)
    del bpy.types.Object.shape_keys_props
    bpy.utils.unregister_class(ShapeKeysProperties)

if __name__ == "__main__":
    register()


