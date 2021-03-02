#!/bin/env python3
import sys
import argparse

from . import komamap
from . import rwgps
from .maplib import MapType


def get_opt() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Create Koma-Map from GPX')
    parser.add_argument("-f", dest="gpx",
                        type=str, metavar="GPX FILEPATH", required=False,
                        help="GPX File with Track")

    parser.add_argument("--route", dest="route",
                        type=str, metavar="FILEPATH", required=False,
                        help="GPX File with Cue as Route or Excel Cue Sheet")

    parser.add_argument("--rwgps", dest="route_id",
                        type=str, metavar="ROUTE ID", required=False,
                        help="RWGPS Route ID")

    parser.add_argument("--privacy-code", dest="privacy_code",
                        type=str, metavar="PRIVACY CODE", required=False,
                        help="RWGPS Route Privacy Code")

    parser.add_argument("--col", dest="xl_dist_col",
                        type=int, metavar="NUMBER", required=False, default=4,
                        help="Column Number of Total Distance for Excel Cue Sheet (A -> 1)")

    parser.add_argument("--row", dest="xl_start_row",
                        type=int, metavar="NUMBER", required=False, default=3,
                        help="Starting Row Number of for Excel Cue Sheet")

    parser.add_argument("--maptype", dest="map_type",
                        type=str, metavar="MAP TYPE",
                        choices=MapType,
                        default="openstreetmap", help=", ".join(MapType))

    parser.add_argument("--size", dest="crop_size",
                        type=int, metavar="KOMA SIZE", required=False, default=200,
                        help="Crop size")

    # parser.add_argument("command", action="store")
    # parser.add_argument("files", action="store", nargs="+")
    # parser.add_argument("-n", "--num", dest="num",
    #                     type=int, metavar="N",
    #                     help="some help")
    # # parser.add_argument("--to", dest="to",
    # #                     type=str, metavar="EMAIL", required=True,
    # #                     help="some help")
    # parser.add_argument("-q", dest="quiet",
    #                     action="store_true",
    #                     help="some help")
    # parser.add_argument("--ssl", dest="port",
    #                     action="store_const", default=80, const=443,
    #                     help="some help")

    args = parser.parse_args()

    return args


def main() -> int:
    args = get_opt()

    if args.route_id:
        rwgps.download_gpx("rwgps_track.gpx", args.route_id, "track", args.privacy_code)
        args.gpx = "rwgps_track.gpx"

        if not args.route:
            rwgps.download_gpx("rwgps_route.gpx", args.route_id, "route", args.privacy_code)
            args.route = "rwgps_route.gpx"

    route = args.route if args.route else args.gpx

    komamap.komamap(args.gpx, route, args.xl_dist_col, args.xl_start_row, args.map_type, crop_size=args.crop_size)

    return 0


if __name__ == "__main__":
    sys.exit(main())
