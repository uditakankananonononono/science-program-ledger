import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def load(which):
    p=module('m5_'+which+'_proof',ROOT.parent/which/'proof.py');m=module('m5_'+which+'_method',ROOT.parent/which/'method.py')
    m.proof_check=p.check;m.scenario_check=p.scenario_check;m.incumbent_check=p.incumbent_check
    m.original_t7_proof=p.original_t7_proof if which=='t9' else p.original
    return m,p
