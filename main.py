import bpy
import os
import sys
import argparse

# Add all subdirectories of the script directory to the system path so Blender can find the modules
def add_subdirs_to_sys_path(root_dir):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if os.path.basename(dirpath) == "__pycache__":
            continue
        sys.path.append(dirpath)

script_dir = os.path.dirname(os.path.abspath(__file__))
add_subdirs_to_sys_path(script_dir)

from config.config_loader import load_config
from _helpers.scene import setup_scene, clear_scene, snap_to_ground_plane, apply_all_transforms, scale_obj
from smpl.avatar import import_obj, join_as_shapes, animate_shape_key
from clothing.fit_garment import add_garment, set_cloth, bake_cloth, post_process
from _helpers.export import export_img, export_3D

# Load the config file
config = load_config()

# Disable the Blender splash screen
bpy.context.preferences.view.show_splash = False

# Parse command line arguments
# parser = argparse.ArgumentParser()
# parser.add_argument("--obj", type=str, required=True, help="Path to the .obj file")
# parser.add_argument("--garment", type=str, required=True, help="Path to the .blend file of the garment")
# parser.add_argument("--output", type=str, required=True, help="Path to the output directory")
# args = parser.parse_args()

# obj_filepath = args.obj
# garment_filepath = args.garment
# output_dir = args.output

# if not os.path.exists(obj_filepath):
#     raise FileNotFoundError(f"File {obj_filepath} not found.")
# if not os.path.exists(garment_filepath):
#     raise FileNotFoundError(f"File {garment_filepath} not found.")

# Setup scene
clear_scene()
setup_scene()

# Create avatar and animate to generated obj
avatar = import_obj(r"D:\Projects\VirtualFit_blender\smpl\base_mesh\male.obj")
scale_obj(avatar, 10)
snap_to_ground_plane(avatar)
apply_all_transforms(avatar)
generated_obj = import_obj(r"D:\Projects\VirtualFit_blender\test\000.obj")
scale_obj(generated_obj, 10)
snap_to_ground_plane(generated_obj)
apply_all_transforms(generated_obj)

shape_key_name = "Generated_Pose"
join_as_shapes(avatar, generated_obj, shape_key_name)
animate_shape_key(avatar, 0, 50, shape_key_name)

# Add garment and simulate cloth
garment = add_garment(r"D:\Projects\VirtualFit_blender\test\M_T-Shirt.blend", "M_T-Shirt")
set_cloth(garment, "T-Shirt")
bake_cloth(0, 80)
post_process(garment, -0.1, 2)

# # Export
# export_img(output_dir, config["export"]["img_format"] ,config["export"]["img_type"], transparent_bg=True)
# export_3D(output_dir, config["export"]["3D_format"],config["export"]["3D_type"])