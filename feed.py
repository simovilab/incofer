import marimo

__generated_with = "0.23.6"
app = marimo.App()


@app.cell
def _(mo):
    mo.md(r"""
    # Revisión del _feed_ de INCOFER
    """)
    return


@app.cell
def _():
    import pandas as pd
    import geopandas as gpd
    from shapely.geometry import LineString

    return LineString, gpd, pd


@app.cell
def _(pd):
    agency = pd.read_csv('files/agency.txt')
    routes = pd.read_csv('files/routes.txt')
    trips = pd.read_csv('files/trips.txt')
    shapes = pd.read_csv('files/shapes.txt')
    return (shapes,)


@app.cell
def _(LineString, gpd, shapes):
    # Create a new GeoDataFrame for shapes, converting the shape points under the same shape_id
    geoshapes = (
        shapes.sort_values("shape_pt_sequence")
        .groupby("shape_id")
        .apply(lambda x: LineString(zip(x["shape_pt_lon"], x["shape_pt_lat"])))
        .rename("geometry")
        .reset_index()
    )

    geoshapes = gpd.GeoDataFrame(geoshapes, geometry="geometry")
    return (geoshapes,)


@app.cell
def _(geoshapes):
    geoshapes
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
