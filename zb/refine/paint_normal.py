import bpy
from .tex_layer import add_tex_layer

class PaintNormal(bpy.types.Operator):
    bl_idname = "object.zb_paint_normal"
    bl_label = "Add Normal"
    bl_description = "Convert the detail from your multires modifier into a normal map"

    def execute(self, context):
        scene = bpy.context.scene
        bt = scene.render.bake_type
        alphaChoice = True
        layerType = "Normal"
        normalChoice = True
        texCol = 1
        texOpas = 0
        if 'DISPLACEMENT' in bt:
            layerType = "Displacement"
            normalChoice = False
        if 'DERIVATIVE' in bt:
            layerType = "Derivative"
            normalChoice = True
        add_tex_layer(layerType, texCol, texOpas, alphaChoice, normalChoice)
        return {'FINISHED'}
