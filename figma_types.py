from pydantic import BaseModel, root_validator

class FigmaComponent(BaseModel):
    id: str
    absoluteBoundingBox: dict
    absoluteRenderBounds: dict

    @root_validator(pre=True)
    def set_absoluteRenderBounds_based_on_absoluteBoundingBox(cls, values):
        absoluteBoundingBox = values.get('absoluteBoundingBox')
        if absoluteBoundingBox:
            values['absoluteRenderBounds'] = absoluteBoundingBox
        return values

class GROUP(FigmaComponent):
    id: str
    name: str
    type: str = 'GROUP'
    scrollBehavior: str = 'SCROLLS'
    blendMode: str = 'NORMAL'
    children: list = []
    absoluteBoundingBox: dict
    absoluteRenderBounds: dict = {}
    preserveRatio: bool = True
    constraints: dict = {'vertical': 'BOTTOM', 'horizontal': 'LEFT'}
    clipsContent: bool = False
    background: list = []
    fills: list = []
    strokes: list = []
    strokeWeight: float = 0.0
    strokeAlign: str = 'CENTER'
    backgroundColor: dict = {'r': 1, 'g': 1, 'b': 1, 'a': 1}
    effects: list = []


class TEXT(FigmaComponent): 
    id: str
    name: str
    type: str = 'TEXT'
    scrollBehavior: str = 'SCROLLS'
    blendMode: str = 'NORMAL'
    absoluteBoundingBox: dict
    absoluteRenderBounds: dict = {}
    constraints: dict = {'vertical': 'BOTTOM', 'horizontal': 'LEFT'}
    layoutAlign: str = 'INHERIT'
    layoutGrow: int = 0
    layoutSizingHorizontal: str = 'FIXED'
    layoutSizingVertical: str = 'FIXED'
    fills: list = []
    strokes: list = []
    strokeWeight: int = 0
    strokeAlign: str = 'CENTER'
    styles: dict = {}
    effects: list = []
    characters: str = ''
    style: dict = {}
    characterStyleOverrides: list = []
    styleOverrideTable: dict = {}
    lineTypes: list = []
    lineIndentations: list = []

    @root_validator(pre=True)
    def set_characters_based_on_name(cls, values):
        name = values.get('name')
        if name:
            values['characters'] = name
        return values

class RECTANGLE(FigmaComponent): 
    id: str
    name: str
    type: str = 'RECTANGLE'
    scrollBehavior: str = 'SCROLLS'
    blendMode: str = 'NORMAL'
    absoluteBoundingBox: dict
    absoluteRenderBounds: dict = {}
    constraints: dict = {}
    fills: list = []
    strokes: list = []
    strokeWeight: int = 0
    strokeAlign: str = 'CENTER'
    effects: list = []
    cornerRadius: int = 0
    cornerSmoothing: int = 0

class COMPONENT(FigmaComponent):
        id: str
        name: str
        type: str = 'COMPONENT'
        scrollBehavior: str = 'SCROLLS'
        blendMode: str = 'PASS_THROUGH'
        children: list = []
        absoluteBoundingBox: dict
        absoluteRenderBounds: dict = {}
        constraints: dict = {}
        clipsContent: bool = False
        background: list = []
        fills: list = []
        strokes: list = []
        strokeWeight: int = 0
        strokeAlign: str = 'CENTER'
        backgroundColor: dict = {'r': 1, 'g': 1, 'b': 1, 'a': 1}
        styles: dict = {}
        effects: list = []

class TypeBuilder:
    mapping = {
        "COMPONENT": COMPONENT,
        "RECTANGLE": RECTANGLE,
        "TEXT": TEXT,
        "GROUP": GROUP,
    }

    def __init__(self):
        self.id = 0

    def build(self, figma_type, name, absoluteBoundingBox, children=[]) -> dict:
        figma = self.mapping[figma_type](id=str(self.id), name=str(name), absoluteBoundingBox=absoluteBoundingBox, children=children).dict()
        self.id += 1
        return  figma

