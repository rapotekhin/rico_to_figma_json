import json
import argparse
from copy import deepcopy

from figma_types import TypeBuilder

type_builder = TypeBuilder()

TYPES_MAPPING = {
    "Text Button": 'RECTANGLE',
    "List Item": 'GROUP',
    "Video": 'GROUP',
    "Background Image": 'GROUP',
    "Button Bar": 'GROUP',
    "Web View": 'GROUP',
    "Advertisement": 'GROUP',
    "Toolbar": 'GROUP',
    "Number Stepper": 'GROUP',
    "Map View": 'GROUP',
    "Image": 'GROUP',
    "Slider": 'GROUP',
    "Radio Button": 'RECTANGLE',
    "Pager Indicator": 'RECTANGLE',
    "Drawer": 'RECTANGLE',
    "Icon": 'RECTANGLE',
    "Input": 'GROUP',
    "Date Picker": 'GROUP',
    "Bottom Navigation": 'RECTANGLE',
    "Checkbox": 'GROUP',
    "Text": 'TEXT',
    "On/Off Switch": 'GROUP',
    "Card": 'GROUP',
    "Modal": 'GROUP',
    "Multi-Tab": 'GROUP',
}
FIGMA_JSON_PLACEHOLDER = {
    "document": {
        "id": "0:0",
        "name": "Document",
        "type": "DOCUMENT",
        "scrollBehavior": "SCROLLS",
        "children": [
            {
                "id": "33:444",
                "name": "Screens",
                "type": "CANVAS",
                "scrollBehavior": "SCROLLS",
                "children": [],
                "backgroundColor": {"r": 1, "g": 1, "b": 1, "a": 1},
                "prototypeStartNodeID": None,
                "flowStartingPoints": [],
                "prototypeDevice": {"type": "NONE", "rotation": "NONE"},
            }
        ],
    },
    "components": {
        # "id": None,
        # "key": None,
        # "name": None,
        # "description": "",
        # "remote": False,
        # "documentationLinks": [],
    },
    "componentSets": [],
    "schemaVersion": 0,
    "styles": {},  # {"id": None, "key": None, "name": None, "styleType": None, "remote": False, "description": ""}
    "name": "Delivery App_UI Kit (Community)",
    "lastModified": "2023-10-19T19:10:37Z",
    "thumbnailUrl": "https://",
    "version": "4374935974",
    "role": "owner",
    "editorType": "figma",
    "linkAccess": "view",
}


def run_for_children(obj):
    name = ""
    absoluteBoundingBox = {}

    if isinstance(obj, dict):
        if "componentLabel" in obj:
            figma_type = TYPES_MAPPING.get(obj["componentLabel"], 'RECTANGLE')
            name = obj["componentLabel"]
        else:
            figma_type = "COMPONENT"
            name = 'COMPONENT'

        if "text" in obj:
            name = obj["text"]

        if "bounds" in obj:
            absoluteBoundingBox = {
                "x": obj["bounds"][0],
                "y": obj["bounds"][1],
                "width": abs(obj["bounds"][0] - obj["bounds"][2]),
                "height": abs(obj["bounds"][1] - obj["bounds"][3]),
            }

        children = []
        if "children" in obj:
            for child in obj["children"]:
                children.append(run_for_children(child))

        figma_component = type_builder.build(
            figma_type=figma_type,
            name=name,
            absoluteBoundingBox=absoluteBoundingBox,
            children=children,
        )

    return figma_component


def convert(args):
    with open(args.rico_json_path) as f:
        rico_json = json.load(f)

    figma_json = deepcopy(FIGMA_JSON_PLACEHOLDER)

    figma_json["document"]["children"][0]["children"].append(run_for_children(rico_json))
    return figma_json


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Json converter")
    parser.add_argument("--rico_json_path", type=str)
    parser.add_argument("--figma_json_out_path", type=str)
    args = parser.parse_args()
    figma_json = convert(args)

    with open(args.figma_json_out_path, 'w') as f:
        json.dump(figma_json, f, indent=4)
