import os
from pathlib import Path

dir =os.path.join(os.getcwd(),'data','document_compare')

fold = Path(dir)
folders = [f for f in fold.iterdir() if f.is_dir()]

print(fold)
print(folders)