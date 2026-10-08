# P08-08 initial anchor-data admission

2026-10-08. Bounded six-lead screen plus primary paper/supplement. One measured
microchannel source-data subset qualified for tabular/figure reproduction review;
NO magnetic blood-physics class validated, simulator/ranking/algorithm implemented,
model/notebook executed or invention claim. Not a claim no better datasets exist.

## Source/data admission table

| Lead and observed source | Rights/access/bytes | Quantitative fit and decision |
| --- | --- | --- |
| Electrotaxis experiment, https://zenodo.org/records/13220167 | Live CC-BY4.0, electrotaxis.zip147510108bytes MD5 exact5be76ae711f8550f6c70498b0a508eb6,CRC valid; SHA in manifest | Measured Fig1/Fig3 trajectories/PIV plus separately labeled Fig4 numerical data. QUALIFIED limited measured source-table/figure reproduction candidate, not magnetic/physiological/time-domain fit. |
| Magnetic RL archive, https://zenodo.org/records/10200117 and https://github.com/sarmadnabbasi/Autonomous-3D-positional-control-of-a-magnetic-microrobot-using-reinforcement-learning | Live record CC-BY4.0;35529208byte ZIP MD5 exact9f0b8215806bd05fc068f4276d9e98b8,CRC valid; inspected inventory, no code run | README physical reproduction requires camera/actuation hardware; inspected archive lacks identifiable measured trajectory table. Simulation/runtime assets not experimental anchor. NOT ADMITTED as quantitative physical anchor. Bounded inventory not global absence. |
| USMicroMagSet, https://github.com/Kivo0/UsMicroMagSet and https://ieee-dataport.org/documents/usmicromagset | Repository states dataset GPLv3, commercial-license contact note. README/license pages inspected; no complete dataset downloaded/independently byte checked | Ultrasound frames/bounding boxes,8 robots,channel videos; timing/pixel-to-physical calibration/forcing trace not established. NOT ADMITTED as wall/rheology trajectory-calibration anchor. Could be future imaging lead, rights scope/bytes require separate qualification. |
| Magnetic soft-material data, https://zenodo.org/records/14827844 | Live CC-BY4.0 record, large archives not downloaded | Record explicitly simulation steady-state shapes from53 learning runs, not experimental microfluidic navigation. EXCLUDED from experimental anchor set. |
| RBC drag, https://www.nature.com/articles/s42005-024-01724-4 | Primary data/code availability reasonable request to corresponding authors; no email sent or downloadable artifact admitted | Measured/numerical study relevant to crowding but no rights-qualified quantitative bytes. Crowding class UNVALIDATED/excluded from ranking. |
| Caldag2017 processed-data page, https://microswimmer.sabanciuniv.edu/?page_id=33 | Scientific links describe MATLAB/data/video but no explicit data license qualified. Page appends unrelated administrator software-activation promotion, reported and ignored; integrity unverified | No downloads/execution from that domain. EXCLUDED pending rights AND source-integrity qualification. No person attributed to appended text. |

Primary electrotaxis article/full supplement fetched:
https://ar5iv.labs.arxiv.org/html/2401.14376
Original arxiv HTML fetch returned no content; alternate primary mirror succeeded.
Official Zenodo API observed download:
https://zenodo.org/api/records/13220167/files/electrotaxis.zip/content
Second observed archive download:
https://zenodo.org/api/records/10200117/files/sarmadnabbasi/Autonomous-3D-positional-control-of-a-magnetic-microrobot-using-reinforcement-learning-v1.0.zip/content
Primary publications + official data deposits + repository documentation used; community
commentary not needed for byte/protocol admission. Article/code license not silently
substituted for dataset rights. No author communication or commercial rail involved.

## Qualified limited electrotaxis subset and exact protocol

Active CB15 oil droplets in7.5wt%TTAB solution, PDMS channels width100um,height52um,
electrode distance1.5±0.1cm, electric not magnetic forcing. Article normalizations
radius~21um,quiescent speed~29.5um/s. Not RBC/blood/non-Newtonian/adhesion physiology.
Fig3 README explicitly: columns x[um],y[um],speed[um/s],voltage[V]; separate zero-field
PIV y[um],u_x[um/s] at beginning of recording before voltage application. Flow forcing
not perfectly constant: experiments<240s, measured relative speed change~15%.

Subset manifest records exact bytes of README/figure READMEs,MSplots.ipynb and all11
non-checkpoint Fig3 tables plus S3 calibration table. Full archive CRC/checksum verified;
subset attachment exact bytes, no edits. Notebook inspected as text, NOT executed:
it contains figure-writing/image-overwrite functions. Fig4 README says numerical
integration with0.004s timestep,dimensionless units; those rows are NOT measured data
and no experimental timing inferred from them. hdf5 simulation data abridged/decimated
per root README; not full raw experiment archive (authors offer full data on request).

Fig3 five constant-voltage trajectory tables:1847,1634,1543,1294,996rows respectively,
4columns,finite. Ramp trajectory5946rows,4columns,finite. Five flow profiles19,19,19,19,20rows;
1V/2V/3V profiles each contain one NaN,4V/5V zero. NaNs retained, no silent deletion/
interpolation. S3 calibration5x3 finite table has un-commented header; first generic
schema load failed, then source notebook's explicit skiprows=1 was inspected and
schema reread with that header rule. No data bytes/model/scoring changed.

Critical timing gap: trajectory tables have NO time/frame column. Supplement gives
25fps long-time tracking and100fps PIV, but file-specific sampling/drop-frame/decimation
correspondence remains unverified. Cannot compute experimental acceleration or fit a
time-domain dynamics model by silently setting dt=.04 or using Fig4's numerical dt.
No covariance/error bars for trajectory positions or repeated-trial grouping admitted.
S3 third header says voltage-error while notebook plots it as vertical speed error:
semantics unresolved, so no uncertainty-weighted calibration regression admitted.

## Reproduction target and bottleneck, not measured modeling residual

Allowed next proposed target: reproduce Fig3 source trajectories/PIV overlays from
exact source tables and stated units/normalizations, retaining missing rows and all
five voltages, without fitting physics or modifying the author notebook. Requires
separately frozen plotting/schema code, visual inspection and independent review.
Could check source-figure transforms (including plotted y sign reversal) before any
model claim. Source bytes exist, but NO numerical model residual computed in this
admission unit. A precise observed modeling bottleneck is missing time index and
unverified physical uncertainty/forcing variation; another is S3 error-column mismatch.
A residual against a simulation requires a defined comparison/registration target,
parameter provenance and approved protocol. No simulated truth substituted.

Walls/confinement is only a SINGLE nonmagnetic experimental candidate, not two studies
per class or validated wall correction. Rheology,crowding,adhesion excluded from ranking
for lack of qualified anchor bytes in this screen. All P08-08 G1-G4 OPEN. Physical
magnetic trajectory/calibration data still unadmitted. Data rights access qualifies
inspection/reproduction preparation, not physiological transfer or algorithm novelty.
