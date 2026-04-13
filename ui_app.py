from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


def _load_lab_ui_module():
    repo_root = Path(__file__).resolve().parent
    lab_ui_path = repo_root / "day08" / "lab" / "ui_app.py"

    if not lab_ui_path.exists():
        raise FileNotFoundError(f"Cannot find lab UI app at: {lab_ui_path}")

    spec = spec_from_file_location("lab_ui_app", lab_ui_path)
    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load day08/lab/ui_app.py")

    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


if __name__ == "__main__":
    _load_lab_ui_module().run()