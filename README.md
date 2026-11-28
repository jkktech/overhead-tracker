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

## Screens
The display rotates through four screens: **Closest plane** (12 s) -> **Radar** (12 s) -> **Stats** (10 s) -> **Weather** (10 s).
Tap a dot at the bottom to jump to a screen; tapping the screen pauses the rotation for 60 seconds. Tapping a plane on the
radar or in its list opens it on the Closest plane screen. Times (0 = hide a screen), rotation and photos are in Settings.
Closest plane is skipped when nothing is in range, Weather until it has loaded. "LOOK UP!" still takes over the screen.

## Data sources
- Planes: adsb.lol (free), falling back to adsb.fi. FlyItalyADSB and AeroDataBox are used only for route lookups.
- Routes for the card plane, in order - each must fit the plane's actual position/climb/descent:
  0. AirLabs area snapshot (free at lookup time): one /flights query for a box ~250 mi around home,
     every 30 min 8 AM-8 PM and every 2 h overnight (30/day). Matched by aircraft hex AND flight number.
  1. FlyItalyADSB: every route that callsign flew recently (7 days, or the plan's max_days if less; one lookup per flight, cached 6 h)
  2. AirLabs Flight Info by flight number (free 1,000/month; capped 3/day; 950/month shared with snapshots). Its reported
     position must be near the plane, so a same-number flight elsewhere is ignored. Adds arrival time.
  3. AeroDataBox live status by aircraft (capped: 6/day, 190/month)
     Each pauses until tomorrow on any quota/limit/key reply; each flight is looked up once (cached 8 h).
  4. Free community route DB (only when FlyItalyADSB isn't available)
  5. Otherwise "Route unknown" - no guessing.
- Owner of private/GA/medical/government aircraft: free adsbdb aircraft lookup (card plane only, cached 30 days), tagged Air ambulance / Police / Military.
- Aircraft photos: [planespotters.net](https://www.planespotters.net/photo/api) public photo API, by transponder hex, card plane only.
  Per their terms the reply is cached at most 24 h, the image loads straight from their URL (never stored), the
  photographer is credited and the photo links to its page. No photo -> the tinted silhouette.
- Weather: [Open-Meteo](https://open-meteo.com/) (free, no key, CC BY 4.0), once every 30 minutes.
- Stats: counted on the device from the plane data it already receives (no extra lookups), reset at midnight.
- Airport coordinates: `airports.json`, built from OurAirports (public domain) by `tools/mk_airports.py`.
- Aircraft silhouettes: `shapes/`, from [AircraftShapesSVG](https://github.com/RexKramer1/AircraftShapesSVG) by RexKramer1 and contributors, **GPL-3.0** (see `shapes/LICENSE` and `shapes/NOTICE.md`), prepared by `tools/norm_shapes.py`.

## Releasing an update
Edit `index.html`, then run `./release.sh`. The page checks `version.json` every 30 minutes
and reloads itself when the version changes. GitHub Pages caches for ~10 minutes, so allow up to ~40 minutes.

Demo: add `?demo=1` to the URL.
