from typing import List, Union
from dataclasses import dataclass

import gpxpy
import xlrd

from .track import Track, Point


@dataclass
class CuePoint:
    latitude: float
    longitude: float
    description: str


@dataclass
class CueDistance:
    distance: float
    description: str


def read_waypoint(filename: str) -> List[CuePoint]:
    gpx_file = open(filename, 'r')
    gpx = gpxpy.parse(gpx_file)

    cues: List[CuePoint] = []
    for wpt in gpx.waypoints:
        cues.append(CuePoint(
            wpt.latitude,
            wpt.longitude,
            wpt.name))

    return cues


def read_route(filename: str) -> List[CuePoint]:
    gpx_file = open(filename, 'r')
    gpx = gpxpy.parse(gpx_file)

    cues: List[CuePoint] = []
    for route in gpx.routes:
        for point in route.points:
            cues.append(CuePoint(
                point.latitude,
                point.longitude,
                point.comment))

    return cues


def read_excel(filename: str, dist_col: int, start_row: int) -> List[CueDistance]:
    wb = xlrd.open_workbook(filename)
    ws: xlrd.sheet.Sheet = wb.sheets()[0]

    cues: List[CuePoint] = []
    started = False
    for val in ws.col_values(dist_col - 1, start_rowx=start_row - 1):
        if isinstance(val, str):
            if started:
                break
            else:
                continue

        cues.append(CueDistance(val, ""))
        started = True

    return cues


def get_points_near_cuepoint(points: Track, cues: List[CuePoint]) -> List[Point]:
    cue_points = []
    n = 0
    cue = cues[0]
    for point in points:
        if isinstance(cue, CuePoint):
            dist = point.distance_from(Point(cue.latitude, cue.longitude))
        else:
            dist = cue * 1000 - point.distance

        if dist <= 10:
            cue_points.append(point)
            n += 1
            if n >= len(cues):
                break

            cue = cues[n]

    return cue_points


def get_points_near_cuedistance(points: Track, cues: List[CueDistance]) -> List[Point]:
    cue_points = []
    n = 0
    cue = cues[0]
    for point in points:
        dist = cue.distance * 1000 - point.distance

        if dist <= 50:
            cue_points.append(point)
            n += 1
            if n >= len(cues):
                break

            cue = cues[n]

    return cue_points


def get_points_near_cue(points: Track, cues: List[Union[CuePoint, CueDistance]]) -> List[Point]:
    if cues and isinstance(cues[0], CuePoint):
        return get_points_near_cuepoint(points, cues)
    else:
        return get_points_near_cuedistance(points, cues)
