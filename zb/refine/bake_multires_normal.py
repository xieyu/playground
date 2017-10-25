import bpy
from .utils import create_normal_map_node
from .utils import set_object_mode
from .utils import set_lamp_visible

from .utils import apply_modifiers
from .utils import get_multires_modifier
from .utils import only_select_object

class BakeMultiresNormal(bpy.types.Operator):
    bl_idname = "object.zb_bake_normal"
    bl_label = "Bake Multires Normal"
    bl_description = "Apply multires sculpt detail as a normal map to your object (may take several minutes)."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = bpy.context.scene
        origin_mode = bpy.context.mode

        ob = bpy.context.active_object
        bt = scene.render.bake_type

        only_select_object(ob)

        fastModeState = False
        if scene.zbFastMode:
            fastModeState = True
            scene.zbFastMode = False

        set_lamp_visible()
        apply_modifiers(ob, exclude_list=["MULTIRES", "SUBSURF"])
        multires = get_multires_modifier(ob)

        if not multires:
            print('Multires modifier could not be added to', ob.name)
            print('Aborted bake')
            set_object_mode(origin_mode)
            return {'FINISHED'}

        if bt != 'DISPLACEMENT' and bt != 'DERIVATIVE':
            if not ob.active_material:
                bpy.ops.object.zb_paint_color()

        bpy.ops.object.zb_paint_normal()
        mat = ob.active_material
        tex = mat.active_texture

        if bt != 'DISPLACEMENT' and bt != 'DERIVATIVE':
            for i in range(16):
                bpy.ops.object.zb_move_texture(tex_move_up=1)
            tex.use_normal_map = True
            mat.texture_slots[tex.name].normal_factor = 5

        if bt == 'DERIVATIVE':
            mat.texture_slots[tex.name].normal_factor = .4

        mat.texture_slots[tex.name].use_map_color_diffuse = False        
        set_lamp_visible()
        levels = multires.levels
        reduced = max(int(levels/2), 1)
        multires.levels = reduced
        scene.render.bake_margin = 25
        if bt != 'DISPLACEMENT' and bt != 'DERIVATIVE':
            scene.render.bake_type = 'NORMALS'
        scene.render.use_bake_multires = True
        scene.render.use_bake_selected_to_active = False
        bpy.ops.object.bake_image()
        if bt != 'DISPLACEMENT' and bt != 'DERIVATIVE':
            create_normal_map_node(mat)
        try: 
            multires.levels = levels
        except:
            pass
        if fastModeState:
            scene.zbFastMode = True 

        set_object_mode(origin_mode)
        return {'FINISHED'}
