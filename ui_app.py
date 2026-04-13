from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


def _load_lab_ui_module():
    repo_root = Path(__file__).resolve().parent
    lab_ui_path = repo_root / "day08" / "lab" / "ui_app.py"

    if not lab_ui_path.exists():
        raise FileNotFoundError(f"Cannot find lab UI app at: {lab_ui_path}")

    # Ensure internal imports in day08/lab/ui_app.py resolve correctly.
    sys.path.insert(0, str(lab_ui_path.parent))

    spec = spec_from_file_location("lab_ui_app", lab_ui_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load day08/lab/ui_app.py")

    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


if __name__ == "__main__":
    _load_lab_ui_module().run()