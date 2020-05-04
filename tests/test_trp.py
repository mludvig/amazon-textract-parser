from trp import (
    __version__,
    BoundingBox,
)

def test_version():
    assert __version__ == '0.1.0'

def text_BoundingBox():
    bbox = BoundingBox(0.01, 0.02, 0.3, 0.4)
    assert bbox.width == 0.01
    assert bbox.height == 0.02
    assert bbox.left == 0.3
    assert bbox.top == 0.4
    assert bbox.bottom == 0.41
    assert bbox.right == 0.32
