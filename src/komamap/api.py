import falcon
from wsgiref import simple_server
import tempfile
import os
import glob
from zipfile import ZipFile


from . import komamap
from . import rwgps


class CORSMiddleware:
    def process_request(self, req, resp):
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Headers', 'Content-Type')


class KomaMapAPI(object):
    def on_get(self, req, resp, route_id):

        privacy_code = req.params.get("privacy_code", None)
        # "mfUk7xmZReB23jCQ"

        with tempfile.TemporaryDirectory() as tmpdir:
            outdir = os.path.join(tmpdir, "output")
            os.makedirs(outdir)
            rwgps.download_gpx(os.path.join(outdir, "rwgps_track.gpx"), route_id, "track", privacy_code)
            rwgps.download_gpx(os.path.join(outdir, "rwgps_route.gpx"), route_id, "route", privacy_code)

            komamap.komamap(
                os.path.join(outdir, "rwgps_track.gpx"),
                os.path.join(outdir, "rwgps_route.gpx"),
                outdir=outdir)

            with ZipFile(os.path.join(tmpdir, 'map.zip'), 'w') as myzip:
                for filepath in glob.glob(os.path.join(outdir, "*")):
                    myzip.write(filepath, os.path.basename(filepath))

            data = open(os.path.join(tmpdir, 'map.zip'), "rb").read()

        resp.set_header('Content-Type', 'application/zip')
        # resp.media = data
        resp.set_header("Content-Disposition", "attachment; filename=komamap.zip")
        resp.data = data
        resp.status = falcon.HTTP_200


app = falcon.API(middleware=[CORSMiddleware()])
app.add_route("/komamap/{route_id}", KomaMapAPI())


def run() -> None:
    httpd = simple_server.make_server("0.0.0.0", 8000, app)
    httpd.serve_forever()
