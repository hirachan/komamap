from typing import List
import os

import folium

from .track import Point, Track


MapType = [
    'openstreetmap',
    'cartodbpositron',
    'cartodbpositronnolabels',
    'cartodbpositrononlylabels',
    'mapboxbright',
    'mapboxcontrolroom',
    'openstreetmap',
    'stamenterrain',
    'stamentoner',
    'stamentonerbackground',
    'stamentonerlabels',
    'stamenwatercolor',
]

api_key = os.environ["GOOGLEMAP_API_KEY"]

folium.folium._default_js.append(
    ("googlemap",
     f"https://maps.googleapis.com/maps/api/js?key={api_key}"))

folium.folium._default_js.append(
    ("googleleaflet",
     "https://unpkg.com/leaflet.gridlayer.googlemutant@latest/Leaflet.GoogleMutant.js"))


def get_point_by_distance(points: Track, distance: float, offset: int = 0) -> Point:
    _distance = points[offset].distance
    for i in range(offset + 1, len(points)):
        if points[i].distance - _distance >= distance:
            return points[i]

    return points[-1]


class Map:
    def __init__(self, points: Track, map_type: str):
        print(map_type)
        latitude = points[0].latitude
        longitude = points[0].longitude
        # self.map = folium.Map(location=[latitude, longitude], zoom_start=16, tiles=map_type)
        self.map = folium.Map(location=[latitude, longitude], zoom_start=18, tiles=None)

        folium.PolyLine(
            [(_.latitude, _.longitude) for _ in points],
            color="#0000ff",
            opacity=0.8,
            weight=4
        ).add_to(self.map)

    @property
    def map_id(self):
        return self.map.to_dict()["id"]

    def add_arrow(self, points: Track, cue_points: List[Point]):
        for cue_point in cue_points:

            # get point 50m far from here. I hope this is after turning corner.
            point = cue_point.get_point_by_distance(50)

            folium.RegularPolygonMarker(
                location=(point.prev.latitude, point.prev.longitude),
                fill=True,
                fill_rule="nonzero",
                fill_opacity=1.0,
                color='#0000ff',
                number_of_sides=3,
                radius=15,
                rotation=point.direction - 90
            ).add_to(self.map)

    def save(self, filename: str):
        self.map.save(filename)
        with open(filename, "a") as fw:
            fw.write("""<script>
var Gmap = L.gridLayer.googleMutant({
    maxZoom: 24,
    type:'roadmap'
});

map_%s.addLayer(Gmap);
</script>
""" % (self.map_id))
