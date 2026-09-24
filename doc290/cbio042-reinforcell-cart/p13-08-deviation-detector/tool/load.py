"""Load IndPenSim V3 process variables (Raman columns dropped). The source header splits one name across commas,
so columns are re-named by position: c32 Fault_ref, c33 Control_ref, c34 PAT_ref, c35 Batch_ref, c36 Batch_ID, c37 Fault_flag."""
import pandas as pd
def load(p="data/ips_process.csv"):
    d=pd.read_csv(p,header=None,skiprows=1,usecols=range(37))
    raw=[c.strip() for c in open(p).readline().split(",")][:31]
    names=[r.split("(")[1].split(":")[0] if "(" in r else r for r in raw]
    names[0]="Time"; d.columns=names+["Fault_ref","Control_ref","PAT_ref","Batch_ref","Batch_ID","Fault_flag"]
    return d
