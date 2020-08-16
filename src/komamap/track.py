from typing import Optional
from dataclasses import dataclass
from collections import UserList

import gpxpy
from gpxpy import geo


@dataclass
class Point:
    latitude: float
    longitude: float
    altitude: float = 0.0
    distance: float = 0.0
    direction: float = 0.0
    prev: Optional["Point"] = None
    next: Optional["Point"] = None

    def distance_from(self, point: "Point") -> float:
        return geo.distance(point.latitude, point.longitude, None,
                            self.latitude, self.longitude, None)


class Track(UserList):
    def __init__(self, point: Optional[Point] = None):
        self.data: Point
        super().__init__(point)

    def append(self, point: Point):
        if len(self.data) >= 1:
            prev: Point = self.data[-1]
            prev.next = point
            point.prev = prev

            point.distance = prev.distance + point.distance_from(prev)
            point.direction = geo.get_course(prev.latitude, prev.longitude, point.latitude, point.longitude)

        super().append(point)


def read_track_from_gpx(filename: str) -> Track:
    gpx_file = open(filename, 'r')
    gpx = gpxpy.parse(gpx_file)

    points: Track = Track()

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                pt = Point(point.latitude, point.longitude, point.elevation)

                points.append(pt)

    return points
