# G1 coordinate-to-wall provenance audit

All five per-profile metrological bindings UNRESOLVED in the checked records.
Author plotting convention IS explicit: each PIV y divided by21um, no additional
translation/sign inversion for profiles, wall shading at±50/21 in the same inset.
This binds the display convention to all five entries, but does not recover measured
wall positions or the upstream per-record pixel-origin/scale calibration. Thus do
not label all coordinate information absent. P1 remains a measured fixed-model
mismatch/model-admission bottleneck; physical attribution remains unresolved.

## Checked primary record set and scope correction

- https://zenodo.org/records/13220167 current description, license and archive link;
  full147510108byte archived electrotaxis.zip re-hashed before static extraction,
  SHA256ec065d6c3ed0991758d30bd9308fb9dbd492992bc008b90464e45de767a3dab7.
- https://zenodo.org/api/records/13220167/files/electrotaxis.zip/content exact
  README,Fig3/README,five source tables,MSplots.ipynb static cell2 and cell9.
- https://ar5iv.labs.arxiv.org/html/2401.14376 paper including supplementary text.
- https://arxiv.org/abs/2401.14376 confirms v1; its actual PDF link was recovered,
  https://arxiv.org/pdf/2401.14376 downloaded,text extracted,and actual page8/9
  pixels inspected. FigS2(d) gives schematic coordinate DIRECTIONS,not a per-profile
  origin/wall calibration. General width and approximate PIV scale are supported.
- https://doi.org/10.1103/physrevlett.133.158301 is the journal DOI linked by Zenodo;
  fetch returned NO_CONTENT_RETURNED. Final journal/supplement not independently
  audited here. Conclusion bounded to checked archive/arXiv records,not all possible
  calibration records. Authors offer raw data on reasonable request; none requested.

Admission memo's Nature URL https://www.nature.com/articles/s42005-024-01724-4
was an incorrect corpus lead: live fetch shows 'Drag force on a microrobot propelled
through blood',a DIFFERENT article. Excluded,never used for coordinate evidence.
The ar5iv FigS2 image URL returned a 'NO IMAGE AVAILABLE' placeholder,not the
schematic. Not counted as visual evidence; resolved by actual PDF page9 inspection.
No six-source quota padding: question is about these exact original measurements,
not an opinion survey. Public search leads only; no external PIV theory used to
claim record-specific calibration. Static author text inspected,never executed.

## Exact evidence excerpts

E1: archive Fig3/README lines4-6 (retained exact evidence file):
'Poiseuille_E0V_flowprofile_[X]V.txt'; 'PIV data was taken at the beginning of the
recording for U=0V, before a field of [X] was applied. Columns are y[um] u_x[um/s]
for the y dependent flow in x.' All five are separate pre-field records,not applied
voltage effects. README supplies units/association,not origin/wall calibration.

E2: each named source table line1 exactly '#y[um] u[um/s] ' (including trailing
space); raw first/last rows in table below. All exact source bytes/hash retained.

E3: original MSplots.ipynb cell2 lines1-3: '# non-dimensionalisation',
'v0 = 29.5','r0 = 21'. Cell9 lines11,13,15-16:
'volts=[1,2,3,4,5]'; 'for V in range(len(volts)):';
"prof = np.loadtxt('Fig3/Poiseuille_E0V_flowprofile_%dV.txt'%volts[V])*np.array([1/r0,1/v0])";
"axpoiss.plot(prof[:,1],prof[:,0], '.', c=voltmap(volts[V]/5.), markeredgewidth=0,ms=4)".
Cell9 lines25-26:
'axpoiss.axhspan(50/r0,spac/2,color="#"+"b"*6)';
'axpoiss.axhspan(-50/r0,-spac/2,color="#"+"b"*6)'.
Explicit±50um plotting walls for ALL five,not individually measured wall estimates.
No profile y translation/sign flip there; trajectory branch at cell9 line14 DOES
flip its y,so do not transfer that transformation to the profiles.

E4: arXiv PDF page8,Supplement 'Channel setup',PDF text lines475-477 (UNIX newline convention):
'quasi-two-dimensional PDMS structure containing12parallel channels of length9mm,
width100um and height52um'. Fig1 caption says approximately100um width. This is
nominal/general geometry,not measured wall/origin records for the five PIV tables.

E5: arXiv PDF page9,Supplement 'Particle Image Velocimetry',PDF text lines543-550 (UNIX newline convention):
'open-source MATLAB module PIVlab'; 'flow field grid spacing was5x5px2 at a
magnification of40x (Interrogation area:Pass1:24,pass2:16and pass3:10),yielding
a spatial resolution of approximately2.5x2.5um2. Wall slip below this length scale
could not be resolved.' Generic analysis description,not per-profile pixel-origin
or wall-position calibration. No scale correction inferred from grid spacings.

## Per-profile coordinate-to-wall binding

Full filenames below refer to Fig3/ in the source archive; each has E1/E2/E3 common
units/display convention and E4/E5 generic geometry/methods. Entry-specific boundary
rows quote source y fields,not inferred physical walls. 'Unresolved' applies to
metrological binding of BOTH physical walls and origin/scale,not display convention.

| Entry | Table lines | First y um | Last y um | Explicit per-profile physical wall/origin/scale record | Binding |
|---|---|---|---|---|---|
| Poiseuille_E0V_flowprofile_1V.txt | header1; boundaries2,20 | -48.77999999999999 | 48.78 | Not recovered; common display±50um,not measured walls | unresolved |
| Poiseuille_E0V_flowprofile_2V.txt | header1; boundaries2,20 | -48.78 | 48.78 | Not recovered; common display±50um,not measured walls | unresolved |
| Poiseuille_E0V_flowprofile_3V.txt | header1; boundaries2,20 | -48.77999999999999 | 48.78 | Not recovered; common display±50um,not measured walls | unresolved |
| Poiseuille_E0V_flowprofile_4V.txt | header1; boundaries2,20 | -48.78 | 48.78 | Not recovered; common display±50um,not measured walls | unresolved |
| Poiseuille_E0V_flowprofile_5V.txt | header1; boundaries2,21 | -51.48999999999992 | 51.489999999999924 | Not recovered; source points outside common display wall positions retained | unresolved |

5V outside±50 is a table/display-domain tension,NOT two conflicting measured wall
bindings. Do not use 'conflicting' classification without opposing explicit bindings.
For1V-4V,symmetric in-domain grids likewise do not prove measured physical centering.
Five source SHA256s and raw files retained in evidence-manifest.json/evidence/. The
three NaN speeds at line20 of1V-3V retained. No new fit/table correction performed.

## Endpoint

G1 can close on unresolved metrological binding. Needed to change that conclusion:
record-specific raw PIV calibration/processing metadata linking pixel coordinates,
measured two-wall locations and the published y origin/scale. Generic schematics,
nominal100um width or plausible5.42um grid steps are insufficient. No owner/contact
action or raw-data request underway. No new residuals/refits/retuning/method comparison.
P1 mismatch is measured-but-unattributed,not dismissed or promoted to missing physics,
wall slip,invention,voltage-effect evidence or a completed P08 scientific gate.

Excerpt-ledger correction after review: original ledger used Python splitlines,which
counts form feeds as breaks,while citations used UNIX PDF text lines. Ledger now
regenerated with UNIX newline counting (equivalent to nl -ba),matching the citation
convention,and includes full PIVlab/grid details. Review independently verified the
PDF text citations and actual pages8/9; only ledger needed repair. Follow-up ad0bdb2
briefly standardized on splitlines; this commit follows the clarified reviewer request
to keep verified PDF citation ranges and repair the excerpt ledger. No source content
or binding classification change; no computation/refitting performed.
