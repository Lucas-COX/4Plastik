import kagglehub
import os

# Download latest version
path = kagglehub.dataset_download("nikhileswarkomati/suicide-watch")
print("Path to dataset files:", path)

new_path = os.path.join(os.path.dirname(__file__), "datasets/")
os.system(f"cp {path}/* {new_path}")
print("Moved dataset to :", new_path)
