# Tesla declared workspace and caller-side domain gap

Targeted inspection at upstream 5ef021b0f4c0b91d1d8f3aedf353fe24bf793e84:
https://github.com/ethz-msrl/Tesla_core_public
Exact blobs/hashes already retained in TESLA-QUALIFICATION.md. No upstream execution
or imported coefficients. Original qualification remains bounded, not blanket absence.

OctoMag_Calibration.yaml declares Workspace_Dimensions [-0.01,0.01] on each of three
axes and System_Name OctoMag_Calibration_Order_1. These are source-declared coordinate
ranges, NOT independently held-out validated error bounds or admission of in-vivo
workspace. The README uses meters for position measurements, but a declared number
alone does not certify device fit or convert our arbitrary-unit synthetic fixtures.

Parsed YAML top-level keys: Coil_0..Coil_7, Coil_List, System_Name,
Workspace_Dimensions. No current limit/slew/error/timestamp metadata at that level.
This statement is exact to this file/top-level inspection, not a repository-wide
absence claim. Source coefficient content was read but no fit validity inferred.

Header documents gradient packing [dBx/dx,dBx/dy,dBx/dz,dBy/dy,dBy/dz]. This differs
from our synthetic constructor coefficient order [xx,yy,xy,xz,yz]. Any future adapter
must explicitly reorder indices; direct vector reuse would be incorrect.

Source fieldAtPoint loops over coils and returns field without enforcing workspace.
gradientAtPoint delegates to gradientCurrentJacobian; Jacobian routines show optional
MPEM_SHOW_WARNINGS workspace warning blocks, not rejection. pointInWorkspace uses
inclusive coordinate comparisons. This is static source inspection only, not a
compiled behavior test; release/debug assertions and warning settings not executed.

Physical-admission implication: implement explicit caller-side position-domain
validation before using such models, and do not confuse a warning-only upstream path
with a fail-closed domain contract. Still need exact device/current regime, held-out
fit errors, current/slew/thermal limits, magnetic moment/orientation and fluid mobility.
No device profile imported, hardware/anatomy/safety gate or novelty established.
