# P1 executable freeze

Implements reviewed design4c6d908. Literal fixtures only have been executed. No full
measured profiles loaded or fitted by this executable yet. Five exact entry names,
order, byte size/hash/header, shape and nonfinite count checked after whole archive
SHA256/CRC and Python/numpy/matplotlib pins. No other entry admitted.

Run literal tests: `python3 -m unittest -v` in this directory.
Run after review/publication only:
`python3 diagnose.py /path/to/electrotaxis-subset.zip protocol.json results`
Output directory must not already exist. Freeze/review precedes measured run.

Seven tests: exact parabola and leave-one-location zero errors; missing row retained;
zero-denominator full/fold guards; invalid positions/inf speeds/insufficient rows;
nonzero literal amplitude; literal-only archive success and hash/order/missingness/
whole-archive rejection; environment mismatch rejected before file access.

Outputs: all raw rows/per-profile summaries JSON, five CSVs, five-panel profile
figure and five-panel residual figure, code/protocol/environment/output manifest.
Missing speed marker is in a bottom axes-coordinate strip, not a fabricated speed.
Both actual images require visual inspection after the measured run; none generated
yet. Numerical agreement tolerance tests arithmetic only. No physical tolerance,
error bars, CI, physics pass, voltage effect, dynamics, dt or S3 column use.

Buness,Rana,Maass,Dey: https://zenodo.org/records/13220167 CC-BY4.0. Per-profile
amplitude estimates and all three speed NaNs retained; no inference of independent
folds/trials or held-out validation.
