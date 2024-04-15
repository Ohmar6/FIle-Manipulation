import os
import cv2
import numpy as np

def separate_masks(input_folder, output_folder_human, output_folder_background):
    # Create output folders if they don't exist
    os.makedirs(output_folder_human, exist_ok=True)
    os.makedirs(output_folder_background, exist_ok=True)

    # List all files in the input folder
    files = os.listdir(input_folder)

    for file in files:
        try:
            # Read mask image
            image_path = os.path.join(input_folder, file)
            mask = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

            if mask is None:
                print(f"Unable to read {file}. Skipping...")
                continue

            # Thresholding
            _, mask_binary = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)

            # Labeling
            num_labels, labels = cv2.connectedComponents(mask_binary)

            # Filtering
            min_size = 1000  # Adjust according to your requirement
            mask_filtered = np.zeros_like(mask_binary)

            for label in range(1, num_labels):
                mask_region = (labels == label).astype(np.uint8)
                if cv2.countNonZero(mask_region) > min_size:
                    mask_filtered += mask_region

            # Extract annotation type from image name
            annotation_type = file.split('_')[-1][:5]  # Extracts the '00000' or '00001' part
            if annotation_type == '00000':
                output_folder = output_folder_human
            elif annotation_type == '00001':
                output_folder = output_folder_background
            else:
                continue  # Skip if the annotation type is neither '00000' nor '00001'

            # Save separated mask
            cv2.imwrite(os.path.join(output_folder, file), mask_filtered)
        
        except Exception as e:
            print(f"Error processing {file}: {e}")

    print("Masks separated and saved successfully!")

# Specify input and output folders
input_folder = r"C:\Users\Nana\Downloads\Practical Test-20240410T195554Z-001\Practical Test\Task 2\mask-images\masks"
output_folder_human = r"C:\Users\Nana\Downloads\Practical Test-20240410T195554Z-001\Practical Test\Task 2\human_annotations"
output_folder_background = r"C:\Users\Nana\Downloads\Practical Test-20240410T195554Z-001\Practical Test\Task 2\background_annotations"

# Call the function to separate masks
separate_masks(input_folder, output_folder_human, output_folder_background)
