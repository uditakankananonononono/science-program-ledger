#!/usr/bin/env python3
"""amp_guided_design.py - 014F score-guided AMP refinement tool.
Wraps the locked loop (refine.py): seed FASTA -> N iterations of 15% remask +
ESM-2 8M resample + Macrel greedy accept -> judge shortlist (amPEPpy + AMPlify).
WARNING (014F finding): Macrel-guided refinement climbs the guide (median +0.208)
while independent judges DOWNGRADE the output (both-judges AMP+ 0.575 -> 0.450).
Use for mechanism study, not for design claims scored by the guide itself.
Usage: python3 amp_guided_design.py seeds.fasta [iterations]"""
import os, sys, subprocess
if __name__ == '__main__':
    assert len(sys.argv) > 1, 'need a seed FASTA'
    iters = sys.argv[2] if len(sys.argv) > 2 else '30'
    here = os.path.dirname(os.path.abspath(__file__))
    print(f'running locked refinement loop ({iters} iterations) via refine.py...')
    env = dict(os.environ, REFINE_ITERS=iters)
    subprocess.run([sys.executable, os.path.join(here, 'refine.py')], check=True, env=env)
    print('done - see final.fasta and trajectories.json; score finals with ampep/AMPlify, NOT the guide alone')
