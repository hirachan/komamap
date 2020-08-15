from typing import Tuple, List, Optional
from dataclasses import dataclass
import math
import os
import time

import folium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
import gpxpy
import geopy.distance
import requests


@dataclass
class Point:
    latitude: float
    longitude: float
    altitude: float = 0.0
    distance: float = 0.0
    direction: float = 0.0
    before: Optional["Point"] = None


@dataclass
class WayPoint:
    latitude: float
    longitude: float
    description: str
    rotate: float = 0


def get_direction(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    x1, y1 = math.radians(p1[1]), math.radians(p1[0])
    x2, y2 = math.radians(p2[1]), math.radians(p2[0])
    dx = x2 - x1

    rot = math.degrees(
        math.atan2(
            math.sin(dx),
            math.cos(y1) * math.tan(y2) - math.sin(y1) * math.cos(dx))
    )

    if rot < 0:
        rot += 360

    return rot


def get_track_from_gpx(filename: str) -> List[Point]:
    gpx_file = open(filename, 'r')
    gpx = gpxpy.parse(gpx_file)

    points: List[Point] = []

    prev_pt: Optional[Point] = None
    distance = 0.0
    direction = 0.0
    prev_point = None
    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                if prev_pt:
                    # I think distance_2d() in gpxpy is closer to rwgps distance
                    # distance += geopy.distance.distance(
                    #     geopy.Point(prev_pt.latitude, prev_pt.longitude),
                    #     geopy.Point(point.latitude, point.longitude)).m
                    distance += point.distance_2d(prev_point)
                    # distance += point.distance_3d(prev_point)

                    direction = get_direction((prev_pt.latitude, prev_pt.longitude), (point.latitude, point.longitude))

                pt = Point(point.latitude, point.longitude, point.elevation, distance, direction, prev_pt)

                points.append(pt)
                prev_pt = pt
                prev_point = point

    return points


def read_waypoint(filename: str) -> List[WayPoint]:
    gpx_file = open(filename, 'r')
    gpx = gpxpy.parse(gpx_file)

    wpts: List[WayPoint] = []
    for wpt in gpx.waypoints:

        wpts.append(WayPoint(
            wpt.latitude,
            wpt.longitude,
            wpt.name))

    return wpts


def read_route(filename: str) -> List[WayPoint]:
    gpx_file = open(filename, 'r')
    gpx = gpxpy.parse(gpx_file)

    wpts: List[WayPoint] = []
    for route in gpx.routes:
        for point in route.points:
            wpts.append(WayPoint(
                point.latitude,
                point.longitude,
                point.comment))

    return wpts


def get_point_by_distance(points: List[Point], distance: float, offset: int = 0) -> Point:
    _distance = points[offset].distance
    for i in range(offset + 1, len(points)):
        if points[i].distance - _distance >= distance:
            return points[i]

    return points[-1]


def get_points_near_waypoint(points: List[Point], wpts: List[WayPoint]):
    cue_points = []
    n = 0
    wpt = wpts[0]
    for point_no, point in enumerate(points):
        dist = geopy.distance.distance(geopy.Point(wpt.latitude, wpt.longitude), geopy.Point(point.latitude, point.longitude)).m

        if dist <= 10:
            cue_points.append(point_no)
            n += 1
            if n >= len(wpts):
                break

            wpt = wpts[n]

    return cue_points


def download_rwgps(filename: str, route_id: str, format: str, privacy_code: Optional[str] = None):
    url = f"https://ridewithgps.com/routes/{route_id}.gpx?sub_format={format}"

    if privacy_code:
        url += f"&privacy_code={privacy_code}"

    res = requests.get(url)
    with open(filename, "wb") as fw:
        fw.write(res.content)


def komamap(gpx: str, route: str):
    points = get_track_from_gpx(gpx)
    map = make_map(points)

    if route:
        wpts = read_route(route)
    else:
        wpts = read_waypoint(gpx)

    cue_points = get_points_near_waypoint(points, wpts)

    add_arrow(map, points, cue_points)
    map.save("map.html")

    chrome = Chrome("map.html", map.to_dict()["id"])

    os.makedirs("output", exist_ok=True)
    for no, qp_no in enumerate(cue_points):
        qp = points[qp_no]
        chrome.save_koma(os.path.join("output", f"{no + 1}.png"), qp)


def get_waypoints(gpx) -> List[WayPoint]:
    wpts: List[WayPoint] = []
    for wpt in gpx.waypoints:

        wpts.append(WayPoint(
            wpt.latitude,
            wpt.longitude,
            wpt.name))

    return wpts


def make_map(points: List[Point]) -> str:
    latitude = points[0].latitude
    longitude = points[0].longitude
    map = folium.Map(location=[latitude, longitude], zoom_start=16)

    folium.TileLayer('openstreetmap').add_to(map)
    # folium.TileLayer('cartodbpositron').add_to(map)
    # folium.TileLayer('cartodbpositronnolabels').add_to(map)
    # folium.TileLayer('cartodbpositrononlylabels').add_to(map)
    # folium.TileLayer('mapboxbright').add_to(map)
    # folium.TileLayer('mapboxcontrolroom').add_to(map)
    # folium.TileLayer('openstreetmap').add_to(map)
    # folium.TileLayer('stamenterrain').add_to(map)
    # folium.TileLayer('stamentoner').add_to(map)
    # folium.TileLayer('stamentonerbackground').add_to(map)
    # folium.TileLayer('stamentonerlabels').add_to(map)
    # folium.TileLayer('stamenwatercolor').add_to(map)

    # folium.LayerControl().add_to(map)
    folium.PolyLine(
        [(_.latitude, _.longitude) for _ in points],
        color="#0000ff",
        opacity=0.8,
        weight=2
    ).add_to(map)

    return map


def add_arrow(mp: folium.Map, points: List[Point], cue_points: List[int]):
    for cue_point in cue_points:

        # get point 35m far from here
        point = get_point_by_distance(points, 35, cue_point)

        folium.RegularPolygonMarker(
            location=(point.before.latitude, point.before.longitude),
            fill=True,
            fill_rule="nonzero",
            fill_opacity=1.0,
            color='#0000ff',
            number_of_sides=3,
            radius=10,
            rotation=point.direction - 90
        ).add_to(mp)


class Chrome:
    def __init__(self, filename: str, map_id: str):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")  # needs in docker
        options.add_argument("--disable-dev-shm-usage")  # needs in docker
        driver = webdriver.Chrome(options=options)
        driver.set_window_size(400, 400)

        driver.get(f"file:///{os.getcwd()}/{filename}")

        self._driver = driver
        self._map_id = map_id

    def _image_loaded(self, img) -> bool:
        colors = [
            img.getpixel((0, 0)),
            img.getpixel((149, 0)),
            img.getpixel((0, 149)),
            img.getpixel((149, 149))]

        return all(map(lambda _: _ != (221, 221, 221, 255), colors))

    def crop_center(self, img, crop_width, crop_height):
        img_width, img_height = img.size
        return img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))

    def save_koma(self, filename: str, point: Point):
        self._driver.execute_script(
            f"map_{self._map_id}.panTo(new L.LatLng({point.latitude}, {point.longitude}), {{'animate': false}});")

        while True:
            time.sleep(1.0)
            self._driver.save_screenshot("_map.png")
            img = Image.open('_map.png')
            img = img.rotate(point.direction)
            img = self.crop_center(img, 150, 150)

            if self._image_loaded(img):
                break

        img.save(filename)
        print(filename)
