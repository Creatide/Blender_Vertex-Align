bl_info = {
    "name": "Vertex Align",
    "description": "Align selected vertices to same line with active vertex and selected axis.",
    "category": "Mesh",
    "author": "Sakari Niittymaa",
    "location": "Edit Mode > Mesh > Vertex Align (X/Y/Z)"
}


import bpy
import bmesh
import mathutils

def alignVertices( axis ):
    
    scale = active_vert = None
    
    obj = bpy.context.edit_object
    me = obj.data
    
    bm = bmesh.from_edit_mesh(me)
    selected_verts = [v for v in bm.verts if v.select]
    
    # Get last active vertex
    for elem in reversed(bm.select_history):
        if isinstance(elem, bmesh.types.BMVert):
            active_vert = elem
            break
    
    # Move vertices to selected axis
    if obj.mode == 'EDIT' and obj.data:
        
        if axis == "X":
            scale = mathutils.Vector((0.0, 1.0, 1.0))
            
        if axis == "Y":
            scale = mathutils.Vector((1.0, 0.0, 1.0))
            
        if axis == "Z":
            scale = mathutils.Vector((1.0, 1.0, 0.0))
            
        # Make scale process for selected vertices
        for v in selected_verts:
            #v.co[axis] = selected_verts[-1].co[axis]
            v.co[axis] = active_vert.co[axis]
        
        # Update bmesh to viewport
        bmesh.update_edit_mesh(me, True)
        
    else:
        print("Object is not in edit mode.") 
        
# X Align
class VertexAlignX(bpy.types.Operator):
    
    bl_idname = "mesh.vertex_align_x"
    bl_label = "Vertex Align X"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        alignVertices(0)
        return {'FINISHED'}

# Y Align
class VertexAlignY(bpy.types.Operator):
    
    bl_idname = "mesh.vertex_align_y"
    bl_label = "Vertex Align Y"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        alignVertices(1)
        return {'FINISHED'}

# Z Align
class VertexAlignZ(bpy.types.Operator):
    
    bl_idname = "mesh.vertex_align_z"
    bl_label = "Vertex Align Z"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        alignVertices(2)
        return {'FINISHED'}

# Set menu items
def menu_func(self, context):
    self.layout.operator(VertexAlignX.bl_idname, icon = "PLUGIN")
    self.layout.operator(VertexAlignY.bl_idname, icon = "PLUGIN")
    self.layout.operator(VertexAlignZ.bl_idname, icon = "PLUGIN")

# Store keymaps
addon_keymaps = []

# Register classes and set keymaps
def register():
    bpy.utils.register_class(VertexAlignX)
    bpy.utils.register_class(VertexAlignY)
    bpy.utils.register_class(VertexAlignZ)
    bpy.types.VIEW3D_MT_edit_mesh.append(menu_func)

    # Keymaps
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Mesh', space_type='EMPTY')
    
    kmix = km.keymap_items.new(VertexAlignX.bl_idname, 'X', 'PRESS', alt=True, shift=True, ctrl=True)
    kmiy = km.keymap_items.new(VertexAlignY.bl_idname, 'Y', 'PRESS', alt=True, shift=True, ctrl=True)
    kmiz = km.keymap_items.new(VertexAlignZ.bl_idname, 'Z', 'PRESS', alt=True, shift=True, ctrl=True)
    
    addon_keymaps.append((km, kmix, kmiy, kmiz))

# Unregister and remove keymaps
def unregister():
    bpy.utils.unregister_class(VertexAlignX)
    bpy.utils.unregister_class(VertexAlignY)
    bpy.utils.unregister_class(VertexAlignZ)
    bpy.types.VIEW3D_MT_edit_mesh.remove(menu_func)

    # Remove keymaps
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


# This allows you to run the script directly from blenders text editor
if __name__ == "__main__":
    register()
import bpy