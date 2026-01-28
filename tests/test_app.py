from dash import dcc, html
from app import app


def find_component(component_type, layout):
    """Recursively search layout for a component type"""
    found = []
    if isinstance(layout, component_type):
        found.append(layout)
    elif hasattr(layout, "children") and layout.children is not None:
        if isinstance(layout.children, list):
            for child in layout.children:
                found.extend(find_component(component_type, child))
        else:
            found.extend(find_component(component_type, layout.children))
    return found


def test_header_present():
    headers = find_component(html.H1, app.layout)
    assert len(headers) > 0


def test_visualisation_present():
    graphs = find_component(dcc.Graph, app.layout)
    assert len(graphs) > 0


def test_region_picker_present():
    radios = find_component(dcc.RadioItems, app.layout)
    assert len(radios) > 0


#Run command 
#pytest