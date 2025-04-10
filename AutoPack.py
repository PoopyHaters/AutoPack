# Just to clarify: This document and all the text/code in it is owned by the BDPackUtils group including qAustria, muz011 and happypooky.
# Credit of using code is required at ANY type of remaster/skid.
# BETA TESTING
# Some packs may break, report an issue

import bpy, os, shutil, zipfile, time, requests, pyperclip, json
from PIL import Image

def extractZip(zip_path, copy_to=None, swords=None, pickaxes=None, items=None, bow=None, blocks=None, sky=None):
    if zip_path is None:
        print("Extraction cancelled!")
    else:
        extract_to = os.path.splitext(zip_path)[0]
        
        os.makedirs(extract_to, exist_ok=True)
        target_dir = os.path.join(extract_to, "assets/minecraft/textures/items")
        block_dir = os.path.join(extract_to, "assets/minecraft/textures/blocks")
        sky_dir = os.path.join(extract_to, "assets/minecraft/mcpatcher/sky/world0")
        os.makedirs(target_dir, exist_ok=True)
        os.makedirs(block_dir, exist_ok=True)
        os.makedirs(sky_dir, exist_ok=True)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for file in zip_ref.namelist():
                if file.startswith("assets/minecraft/textures/items/"):
                    zip_ref.extract(file, extract_to)
                if file.startswith("assets/minecraft/textures/blocks/"):
                    zip_ref.extract(file, extract_to)
                if file.startswith("assets/minecraft/mcpatcher/sky/world0/"):
                    zip_ref.extract(file, extract_to)

        if swords:
            os.makedirs(copy_to, exist_ok=True)
            for image in swords:
                item_path = os.path.join(target_dir, image)
                if os.path.exists(item_path):
                    shutil.copy(item_path, os.path.join(copy_to, image))
        if pickaxes:
            os.makedirs(copy_to, exist_ok=True)
            for image in pickaxes:
                item_path = os.path.join(target_dir, image)
                if os.path.exists(item_path):
                    shutil.copy(item_path, os.path.join(copy_to, image))
        if items:
            os.makedirs(copy_to, exist_ok=True)
            for image in items:
                item_path = os.path.join(target_dir, image)
                if os.path.exists(item_path):
                    shutil.copy(item_path, os.path.join(copy_to, image))
        if bow:
            os.makedirs(copy_to, exist_ok=True)
            for image in bow:
                item_path = os.path.join(target_dir, image)
                if os.path.exists(item_path):
                    shutil.copy(item_path, os.path.join(copy_to, image))
        if blocks:
            os.makedirs(copy_to, exist_ok=True)
            for image in blocks:
                block_path = os.path.join(block_dir, image)
                if os.path.exists(block_path):
                    shutil.copy(block_path, os.path.join(copy_to, image))
        if sky:
            os.makedirs(copy_to, exist_ok=True)
            for image in sky:
                sky_path = os.path.join(sky_dir, image)
                if os.path.exists(sky_path):
                    shutil.copy(sky_path, os.path.join(copy_to, image))

swords = ["wood_sword.png", "stone_sword.png", "iron_sword.png", "diamond_sword.png"]
pickaxes = ["wood_pickaxe.png", "stone_pickaxe.png", "iron_pickaxe.png", "diamond_pickaxe.png"]
items = ["apple_golden.png", "ender_pearl.png", "emerald.png", "diamond.png", "iron_ingot.png"]
bow = ["bow_standby.png", "bow_pulling_0.png", "bow_pulling_1.png", "bow_pulling_2.png"]
blocks = [
    "wool_colored_blue.png",
    "wool_colored_red.png",
    "wool_colored_green.png",
    "wool_colored_yellow.png",
    "wool_colored_white.png",
    "wool_colored_orange.png",
    "wool_colored_grey.png",
    "wool_colored_cyan.png",
    "wool_colored_purple.png"
]

# Use absolute path to config.json
script_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(script_dir, 'config.json')
with open(config_path, 'r') as file:
    data = json.load(file)
userId = data.get('userId', 'Not found')
api_key = data.get('api_key', 'Not found')
base_folder = data.get('base_folder', 'Not found')
output_path = data.get('output_path', 'Not found')
img_path = data.get('img_path', 'Not found')
texture_pack = data.get('texture_pack', 'Not found')

sky = ["cloud1.png"]  # Note: you can choose your own sky by going into assets/minecraft/mcpatcher/sky/world0

os.makedirs(base_folder, exist_ok=True)
os.makedirs(output_path, exist_ok=True)

if os.path.exists(os.path.join(base_folder, "wood_sword.png")):
    print("Skipping Extraction!")
else:
    result = extractZip(texture_pack, base_folder, swords, pickaxes, items, bow, blocks, sky)
    print("Run the script again!")
    print(result)

sky_path = os.path.join(base_folder, "cloud1.png")  # Sky image goes here
# AutoSky by @happypooky
def splitSky(sky_path):
    image = Image.open(sky_path)
    img_width, img_height = image.size
    tile_size = min(img_width // 3, img_height // 2)
    regions = {
        "sky_bottom": (0, 0, tile_size, tile_size),
        "sky_left": (img_width - tile_size, 0, img_width, tile_size),
        "sky_back": (0, img_height - tile_size, tile_size, img_height),
        "sky_front": (img_width - tile_size, img_height - tile_size, img_width, img_height),
        "sky_top": ((img_width - tile_size) // 2, 0, (img_width + tile_size) // 2, tile_size),
        "sky_right": ((img_width - tile_size) // 2, img_height - tile_size, (img_width + tile_size) // 2, img_height)
    }
    os.makedirs(base_folder, exist_ok=True)
    for name, box in regions.items():
        cropped_img = image.crop(box)
        cropped_img.save(os.path.join(base_folder, f"{name}.png"))
if os.path.exists(os.path.join(base_folder, "cloud1.png")):
    splitSky(sky_path)
else:
    print("Sky not trucked!")

def create(image_name):
    image_path = os.path.join(base_folder, f"{image_name}.png")
    if not os.path.exists(image_path):
        print(f"Image does not exist! ({image_name})")
        return None

    export_name = os.path.join(output_path, f"{image_name}.fbx")
    image = Image.open(image_path).convert("RGBA")
    pixels = image.load()
    width, height = image.size
    
    if width != height:
        print(f"Skipping {image_name}: Image must be square ({width}x{height})")
        return None
    
    original_resolution = width
    final_plane_size = 2.0
    pixel_size = final_plane_size / original_resolution
    
    if image.size in [(16, 16), (32, 32), (64, 64), (128, 128), (256, 256)]:
        resized = image.resize((512, 512), Image.Resampling.NEAREST)
        resize_path = os.path.join(base_folder, f"{image_name}_resized.png")
        resized.save(resize_path)
    else:
        resize_path = image_path
    
    # Clear all existing objects in the scene (removes default cube)
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

    # Create the pixel-based mesh
    mesh = bpy.data.meshes.new(image_name)
    obj = bpy.data.objects.new(image_name, mesh)
    bpy.context.collection.objects.link(obj)

    verts = []
    faces = []
    uvs = []
    x_offset = original_resolution / 2
    y_offset = original_resolution / 2

    for y in range(original_resolution):
        for x in range(original_resolution):
            pixel_x = x
            pixel_y = y
            r, g, b, a = pixels[pixel_x, pixel_y]
            if a > 0:
                z = 0
                v1 = ((x - x_offset) * pixel_size, (y_offset - y) * pixel_size, z)
                v2 = ((x + 1 - x_offset) * pixel_size, (y_offset - y) * pixel_size, z)
                v3 = ((x + 1 - x_offset) * pixel_size, (y_offset - (y + 1)) * pixel_size, z)
                v4 = ((x - x_offset) * pixel_size, (y_offset - (y + 1)) * pixel_size, z)
                verts.extend([v1, v2, v3, v4])
                face = [len(verts) - 4, len(verts) - 3, len(verts) - 2, len(verts) - 1]
                faces.append(face)
                uv1 = (x / original_resolution, (original_resolution - y) / original_resolution)
                uv2 = ((x + 1) / original_resolution, (original_resolution - y) / original_resolution)
                uv3 = ((x + 1) / original_resolution, (original_resolution - (y + 1)) / original_resolution)
                uv4 = (x / original_resolution, (original_resolution - (y + 1)) / original_resolution)
                uvs.extend([uv1, uv2, uv3, uv4])

    mesh.from_pydata(verts, [], faces)
    mesh.update()
    uv_layer = mesh.uv_layers.new(name="UVMap")
    for i, uv in enumerate(uvs):
        uv_layer.data[i].uv = uv

    solidify = obj.modifiers.new(name="Solidify", type="SOLIDIFY")
    solidify.thickness = 0.13
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

    valid_names = ["iron_ingot", "diamond", "ender_pearl", "emerald", "apple_golden"]
    if image_name in valid_names:
        obj.rotation_euler[0] = 90 * (3.14159265 / 180)
    else:
        obj.rotation_euler[0] = 90 * (3.14159265 / 180)
        obj.rotation_euler[1] = -45 * (3.14159265 / 180)

    mat = bpy.data.materials.new(name="PixelArtMaterial")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    for node in nodes:
        nodes.remove(node)
    output_node = nodes.new(type="ShaderNodeOutputMaterial")
    principled_node = nodes.new(type="ShaderNodeBsdfPrincipled")
    texture_node = nodes.new(type="ShaderNodeTexImage")
    output_node.location = (400, 0)
    principled_node.location = (200, 0)
    texture_node.location = (0, 0)
    links.new(texture_node.outputs["Color"], principled_node.inputs["Base Color"])
    links.new(principled_node.outputs["BSDF"], output_node.inputs["Surface"])
    image_texture = bpy.data.images.load(resize_path)
    texture_node.image = image_texture
    texture_node.interpolation = 'Closest'
    obj.data.materials.append(mat)

    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT')

    object = bpy.data.objects.get(image_name)
    for obj in bpy.data.objects:
        if obj.type == 'LIGHT':
            bpy.data.objects.remove(obj)
    if object:
        object.select_set(True)
        bpy.context.view_layer.objects.active = object
        bpy.ops.export_scene.fbx(filepath=export_name, global_scale=0.01)
        print(f"Object exported to {export_name}")
        
        # Get userId.measure from JSON data
        user_id = data.get('userId', '2741568527')  # Fallback to default if not found

        # Upload Mesh
        mesh_id = None
        texture_id = None
        if os.path.exists(fbx_path := export_name):
            headers = {
                'x-api-key': api_key,
            }
            files = {
                'request': (None, f'{{ \n  "assetType": "Mesh",  \n  "displayName": "Item", \n  "description": "This is a description", \n  "creationContext": {{ \n    "creator": {{ \n      "userId": "{user_id}" \n    }} \n  }} \n}}'),
                'fileContent': (fbx_path, open(fbx_path, 'rb'), 'model/fbx'),
            }
            try:
                r = requests.post("https://apis.roblox.com/assets/v1/assets", headers=headers, files=files)
                if r.status_code == 200:
                    json_data = r.json()
                    op = json_data.get("operationId")
                    if op:
                        while True:
                            op_r = requests.get('https://apis.roblox.com/assets/v1/operations/' + op, headers=headers)
                            if op_r.status_code == 200:
                                op_r_json = op_r.json()
                                if op_r_json.get("done") == True:
                                    mesh_id = op_r_json.get("response", {}).get("assetId")
                                    break
                            time.sleep(1)
            except requests.exceptions.RequestException:
                mesh_id = None

        # Upload Image
        if os.path.exists(image_path):
            headers = {
                'x-api-key': api_key,
            }
            files_decal = {
                'request': (None, f'{{ \n  "assetType": "Image",  \n  "displayName": "Item", \n  "description": "This is a description", \n  "creationContext": {{ \n    "creator": {{ \n      "userId": "{user_id}" \n    }} \n  }} \n}}'),
                'fileContent': (os.path.basename(resize_path), open(resize_path, 'rb'), 'image/png'),
            }
            try:
                img_r = requests.post("https://apis.roblox.com/assets/v1/assets", headers=headers, files=files_decal)
                if img_r.status_code == 200:
                    img_json = img_r.json()
                    op_img = img_json.get("operationId")
                    if op_img:
                        while True:
                            op_img_r = requests.get('https://apis.roblox.com/assets/v1/operations/' + op_img, headers=headers)
                            if op_img_r.status_code == 200:
                                op_img_json = op_img_r.json()
                                if op_img_json.get("done") == True:
                                    texture_id = op_img_json.get("response", {}).get("assetId")
                                    break
                            time.sleep(1)
            except requests.exceptions.RequestException:
                texture_id = None

        bpy.data.objects.remove(object)
        return {"mesh_id": int(mesh_id) if mesh_id else None, "texture_id": int(texture_id) if texture_id else None}
    
    return None

def resizeWool(img):
    image_path = os.path.join(base_folder, f"{img}.png")
    if os.path.exists(image_path):
        image = Image.open(image_path).convert("RGBA")
        resized = image.resize((512, 512), Image.Resampling.NEAREST)
        resized_path = os.path.join(base_folder, f"{img}_resized.png")
        resized.save(resized_path)
        return resized_path
    return None

def uploadSky(image_name):
    # Use the resized image if it exists, otherwise fall back to original
    resized_path = os.path.join(base_folder, f"{image_name}_resized.png")
    image_path = os.path.join(base_folder, f"{image_name}.png")
    upload_path = resized_path if os.path.exists(resized_path) else image_path
    
    if os.path.exists(upload_path):
        headers = {
            'x-api-key': api_key,
        }
        user_id = data.get('userId', '2741568527')  # Get userId from JSON
        files_decal = {
            'request': (None, f'{{ \n  "assetType": "Image",  \n  "displayName": "Item", \n  "description": "This is a description", \n  "creationContext": {{ \n    "creator": {{ \n      "userId": "{user_id}" \n    }} \n  }} \n}}'),
            'fileContent': (os.path.basename(upload_path), open(upload_path, 'rb'), 'image/png'),
        }
        try:
            img_r = requests.post("https://apis.roblox.com/assets/v1/assets", headers=headers, files=files_decal)
            if img_r.status_code == 200:
                img_json = img_r.json()
                op_img = img_json.get("operationId")
                if op_img:
                    while True:
                        op_img_r = requests.get('https://apis.roblox.com/assets/v1/operations/' + op_img, headers=headers)
                        if op_img_r.status_code == 200:
                            op_img_json = op_img_r.json()
                            if op_img_json.get("done") == True:
                                decalId = op_img_json.get("response", {}).get("assetId")
                                return int(decalId) if decalId else None
                        time.sleep(1)
        except requests.exceptions.RequestException:
            return None
    return None

WoodSwordMesh = StoneSwordMesh = IronSwordMesh = DiamondSwordMesh = \
WoodPickMesh = StonePickMesh = IronPickMesh = DiamondPickMesh = \
GoldenAppleMesh = EnderPearlMesh = EmeraldMesh = DiamondMesh = IronMesh = \
BowStandbyMesh = BowPulling0Mesh = BowPulling1Mesh = BowPulling2Mesh = \
WoodSwordTexture = StoneSwordTexture = IronSwordTexture = DiamondSwordTexture = \
WoodPickTexture = StonePickTexture = IronPickTexture = DiamondPickTexture = \
GoldenAppleTexture = EnderPearlTexture = EmeraldTexture = DiamondTexture = IronTexture = \
BowStandbyTexture = BowPulling0Texture = BowPulling1Texture = BowPulling2Texture = \
WoolColoredBlueTexture = WoolColoredRedTexture = WoolColoredGreenTexture = WoolColoredYellowTexture = WoolColoredWhiteTexture = \
SkyTop = SkyRight = SkyBack = SkyBottom = SkyLeft = SkyFront = \
WoolColoredOrangeTexture = WoolColoredGreyTexture = WoolColoredCyanTexture = WoolColoredPurpleTexture = None    

def create_objects():
    asset_mapping = {
        "wood_sword": {"texture": "WoodSwordTexture", "mesh": "WoodSwordMesh"},
        "stone_sword": {"texture": "StoneSwordTexture", "mesh": "StoneSwordMesh"},
        "iron_sword": {"texture": "IronSwordTexture", "mesh": "IronSwordMesh"},
        "diamond_sword": {"texture": "DiamondSwordTexture", "mesh": "DiamondSwordMesh"},
        "wood_pickaxe": {"texture": "WoodPickTexture", "mesh": "WoodPickMesh"},
        "stone_pickaxe": {"texture": "StonePickTexture", "mesh": "StonePickMesh"},
        "iron_pickaxe": {"texture": "IronPickTexture", "mesh": "IronPickMesh"},
        "diamond_pickaxe": {"texture": "DiamondPickTexture", "mesh": "DiamondPickMesh"},
        "apple_golden": {"texture": "GoldenAppleTexture", "mesh": "GoldenAppleMesh"},
        "emerald": {"texture": "EmeraldTexture", "mesh": "EmeraldMesh"},
        "diamond": {"texture": "DiamondTexture", "mesh": "DiamondMesh"},
        "iron_ingot": {"texture": "IronTexture", "mesh": "IronMesh"},
        "bow_standby": {"texture": "BowStandbyTexture", "mesh": "BowStandbyMesh"},
        "bow_pulling_0": {"texture": "BowPulling0Texture", "mesh": "BowPulling0Mesh"},
        "bow_pulling_1": {"texture": "BowPulling1Texture", "mesh": "BowPulling1Mesh"},
        "bow_pulling_2": {"texture": "BowPulling2Texture", "mesh": "BowPulling2Mesh"},
        "ender_pearl": {"texture": "EnderPearlTexture", "mesh": "EnderPearlMesh"},
        "wool_colored_blue": {"texture": "WoolColoredBlueTexture"},
        "wool_colored_red": {"texture": "WoolColoredRedTexture"},
        "wool_colored_green": {"texture": "WoolColoredGreenTexture"},
        "wool_colored_yellow": {"texture": "WoolColoredYellowTexture"},
        "wool_colored_white": {"texture": "WoolColoredWhiteTexture"},
        "sky_back": {"texture": "SkyBack"},
        "sky_bottom": {"texture": "SkyBottom"},
        "sky_front": {"texture": "SkyFront"},
        "sky_left": {"texture": "SkyLeft"},
        "sky_right": {"texture": "SkyRight"},
        "sky_top": {"texture": "SkyTop"},
        "wool_colored_orange": {"texture": "WoolColoredOrangeTexture"},
        "wool_colored_grey": {"texture": "WoolColoredGreyTexture"},
        "wool_colored_cyan": {"texture": "WoolColoredCyanTexture"},
        "wool_colored_purple": {"texture": "WoolColoredPurpleTexture"}
    }

    for asset_key, asset in asset_mapping.items():
        if asset_key.startswith("sky") and "texture" in asset:
            texture1 = uploadSky(asset_key)
            globals()[asset["texture"]] = texture1
        elif asset_key.startswith("wool") and "texture" in asset:
            resized_path = resizeWool(asset_key)
            if resized_path:
                texture1 = uploadSky(asset_key)
                globals()[asset["texture"]] = texture1
        else:
            result = create(asset_key)
            if result:
                if "mesh" in asset:
                    globals()[asset["mesh"]] = result["mesh_id"]
                if "texture" in asset:
                    globals()[asset["texture"]] = result["texture_id"]

create_objects()

Textures = {
    "DiamondSwordVPImage": DiamondSwordTexture,
    "Bow0Texture": BowStandbyTexture,
    "Bow1Texture": BowPulling0Texture,
    "DiamondPickaxeTexture": DiamondPickTexture,
    "WoodenSwordVPImage": WoodSwordTexture,
    "Bow2Texture": BowPulling1Texture,
    "GoldPickaxeTexture": IronPickTexture,
    "EmeraldTexture": EmeraldTexture,
    "Bow3Texture": BowPulling2Texture,
    "DefaultBowVPImage": BowStandbyTexture,
    "WoodenPickaxeTexture": WoodPickTexture,
    "IronTexture": IronTexture,
    "DiamondSwordTexture": DiamondSwordTexture,
    "GoldSwordVPImage": IronSwordTexture,
    "EmeraldVPImage": EmeraldTexture,
    "WoodenSwordTexture": WoodSwordTexture,
    "GoldAppleVPImage": GoldenAppleTexture,
    "DiamondTexture": DiamondTexture,
    "GoldPickaxeVPImage": IronPickTexture,
    "SwordTexture": StoneSwordTexture,
    "GoldAppleTexture": GoldenAppleTexture,
    "IronVPImage": IronTexture,
    "WoodenPickaxeVPImage": WoodPickTexture,
    "DiamondVPImage": DiamondTexture,
    "SwordVPImage": StoneSwordTexture,
    "GoldSwordTexture": IronSwordTexture,
    "PearlVPImage": EnderPearlTexture,
    "DiamondPickaxeVPImage": DiamondPickTexture,
    "PickaxeVPImage": StonePickTexture,
    "PickaxeTexture": StonePickTexture,
    "PearlTexture": EnderPearlTexture,
    "GoldAppleMesh": GoldenAppleMesh,
    "Bow3Mesh": BowPulling2Mesh,
    "PearlMesh": EnderPearlMesh,
    "EmeraldMesh": EmeraldMesh,
    "Bow1Mesh": BowPulling0Mesh,
    "Bow2Mesh": BowPulling1Mesh,
    "DiamondMesh": DiamondMesh,
    "IronMesh": IronMesh,
    "SwordMesh": IronSwordMesh,
    "Bow0Mesh": BowStandbyMesh,
    "PickaxeMesh": IronPickMesh,
    "ClayVPImage": 0,
    "ClayWhite": WoolColoredWhiteTexture,
    "ClayGreen": WoolColoredGreenTexture,
    "ClayBlue": WoolColoredBlueTexture,
    "ClayOrange": WoolColoredOrangeTexture,
    "ClayGrey": WoolColoredGreyTexture,
    "ClayCyan": WoolColoredCyanTexture,
    "ClayYellow": WoolColoredYellowTexture,
    "ClayPurple": WoolColoredPurpleTexture,
    "ClayRed": WoolColoredRedTexture,
    "SkyBack": SkyBack,
    "SkyRight": SkyRight,
    "SkyLeft": SkyLeft,
    "SkyBottom": SkyBottom,
    "SkyTop": SkyTop,
    "SkyFront": SkyFront
}
filter = {k: v for k, v in Textures.items() if v is not None}

str = json.dumps(filter, indent=4)
pyperclip.copy(str)
print("Thanks for using AutoPack. The pack is copied to your clipboard. Press CTRL + V to paste it")
