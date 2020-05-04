import os
import json

from trp import (
    __version__,
    BoundingBox,
    Document,
)

print(__file__)
blocks_json = os.path.join(os.path.dirname(__file__), "blocks.json")

def test_version():
    assert __version__ == '0.1.0'

def test_BoundingBox():
    width = 0.01
    height = 0.02
    left = 0.3
    top = 0.5

    bbox = BoundingBox(width, height, left, top)

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
    doc = Document(blocks)
    assert doc
