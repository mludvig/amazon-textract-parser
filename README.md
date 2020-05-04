# Amazon Textract Results Parser - `textract-trp`

Amazon *Textract Results Parser* or `trp` module packaged and improved for ease of use.

## TL;DR

```
pip install textract-trp
```

Requires Python 3.6 or newer.

## Usage

```python
import boto3
import trp

textract_client = boto3.client('textract')
results = textract_client.analyze_document(... your file and other params ...)
doc = trp.Document(results)
```

Now you can examine `doc.pages`. For example print all the detected on the page:

```python
print(doc.pages[0].text)
```

Or print out the detected tables in CSV format:

```python
for row in doc.pages[0].tables[0].rows:
    for cell in row.cells:
        print(cell.text.strip(), end=",")
    print()
```

Or retrieve text from a given position on the page. For that we have to create
*Bounding Box* with the required coordinates relative to the page.

```python
# Coordinates are from top-left corner [0,0] to bottom-right [1,1]
bbox = trp.BoundingBox(width=0.220, height=0.085, left=0.734, top=0.140)
lines = doc.pages[0].getLinesInBoundingBox(bbox)

# Print only the lines contained in the Bounding Box
for line in lines:
    print(line.text)
```

Refer to the [Textract blog post](https://aws.amazon.com/blogs/machine-learning/automatically-extract-text-and-structured-data-from-documents-with-amazon-textract/)
and to [amazon-textract-code-samples](https://github.com/aws-samples/amazon-textract-code-samples) GitHub repository for more details.

## Background

The [Amazon blog post about Textract](https://aws.amazon.com/blogs/machine-learning/automatically-extract-text-and-structured-data-from-documents-with-amazon-textract/)
refers to a python module `trp.py` which used to be quite hard to find. There
are many posts on the internet from people looking for the module, often confused by
the *"other trp module"* that's got nothing to do with Textract.

Hence I decided to package and publish the `trp.py` module from the
[aws-samples/amazon-textract-code-samples](https://github.com/aws-samples/amazon-textract-code-samples)
repository. Fortunately its [MIT
license](https://github.com/aws-samples/amazon-textract-code-samples/blob/master/LICENSE)
permits that.

Over time I have made some improvements to the module for ease of use.

### Maintainer

[Michael Ludvig](https://aws.nz)
