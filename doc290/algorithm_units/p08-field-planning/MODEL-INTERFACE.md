# Explicit gradient packing and workspace precheck

37 local development methods pass (33 prior + 4 interface). Upstream-described
five-gradient order [xx,xy,xz,yy,yz] is explicitly reordered to our constructor's
[xx,yy,xy,xz,yz]. Distinct coefficient and five one-hot controls verify all axis
placements; zz=-xx-yy. Source inspection provenance:
https://github.com/ethz-msrl/Tesla_core_public
at 5ef021b0f4c0b91d1d8f3aedf353fe24bf793e84, exact header hash in qualification note.
No upstream code copied or calibration admitted. Assumes symmetric trace-free
local gradient convention, not general unrestricted matrices.

Caller precheck requires finite point and finite non-reversed 3x2 bounds, inclusively.
No tolerance inflation or unit conversion. Endpoint accepted, immediately next
representable point outside rejected. Returns copy, caller buffers unaffected.
The function checks ONLY the supplied point/bounds. It does not enforce a planner
trajectory automatically or prove calibration error, continuous safety, device
identity, SI units or global coil realizability. Future upstream wrappers must call
it for every model evaluation; no upstream wrapper/executable introduced here.

All coefficients/bounds in development are synthetic examples. Arithmetic overflow
and gradient-structure tolerance remain inherited limitations. Prior production
modules unchanged; no score, invention, hardware/scientific gate. Review pending.
