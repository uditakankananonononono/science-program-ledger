# 199 frozen r04_outer.sh
```
#!/bin/bash
# external enforcement of the 1800 s timeout; records versions
export R04_REPO=$1 R04_OUT=$2
python3 -c "import sklearn,numpy,pandas,sys;print('python',sys.version.split()[0],'sklearn',sklearn.__version__,'numpy',numpy.__version__,'pandas',pandas.__version__)" > ${2}.versions
timeout 1800 python3 $(dirname $0)/r04_run.py > ${2}.log 2>&1; echo "exit $?" >> ${2}.versions
```
