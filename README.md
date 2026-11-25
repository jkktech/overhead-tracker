# Overhead

A PlaneSlate-style "what's flying over my house" display for a jailbroken Amazon Echo Show 5
(LineageOS + Fully Kiosk Browser), or any browser. Single HTML file, free data sources only:

- Satellite imagery: Esri World Imagery

## Install on the Echo
The free flight-data sites don't allow web pages hosted elsewhere (like github.io) to read their data,
but Fully Kiosk lets a *local file* through. So the Echo runs a tiny local loader that
downloads the latest tracker from GitHub Pages and runs it as a local page.

1. GitHub Pages enabled for this repo (Settings -> Pages -> `main` / root).
2. `adb push loader.html /sdcard/overhead.html`
3. Fully Kiosk **Start URL**: `file:///sdcard/overhead.html`
   (Fully Kiosk -> Web Content Settings: "Enable File Access" and
   "Allow Universal Access from File URLs" must be on.)
4. Enter your latitude/longitude on first launch.

The loader caches the last downloaded copy, so the display still works if GitHub is unreachable.

## API keys (set remotely, never committed)
Copy `overhead-config.example.json` to `overhead-config.json`, put your keys in it, and push it next to the loader:

    adb push overhead-config.json /sdcard/overhead-config.json

Values in this file override what's typed on the Echo's settings screen. It's read each time the loader
starts, so restart Fully Kiosk (or reboot) after pushing. Supported keys include `fiaKey`, `alKey`, `alDay`, `alMonth`,
`adbKey`, `adbDay`, `adbMonth`, plus any other setting (`lat`, `lon`, `name`, `radius`, ...).

## Data sources
- Planes: adsb.lol (free), falling back to adsb.fi. FlyItalyADSB and AeroDataBox are used only for route lookups.
- Routes for the card plane, in order - each must fit the plane's actual position/climb/descent:
  1. FlyItalyADSB: every route that callsign flew in the last 14 days (one lookup per flight, cached 6 h)
  2. AirLabs Flight Info by flight number (free 1,000/month; capped 30/day, 950/month). Its reported
     position must be near the plane, so a same-number flight elsewhere is ignored. Adds arrival time.
  3. AeroDataBox live status by aircraft (capped: 6/day, 190/month)
     Each pauses until tomorrow on any quota/limit/key reply; each flight is looked up once (cached 8 h).
  4. Free community route DB (only when FlyItalyADSB isn't available)
  5. Otherwise "Route unknown" - no guessing.
- Airport coordinates: `airports.json`, built from OurAirports (public domain) by `tools/mk_airports.py`.
- Aircraft silhouettes: `shapes/`, from [AircraftShapesSVG](https://github.com/RexKramer1/AircraftShapesSVG) by RexKramer1 and contributors, **GPL-3.0** (see `shapes/LICENSE` and `shapes/NOTICE.md`), prepared by `tools/norm_shapes.py`.

## Releasing an update
Edit `index.html`, then run `./release.sh`. The page checks `version.json` every 30 minutes
and reloads itself when the version changes. GitHub Pages caches for ~10 minutes, so allow up to ~40 minutes.

Demo: add `?demo=1` to the URL.
