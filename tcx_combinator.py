import os
import shutil

if os.getenv('TCX_FILE_PATH'):
    directory_path = os.getenv('TCX_FILE_PATH')
else:
    directory_path = input("Full path of directory containing tcx files: ")

num_tcx_files = 0 

this_is_the_first_file = True

output_file_number = 1  # If we need multiple files, then this will be the number appended to the output file name

MAX_FILE_SZE = 24800000  # Max file size, leaving some margin for the footer

current_output_path = os.path.join(directory_path, f"OUTPUT_{output_file_number}.tcx")


def add_footer(file, footer):
    # Once all <activities> have been copied, append the 'footer' (ie everything that comes after the <activities>)
    with open(file, 'a') as output_file:
        for line in footer:
            output_file.write(line)


# Loop through all files 
for file in os.listdir(directory_path):
    file = os.path.join(directory_path, file)

    # Consider only .tcx files
    if file.endswith(".tcx"):
        num_tcx_files += 1

        try:
            # Only append if we will not surpass 25MB
            if os.path.getsize(current_output_path) + os.path.getsize(file) > MAX_FILE_SZE:
                add_footer(current_output_path, footer)
                this_is_the_first_file = True
                output_file_number += 1
                current_output_path = os.path.join(directory_path, f"OUTPUT_{output_file_number}.tcx")

        except OSError:
            pass  # Assume the file does not exist, so it wil definitely not be too small:)


        # For the first file copy the 'header' as well as the <activity>
        if this_is_the_first_file:
            print("Dealing with the first file...")
            footer = []  # Make sure it is empty so we do not repeat the footer
            with open(current_output_path, 'w') as output_file, open(file, 'r') as input_file:
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
        with open(current_output_path, 'a') as output_file, open(file, 'r') as input_file:
            
            reached_begin_activity = False
            for line in input_file:
                if "<Activities>" in line:
                    reached_begin_activity = True
                    continue  # Start copying from the next line

                if "</Activities>" in line:
                    break  # End of activities - move to next file

                if reached_begin_activity:
                    output_file.write(line)

        print(print(num_tcx_files))


# Add footer to last file
add_footer(current_output_path, footer)


print(f"Found {num_tcx_files} .tcx files in {directory_path}")