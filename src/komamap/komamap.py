import os
import sys
from typing import List, Union

from .track import read_track_from_gpx
from .maplib import Map
from .chrome import Chrome
from . import cue


def komamap(gpx: str, route: str, xl_dist_col: int = 4, xl_start_row: int = 3, map_type: str = "openstreetmap", outdir: str = "output", crop_size: int = 200):
    points = read_track_from_gpx(gpx)
    mp = Map(points, map_type)

    cues: List[Union[cue.CuePoint, cue.CueDistance]]
    if route:
        ext = os.path.splitext(route.lower())[1]
        if ext == ".gpx":
            cues = cue.read_route(route)
        elif ext == ".xlsx":
            cues = cue.read_excel(route, xl_dist_col, xl_start_row)
        else:
            sys.stderr.write("Unknown Route File Type")
            sys.exit(1)
    else:
        cues = cue.read_waypoint(gpx)

    cue_points = cue.get_points_near_cue(points, cues)

    mp.add_arrow(points, cue_points)
    mp.save("map.html")

    chrome = Chrome("map.html", mp.map_id)

    os.makedirs(outdir, exist_ok=True)
    prev_distance = -1.
    sub_name = 0
    for qp in cue_points:
        if qp.distance == prev_distance:
            filename = "%06.1f-%d.png" % (qp.distance / 1000, sub_name)
            sub_name += 1
        else:
            filename = "%06.1f.png" % (qp.distance / 1000)
            sub_name = 0

        chrome.save_koma(os.path.join(outdir, filename), qp, crop_size)
        prev_distance = qp.distance
