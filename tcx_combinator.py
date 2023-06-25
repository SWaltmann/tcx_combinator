import os
import shutil

if os.getenv('TCX_FILE_PATH'):
    directory_path = os.getenv('TCX_FILE_PATH')
else:
    directory_path = input("Full path of directory containing tcx files: ")

OUTPUT_PATH = os.path.join(directory_path, "OUTPUT.tcx")

num_tcx_files = 0

# Loop through all files 
for file in os.listdir(directory_path):
    if file.endswith(".tcx"):
        # The first file will be fully copied in the output
        if not os.path.exists(OUTPUT_PATH):
            shutil.copy2(file, OUTPUT_PATH)
        # Only the activity part of the other files are copied in the output
        else:
            with open(OUTPUT_PATH, 'a') as output_file, open(file, 'r') as input_file:
                reached_begin_activity = False
                for line in input_file:
                    if "<Activities>" in line:
                        reached_begin_activity = True
                        continue  # Start copying from the next line

                    if "</Activities>" in line:
                        break  # End of activities - move to next file

                    if reached_begin_activity:
                        print(line) 


        num_tcx_files += 1


print(f"Found {num_tcx_files} .tcx files in {directory_path}")