# Week 4 GPS practice data

These nine coordinates are **synthetic teaching data**, not collected phone observations or
surveyed landmark coordinates. `Demo_A`, `Demo_B`, and `Demo_C` are illustrative locations
around BYU campus, not names from the field assignment. Receivers A, B, and C are fictional.

- `practice_gps.csv`: WGS 84 (EPSG:4326), `name,site,lat,lon`; X = lon, Y = lat.
- `week04-practice.zip`: unzip and open `week04-practice.qgz` in QGIS 3.44. Keep its CSV and
  GeoPackage in the same folder. No online basemap is needed.

The projected layer is NAD83 / UTM zone 12N (EPSG:26912). Demo_A receiver A is approximately
(444700, 4455300) meters; B is (444706, 4455308). Their planar separation is about 10 meters.
The last millimeters may differ after rounding the degree coordinates and transforming back.

Rebuild data and screenshots with `tools/qgis_week04_shots.py` at the repository root.
The script header gives the command. It uses an isolated temporary QGIS profile and creates
real QGIS widget captures. The two accompanying SVG concept diagrams are original vector
illustrations, not application screenshots.
