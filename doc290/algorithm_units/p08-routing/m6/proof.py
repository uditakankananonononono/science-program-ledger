import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('m5_t9_proof',Path(__file__).resolve().parent.parent/'t9'/'proof.py');p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
check=p.check;scenario_check=p.scenario_check;incumbent_check=p.incumbent_check;original=p.original;original_t7_proof=p.original_t7_proof
