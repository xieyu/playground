import bpy

from .utils import create_normal_map_node
from .utils import set_object_mode

class MergeNormals(bpy.types.Operator):
    bl_idname = "object.zb_bump_to_normal"
    bl_label = "ZB Merge Normals"
    bl_description = "Merge visible bump and normal layers into a single normal layer (may take several minutes)."

    def execute(self, context):
        scene = bpy.context.scene
        mode = bpy.context.mode
        re = scene.render.engine
        wm = bpy.context.window_manager
        ob = bpy.context.active_object
        mat = ob.active_material
        selected = bpy.context.selected_objects
        bpy.ops.object.zb_save_layers(save_only_active=True)
        bpy.ops.object.mode_set(mode='OBJECT')
        if re == 'CYCLES':
            scene.zbGoCycles = False
        newName = ob.name[:4] + 'Normal'        

        img = bpy.data.images.new(name=newName, width=scene.zbImgSize, height=scene.zbImgSizeH)        
        for obj in bpy.data.objects:
            if hasattr(obj,'active_material'):
                if obj.active_material == ob.active_material:
                    obj.select = True
                    if obj.data.uv_textures:
                        for uv_face in ob.data.uv_textures.active.data:
                            uv_face.image = img
                else:
                    obj.select = False
        override = bpy.context.copy()
        override['edit_image'] = img
        bpy.ops.image.pack(override, as_png = True)
        scene.render.use_bake_multires = False
        scene.render.bake_type = 'NORMALS'
        bpy.ops.object.bake_image()
        bpy.ops.object.zb_paint_normal()
        for i in range(16):
            bpy.ops.object.zb_move_texture(tex_move_up=1)
        mat = ob.active_material
        tex = mat.active_texture
        tex.image = img
        tex.use_normal_map = True
        mat.texture_slots[tex.name].use_map_color_diffuse = False
        mat.texture_slots[tex.name].normal_factor = 5
        create_normal_map_node(mat)
        try: 
            for slot in mat.texture_slots:
                try: 
                    if slot.use_map_normal:
                        if slot.texture.use_normal_map == False:
                            if slot.use_map_color_diffuse == False:
                                slot.use = False
                except:
                    pass
                try: 
                    if slot.use_map_color_diffuse:
                        if slot.use_map_normal:
                            slot.normal_factor = 0
                except:
                    pass
                try: 
                    if slot.texture.use_normal_map:
                        if slot.texture.name != mat.active_texture.name:
                            slot.use = False
                except:
                    pass
        except:
            pass
        if re == 'CYCLES':
            scene.zbGoCycles = True
        set_object_mode(mode)
        fu0()
        return{'FINISHED'}
