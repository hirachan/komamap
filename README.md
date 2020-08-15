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
