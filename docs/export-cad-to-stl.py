from pathlib import Path
import sys

import FreeCAD as App
import Import
import Mesh


source = Path(sys.argv[-2])
output = Path(sys.argv[-1])
if source.suffix.lower() in {'.step', '.stp'}:
    Import.open(str(source))
    document = App.ActiveDocument
else:
    document = App.openDocument(str(source))

candidates = [
    obj for obj in document.Objects
    if hasattr(obj, 'Shape') and not obj.Shape.isNull()
]
if not candidates:
    raise RuntimeError(f'No exportable shapes found in {source}')

# The largest solid is a safer headless approximation of the final visible
# result than the last feature, which may be an empty helper or construction.
result = max(candidates, key=lambda obj: obj.Shape.Volume)
output.parent.mkdir(parents=True, exist_ok=True)
Mesh.export([result], str(output))
App.closeDocument(document.Name)
