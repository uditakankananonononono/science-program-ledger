# R1 measured Fig3 table/figure reproduction design

No fitting, dynamic residual, inferred dt,physiology or novelty. Source bytes qualified
in195e6440e97b3051cdf10284e3df1cd3e9b2646c. Full target generation awaits executable
review/publication. Author notebook not run; inspect transformations only.

Outputs: exact unchanged five constant-voltage trajectory tables, ramp table and five
PIV profile tables retained as input subset; derived CSVs with explicitly named plotted
coordinates; manifest row/nonfinite counts, source+derived hashes; readable two figures.
Do NOT claim pixel-identical manuscript style. Source-content/coordinate reproduction
with re-laid-out axes/legend/colorbar and missing-data annotation. No source article
images copied or numerical Fig4 curve substituted as experiment.

Constants match notebook: r0=21um,v0=29.5um/s; no fit or precision inference. Panel-a
source transform: x_plot=-y_um/21 and y_plot=x_um/21+20-6*(voltage_case-1).
This axis swap/sign/stagger matches author scatter call; source axes named xbar/ybar
are convention-specific, our plot labels the displayed axes explicitly, with offsets
not silently called measured coordinates. Colors use table voltage not constant filename.
Profile transform: u_plot=u_um_per_s/29.5,y_plot=y_um/21. Five profiles, NaN cells
preserved, drawn as missing annotations not interpolated; finite points only rendered
with count displayed and original nonfinite records retained in CSV/JSON.

Ramp-panel transform copied exactly after confirming rotateXY definition: divide x/y
by21,rotate by source0.8 angle with confirmed unit convention,apply source
(data1[0]-data[0])/2 translation then subtract [data1[0,0],148/21],plot negative x and
positive y. Derived transformed arrays exported, no time axis or interpolation.
Source main/zoom windows documented but our content figure may show all rows with
source windows as optional explicit views, not silently drop rows. If angle unit
cannot be established, hold ramp transform rather than guess degrees/radians.

S3 error-column table excluded from plots/fit due to unresolved header-vs-notebook
uncertainty semantics. Full archive checksum/per-file subset hash verified before
processing; schema exact header/column counts; nonfinite allowed only in stated PIV
speed cells (three known NaNs), no other silent coercion. Development tests literal
coordinate transforms,rotation,nonfinite retention/hash refusal. Full generation only
after executable+protocol freeze and readback. Visual pixels inspected before results
ready; all data points/source rows retained even if plotting windows hide some.
