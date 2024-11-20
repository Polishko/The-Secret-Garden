import os
import pandas as pd


def process_images_for_app(image_dir, app_name, writer):
    """
    Processes images in the given directory and adds a sheet with mapping in the provided Excel writer.
    :param image_dir: Directory containing images for the app.
    :param app_name: Name of the app (sheet name in Excel).
    :param writer: Excel writer object.
    """

    if not os.path.exists(image_dir):
        print(f'{image_dir} directory does not exist, skipped.')
        return

    image_files = [f for f in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, f))]
    new_names = [f'{app_name}_image_{i + 1}.jpg' for i in range(len(image_files))]

    data = [{'Original Name': original_name, 'New Name': new_name} for original_name, new_name in zip(image_files, new_names)]

    df = pd.DataFrame(data)
    df.to_excel(writer, sheet_name=app_name, index=False)

if __name__ == '__main__':
    app_directories = {
        'flowers': r'C:\Users\nalan\Desktop\Phyton\GitHub\The-Secret-Garden\thesecretgarden\mediafiles\images\flowers',
        'gifts': r'C:\Users\nalan\Desktop\Phyton\GitHub\The-Secret-Garden\thesecretgarden\mediafiles\images\gifts',
        'event': r'C:\Users\nalan\Desktop\Phyton\GitHub\The-Secret-Garden\thesecretgarden\mediafiles\images\events'
    }

    output_excel_file = '../image_mappings.xlsx'

    with pd.ExcelWriter(output_excel_file, engine="openpyxl") as writer:
        for app_name, image_directory in app_directories.items():
            process_images_for_app(image_directory, app_name, writer)

    print(f"Excel file created at: {os.path.abspath('image_mapping.xlsx')}")
