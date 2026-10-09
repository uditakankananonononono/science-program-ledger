import importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parent

def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def load(which):
    p=module('t17_'+which+'_proof',ROOT.parent/which/'proof.py');m=module('t17_'+which+'_method',ROOT.parent/which/'method.py')
    m.proof_check=p.check;m.scenario_check=p.scenario_check;m.incumbent_check=p.incumbent_check
    m.original_t7_proof=p.original_t7_proof if which in ('t9','t11','t12','t13','t14','t15','t16','t17') else p.original
    if Path(m.__file__).resolve()!=(ROOT.parent/which/'method.py').resolve() or Path(p.__file__).resolve()!=(ROOT.parent/which/'proof.py').resolve():raise RuntimeError('method/proof loaded path')
    if which in ('t11','t12','t13','t14','t15','t16','t17'):m.charged_check=p.charged_check
    if which in ('t13','t14','t15','t16','t17'):m.candidates_check=p.candidates_check
    return m,p
