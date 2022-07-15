# __init__.py


from pathlib import Path


__all__ = [file.stem for file in Path().iterdir()]
