"""Use unchanged pinned P3 admitted model/witness."""
import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location('p3_model',Path(__file__).resolve().parent.parent/'p3'/'model.py');helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
model,witness,integer,Invalid,MAX,EDGE_MAX=(getattr(helper,k) for k in ('model','witness','integer','Invalid','MAX','EDGE_MAX'))
