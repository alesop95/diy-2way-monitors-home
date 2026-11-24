#!/usr/bin/env python3
"""Collaudo FreeCAD: pannello parametrico di prova, FCStd, STEP e profilo DXF.

Eseguire con freecadcmd; DIY_CAD_TEST_DIR deve indicare una cartella nuova.
DIY_CAD_TEST_SCALE_STEP=2 produce un controllo negativo sulle unita STEP.
Non definisce il cabinet finale e non apre periferiche audio.
"""

import json
import math
import os
from pathlib import Path

import FreeCAD as App
import Part


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def near(value, expected, message, tolerance=1e-5):
    require(abs(value - expected) <= tolerance, f"{message}: {value} != {expected}")


output = Path(os.environ["DIY_CAD_TEST_DIR"])
output.mkdir(parents=True, exist_ok=False)
report = {"status": "running", "version": App.Version()[:3], "checks": []}


def solid_check(shape, expected_volume):
    require(not shape.isNull() and shape.isValid(), "Geometria non valida")
    require(len(shape.Solids) == 1, "Il risultato non e un solo solido")
    near(shape.Volume, expected_volume, "Volume mm3")


try:
    width, depth, thickness, radius = 240.0, 300.0, 18.0, 40.0
    volume = (width * depth - math.pi * radius**2) * thickness
    doc = App.newDocument("CollaudoPannello")
    blank = doc.addObject("Part::Box", "Blank")
    blank.Length, blank.Width, blank.Height = width, depth, thickness
    bore = doc.addObject("Part::Cylinder", "Bore")
    bore.Radius, bore.Height = radius, thickness
    bore.Placement.Base = App.Vector(width / 2, depth / 2, 0)
    panel = doc.addObject("Part::Cut", "WoodPanel")
    panel.Base, panel.Tool = blank, bore
    doc.recompute()
    solid_check(panel.Shape, volume)
    report["checks"].append("solido e volume analitico")

    blank.Length = width + 10
    doc.recompute()
    solid_check(panel.Shape, volume + 10 * depth * thickness)
    blank.Length = width
    doc.recompute()
    report["checks"].append("ricomputazione parametrica")

    native = output / "pannello-prova.FCStd"
    doc.saveAs(str(native))
    App.closeDocument(doc.Name)
    doc = App.openDocument(str(native))
    doc.recompute()
    panel = doc.getObject("WoodPanel")
    solid_check(panel.Shape, volume)
    near(doc.getObject("Blank").Length.Value, width, "Parametro riaperto")
    report["checks"].append("salvataggio e riapertura FCStd")

    scale_step = float(os.environ.get("DIY_CAD_TEST_SCALE_STEP", "1"))
    export_object = panel
    if scale_step != 1:
        export_object = doc.addObject("Part::Feature", "ErroreUnitaSimulato")
        wrong_shape = panel.Shape.copy()
        wrong_shape.scale(scale_step)
        export_object.Shape = wrong_shape
        doc.recompute()
    step = output / "pannello-prova.step"
    Part.export([export_object], str(step))
    restored = Part.read(str(step))
    solid_check(restored, volume)
    near(restored.BoundBox.XLength, width, "STEP larghezza mm")
    near(restored.BoundBox.YLength, depth, "STEP profondita mm")
    near(restored.BoundBox.ZLength, thickness, "STEP spessore mm")
    report["checks"].append("STEP reimportato: solido, volume e dimensioni")

    bottom = [edge for edge in panel.Shape.Edges
              if abs(edge.BoundBox.ZMin) < 1e-7 and abs(edge.BoundBox.ZMax) < 1e-7]
    require(len(bottom) == 5, "Profilo inferiore diverso da quattro lati e un foro")
    profile = doc.addObject("Part::Feature", "ProfiloTaglio")
    profile.Shape = Part.makeCompound(bottom)
    doc.recompute()
    import importDXF
    dxf = output / "profilo-prova.dxf"
    importDXF.export([profile], str(dxf))
    dxf_doc = App.newDocument("RiletturaDXF")
    importDXF.insert(str(dxf), dxf_doc.Name)
    dxf_doc.recompute()
    edges = [edge for obj in dxf_doc.Objects if hasattr(obj, "Shape")
             for edge in obj.Shape.Edges]
    require(len(edges) == 5, f"DXF reimportato: {len(edges)} spigoli anziche cinque")
    geometry = Part.makeCompound(edges)
    near(geometry.BoundBox.XLength, width, "DXF larghezza")
    near(geometry.BoundBox.YLength, depth, "DXF profondita")
    near(geometry.BoundBox.ZLength, 0, "DXF planarita")
    circles = [edge.Curve for edge in edges if isinstance(edge.Curve, Part.Circle)]
    require(len(circles) == 1, "DXF senza il solo foro atteso")
    near(circles[0].Radius, radius, "DXF raggio foro")
    near(circles[0].Center.x, width / 2, "DXF centro foro X")
    near(circles[0].Center.y, depth / 2, "DXF centro foro Y")
    report["checks"].append("DXF reimportato: lati, foro, dimensioni e planarita")
    report.update({"status": "success", "volume_mm3": volume,
                   "dimensioni_mm": [width, depth, thickness], "foro_raggio_mm": radius,
                   "dxf_unita_dichiarate": "coordinate in mm, da specificare al destinatario",
                   "artifacts": [native.name, step.name, dxf.name]})
except Exception as error:
    report.update({"status": "failed", "error": str(error)})
    raise
finally:
    (output / "esito.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for name in list(App.listDocuments()):
        App.closeDocument(name)
    print(json.dumps(report, ensure_ascii=False))
