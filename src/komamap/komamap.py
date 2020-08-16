from typing import List
from dataclasses import dataclass
import os

import gpxpy

from .track import Track, read_track_from_gpx, Point
from .maplib import Map
from .chrome import Chrome


@dataclass
class CuePoint:
    latitude: float
    longitude: float
    description: str
    rotate: float = 0


def read_waypoint(filename: str) -> List[CuePoint]:
    gpx_file = open(filename, 'r')
    gpx = gpxpy.parse(gpx_file)

    wpts: List[CuePoint] = []
    for wpt in gpx.waypoints:

        wpts.append(CuePoint(
            wpt.latitude,
            wpt.longitude,
            wpt.name))

    return wpts


def read_route(filename: str) -> List[CuePoint]:
    gpx_file = open(filename, 'r')
    gpx = gpxpy.parse(gpx_file)

    wpts: List[CuePoint] = []
    for route in gpx.routes:
        for point in route.points:
            wpts.append(CuePoint(
                point.latitude,
                point.longitude,
                point.comment))

    return wpts


def get_points_near_cuepoint(points: Track, wpts: List[CuePoint]):
    cue_points = []
    n = 0
    wpt = wpts[0]
    for point_no, point in enumerate(points):
        dist = point.distance_from(Point(wpt.latitude, wpt.longitude))
        print(dist)

        if dist <= 10:
            cue_points.append(point_no)
            n += 1
            if n >= len(wpts):
                break

            wpt = wpts[n]

    return cue_points


def komamap(gpx: str, route: str):
    points = read_track_from_gpx(gpx)
    mp = Map(points)

    if route:
        wpts = read_route(route)
    else:
        wpts = read_waypoint(gpx)

    cue_points = get_points_near_cuepoint(points, wpts)

    mp.add_arrow(points, cue_points)
    mp.save("map.html")

    chrome = Chrome("map.html", mp.map_id)

    os.makedirs("output", exist_ok=True)
    for no, qp_no in enumerate(cue_points):
        qp = points[qp_no]
        chrome.save_koma(os.path.join("output", f"{no + 1}.png"), qp)
