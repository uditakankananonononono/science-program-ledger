import sys;sys.path.insert(0,'..')
from dossier import validate
import pytest
BASE={'schema_version':'1.0','protocol_sha256':'1e4fd59df50e558be7ed7dbae866a2313cd083aa60d932a370adf5b3ad11185f','domain':'heart','config_id':'x','dimensions':dict.fromkeys(['dependence','feature_shift','missingness','prevalence','calibration','instability'],.2),'provenance':['manifest:a']}
def test_valid_deterministic(): assert validate(BASE)==validate(BASE)
def test_missing_dimension_rejected():
 x={**BASE,'dimensions':{**BASE['dimensions']}};del x['dimensions']['calibration']
 with pytest.raises(ValueError):validate(x)
def test_corrupt_protocol_rejected():
 x={**BASE,'protocol_sha256':'bad'}
 with pytest.raises(ValueError):validate(x)
def test_bad_range_rejected():
 x={**BASE,'dimensions':{**BASE['dimensions'],'feature_shift':1.1}}
 with pytest.raises(ValueError):validate(x)
def test_missing_provenance_rejected():
 x={**BASE,'provenance':[]}
 with pytest.raises(ValueError):validate(x)
