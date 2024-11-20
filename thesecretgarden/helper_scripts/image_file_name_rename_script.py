import os
import pandas as pd


def rename_images_from_excel(excel_file, media_root):
    """
    Renames images in media folders based on an Excel file mapping.

    :param excel_file: Path to the Excel file containing the mapping.
    :param media_root: Root directory where media files are stored.
    """
    # The excel file and all sheeds loaded as dict
    mappings = pd.read_excel(excel_file, sheet_name=None)

    for app_name, df in mappings.items():

        # App dir path
        app_dir = os.path.join(media_root, "images", app_name)

        if not os.path.exists(app_dir):
            print(f"Directory does not exist: {app_dir}")
            continue

        # Iterate through the rows of the DataFrame
        for _, row in df.iterrows():
            original_name = row['Original Name']
            new_name = row['New Name']

            # New paths
            original_path = os.path.join(app_dir, original_name)
            new_path = os.path.join(app_dir, new_name)

            if os.path.exists(original_path):
                os.rename(original_path, new_path)
                print(f"Renamed: {original_path} -> {new_path}")
            else:
                print(f"File not found: {original_path}")


if __name__ == "__main__":
    excel_file = "../image_mappings.xlsx"

    # Media root directory
    media_root = r"C:\Users\nalan\Desktop\Phyton\GitHub\The-Secret-Garden\thesecretgarden\mediafiles"

    rename_images_from_excel(excel_file, media_root)
