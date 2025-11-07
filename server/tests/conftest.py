import os
import sys
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning, module="PyPDF2")

# Append the project root directory to sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)
