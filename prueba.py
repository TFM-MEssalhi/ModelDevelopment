from transformers.utils import cached_path
from pathlib import Path
import os

# Ruta donde se almacenan los modelos por defecto
default_cache_path = Path.home() / ".cache" / "huggingface" / "transformers"

# Listar los modelos descargados
for root, dirs, files in os.walk(default_cache_path):
    for dir in dirs:
        print(os.path.join(root, dir))
