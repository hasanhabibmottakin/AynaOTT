import pyzipper
import os
import sys

ZIP_PATH = "app.zip"
OUT_DIR = "."

pwd = os.environ.get("ZIP_PWD")
if not pwd:
    print("")
    sys.exit(2)

if not os.path.exists(ZIP_PATH):
    print("")
    sys.exit(3)

try:
    with pyzipper.AESZipFile(ZIP_PATH, 'r') as zf:
        zf.setpassword(pwd.encode())
        zf.extractall(path=OUT_DIR)
    print("")
except RuntimeError as e:
    print("Extraction failed:", e)
    sys.exit(4)
except Exception as e:
    print("Extraction error:", e)
    sys.exit(5)