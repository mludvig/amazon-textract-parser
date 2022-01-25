# Copyright 2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from .__version__ import __version__

import json

class BoundingBox:
    def __init__(self, width, height, left, top):
        self._width = width
        self._height = height
        self._left = left
        self._top = top

    def __str__(self):
        return "width: {}, height: {}, left: {}, top: {}".format(self._width, self._height, self._left, self._top)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def left(self):
        return self._left

    @property
    def right(self):
        return self._left + self._width

    @property
    def top(self):
        return self._top

    @property
    def bottom(self):
        return self._top + self._height

class Polygon:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def __str__(self):
        return "x: {}, y: {}".format(self._x, self._y)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

class Geometry:
    def __init__(self, geometry):
        boundingBox = geometry["BoundingBox"]
        polygon = geometry["Polygon"]
        bb = BoundingBox(boundingBox["Width"], boundingBox["Height"], boundingBox["Left"], boundingBox["Top"])
        pgs = []
        for pg in polygon:
            pgs.append(Polygon(pg["X"], pg["Y"]))

        self._boundingBox = bb
        self._polygon = pgs

    def __str__(self):
        s = "BoundingBox: {}\n".format(str(self._boundingBox))
        return s

    @property
    def boundingBox(self):
        return self._boundingBox

    @property
    def polygon(self):
        return self._polygon

class Word:
    def __init__(self, block, blockMap):
        self._block = block
        self._confidence = block['Confidence']
        self._geometry = Geometry(block['Geometry'])
        self._id = block['Id']
        self._text = ""
        if(block['Text']):
            self._text = block['Text']

    def __str__(self):
        return self._text

    @property
    def confidence(self):
        return self._confidence

    @property
    def geometry(self):
        return self._geometry

    @property
    def id(self):
        return self._id

    @property
    def text(self):
        return self._text

    @property
    def block(self):
        return self._block

class Line:
    def __init__(self, block, blockMap):

        self._block = block
        self._confidence = block['Confidence']
        self._geometry = Geometry(block['Geometry'])
        self._id = block['Id']

        self._text = ""
        if(block['Text']):
            self._text = block['Text']

        self._words = []
        if('Relationships' in block and block['Relationships']):
            for rs in block['Relationships']:
                if(rs['Type'] == 'CHILD'):
                    for cid in rs['Ids']:
                        if(blockMap[cid]["BlockType"] == "WORD"):
                            self._words.append(Word(blockMap[cid], blockMap))
    def __str__(self):
        s = "Line\n==========\n"
        s = s + self._text + "\n"
        s = s + "Words\n----------\n"
        for word in self._words:
            s = s + "[{}]".format(str(word))
        return s

    @property
    def confidence(self):
        return self._confidence

    @property
    def geometry(self):
        return self._geometry

    @property
    def id(self):
        return self._id

    @property
    def words(self):
        return self._words

    @property
    def text(self):
        return self._text

    @property
    def block(self):
        return self._block

class SelectionElement:
    def __init__(self, block, blockMap):
        self._confidence = block['Confidence']
        self._geometry = Geometry(block['Geometry'])
        self._id = block['Id']
        self._selectionStatus = block['SelectionStatus']

    @property
    def confidence(self):
        return self._confidence

    @property
    def geometry(self):
        return self._geometry

    @property
    def id(self):
        return self._id

    @property
    def selectionStatus(self):
        return self._selectionStatus

class FieldKey:
    def __init__(self, block, children, blockMap):
        self._block = block
        self._confidence = block['Confidence']
        self._geometry = Geometry(block['Geometry'])
        self._id = block['Id']
        self._text = ""
        self._content = []

        t = []

        for eid in children:
            wb = blockMap[eid]
            if(wb['BlockType'] == "WORD"):
                w = Word(wb, blockMap)
                self._content.append(w)
                t.append(w.text)

        if(t):
            self._text = ' '.join(t)

    def __str__(self):
        return self._text

    @property
    def confidence(self):
        return self._confidence

    @property
    def geometry(self):
        return self._geometry

    @property
    def id(self):
        return self._id

    @property
    def content(self):
        return self._content

    @property
    def text(self):
        return self._text

    @property
    def block(self):
        return self._block

class FieldValue:
    def __init__(self, block, children, blockMap):
        self._block = block
        self._confidence = block['Confidence']
        self._geometry = Geometry(block['Geometry'])
        self._id = block['Id']
        self._text = ""
        self._content = []

        t = []

        for eid in children:
            wb = blockMap[eid]
            if(wb['BlockType'] == "WORD"):
                w = Word(wb, blockMap)
                self._content.append(w)
                t.append(w.text)
            elif(wb['BlockType'] == "SELECTION_ELEMENT"):
                se = SelectionElement(wb, blockMap)
                self._content.append(se)
                self._text = se.selectionStatus

        if(t):
            self._text = ' '.join(t)

    def __str__(self):
        return self._text

    @property
    def confidence(self):
        return self._confidence

    @property
    def geometry(self):
        return self._geometry

    @property
    def id(self):
        return self._id

    @property
    def content(self):
        return self._content

    @property
    def text(self):
        return self._text
    
    @property
    def block(self):
        return self._block

class Field:
    def __init__(self, block, blockMap):
        self._key = None
        self._value = None

        for item in block['Relationships']:
            if(item["Type"] == "CHILD"):
                self._key = FieldKey(block, item['Ids'], blockMap)
            elif(item["Type"] == "VALUE"):
                for eid in item['Ids']:
                    vkvs = blockMap[eid]
                    if 'VALUE' in vkvs['EntityTypes']:
                        if 'Relationships' in vkvs and vkvs['Relationships']!= None:
                            for vitem in vkvs['Relationships']:
                                if(vitem["Type"] == "CHILD"):
                                    self._value = FieldValue(vkvs, vitem['Ids'], blockMap)
    def __str__(self):
        s = "\nField\n==========\n"
        k = ""
        v = ""
        if(self._key):
            k = str(self._key)
        if(self._value):
            v = str(self._value)
        s = s + "Key: {}\nValue: {}".format(k, v)
        return s

    @property
    def key(self):
        return self._key

    @property
    def value(self):
        return self._value

class Form:
    def __init__(self):
        self._fields = []
        self._fieldsMap = {}

    def addField(self, field):
        self._fields.append(field)
        self._fieldsMap[field.key.text] = field

    def __str__(self):
        s = ""
        for field in self._fields:
            s = s + str(field) + "\n"
        return s

    @property
    def fields(self):
        return self._fields

    def getFieldByKey(self, key):
        field = None
        if(key in self._fieldsMap):
            field = self._fieldsMap[key]
        return field
    
    def searchFieldsByKey(self, key):
        searchKey = key.lower()
        results = []
        for field in self._fields:
            if(field.key and searchKey in field.key.text.lower()):
                results.append(field)
        return results

class Cell:

    def __init__(self, block, blockMap):
        self._block = block
        self._confidence = block['Confidence']
        self._rowIndex = block['RowIndex']
        self._columnIndex = block['ColumnIndex']
        self._rowSpan = block['RowSpan']
        self._columnSpan = block['ColumnSpan']
        self._geometry = Geometry(block['Geometry'])
        self._id = block['Id']
        self._content = []
        self._text = ""
        if('Relationships' in block and block['Relationships']):
            for rs in block['Relationships']:
                if(rs['Type'] == 'CHILD'):
                    for cid in rs['Ids']:
                        blockType = blockMap[cid]["BlockType"]
                        if(blockType == "WORD"):
                            w = Word(blockMap[cid], blockMap)
                            self._content.append(w)
                            self._text = self._text + w.text + ' '
                        elif(blockType == "SELECTION_ELEMENT"):
                            se = SelectionElement(blockMap[cid], blockMap)
                            self._content.append(se)
                            self._text = self._text + se.selectionStatus + ', '

    def __str__(self):
        return self._text

    @property
    def confidence(self):
        return self._confidence

    @property
    def rowIndex(self):
        return self._rowIndex

    @property
    def columnIndex(self):
        return self._columnIndex

    @property
    def rowSpan(self):
        return self._rowSpan

    @property
    def columnSpan(self):
        return self._columnSpan

    @property
    def geometry(self):
        return self._geometry

    @property
    def id(self):
        return self._id

    @property
    def content(self):
        return self._content

    @property
    def text(self):
        return self._text

    @property
    def block(self):
        return self._block

class Row:
    def __init__(self):
        self._cells = []

    def __str__(self):
        s = ""
        for cell in self._cells:
            s = s + "[{}]".format(str(cell))
        return s

    @property
    def cells(self):
        return self._cells

class Table:

    def __init__(self, block, blockMap):

        self._block = block

        self._confidence = block['Confidence']
        self._geometry = Geometry(block['Geometry'])

        self._id = block['Id']
        self._rows = []

        ri = 1
        row = Row()
        cell = None
        if('Relationships' in block and block['Relationships']):
            for rs in block['Relationships']:
                if(rs['Type'] == 'CHILD'):
                    for cid in rs['Ids']:
                        cell = Cell(blockMap[cid], blockMap)
                        if(cell.rowIndex > ri):
                            self._rows.append(row)
                            row = Row()
                            ri = cell.rowIndex
                        row.cells.append(cell)
                    if(row and row.cells):
                        self._rows.append(row)

    def __str__(self):
        s = "Table\n==========\n"
        for row in self._rows:
            s = s + "Row\n==========\n"
            s = s + str(row) + "\n"
        return s

    @property
    def confidence(self):
        return self._confidence

    @property
    def geometry(self):
        return self._geometry

    @property
    def id(self):
        return self._id

    @property
    def rows(self):
        return self._rows

    @property
    def block(self):
        return self._block

class Page:

    def __init__(self, blocks, blockMap):
        self._blocks = blocks
        self._text = ""
        self._lines = []
        self._form = Form()
        self._tables = []
        self._content = []

        self._parse(blockMap)

    def __str__(self):
        s = "Page\n==========\n"
        for item in self._content:
            s = s + str(item) + "\n"
        return s

    def _parse(self, blockMap):
        for item in self._blocks:
            if item["BlockType"] == "PAGE":
                self._geometry = Geometry(item['Geometry'])
                self._id = item['Id']
            elif item["BlockType"] == "LINE":
                l = Line(item, blockMap)
                self._lines.append(l)
                self._content.append(l)
                self._text = self._text + l.text + '\n'
            elif item["BlockType"] == "TABLE":
                t = Table(item, blockMap)
                self._tables.append(t)
                self._content.append(t)
            elif item["BlockType"] == "KEY_VALUE_SET":
                if 'KEY' in item['EntityTypes']:
                    f = Field(item, blockMap)
                    if(f.key):
                        self._form.addField(f)
                        self._content.append(f)
                    else:
                        print("WARNING: Detected K/V where key does not have content. Excluding key from output.")
                        print(f)
                        print(item)

    def getLinesInReadingOrder(self):
        starting_point_tolerance = 0.01
        height_tolerance = 3
        same_line_top_tolerance = 0.001
        same_line_spacing_tolerance = 5
        columns = []
        lines = []
        for item in self._lines:
                column_found=False
                for index, column in enumerate(columns):
                    bbox_left = item.geometry.boundingBox.left
                    bbox_right = item.geometry.boundingBox.left + item.geometry.boundingBox.width
                    bbox_centre = item.geometry.boundingBox.left + item.geometry.boundingBox.width/2
                    bbox_top = item.geometry.boundingBox.top
                    bbox_height = item.geometry.boundingBox.height

                    # new logic:  
                    # if the starting point is within starting_point_tolerance (first_condition) and 
                    # the top location is within height_tolerance * bbox_height (second_condition), or
                    # the new line appeared to be broken by Textract mistake and should be of the same line 
                    # by looking at the top (third_condition) and 
                    # the left of the new line appears right next to the right of the last line (fourth_condition)
                    # then consider the new line as part of said column
                    first_condition = abs(bbox_left - column['left']) < starting_point_tolerance
                    second_condition = abs(bbox_top - column['top']) < height_tolerance * bbox_height
                    third_condition = abs(bbox_top - column['top']) < same_line_top_tolerance # appeared to be in the same line
                    fourth_condition = abs(bbox_left - column['right']) < same_line_spacing_tolerance * starting_point_tolerance
                    if (first_condition and second_condition) or (third_condition and fourth_condition):
                        #Bbox appears inside the column
                        lines.append([index, item.text])
                        # update the top and right with the new line added.
                        columns[index]['top'] = bbox_top
                        columns[index]['right'] = bbox_right
                        column_found=True
                        break
                if not column_found:
                    columns.append({'left':item.geometry.boundingBox.left, 
                                    'right':item.geometry.boundingBox.left + item.geometry.boundingBox.width,
                                    'top':item.geometry.boundingBox.top})
                    lines.append([len(columns)-1, item.text])

        lines.sort(key=lambda x: x[0])
        return lines

    def getTextInReadingOrder(self):
        lines = self.getLinesInReadingOrder()
        text = ""
        for line in lines:
            text = text + line[1] + '\n'
        return text

    def getLinesInBoundingBox(self, boundingBox):
        lines = []
        for line in self._lines:
            line_bbox = line.geometry.boundingBox
            if (line_bbox.left >= boundingBox.left and
                line_bbox.left <= boundingBox.right and
                line_bbox.top >= boundingBox.top and
                line_bbox.top <= boundingBox.bottom):
                    lines.append(line)
        return lines

    @property
    def blocks(self):
        return self._blocks

    @property
    def text(self):
        return self._text

    @property
    def lines(self):
        return self._lines

    @property
    def form(self):
        return self._form

    @property
    def tables(self):
        return self._tables

    @property
    def content(self):
        return self._content

    @property
    def geometry(self):
        return self._geometry

    @property
    def id(self):
        return self._id

class Document:

    def __init__(self, responsePages):

        if(not isinstance(responsePages, list)):
            rps = []
            rps.append(responsePages)
            responsePages = rps

        self._responsePages = responsePages
        self._pages = []

        self._parse()

    def __str__(self):
        s = "\nDocument\n==========\n"
        for p in self._pages:
            s = s + str(p) + "\n\n"
        return s

    def _parseDocumentPagesAndBlockMap(self):

        blockMap = {}

        documentPages = []
        documentPage = None
        for page in self._responsePages:
            for block in page['Blocks']:
                if('BlockType' in block and 'Id' in block):
                    blockMap[block['Id']] = block

                if(block['BlockType'] == 'PAGE'):
                    if(documentPage):
                        documentPages.append({"Blocks" : documentPage})
                    documentPage = []
                    documentPage.append(block)
                else:
                    documentPage.append(block)
        if(documentPage):
            documentPages.append({"Blocks" : documentPage})
        return documentPages, blockMap

    def _parse(self):

        self._responseDocumentPages, self._blockMap = self._parseDocumentPagesAndBlockMap()
        for documentPage in self._responseDocumentPages:
            page = Page(documentPage["Blocks"], self._blockMap)
            self._pages.append(page)

    @property
    def blocks(self):
        return self._responsePages

    @property
    def pageBlocks(self):
        return self._responseDocumentPages

    @property
    def pages(self):
        return self._pages

    def getBlockById(self, blockId):
        block = None
        if(self._blockMap and blockId in self._blockMap):
            block = self._blockMap[blockId]
        return block
