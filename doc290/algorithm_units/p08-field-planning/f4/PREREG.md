# F4 exact rectangular terminal reachability certificate adapter

Parent6b7922a29f5b44eb47760f2fc0105f3d19758af2. Existing reduced floating LP
allows rectangular/singular maps but status2 lacks independent infeasibility proof;
existing exact terminal solver handles square invertible maps only. New adapter
checks externally supplied rational witnesses or separating directions, not an
invention, automatic solver or measured/hardware validation. Earlier modules fixed.

## Supplied model and certificates

Same strict rational grammar/caps as F3: integers excludingbool, <=80chars; strings
canonical reduced n/d, positive denominator, no signedzero/leadingzero/plus;
integer -0 normalizes0. Model keys x,target,dt,B,limit,slew,previous. Positive times
andlimits, nonnegative slew, previous within limits, all dimensions consistent;
steps<=8,actuators<=4,coordinates<=4. Finite constantB and independentcomponentwise
constraints only, no scenario coupling/corridor/continuous obstacle/hardware units.
StrictUTF8JSON128KiB/depth10/duplicate/nonfinite refusal. Exact loadedmodule/
executable/sourceidentities/environment pinned and verified before comparisons.

Compute each actuator's exact saturated upper/lower ramp fromprevious and slew*dt;
weighted sums L_j,U_j define integratedcontrolintervals. Convex independentcontrol
polytopes imply full integralbox. Witnesskind feasible supplies integralvector z;
accept only L<=z<=U and Bz=target-x EXACTLY. Lift by mixing corresponding lower/
upper ramps with alpha=(z-L)/(U-L); degenerate interval requires z=L, useslower.
Replay all controls, first/next slew, integral andterminal equality EXACTLY before
REACHABLE; claimed integral alone not enough. No square-invertibility requirement.

Witnesskind separator supplies nonzero direction v in coordinate dimension.
Let q=B^T v, exact support h=sum max(q_j*L_j,q_j*U_j); target projection
p=v*(target-x). UNREACHABLE only if p>h strictly. Negative direction permitted;
orientation is explicit, no inferredflip. Nonseparatingdirection (includingboundary)
UNAVAILABLE, never jointfeasibility inference; missing witness alsoUNAVAILABLE
AFTERmodel validation. Malformedmodel/witness/failedfeasibleclaim INVALID.
Explicitkind prevents failedfeasibleclaim from being silently switched toseparator.
No arbitrary callable/iterable/sourcecode execution or automaticdirectionsearch.

## Frozen construction comparator scope

Four exposed models, x0,dt[1],limit1,slew2,previous0 unless explicitly changed:
R1 redundant row B=[1,1], target1, feasiblez[1/2,1/2].
R2 rank-deficient B=[[1],[1]], target[1,-1], separator[1,-1], support0,projection2.
R3 correlated-coordinate B=[[1],[2]], target[1,0], separator[2,-1],support0,projection2.
R4 slew-tight rectangle B=[1,2],x1,target3/2,dt[1/2],limit[2,2],slew[1,1],
 previous[1/2,0],feasiblez[1/4,1/8], within exact integralintervals.

Fourvalidcases; R1/R4 each fourmutations: out-of-boxintegral, wrongterminalintegral,
truncatedintegral, booleanintegral. R2/R3 each fourmutations: oppositedirection
(nonseparating UNAVAILABLE), zero direction INVALID, truncateddirection INVALID,
floatdirection INVALID. Six standalonecontrols: missingwitnessUNAVAILABLE,
floatdtINVALID, negativetimeINVALID, badBshapeINVALID, signedzerostringINVALID,
separatoratboundaryUNAVAILABLE (R1direction[1],target2). Total26rows;
allretained with verdict/reason/inputhash/expectedagreement. For4validmodels only,
unchanged reducedfloatingLP called descriptively; rawstatus/controls/exception
retained, never exactproof status or floatwitnessgeneration. No speed/CI/holdout.

Independentdevelopmenttests reconstruct nonunitdt/nonzerox/previous/asymmetric
multidimensional ramps, exact support vs cornerenumeration, liftedactuator/slew/
integral/terminal semantics, degenerateinterval and invalidmodelfirst behavior.
Notfullbattery; comparator disagreement/refusal tests and sourceidentitytamper
before scoring. Mathverifier must not depend on solver/candidate directions found
by floatingcalls. Earlier rational_support/integral_lift/reduced_terminal unchanged;
newexactadapter may reconstruct ramps independently, developmentcompare explicit.

Prereg review/publication BEFOREimplementation; executable/protocol/inputs/source/
environmentfreeze review/publication BEFORE26rowbattery/fourfloatingcalls;
resultreview beforepublication. No postfreeze repair, droppedlosses, floatrescue,
physicaltruth/medical/novelty/sciencecompletion claims. Exact suppliedmodel algebra
and external witness checking only, unresolved witness staysunavailable. Fraction/
loader/resource caps notcompleteOSprovenance/peakmemory/adversarialsandbox proof.
