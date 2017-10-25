import bpy

def create_normal_map_node(mat):
    scene = bpy.context.scene
    ob = bpy.context.active_object
    tex = mat.active_texture
    needNodes = True
    if hasattr(mat.node_tree,'nodes'):
        if 'Normal Map zbNormal' in mat.node_tree.nodes: 
            mat.node_tree.nodes['Image Texture zbNormal'].image = tex.image
            needNodes = False
        if 'Diffuse BSDF zbColor' not in mat.node_tree.nodes:
            if scene.render.engine == 'BLENDER_RENDER':
                scene.zbGoCycles = True
                scene.render.engine = 'BLENDER_RENDER'
    else:
        if scene.render.engine == 'BLENDER_RENDER':
            scene.zbGoCycles = True
            scene.render.engine = 'BLENDER_RENDER'
    if needNodes:                        
        nodeTex = mat.node_tree.nodes.new(type = 'ShaderNodeTexImage')
        nodeTex.label = nodeTex.name + ' zb' + 'Normal'
        nodeTex.name = nodeTex.label
        nodeTex.color_space = 'NONE'
        nodeTex.image = tex.image

        nodeNormal = mat.node_tree.nodes.new(type = 'ShaderNodeNormalMap')
        nodeNormal.label = nodeNormal.name + ' zb' + 'Normal'
        nodeNormal.name = nodeNormal.label
        nodeNormal.uv_map = 'UVMap'
        nodeNormal.inputs[0].default_value = 5

        nodeDifCol = mat.node_tree.nodes['Diffuse BSDF zbColor']
        mat.node_tree.links.new(nodeTex.outputs['Color'], nodeNormal.inputs['Color'])
        mat.node_tree.links.new(nodeNormal.outputs['Normal'], nodeDifCol.inputs['Normal'])
        mat.node_tree.nodes[nodeTex.name].hide = True
        mat.node_tree.nodes[nodeNormal.name].hide = True
        nodeTex.location = (120, -105)
        nodeNormal.location = (120, -160)
    try:
        normalMapNode = mat.node_tree.nodes['Normal Map zbNormal']
        normalMapNode.uv_map = ob.data.uv_textures.active.name
    except:
        pass

def set_object_mode(mode):
    if 'EDIT' in mode:
        mode = 'EDIT'
    if 'TEXTURE' in mode:
        mode = 'TEXTURE_PAINT'
    if 'VERTEX' in mode:
        mode = 'VERTEX_PAINT'
    if 'WEIGHT' in mode:
        mode = 'WEIGHT_PAINT'    
    if 'PARTICLE' in mode:
        mode = 'PARTICLE_EDIT'
    try:
        bpy.ops.object.mode_set(mode= mode)
    except:
        print('unable to return to previous mode')
    return

def set_lamp_visible():
    if len(bpy.data.lamps) < 1:
        newLamp = bpy.data.lamps.new(name='Basic Lamp',type ='HEMI')
        txt1 = 'No lamps were found in the scene, so one was created ' 
        txt2 = 'because it was required for this type of baking process.'
    else:
        visibleLamp = False
        for ob in bpy.data.objects:
            if ob.type == 'LAMP':
                if ob.hide_render is False:
                    visibleLamp = True
                    break
        if visibleLamp == False:
            for ob in bpy.data.objects:
                if ob.type == 'LAMP':
                    ob.hide_render = False
                    break


def apply_modifiers(obj, exclude_list):
    origin_mode = bpy.context.mode
    bpy.ops.object.mode_set(mode='OBJECT')
    for mod in obj.modifiers:
        if mod.type not in exclude_list:
            bpy.ops.object.modifier_apply(modifier=mod.name, apply_as='DATA')
    bpy.ops.object.mode_set(mode=origin_mode)


def get_multires_modifier(obj, create_if_not_exsits=True):
    for mod in obj.modifiers:
        if mod.type == 'MULTIRES':
            return mod
    if create_if_not_exsits:
        return obj.modifiers.new(name='Multires', type='MULTIRES')
    return None


def only_select_object(obj):
    origin_mode = bpy.context.mode
    bpy.ops.object.mode_set(mode='OBJECT')
    for item in bpy.context.selected_objects:
        item.select = False
    obj.select = True
    bpy.ops.object.mode_set(mode=origin_mode)
