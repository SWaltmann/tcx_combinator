import os

if os.getenv('TCX_FILE_PATH'):
    directory_path = os.getenv('TCX_FILE_PATH')
else:
    directory_path = input("Full path of directory containing tcx files: ")

num_tcx_files = 0

for file in os.listdir(directory_path):
    if file.endswith(".tcx"):
        num_tcx_files += 1


print(f"Found {num_tcx_files} .tcx files in {directory_path}")