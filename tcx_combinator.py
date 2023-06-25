import os
import shutil

if os.getenv('TCX_FILE_PATH'):
    directory_path = os.getenv('TCX_FILE_PATH')
else:
    directory_path = input("Full path of directory containing tcx files: ")

OUTPUT_PATH = os.path.join(directory_path, "OUTPUT.tcx")

num_tcx_files = 0

this_is_the_first_file = True

footer = []

# Loop through all files 
for file in os.listdir(directory_path):
    # Consider only .tcx files
    if file.endswith(".tcx"):

        # For the first file copy the 'header' as well as the <activity>
        if this_is_the_first_file:
            print("Dealing with the first file...")
            with open(OUTPUT_PATH, 'w') as output_file, open(file, 'r') as input_file:
                reached_end_activities = False
                for line in input_file:
                    if "</Activities>" in line:
                        reached_end_activities = True

                    if not reached_end_activities:
                        output_file.write(line)
                    else:
                        footer.append(line)
                
                this_is_the_first_file = False
                continue  # Do not append the first file twice

        # Only the <activity> part of the other files are appended in the output
        with open(OUTPUT_PATH, 'a') as output_file, open(file, 'r') as input_file:
            print("Next file...")
            reached_begin_activity = False
            for line in input_file:
                if "<Activities>" in line:
                    reached_begin_activity = True
                    continue  # Start copying from the next line

                if "</Activities>" in line:
                    break  # End of activities - move to next file

                if reached_begin_activity:
                    output_file.write(line)


        num_tcx_files += 1

# Once all <activities> have been copied, append the 'footer' (ie everything that comes after the <activities>)
with open(OUTPUT_PATH, 'a') as output_file:
    for line in footer:
        output_file.write(line)

print(f"Found {num_tcx_files} .tcx files in {directory_path}")