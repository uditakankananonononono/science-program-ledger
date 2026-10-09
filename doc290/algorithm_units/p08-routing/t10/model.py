import importlib.util
from pathlib import Path
SPEC_PATH=Path(__file__).resolve().parent.parent/'t5/certificate.py'
spec=importlib.util.spec_from_file_location('t10_exact_t5',SPEC_PATH);t5=importlib.util.module_from_spec(spec);spec.loader.exec_module(t5)
Invalid,integer,load_bytes=t5.Invalid,t5.integer,t5.load_bytes
class Failure(RuntimeError):pass
def model(s):
    if Path(t5.__file__).resolve()!=SPEC_PATH.resolve() or Path(t5.t2.__file__).resolve()!=(SPEC_PATH.parent.parent/'t2/certificate.py').resolve():raise Failure('unchanged loaded T5/T2 path')
    return t5.model(s)
