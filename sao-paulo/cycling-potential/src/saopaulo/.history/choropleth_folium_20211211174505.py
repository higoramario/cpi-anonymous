import bikescience.map_widgets as mpw
import saopaulo.cycling_infrastructure as cinfra
import folium

def plot_zones(fmap, geodf_zones, value_column, color):
    style_zones = lambda x: {'color': 'black', 'weight': 1, 'opacity': 0.3, 'fillOpacity': 0.1}
    folium.GeoJson(geodf_zones.loc[geodf_zones['NumeroMuni'] != 36],
                style_function = style_zones,
                name='Zonas', control=False).add_to(fmap)
    folium.Choropleth(
                geo_data=geodf_zones,
                data=geodf_zones,
                columns=['NumeroZona', value_column],
                key_on="feature.properties.NumeroZona",
                fill_color = color,
                fill_opacity = 1,
                line_opacity = 1,
                Highlight= True,
                line_color = "black",
                show=True,
                overlay=True,
                control=False,
                nan_fill_color = "Black"
                ).add_to(fmap)
    
def plot_zones_tooltip(fmap, geodf, fields, aliases):
    """
        Function to set the tooltip (text that appear when the cursor is over)
        Fields are the collumns of the geodf to be written
        Aliases and fields must be in the same order 
    """
    tooltip_zona=folium.features.GeoJsonTooltip(
                        fields, aliases)
    folium.GeoJson(geodf,
                   style_function = lambda x : {'opacity': 0, 'fillOpacity': 0},
                   name = 'Detalhes da zona', control = True,
                   tooltip = tooltip_zona).add_to(fmap)

def plot_choropleth(fmap, title, color, value_function, geodf_zones, 
                      tooltip_columns, tooltip_aliases):
    """
        Add a choropleth style element to fmap, calculating values for the geodf_zones.
        this geoDataFrame must be on the SaoPaulo zone DataFrames pattern,
        i.e., contain a column 'NumeroMuni' and the SaoPaulo number must be 36
    """
    geodf_zones['choropleth_value'] = geodf_zones.apply(value_function, axis=1)
    
    plot_zones(fmap, geodf_zones, 'choropleth_value', color)
    plot_zones_tooltip(fmap, geodf_zones, tooltip_columns, tooltip_aliases)
    
    fmap.get_root().html.add_child(folium.Element(mpw.build_title(title)))