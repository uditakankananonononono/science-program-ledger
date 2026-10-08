# R1 source-content reproduction

Generated once from published frozen c32722011fd2ecc46201b1a2e5235293c1a33079.
No code/protocol/coordinate changes after freeze. Eleven CSVs read back: six trajectory
arrays match source row counts/4columns, five profiles retain19,19,19,19,20rows/2columns
and three NaNs. All rows retained, no fitted model, inferred timestamps or residual.
Code/protocol copies, environment, CSV/figure hashes in receipt and derived manifest.

Visually inspected BOTH actual PNG pixels with file viewer. constant_and_profiles.png:
five staggered trajectories, actual table-voltage coloring, readable axes/colorbar;
profile finite counts18/19,18/19,18/19,19/19,20/20 visible in legend, title states3NaNs.
NaN cells are endpoint speed values, so plots terminate rather than show interior
line breaks; they are not interpolated or silently discarded in CSV. ramp.png:
all5946 source rows plotted, full oscillatory content and voltage colorbar, axis
rotation/translation spelled out. Both layouts readable, no clipped labels/overlaps
noticed. Initial viewer call used relative path and was refused; absolute-path pixel
inspection then succeeded. No figure edits/regeneration needed.

These are new content layouts, not pixel-identical manuscript figures. No original
zoom windows/insets/style replicated; all-row view is explicit. Panel-a coordinate
axis swap/sign/stagger exactly source scatter convention, not untransformed measured
x/y; CSV columns/labels name this. Ramp rotation0.8degrees confirmed in source helper.

Source: Buness,Rana,Maass,Dey,Electrotaxis of self-propelling artificial swimmers in
microchannels, https://zenodo.org/records/13220167 CC-BY4.0. Derived coordinates/plots
are transformations of licensed source tables; original bytes unchanged. Source
notebook inspected as text, never executed. Electrical active-droplet channel data,
not magnetic blood navigation/physiological validation. Timing-column absence and
S3error-column mismatch unresolved/excluded, no silent workaround. No algorithm
invention or model-validation residual established. Publish-before-generation log
is provenance; independent replay validates content, not external chronology alone.
