# Overhead

A PlaneSlate-style "what's flying over my house" display for a jailbroken Amazon Echo Show 5
(LineageOS + Fully Kiosk Browser), or any browser. Single HTML file, free data sources only:

- Aircraft positions: adsb.lol / airplanes.live / adsb.fi (or your own tar1090 receiver)
- Routes: adsb.lol routeset + adsbdb, sanity-checked against the plane's position
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

## Releasing an update
Edit `index.html`, then run `./release.sh`. The page checks `version.json` every 30 minutes
and reloads itself when the version changes. GitHub Pages caches for ~10 minutes, so allow up to ~40 minutes.

Demo: add `?demo=1` to the URL.
