import json
import os

notebook_path = "day-4a-agent-observability.ipynb"
env_path = "/home/m1txel/Escritorio/GenAI/exercise_Day2b/.env" # User specified .env path

# Read the notebook content
with open(notebook_path, "r") as f:
    notebook_content = json.load(f)

# The new code to insert
new_code = """
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path='{}')

try:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY not found in .env file")
    os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
    print("✅ Setup and authentication complete.")
except Exception as e:
    print(
        f"🔑 Authentication Error: Please make sure you have 'GOOGLE_API_KEY' set in your .env file. Details: {{e}}"
    )
"""

# Find the cell to modify
for cell in notebook_content["cells"]:
    if cell["cell_type"] == "code":
        source_code = "".join(cell["source"])
        if "from kaggle_secrets import UserSecretsClient" in source_code:
            cell["source"] = new_code.format(env_path).splitlines(keepends=True)
            print("Modified the cell successfully.")
            break

# Write the modified notebook content back
with open(notebook_path, "w") as f:
    json.dump(notebook_content, f, indent=4)

print(f"Notebook '{notebook_path}' updated.")