from typing import List

import folium

from .track import Point, Track


def get_point_by_distance(points: Track, distance: float, offset: int = 0) -> Point:
    _distance = points[offset].distance
    for i in range(offset + 1, len(points)):
        if points[i].distance - _distance >= distance:
            return points[i]

    return points[-1]


class Map:
    def __init__(self, points: Track):
        latitude = points[0].latitude
        longitude = points[0].longitude
        self.map = folium.Map(location=[latitude, longitude], zoom_start=16)

        folium.TileLayer('openstreetmap').add_to(self.map)
        # folium.TileLayer('cartodbpositron').add_to(self.map)
        # folium.TileLayer('cartodbpositronnolabels').add_to(self.map)
        # folium.TileLayer('cartodbpositrononlylabels').add_to(self.map)
        # folium.TileLayer('mapboxbright').add_to(self.map)
        # folium.TileLayer('mapboxcontrolroom').add_to(self.map)
        # folium.TileLayer('openstreetmap').add_to(self.map)
        # folium.TileLayer('stamenterrain').add_to(self.map)
        # folium.TileLayer('stamentoner').add_to(self.map)
        # folium.TileLayer('stamentonerbackground').add_to(self.map)
        # folium.TileLayer('stamentonerlabels').add_to(self.map)
        # folium.TileLayer('stamenwatercolor').add_to(self.map)

        # folium.LayerControl().add_to(self.map)
        folium.PolyLine(
            [(_.latitude, _.longitude) for _ in points],
            color="#0000ff",
            opacity=0.8,
            weight=2
        ).add_to(self.map)

    @property
    def map_id(self):
        return self.map.to_dict()["id"]

    def add_arrow(self, points: Track, cue_points: List[int]):
        for cue_point in cue_points:

            # get point 35m far from here
            point = get_point_by_distance(points, 35, cue_point)

            folium.RegularPolygonMarker(
                location=(point.prev.latitude, point.prev.longitude),
                fill=True,
                fill_rule="nonzero",
                fill_opacity=1.0,
                color='#0000ff',
                number_of_sides=3,
                radius=10,
                rotation=point.direction - 90
            ).add_to(self.map)

    def save(self, filename: str):
        self.map.save(filename)
