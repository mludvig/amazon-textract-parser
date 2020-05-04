import os
import json
import toml

import trp

_our_dir = os.path.dirname(__file__)
blocks_json = os.path.join(_our_dir, "blocks.json")
pyproject_toml = os.path.join(_our_dir, "..", "pyproject.toml")

def test_version():
    with open(pyproject_toml, "rt") as f:
        pyproject = toml.load(f)
    assert pyproject['tool']['poetry']['version'] == trp.__version__

def test_BoundingBox():
    width = 0.01
    height = 0.02
    left = 0.3
    top = 0.5

    bbox = trp.BoundingBox(width, height, left, top)

    assert bbox.top == top
    assert bbox.bottom == top + height
    assert bbox.height == height
    assert bbox.left == left
    assert bbox.right == left + width
    assert bbox.width == width
    assert str(bbox) == f"width: {width}, height: {height}, left: {left}, top: {top}"

def test_Document():
    with open(blocks_json, "rt") as f:
        blocks = json.load(f)
    doc = trp.Document(blocks)
    assert doc
