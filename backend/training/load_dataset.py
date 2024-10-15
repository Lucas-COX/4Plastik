import kagglehub
import os

# Download latest version
path = kagglehub.dataset_download("nikhileswarkomati/suicide-watch")
print("Path to dataset files:", path)


new_path = "."
os.system(f"mv {path}/* {new_path}")
print("Moved dataset to :", new_path)
