import bpy

def add_tex_layer(layerType, texCol, texOpas, alphaChoice, normalChoice):
    try: 
        sys = bpy.context.user_preferences.system
        fontState = sys.use_translate_new_dataname
        sys.use_translate_new_dataname = False
    except:
        pass
    wm = bpy.context.window_manager
    scene = bpy.context.scene
    sd = bpy.context.space_data
    re = scene.render.engine
    ob = bpy.context.active_object
    mat = ob.active_material
    try:
        if layerType == "Transparent" or layerType == "Alpha_Mask":
            ob.show_transparent = True
            if mat:
                n = 0
                for ts in mat.texture_slots:
                    if ts is not None:
                        try:
                            if ts.use_map_alpha == True:
                                ts.texture.image = None
                                ts.texture = None
                                mat.texture_slots.clear(n)
                        except:
                            pass
                    n += 1
            try:
                if layerType == 'Alpha_Mask':
                    for node in bpy.data.materials[mat.name].node_tree.nodes:
                        if 'zbTransparent' in node.name:
                            tree = bpy.data.materials[mat.name].node_tree
                            mixed5 = tree.nodes['Mixed5']
                            mixed6 = tree.nodes['Mixed6']
                            mat.node_tree.links.new(mixed5.outputs['Shader'],
                            mixed6.inputs[1])
                            nodeColor = tree.nodes['Image Texture zbColor']
                            for img in bpy.data.images:
                                if "Color" in img.name:
                                    if ob.name[:4] in img.name:
                                        nodeColor.image = img
                                        break
            except:
                pass
        if mat is None or "None" in mat.name:
            mat = bpy.data.materials.new(ob.name)
            mat.diffuse_shader = 'LAMBERT'
            mat.darkness = 0.8
            mat.strand.use_tangent_shading = False
            mat.strand.root_size = 2.5
            mat.strand.tip_size = 0.25
            mat.strand.width_fade = 0.5
            ob.active_material = mat
        try:
            node = mat.node_tree.nodes['Mixed1']
        except:
            mat.use_nodes = True
            mat.node_tree.nodes.clear()
            mixedTotal = 8 
            locX = 250 
            mixedList =[] 
            for mixed in range(1,mixedTotal + 1):
                x = mixed
                mixed = mat.node_tree.nodes.new(type="ShaderNodeMixShader")
                mixed.name = "Mixed" + str(x)
                mixed.label = mixed.name
                mixedList.append(mixed)
                mixed.inputs['Fac'].default_value = 0
                locX += 250
                mixed.location = (locX,0)
            nodeOutput = mat.node_tree.nodes.new(type = 'ShaderNodeOutputMaterial')
            nodeOutput.location = (locX + 250,0) 
            node = mat.node_tree.nodes.new(type = 'ShaderNodeMath')
            node.label = node.name + ' zbDisplace'
            node.name = node.label
            nodeMath = node
            nodeMath.location = (locX + 250,-120)
            mat.node_tree.links.new(nodeMath.outputs['Value'],
            nodeOutput.inputs['Displacement'])
            x = 0
            for mixed in mixedList:
                x += 1
                if x < mixedTotal:
                    mixedNext = mixedList[x] 
                    mat.node_tree.links.new(mixed.outputs['Shader'],
                    mixedNext.inputs['Shader'])
                else:
                    mat.node_tree.links.new(mixed.outputs['Shader'],
                    nodeOutput.inputs['Surface'])
                if "5" in mixed.name:
                    mat.node_tree.links.new(mixed.outputs['Shader'],
                    mixedNext.inputs[2])
        w = round(scene.zbImgSize)
        h = round(scene.zbImgSizeH)
        layerName = ob.name[:4] 
        img = bpy.data.images.new(layerName + layerType, scene.zbImgSize, scene.zbImgSizeH, alpha= alphaChoice)
        override = bpy.context.copy()
        override['edit_image'] = img
        bpy.ops.image.pack(override, as_png = True)
        img.pixels[:] = (texCol, texCol, texCol, texOpas) * w * h
        try: 
            brushCol = bpy.context.tool_settings.image_paint.brush.color
            if wm.zbUseBrushColor:
                l = layerType
                go = 0
                if "Bu" not in l:
                    if "Tr" not in l:
                        if "Ma" not in l:
                            go = 1
                if go:
                    img.pixels[:] = (brushCol.r, brushCol.g, brushCol.b, 1) * w * h
        except:
            pass
        cTexName = layerName + layerType
        cTex = bpy.data.textures.new( name = cTexName, type = 'IMAGE')
        activeTex = -1
        for ts in mat.texture_slots:
            activeTex += 1
            if ts is None:
                break
        mTex = mat.texture_slots.add()
        mTex.texture = cTex
        mTex.texture_coords = 'UV'
        if normalChoice == True:
            mTex.use_map_normal = True
            mTex.bump_method = 'BUMP_MEDIUM_QUALITY'
            mTex.normal_factor = 0.0
        cTex.image = img
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        fu10(ob)
        for uv_face in ob.data.uv_textures.active.data:
            uv_face.image = img
        try: 
            if sd.viewport_shade != 'TEXTURED':
                sd.viewport_shade = 'MATERIAL'
            scene.game_settings.material_mode = 'GLSL'
        except:
            pass
        bpy.ops.object.mode_set(mode = 'TEXTURE_PAINT')
        bleed = 2 
        if w > 512:
            bleed = 5
        if w > 1024:
            bleed = 6
        if w > 2048:
            bleed = 8
        scene.tool_settings.image_paint.seam_bleed = bleed
        bpy.ops.object.zb_set_active_layer(tex_index=activeTex)
        slots = mat.texture_slots
        ts = slots[mat.active_texture_index]
        ctx = bpy.context.copy()
        ctx['texture_slot'] = ts
        x = 0
        while x < 17:
            bpy.ops.texture.slot_move(ctx, type='DOWN')
            x += 1
    except:
        pass
    tn = mat.active_texture_index
    context = bpy.context
    fu12(context,tn)

    if layerType == "Color":
        add_color_layer(mat, layerType, img)
    if layerType == "Bump":
        add_bump_layer(mat, layerType, img)
    if layerType == "Specular":
        add_specular_layer(mat, layerType, img)
    if layerType == "Glow":
        add_glow_layer(mat, layerType, img)
    if layerType == "Transparent":
        add_transparent_layer(mat, layerType, img)
    if layerType == "Alpha_Mask":
        add_alpha_mask_layer(mat, layerType, img)
    if re != 'CYCLES':
        mat.use_nodes = False
    try: 
        sys = bpy.context.user_preferences.system
        sys.use_translate_new_dataname = fontState
    except:
        pass
    return mTex

def fu12(context,tn):
    try:
        ob = bpy.context.active_object
        me = ob.data
        mat = ob.active_material
        mat.active_texture_index = tn
        ts = mat.texture_slots[tn]
        try:  
            ts.use = True
        except:
            pass
        if not me.uv_textures:
            bpy.ops.mesh.uv_texture_add()
        if ts.texture_coords  == 'UV':
            if ts.uv_layer:
                uvtex = me.uv_textures[ts.uv_layer]
            else:
                uvtex = me.uv_textures.active
                me.uv_textures.active= uvtex
        else:
            uvtex = me.uv_textures.active
        uvtex = uvtex.data.values()
        img = ts.texture.image
        m_id = ob.active_material_index
        if img:
            for f in me.polygons:
                if f.material_index == m_id:
                    uvtex[f.index].image = img
        else:
            for f in me.polygons:
                if f.material_index == m_id:
                    uvtex[f.index].image = None
        fu11()
        me.update()
    except:
        pass
    try:
        if "color" in img.name.lower() :
            node = mat.node_tree.nodes['Image Texture zbColor']
        if "bump" in img.name.lower() :
            node = mat.node_tree.nodes['Image Texture zbBump']
        if "specular" in img.name.lower() :
            node = mat.node_tree.nodes['Image Texture zbSpecular']
        if "glow" in img.name.lower() :
            node = mat.node_tree.nodes['Image Texture zbGlow']
        if "alpha_mask" in img.name.lower() :
            node = mat.node_tree.nodes['Image Texture zbAlpha_Mask']
        node.image = img
        node_tree = bpy.data.materials[mat.name].node_tree
        node_tree.nodes.active = node
        me.update()
    except:
        pass
    return


def add_glow_layer(mat, layerType, img):
    try: 
        nodeTex = mat.node_tree.nodes['Image Texture zbGlow']            
        mat.node_tree.nodes['Math zbGlow'].inputs[1].default_value = 6.5
    except:
        node = mat.node_tree.nodes.new(type = 'ShaderNodeTexImage')
        node.label = node.name + ' zb' + layerType
        node.name = node.label
        nodeTex = node
        node = mat.node_tree.nodes.new(type = 'ShaderNodeMixRGB')
        node.label = node.name + ' zb' + layerType
        node.name = node.label
        nodeMixRGB = node
        nodeMixRGB.blend_type = 'MIX'
        nodeMixRGB.inputs['Fac'].default_value = 1
        node = mat.node_tree.nodes.new(type = 'ShaderNodeBrightContrast')
        node.label = node.name + ' zb' + layerType
        node.name = node.label
        nodeBright = node
        node = mat.node_tree.nodes.new(type='ShaderNodeEmission')
        node.label = node.name + ' zb' + layerType
        node.name = node.label
        node.inputs[1].default_value = 6.5
        nodeEmission = node
        node = mat.node_tree.nodes.new(type='ShaderNodeRGBToBW')
        node.label = node.name + ' zb' + layerType
        node.name = node.label
        nodeBW = node
        node = mat.node_tree.nodes.new(type='ShaderNodeMath')
        node.label = node.name + ' zb' + layerType
        node.name = node.label
        nodeMath = node
        nodeMath.operation = 'MULTIPLY'
        nodeMath.inputs[1].default_value = 6.5
        glowMixed7 = mat.node_tree.nodes['Mixed7']
        mat.node_tree.links.new(nodeTex.outputs['Color'], nodeMixRGB.inputs['Color2'])
        mat.node_tree.links.new(nodeMixRGB.outputs['Color'], nodeBright.inputs['Color'])
        mat.node_tree.links.new(nodeBright.outputs['Color'], nodeBW.inputs['Color'])
        mat.node_tree.links.new(nodeBright.outputs['Color'], nodeEmission.inputs['Color'])
        mat.node_tree.links.new(nodeBW.outputs['Val'], nodeMath.inputs['Value'])
        mat.node_tree.links.new(nodeEmission.outputs['Emission'], glowMixed7.inputs[2])
        mat.node_tree.links.new(nodeMath.outputs['Value'], glowMixed7.inputs['Fac'])
        nodeTex.location = (-50, -790)
        nodeMixRGB.location = (120, -795)
        nodeBright.location = (120, -845)
        nodeBW.location = (250,-790)
        nodeMath.location = (250,-880)
        nodeEmission.location = (415,-790)
        mat.node_tree.nodes[nodeBright.name].hide = True
        mat.node_tree.nodes[nodeMixRGB.name].hide = True
    nodeTex.image = img
    node_tree = bpy.data.materials[mat.name].node_tree
    node_tree.nodes.active = nodeTex

def add_transparent_layer(mat, layerType, img):
    try: 
        nodeTex = mat.node_tree.nodes['Image Texture zbColor']
        nodeTex.mute = False
    except:
        bpy.ops.object.zb_paint_color()
        nodeTex = mat.node_tree.nodes['Image Texture zbColor']
    if nodeTex.outputs['Alpha'].is_linked == False:
        try:
            nodeAlpha = mat.node_tree.nodes['Transparent BSDF zbTransparent']
        except:
            node = mat.node_tree.nodes.new(type = 'ShaderNodeBsdfTransparent')
            node.label = node.name + ' zb' + layerType
            node.name = node.label
            nodeAlpha = node
        Mixed5 = mat.node_tree.nodes['Mixed5']
        Mixed6 = mat.node_tree.nodes['Mixed6']
        mat.node_tree.links.new(nodeTex.outputs['Alpha'], Mixed6.inputs['Fac'])
        mat.node_tree.links.new(Mixed5.outputs['Shader'], nodeAlpha.inputs['Color'])
        mat.node_tree.links.new(nodeAlpha.outputs['BSDF'], Mixed6.inputs['Shader'])
        mat.node_tree.links.new(Mixed5.outputs['Shader'], Mixed6.inputs[2])
        nodeAlpha.location = (1750, -130)
    nodeTex.image = img
    node_tree = bpy.data.materials[mat.name].node_tree
    node_tree.nodes.active = nodeTex

def add_alpha_mask_layer(mat, layerType, img):
    try: 
        nodeTex = mat.node_tree.nodes['Image Texture zbAlpha_Mask']
        nodeTex.mute = False
    except:
        pass
    try:
        Mixed6 = mat.node_tree.nodes['Mixed6']
        nodeAlpha = mat.node_tree.nodes['Transparent BSDF zbAlpha_Mask']
        mat.node_tree.links.new(nodeTex.outputs['Alpha'], Mixed6.inputs['Fac'])
        mat.node_tree.links.new(nodeAlpha.outputs['BSDF'], Mixed6.inputs[2])
    except:
        node = mat.node_tree.nodes.new(type = 'ShaderNodeTexImage')
        node.label = node.name + ' zb' + layerType
        node.name = node.label
        nodeTex = node
        node = mat.node_tree.nodes.new(type = 'ShaderNodeBsdfTransparent')
        node.label = node.name + ' zb' + layerType
        node.name = node.label
        nodeAlpha = node
        nodeTex.location = (-50, -1075)
        nodeAlpha.location = (250, -1075)
        Mixed6 = mat.node_tree.nodes['Mixed6']
        mat.node_tree.links.new(nodeTex.outputs['Alpha'], Mixed6.inputs['Fac'])
        mat.node_tree.links.new(nodeAlpha.outputs['BSDF'], Mixed6.inputs[2])
    nodeTex.image = img
    node_tree = bpy.data.materials[mat.name].node_tree
    node_tree.nodes.active = nodeTex


def add_specular_layer(mat, layerType, img):
    try:
        nodeTex = mat.node_tree.nodes['Image Texture zbSpecular']
        mat.node_tree.nodes['Math zbSpecular'].inputs[1].default_value = 1
    except:
        node = mat.node_tree.nodes.new(type = 'ShaderNodeTexImage')
        node.label = node.name + ' zb' + layerType
        node.name = node.label
        nodeTex = node
        node = mat.node_tree.nodes.new(type = 'ShaderNodeMixRGB')
        node.label = node.name + ' zb' + layerType
        node.name = node.label
        nodeMixRGB = node
        nodeMixRGB.blend_type = 'MIX'
        nodeMixRGB.inputs['Fac'].default_value = 1
        node = mat.node_tree.nodes.new(type = 'ShaderNodeBrightContrast')
        node.label = node.name + ' zb' + layerType
        node.name = node.label
        nodeBright = node
        node = mat.node_tree.nodes.new(type='ShaderNodeBsdfGlossy')
        node.label = node.name + ' zb' + layerType
        node.name = node.label
        nodeGloss = node
        node = mat.node_tree.nodes.new(type='ShaderNodeRGBToBW')
        node.label = node.name + ' zb' + layerType
        node.name = node.label
        nodeBW = node
        node = mat.node_tree.nodes.new(type='ShaderNodeMath')
        node.label = node.name + ' zb' + layerType
        node.name = node.label
        nodeMath = node
        nodeMath.operation = 'MULTIPLY'
        nodeMath.inputs[1].default_value = 1
        specularMixed5 = mat.node_tree.nodes['Mixed5']
        mat.node_tree.links.new(nodeTex.outputs['Color'], nodeMixRGB.inputs['Color2'])
        mat.node_tree.links.new(nodeMixRGB.outputs['Color'], nodeBright.inputs['Color'])
        mat.node_tree.links.new(nodeBright.outputs['Color'], nodeBW.inputs['Color'])
        mat.node_tree.links.new(nodeBright.outputs['Color'], nodeGloss.inputs['Color'])
        mat.node_tree.links.new(nodeBW.outputs['Val'], nodeMath.inputs['Value'])
        mat.node_tree.links.new(nodeGloss.outputs['BSDF'], specularMixed5.inputs[2])
        mat.node_tree.links.new(nodeMath.outputs['Value'], specularMixed5.inputs['Fac'])
        nodeTex.location = (-50, -515)
        nodeMixRGB.location = (120, -520)
        nodeBright.location = (120, -570)
        nodeBW.location = (250,-515)
        nodeMath.location = (250,-605)
        nodeGloss.location = (415,-515)
        mat.node_tree.nodes[nodeBright.name].hide = True
        mat.node_tree.nodes[nodeMixRGB.name].hide = True
    nodeTex.image = img
    node_tree = bpy.data.materials[mat.name].node_tree
    node_tree.nodes.active = nodeTex
    

def add_bump_layer(mat, layerType, img):
    try:
        nodeTex = mat.node_tree.nodes['Image Texture zbBump']
    except:
        node = mat.node_tree.nodes.new(type = 'ShaderNodeTexImage')
        node.label = node.name + ' zb' + layerType
        node.name = node.label
        nodeTex = node
        nodeTex.color_space = 'NONE'
        node = mat.node_tree.nodes.new(type = 'ShaderNodeBrightContrast')
        node.label = node.name + ' zb' + layerType
        node.name = node.label
        nodeBright = node
        node = mat.node_tree.nodes.new(type = 'ShaderNodeRGBToBW')
        node.label = node.name + ' zb' + layerType
        node.name = node.label
        nodeBW = node
        node = mat.node_tree.nodes.new(type='ShaderNodeMath')
        node.label = node.name + ' zb' + layerType
        node.name = node.label
        node.inputs[1].default_value = 2.5
        nodeMath = node
        nodeMath.operation = 'MULTIPLY'
        nodeOutput = mat.node_tree.nodes['Material Output']
        nodeMath2 = mat.node_tree.nodes['Math zbDisplace']
        mat.node_tree.links.new(nodeTex.outputs['Color'], nodeBright.inputs['Color'])
        mat.node_tree.links.new(nodeBright.outputs['Color'], nodeBW.inputs['Color'])
        mat.node_tree.links.new(nodeBW.outputs['Val'], nodeMath.inputs[0])
        mat.node_tree.links.new(nodeMath.outputs['Value'], nodeMath2.inputs[1])
        nodeTex.location = (-50, -260)
        nodeBright.location = (120, -260)
        nodeBW.location = (120, -390)
        nodeMath.location = (285, -260)
    nodeTex.image = img
    node_tree = bpy.data.materials[mat.name].node_tree
    node_tree.nodes.active = nodeTex
    try: 
        brush = bpy.context.tool_settings.image_paint.brush
        brush.color = (1,1,1)
    except:
        pass
    

def add_color_layer(mat, layerType, img):
    try:
        nodeTex = mat.node_tree.nodes['Image Texture zbColor']
        nodeTex.mute = False
    except:
        node = mat.node_tree.nodes.new(type = 'ShaderNodeTexImage')
        node.label = node.name + ' zb' + layerType
        node.name = node.label
        nodeTex = node
        node = mat.node_tree.nodes.new(type = 'ShaderNodeMixRGB')
        node.label = node.name + ' zb' + layerType
        node.name = node.label
        nodeMixRGB = node
        nodeMixRGB.blend_type = 'MIX'
        nodeMixRGB.inputs['Fac'].default_value = 1
        node = mat.node_tree.nodes.new(type = 'ShaderNodeBrightContrast')
        node.label = node.name + ' zb' + layerType
        node.name = node.label
        nodeBright = node
        node = mat.node_tree.nodes.new(type = 'ShaderNodeBsdfDiffuse')
        node.label = node.name + ' zb' + layerType
        node.name = node.label
        nodeDiffuse = node
        node = mat.node_tree.nodes.new(type = 'ShaderNodeBump')
        node.label = node.name + ' zb' + layerType
        node.name = node.label
        nodeBump = node
        nodeBump.inputs[1].default_value = 0.015
        nodeBump.invert = True
        node = mat.node_tree.nodes.new(type='ShaderNodeRGBToBW')
        node.label = node.name + ' zb' + layerType
        node.name = node.label
        nodeBW = node
        node = mat.node_tree.nodes.new(type='ShaderNodeBsdfGlossy')
        node.label = node.name + ' zb' + layerType
        node.name = node.label
        nodeGloss = node
        node = mat.node_tree.nodes.new(type='ShaderNodeMath')
        node.label = node.name + ' zb' + layerType
        node.name = node.label
        nodeMath = node
        nodeMath.inputs[1].default_value = 0
        nodeMath.operation = 'MULTIPLY'
        node = mat.node_tree.nodes.new(type='ShaderNodeEmission')
        node.label = node.name + ' zb' + layerType
        node.name = node.label
        nodeEmission = node
        nodeEmission.inputs[1].default_value = 10
        node = mat.node_tree.nodes.new(type = 'ShaderNodeBsdfTransparent')
        node.label = node.name + ' zb' + layerType
        node.name = node.label
        nodeAlpha = node
        mat.node_tree.nodes[nodeBump.name].hide = True
        mat.node_tree.nodes[nodeBW.name].hide = True
        mat.node_tree.nodes[nodeGloss.name].hide = True
        mat.node_tree.nodes[nodeMath.name].hide = True
        mat.node_tree.nodes[nodeBright.name].hide = True
        mat.node_tree.nodes[nodeMixRGB.name].hide = True
        nodeTex.location = (-50, 0)
        nodeMixRGB.location = (120, -5)
        nodeBright.location = (120, -55)
        nodeDiffuse.location = (250, 0)
        nodeMath.location = (250, -130)
        nodeBW.location = (250, -170)
        nodeBump.location = (500, -130)
        nodeGloss.location = (500, -170)
        nodeEmission.location = (750,-130)
        nodeAlpha.location = (1000, -130)
        colorMixed1 = mat.node_tree.nodes['Mixed1']
        colorMixed2 = mat.node_tree.nodes['Mixed2']
        colorMixed3 = mat.node_tree.nodes['Mixed3']
        nodeMath2 = mat.node_tree.nodes['Math zbDisplace']
        nodeMath2.inputs[0].default_value = 0
        mat.node_tree.links.new(nodeTex.outputs['Color'], nodeMixRGB.inputs['Color2'])
        mat.node_tree.links.new(nodeMixRGB.outputs['Color'], nodeBright.inputs['Color'])
        mat.node_tree.links.new(nodeBright.outputs['Color'], nodeDiffuse.inputs['Color'])
        mat.node_tree.links.new(nodeDiffuse.outputs['BSDF'], colorMixed1.inputs['Shader'])
        mat.node_tree.links.new(nodeDiffuse.outputs['BSDF'], colorMixed1.inputs['Shader'])
        mat.node_tree.links.new(nodeBright.outputs['Color'], nodeBW.inputs['Color'])
        mat.node_tree.links.new(nodeBW.outputs['Val'], nodeMath.inputs[0])
        mat.node_tree.links.new(nodeMath.outputs['Value'], nodeMath2.inputs[0])
        mat.node_tree.links.new(nodeBW.outputs['Val'], nodeGloss.inputs['Color'])
        mat.node_tree.links.new(nodeBW.outputs['Val'], nodeBump.inputs['Strength'])
        mat.node_tree.links.new(nodeBW.outputs['Val'], nodeBump.inputs['Height'])
        mat.node_tree.links.new(nodeBump.outputs['Normal'], nodeGloss.inputs['Normal'])
        mat.node_tree.links.new(nodeGloss.outputs['BSDF'], colorMixed1.inputs[2])
        mat.node_tree.links.new(nodeBright.outputs['Color'], nodeEmission.inputs['Color'])
        mat.node_tree.links.new(nodeEmission.outputs['Emission'], colorMixed2.inputs[2])
        mat.node_tree.links.new(nodeAlpha.outputs['BSDF'], colorMixed3.inputs[2])
        mat.node_tree.links.new(colorMixed2.outputs['Shader'], nodeAlpha.inputs['Color'])
    nodeTex.image = img
    node_tree = bpy.data.materials[mat.name].node_tree
    node_tree.nodes.active = nodeTex
    
