from ipyleaflet import Map, GeoData, basemaps, LayersControl, LegendControl, DrawControl
import geopandas as gpd
import leafmap
import numpy as np
import pandas as pd
from shapely.geometry import shape


def maak_interactieve_kaart(pad):
    """Creates an interactive map for selecting polygons from a shapefile."""
    
    # Load shapefile
    dijksecties = gpd.read_file(pad).to_crs(epsg=4326)

    # Create map
    m = Map(
        center=(52.6, 6.0),
        zoom=8,
        scroll_wheel_zoom=True,
    )

    # Add base layer
    geo_data = GeoData(
        geo_dataframe=dijksecties,
        style={
            'color': 'red',
            'fillColor': 'black',
            'fillOpacity': 0.1,
            'weight': 2
        },
        name='Dijksecties'
    )
    m.add_layer(geo_data)
    m.add(LayersControl())

    # Add DrawControl
    draw_control = DrawControl(
        rectangle={"shapeOptions": {"color": "#0000FF", "weight": 2, "fillOpacity": 0.1}},
        circlemarker={}, circle={}, polyline={}, polygon={}
    )
    m.add(draw_control)

    # Define holder for selected polygons
    selected = {"gdf": gpd.GeoDataFrame()}

    def handle_draw(target, action, geo_json):
        drawn_geom = shape(geo_json["geometry"])

        # Find polygons intersecting the new rectangle
        new_selection = dijksecties[dijksecties.intersects(drawn_geom)]

        # Append to existing selection (avoid duplicates)
        selected["gdf"] = pd.concat([selected["gdf"], new_selection]).drop_duplicates(subset=dijksecties.columns.difference(['geometry']).tolist()).reset_index(drop=True)

        print(f"✅ {len(selected['gdf'])} polygons selected (cumulative)")

        # Remove previous highlight layers to avoid clutter
        for layer in list(m.layers):
            if hasattr(layer, "name") and layer.name == 'Selected polygons':
                m.remove_layer(layer)

        # Highlight current cumulative selection
        highlight_layer = GeoData(
            geo_dataframe=selected["gdf"],
            style={
                'color': 'yellow',
                'fillColor': 'black',
                'fillOpacity': 0.1,
                'weight': 3
            },
            name='Selected polygons'
        )
        m.add_layer(highlight_layer)

    # Attach callback
    draw_control.on_draw(handle_draw)

    # Return both the map and the selected polygons container
    return m, selected