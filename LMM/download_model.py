from huggingface_hub import snapshot_download
import os

print(os.getenv("HF_HOME"))

model_id = "allenai/Molmo-7B-D-0924"
snapshot_download(model_id)