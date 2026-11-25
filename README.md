# Overhead

A PlaneSlate-style "what's flying over my house" display for a jailbroken Amazon Echo Show 5
(LineageOS + Fully Kiosk Browser), or any browser. Single HTML file, free data sources only:

- Aircraft positions: adsb.lol / airplanes.live / adsb.fi (or your own tar1090 receiver)
- Routes: adsb.lol routeset + adsbdb, sanity-checked against the plane's position
- Satellite imagery: Esri World Imagery

## Install on the Echo
1. Enable GitHub Pages for this repo (Settings -> Pages -> Deploy from branch -> `main` / root).
2. In Fully Kiosk, set **Start URL** to `https://jkktech.github.io/overhead-tracker/`
3. Enter your latitude/longitude on first launch.

## Releasing an update
Edit `index.html`, then run `./release.sh`. The page checks `version.json` every 30 minutes
and reloads itself when the version changes. GitHub Pages caches for ~10 minutes, so allow up to ~40 minutes.

Demo: add `?demo=1` to the URL.
