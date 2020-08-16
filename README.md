# komamap

Create koma-Map from GPX track data and cue data.

## How to Install (Docker)

Yes, docker is easiest way to create environment.

### Build

```console
docker build -t komamap .
```

### Execute

```console
docker run -it --rm -v $(pwd)/output:/app/output komamap -h
```

```console
docker run -it --rm -v $(pwd)/output:/app/output komamap --rwgps 30477783
```


### Other Options

Use GPX file with Cue as Waypoint:
```console
komamap -f track.gpx
```

Use GPX file without Cue, and GPX file with Cue as Route Data:
```console
komamap -f track.gpx --route route.gpx
```

Use GPX file without Cue, and Excel Cue Sheet which has total distance on Column D, starts from row 3:
```console
komamap -f track.gpx --route route.xlsx --col 4 --row 3
```

Use RideWithGPS and Excel Cue Sheet which has total distance on Column D, starts from row 3:
```console
komamap --rwgps 30477783 --route route.xlsx --col 4 --row 3
```

Change Map Tile:
```console
komamap --rwgps 30477783 --maptype stamentonerbackground
```
