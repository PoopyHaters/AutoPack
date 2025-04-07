
import bpy, os, shutil, zipfile, time, requests, pyperclip, json #type:ignore
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

            os.chdir(target_dir)  # Change directory to the target folder

            if swords:
                os.makedirs(copy_to, exist_ok=True)
                for image in swords:
                    if os.path.exists(image):
                        shutil.copy(os.path.join(target_dir, image), os.path.join(copy_to, image))
            if pickaxes:
                os.makedirs(copy_to, exist_ok=True)
                for image in pickaxes:
                    if os.path.exists(image):
                        shutil.copy(os.path.join(target_dir, image), os.path.join(copy_to, image))
            if items:
                os.makedirs(copy_to, exist_ok=True)
                for image in items:
                    if os.path.exists(image):
                        shutil.copy(os.path.join(target_dir, image), os.path.join(copy_to, image))
            if bow:
                os.makedirs(copy_to, exist_ok=True)
                for image in bow:
                    if os.path.exists(image):
                        shutil.copy(os.path.join(target_dir, image), os.path.join(copy_to, image))
            if blocks:
                os.makedirs(copy_to, exist_ok=True)
                for image in blocks:
                    if os.path.exists(image):
                        shutil.copy(os.path.join(block_dir, image), os.path.join(copy_to, image))
            if sky:
                os.makedirs(copy_to, exist_ok=True)
                for image in sky:
                    if os.path.exists(image):
                        shutil.copy(os.path.join(sky_dir, image), os.path.join(copy_to, image))

swords = ["wood_sword.png", "stone_sword.png", "iron_sword.png", "diamond_sword.png"]
pickaxes = ["wood_pickaxe.png", "stone_pickaxe.png", "iron_pickaxe.png", "diamond_pickaxe.png"]
items = ["apple_golden.png", "ender_pearl.png", "emerald.png", "diamond.png", "iron_ingot.png"]
bow = ["bow_standby.png", "bow_pulling_0.png", "bow_pulling_1.png", "bow_pulling_2.png"]
blocks = ["wool_colored_blue.png", "wool_colored_red.png", "wool_colored_green.png", "wool_colored_yellow.png", "wool_colored_white.png"]
sky = ["cloud1.png"] # Note: you can choose your own sky by going into assets/minecraft/mcpatcher/sky/world0
# Set the base folder where your images are stored (or will be).
base_folder = r""
# Set the output path in which the OBJ's will be exported in.
output_path = r""
# Set the path which will output the extracted images.
img_path = r""
# Set the .zip file's path that you need to extract (leave it null if you don't want to extract).
texture_pack = r""
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

    # Get image dimensions
    img_width, img_height = image.size

    # Sets each tile size
    tile_size = min(img_width // 3, img_height // 2)

    # Define specific regions to extract
    regions = {
        "sky_bottom": (0, 0, tile_size, tile_size),
        "sky_left": (img_width - tile_size, 0, img_width, tile_size),
        "sky_back": (0, img_height - tile_size, tile_size, img_height),
        "sky_front": (img_width - tile_size, img_height - tile_size, img_width, img_height),
        "sky_top": ((img_width - tile_size) // 2, 0, (img_width + tile_size) // 2, tile_size),
        "sky_right": ((img_width - tile_size) // 2, img_height - tile_size, (img_width + tile_size) // 2, img_height)
    }

    # Output
    os.makedirs(base_folder, exist_ok=True)

    # Save Images
    for name, box in regions.items():
        cropped_img = image.crop(box)
        cropped_img.save(os.path.join(base_folder, f"{name}.png"))
if os.path.exists(os.path.join(base_folder, "cloud1.png")):
    splitSky(sky_path)
else:
    print("Sky not found!")
# Paste your API Key in this variable
api_key = ""
def create(image_name):
    if os.path.exists(os.path.join(base_folder, f"{image_name}.png")):
        # Replace with your image name (no extension)
        export_name = os.path.join(output_path, f"{image_name}.fbx")
        # Dynamically construct the full image path with extension
        image_path = os.path.join(base_folder, f"{image_name}.png")
        # Load image
        image = Image.open(image_path).convert("RGBA")  # Ensure RGBA mode
        pixels = image.load()
        width, height = image.size
        # Define the original resolution and target plane size
        original_resolution = image.width
        final_plane_size = 2.0
        pixel_size = final_plane_size / original_resolution
        if image.size in [(16, 16), (32, 32), (64, 64), (128, 128), (256, 256)]:
            resized = image.resize((512, 512), Image.Resampling.NEAREST)
            resize_path = os.path.join(base_folder, f"{image_name}_resized.png")
            resized.save(resize_path)
        # Ensure the resolution matches
        assert width == height, "Image must be square"
        scale_factor = width / original_resolution  # Scale for upscaled images
        mesh = bpy.data.meshes.new(image_name)
        obj = bpy.data.objects.new(image_name, mesh)
        bpy.context.collection.objects.link(obj)

        verts = []
        faces = []
        uvs = []

        # Offset to center the object on the origin
        x_offset = original_resolution / 2
        y_offset = original_resolution / 2

        # Generate vertices, faces, and UVs for each pixel
        for y in range(original_resolution):
            for x in range(original_resolution):
                # Get the corresponding pixel in the upscaled image
                pixel_x = int(x * scale_factor)
                pixel_y = int(y * scale_factor)
                r, g, b, a = pixels[pixel_x, pixel_y]  # Ensure we unpack RGBA

                if a > 0:  # Ignore transparent pixels
                    z = 0  # Flat plane for each pixel

                    # Add vertices for the current pixel
                    v1 = ((x - x_offset) * pixel_size, (y_offset - y) * pixel_size, z)  # Flip y-axis
                    v2 = ((x + 1 - x_offset) * pixel_size, (y_offset - y) * pixel_size, z)
                    v3 = ((x + 1 - x_offset) * pixel_size, (y_offset - (y + 1)) * pixel_size, z)
                    v4 = ((x - x_offset) * pixel_size, (y_offset - (y + 1)) * pixel_size, z)

                    verts.extend([v1, v2, v3, v4])

                    # Add a face for the pixel
                    face = [len(verts) - 4, len(verts) - 3, len(verts) - 2, len(verts) - 1]
                    faces.append(face)

                    # Add UV coordinates for the pixel
                    uv1 = (x / original_resolution, (original_resolution - y) / original_resolution)
                    uv2 = ((x + 1) / original_resolution, (original_resolution - y) / original_resolution)
                    uv3 = ((x + 1) / original_resolution, (original_resolution - (y + 1)) / original_resolution)
                    uv4 = (x / original_resolution, (original_resolution - (y + 1)) / original_resolution)

                    uvs.extend([uv1, uv2, uv3, uv4])

        # Create mesh from vertices and faces
        mesh.from_pydata(verts, [], faces)
        mesh.update()

        # Assign UV map
        uv_layer = mesh.uv_layers.new(name="UVMap")
        for i, uv in enumerate(uvs):
            uv_layer.data[i].uv = uv

        # Add solidify modifier
        solidify = obj.modifiers.new(name="Solidify", type="SOLIDIFY")
        solidify.thickness = 0.13

        # Center the object at the origin
        bpy.context.view_layer.objects.active = obj

        # Set the origin to geometry
        bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='BOUNDS')

        # Apply transformations to ensure correct orientation
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)

        # Rotate object: X 90°, Y -45°
        valid_names = ["iron_ingot", "diamond", "ender_pearl", "emerald", "apple_golden"]
        if image_name in valid_names:
                obj.rotation_euler[0] = 90 * (3.14159265 / 180)  # Convert degrees to radians
        else:
                obj.rotation_euler[0] = 90 * (3.14159265 / 180)  # Convert degrees to radians
                obj.rotation_euler[1] = -45 * (3.14159265 / 180)

        # Create material and assign the texture
        mat = bpy.data.materials.new(name="PixelArtMaterial")
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        links = mat.node_tree.links

        # Clear default nodes
        for node in nodes:
            nodes.remove(node)

        # Add nodes
        output_node = nodes.new(type="ShaderNodeOutputMaterial")
        principled_node = nodes.new(type="ShaderNodeBsdfPrincipled")
        texture_node = nodes.new(type="ShaderNodeTexImage")

        # Set up nodes
        output_node.location = (400, 0)
        principled_node.location = (200, 0)
        texture_node.location = (0, 0)

        links.new(texture_node.outputs["Color"], principled_node.inputs["Base Color"])
        links.new(principled_node.outputs["BSDF"], output_node.inputs["Surface"])

        # Load texture and set to material
        image_texture = bpy.data.images.load(resize_path)
        texture_node.image = image_texture

        # Disable interpolation for crisp pixel art
        texture_node.interpolation = 'Closest'

        # Assign material to the object
        obj.data.materials.append(mat)

        # Recalculate normals to ensure correct shading
        bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.object.mode_set(mode='OBJECT')
        # Auto-Export code
        object = bpy.data.objects.get(image_name)
        if object:
            object.select_set(True)
            bpy.context.view_layer.objects.active = object
            bpy.ops.export_scene.fbx(filepath=export_name, global_scale=0.01)
            print(f"Object exported to {output_path}")
            bpy.data.objects.remove(object)
    else:
        print(f"Image does not exist! ({image_name})")
        return None

def uploadMesh(image_name):
    fbx_path = os.path.join(output_path, f"{image_name}.fbx")
    if os.path.exists(fbx_path):
        headers = {
            'x-api-key': api_key,
        }
        files = {
            'request': (None, '{ \n  "assetType": "Mesh",  \n  "displayName": "Item", \n  "description": "This is a description", \n  "creationContext": { \n    "creator": { \n      "userId": "" \n    } \n  } \n}'),
            'fileContent': (fbx_path, open(fbx_path, 'rb'), 'model/fbx'),
        }
        r = requests.post("https://apis.roblox.com/assets/v1/assets", headers=headers, files=files)
        json = r.json()
        print(json)
        op = json["operationId"]
        print(op)
        while True:
            op_r = requests.get('https://apis.roblox.com/assets/v1/operations/' + op, headers=headers)
            op_r_code = op_r.status_code
            op_r_json = op_r.json()
            print(op_r_json)
            if op_r_code == 200 and op_r_json.get("done") == True:
                break
        print(op_r_json)
        decalId = op_r_json["response"]["assetId"]
        return decalId
    else:
        print(f".fbx not found! ({image_name})")
        return None

def resizeWool(img):
    image_path = os.path.join(base_folder, f"{img}.png")
    if os.path.exists(image_path):
        image = Image.open(image_path).convert("RGBA")
        resized = image.resize((512, 512), Image.Resampling.NEAREST)
        resized_path = os.path.join(base_folder, f"{img}_resized.png")
        resized.save(resized_path)
        print("Wool Resized!")

def uploadImage(image_name):
    image_path = os.path.join(base_folder, f"{image_name}_resized.png")
    if os.path.exists(image_path):
        headers = {
            'x-api-key': api_key,
        }
        files_decal = {
            'request': (None, '{ \n  "assetType": "Image",  \n  "displayName": "Item", \n  "description": "This is a description", \n  "creationContext": { \n    "creator": { \n      "userId": "" \n    } \n  } \n}'),
            'fileContent': (image_path, open(image_path, 'rb'), 'image/png'),
        }
        img_r = requests.post("https://apis.roblox.com/assets/v1/assets", headers=headers, files=files_decal)
        img_json = img_r.json()
        print(img_json)
        op_img = img_json["operationId"]
        print(op_img)
        while True:
            op_img = requests.get('https://apis.roblox.com/assets/v1/operations/' + op_img, headers=headers)
            op_img_code = op_img.status_code
            op_img_json = op_img.json()
            print(op_img_json)
            if op_img_code == 200 and op_img_json.get("done") == True:
                break
        print(op_img_json)
        decalId = op_img_json["response"]["assetId"]
        return decalId
    else:
        print(f"Image does not exist! ({image_name})")
        return None

def uploadSky(image_name):
    image_path = os.path.join(base_folder, f"{image_name}.png")
    if os.path.exists(image_path):
        headers = {
            'x-api-key': api_key,
        }
        files_decal = {
            'request': (None, '{ \n  "assetType": "Image",  \n  "displayName": "Item", \n  "description": "This is a description", \n  "creationContext": { \n    "creator": { \n      "userId": "2741568527" \n    } \n  } \n}'),
            'fileContent': (image_path, open(image_path, 'rb'), 'image/png'),
        }
        img_r = requests.post("https://apis.roblox.com/assets/v1/assets", headers=headers, files=files_decal)
        img_json = img_r.json()
        print(img_json)
        op_img = img_json["operationId"]
        print(op_img)
        while True:
            op_img = requests.get('https://apis.roblox.com/assets/v1/operations/' + op_img, headers=headers)
            op_img_code = op_img.status_code
            op_img_json = op_img.json()
            print(op_img_json)
            if op_img_code == 200 and op_img_json.get("done") == True:
                break
        print(op_img_json)
        decalId = op_img_json["response"]["assetId"]
        return decalId
    else:
        print(f"Sky does not exist! ({image_name})")
        return None

WoodSwordMesh = StoneSwordMesh = IronSwordMesh = DiamondSwordMesh = \
WoodPickMesh = StonePickMesh = IronPickMesh = DiamondPickMesh = \
GoldenAppleMesh = EnderPearlMesh = EmeraldMesh = DiamondMesh = IronMesh = \
BowStandbyMesh = BowPulling0Mesh = BowPulling1Mesh = BowPulling2Mesh = \
WoodSwordTexture = StoneSwordTexture = IronSwordTexture = DiamondSwordTexture = \
WoodPickTexture = StonePickTexture = IronPickTexture = DiamondPickTexture = \
GoldenAppleTexture = EnderPearlTexture = EmeraldTexture = DiamondTexture = IronTexture = \
BowStandbyTexture = BowPulling0Texture = BowPulling1Texture = BowPulling2Texture = \
WoolColoredBlueMesh = WoolColoredRedMesh = WoolColoredGreenMesh = WoolColoredYellowMesh = WoolColoredWhiteMesh = \
SkyTop = SkyRight = SkyBack = SkyBottom = SkyLeft = SkyFront = None

# Create the objects from the image names
def create_objects():
    asset_mapping = {"wood_sword":{"texture":"WoodSwordTexture","mesh":"WoodSwordMesh"},"stone_sword":{"texture":"StoneSwordTexture","mesh":"StoneSwordMesh"},"iron_sword":{"texture":"IronSwordTexture","mesh":"IronSwordMesh"},"diamond_sword":{"texture":"DiamondSwordTexture","mesh":"DiamondSwordMesh"},"wood_pickaxe":{"texture":"WoodPickTexture","mesh":"WoodPickMesh"},"stone_pickaxe":{"texture":"StonePickTexture","mesh":"StonePickMesh"},"iron_pickaxe":{"texture":"IronPickTexture","mesh":"IronPickMesh"},"diamond_pickaxe":{"texture":"DiamondPickTexture","mesh":"DiamondMesh"},"apple_golden":{"texture":"GoldenAppleTexture","mesh":"GoldenAppleMesh"},"emerald":{"texture":"EmeraldTexture","mesh":"EmeraldMesh"},"diamond":{"texture":"DiamondTexture","mesh":"DiamondMesh"},"iron_ingot":{"texture":"IronTexture","mesh":"IronMesh"},"bow_standby":{"texture":"BowStandbyTexture","mesh":"BowStandbyMesh"},"bow_pulling_0":{"texture":"BowPulling0Texture","mesh":"BowPulling0Mesh"},"bow_pulling_1":{"texture":"BowPulling1Texture","mesh":"BowPulling1Mesh"},"bow_pulling_2":{"texture":"BowPulling2Texture","mesh":"BowPulling2Mesh"},"ender_pearl":{"texture":"EnderPearlTexture","mesh":"EnderPearlMesh"},"wool_colored_blue":{"texture":"WoolColoredBlueMesh"},"wool_colored_red":{"texture":"WoolColoredRedMesh"},"wool_colored_green":{"texture":"WoolColoredGreenMesh"},"wool_colored_yellow":{"texture":"WoolColoredYellowMesh"},"wool_colored_white":{"texture":"WoolColoredWhiteMesh"},"sky_back":{"texture":"SkyBack"},"sky_bottom":{"texture":"SkyBottom"},"sky_front":{"texture":"SkyFront"},"sky_left":{"texture":"SkyLeft"},"sky_right":{"texture":"SkyRight"},"sky_top":{"texture":"SkyTop"}}

    for asset_key, asset in asset_mapping.items():
        if asset_key.startswith("sky") and "texture" in asset:
            print(f"Uploading Sky ({asset_key})!")
            texture1 = uploadSky(asset_key)
            globals()[asset["texture"]] = int(texture1) if texture1 is not None else texture1
        elif asset_key.startswith("wool") and "texture" in asset:
            print(f"Uploading Wool ({asset_key})!")
            resizeWool(asset_key)
            texture1 = uploadImage(asset_key)
            globals()[asset["texture"]] = int(texture1) if texture1 is not None else texture1
        else:
            if "mesh" in asset:
                print(f"Uploading Mesh ({asset_key})!")
                create(asset_key)
                mesh1 = uploadMesh(asset_key)
                globals()[asset["mesh"]] = int(mesh1) if mesh1 is not None else mesh1
            if "texture" in asset:
                print(f"Uploading Image/Texture ({asset_key})!")
                texture1 = uploadImage(asset_key)
                globals()[asset["texture"]] = int(texture1) if texture1 is not None else texture1
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
    "ClayBlue": WoolColoredBlueMesh,
    "ClayRed": WoolColoredRedMesh,
    "ClayGreen": WoolColoredGreenMesh,
    "ClayYellow": WoolColoredYellowMesh,
    "ClayWhite": WoolColoredWhiteMesh,
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

print("Your pack is done! Make sure to credit us (you can use extra small text we just want credit thats all.")