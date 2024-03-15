#This script works as follows:
#   1. Iterate through all original ZIP files in the NMR server
#   2. Compare their metadata (file size) with the one collected in the last script execution
#   3. The original ZIP files which are new, or the ones with new metadata, are further processed.
#   4. For each original ZIP file to be processed, the contents are stored in a temporary working directory
#   5. For each different analysis within the contents, the sample name is retrieved.
#   6. Each analysis is copied into a new folder in a second temporary working directory, the name of the folder is taken from the sample name.
#   7. The new folders are zipped and saved in the final destination directory.
#   8. Temporary files are deleted, and the metadata of the processed ZIP file is stored.

import os
import shutil
import glob
import json
from zipfile import ZipFile

# Define source and destination directories
source_pattern = "/Volumes/chab_loc_nmr_s2-1/bode/*/*.zip" # nmr server address
tmp_extraction_dir = "/tmp/openbis/nmr/extracted" # temporary directory to extract zip files
tmp_destination_dir = "/tmp/openbis/nmr/dest" # temporary directory to prepare folders for compression
final_destination_dir = "/Volumes/chab_loc_bode_s1/Instruments/NMR/NMRtoOpenBIS"
metadata_filepath = "/Volumes/chab_loc_bode_s1/Instruments/NMR/NMRtoOpenBIS/metadata/NMR_metadata.json" # metadata of all previously retrieved nmr files

# Load existing metadata if available
metadata = {}
if os.path.exists(metadata_filepath):
    with open(metadata_filepath, "r") as f:
        metadata = json.load(f)
else:
    metadata = {}

# Find all ZIP files in the NMR server
original_zip_files = glob.glob(source_pattern)

# Loop through all ZIP files
for original_filepath in original_zip_files:
    if original_filepath.endswith(".zip"):
        original_filename = os.path.basename(original_filepath) + ".zip"

        # Get current original ZIP files metadata
        current_size = os.path.getsize(original_filepath)

        # Check if metadata has changed since last extraction
        if original_filename in metadata:
            previous_size = metadata[original_filename]["size"]

            if current_size == previous_size:
                continue

        # Extract the ZIP file (either a new one or modified one)        
        with ZipFile(original_filepath, "r") as zip_ref:
            zip_ref.extractall(tmp_extraction_dir)

        # Loop through extracted folders
        for folder in os.listdir(tmp_extraction_dir):
            if os.path.isdir(os.path.join(tmp_extraction_dir, folder)):
                folder_path = os.path.join(tmp_extraction_dir, folder)


                for subfolder in os.listdir(folder_path):
                    if os.path.isdir(os.path.join(folder_path, subfolder)):

                        subfolder_path = os.path.join(folder_path, subfolder)
                        # Try to read the title file and handle potential errors
                        try:
                            title_path = os.path.join(subfolder_path, "pdata", "1", "title")
                            with open(title_path, "r") as title_file:
                                lines = title_file.readlines() # Read all lines
                                first_line = lines[0].strip() # Extract first line (openBIS identifier)

                                # The following part uses a try-except block because files from AV 300MHz instrument don't have a 5th line in the title file, and this would prompt an error
                                
                                try:
                                    fifth_line = lines[4].strip() # Extracts the two first parts of fifth line (Additional information for Method and Solvent)
                                except IndexError:
                                    fifth_line = lines[3].strip()
                                fifth_line_parts = fifth_line.split(" ")[:2]
                            # Remove prefix "Sample " (including the space) from first line
                            if first_line.startswith("Sample "):
                                first_line = first_line[len("Sample "):]  # Slice after removing prefix

                            # Create new folder name
                            new_folder_name = "-".join([first_line, *fifth_line_parts])
                            new_folder_name_path = os.path.join(tmp_destination_dir, new_folder_name)
                            new_subfolder_path = os.path.join(new_folder_name_path, subfolder)
                            zip_filename = f"{new_folder_name}.zip"
                            zip_filepath = os.path.join(final_destination_dir, zip_filename)

                            # Ensure the ZIP file doesn't already exist
                            if not os.path.exists(zip_filepath): 
                                # Copy folder with new name
                                shutil.copytree(subfolder_path, new_subfolder_path)

                                # Create and close ZIP file with a descriptive name
                                with ZipFile(zip_filepath, "w") as zip_file:
                                    for root, _, files in os.walk(new_folder_name_path):
                                        for file in files:
                                            File_to_Compress_path = os.path.join(root, file)
                                            zip_file.write(File_to_Compress_path, os.path.relpath(File_to_Compress_path, tmp_destination_dir))

                                print(f"Folder '{new_folder_name}' copied and compressed to '{zip_filename}'.")

                                shutil.rmtree(new_folder_name_path)
                        except (FileNotFoundError, IndexError, PermissionError) as e:
                            print(f"Error processing folder '{subfolder_path}': {e}")
        
        # Update metadata with current values
        metadata[original_filename] = {"size": current_size}

        # Remove extracted folders
        print(f"Attempting to remove folder: {folder_path}")
        shutil.rmtree(folder_path)
        

#Save updated metadata to file
with open(metadata_filepath, "w") as f:
    json.dump(metadata, f, indent=4)




# Print success message
print("Processing complete!")
