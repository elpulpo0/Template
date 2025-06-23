import os
import subprocess
import re

def test_requirements_completeness():
    temp_file = "temp_requirements.txt"
    subprocess.run([
        "pipreqs", ".", "--force", "--savepath", temp_file, "--ignore", "tests,.venv"
    ], check=True)

    def load_requirements(path):
        with open(path, "r") as f:
            return set(
                re.split(r"[=<>~!]", line.strip())[0]
                for line in f
                if line.strip() and not line.startswith("#")
            )

    try:
        detected = load_requirements(temp_file)
        declared = load_requirements("requirements.txt")

        ignored = {"python_bcrypt", "setuptools"}

        missing = detected - declared - ignored

        assert not missing, f"❌ Les dépendances suivantes sont utilisées dans le code mais absentes de requirements.txt : {missing}"

    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)
