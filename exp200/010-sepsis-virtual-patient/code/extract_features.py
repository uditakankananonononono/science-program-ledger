import os, sys, math, csv
COLS="HR O2Sat Temp SBP MAP DBP Resp EtCO2 BaseExcess HCO3 FiO2 pH PaCO2 SaO2 AST BUN Alkalinephos Calcium Chloride Creatinine Bilirubin_direct Glucose Lactate Magnesium Phosphate Potassium Bilirubin_total TroponinI Hct Hgb PTT WBC Fibrinogen Platelets Age Gender Unit1 Unit2 HospAdmTime ICULOS SepsisLabel".split()
IX={c:i for i,c in enumerate(COLS)}
VITALS="HR O2Sat Temp SBP MAP DBP Resp".split()
LABS="EtCO2 BaseExcess HCO3 FiO2 pH PaCO2 SaO2 AST BUN Alkalinephos Calcium Chloride Creatinine Bilirubin_direct Glucose Lactate Magnesium Phosphate Potassium Bilirubin_total TroponinI Hct Hgb PTT WBC Fibrinogen Platelets".split()
def f(x):
    try: return float(x)
    except: return math.nan
def parse(path):
    rows=[]
    for i,line in enumerate(open(path)):
        if i==0: continue
        rows.append([f(v) for v in line.rstrip('\n').split('|')])
    return rows
def news(hr,resp,temp,sbp,o2,fi):
    s=0
    s+= 3 if resp<=8 else 1 if resp<=11 else 0 if resp<=20 else 2 if resp<=24 else 3
    s+= 3 if o2<=91 else 2 if o2<=93 else 1 if o2<=95 else 0
    s+= 3 if temp<=35 else 1 if temp<=36 else 0 if temp<=38 else 1 if temp<=39 else 2
    s+= 3 if sbp<=90 else 2 if sbp<=100 else 1 if sbp<=110 else 0 if sbp<=219 else 3
    s+= 3 if hr<=40 else 1 if hr<=50 else 0 if hr<=90 else 1 if hr<=110 else 2 if hr<=130 else 3
    if fi>0.21: s+=2
    return s
def sofa_partial(plt,bili,mapv,crea):
    s=0
    s+= 0 if plt>=150 else 1 if plt>=100 else 2 if plt>=50 else 3 if plt>=20 else 4
    s+= 0 if bili<1.2 else 1 if bili<2.0 else 2 if bili<6.0 else 3 if bili<12.0 else 4
    s+= 0 if mapv>=70 else 1
    s+= 0 if crea<1.2 else 1 if crea<2.0 else 2 if crea<3.5 else 3 if crea<5.0 else 4
    return s
def extract(path):
    rows=parse(path)
    if not rows: return None,'empty'
    label=int(max(r[IX['SepsisLabel']] for r in rows))
    if label==1:
        t0=min(r[IX['ICULOS']] for r in rows if r[IX['SepsisLabel']]==1)
        win=[r for r in rows if r[IX['ICULOS']]<t0]
        if len(win)<2: return None,'no_window'
    else:
        win=rows
    t_end=win[-1][IX['ICULOS']]; t_start=win[0][IX['ICULOS']]
    def series(c):
        i=IX[c]; return [(r[IX['ICULOS']],r[i]) for r in win if not math.isnan(r[i])]
    def last(c):
        s=series(c); return s[-1][1] if s else math.nan
    feats={}
    feats['Age']=win[0][IX['Age']]; feats['Gender']=win[0][IX['Gender']]
    feats['Unit1']=win[0][IX['Unit1']]; feats['Unit2']=win[0][IX['Unit2']]
    feats['HospAdmTime']=win[0][IX['HospAdmTime']]
    feats['window_hours']=t_end-t_start
    for v in VITALS:
        s=series(v)
        if s:
            vals=[x[1] for x in s]
            feats[f'{v}_last']=vals[-1]; feats[f'{v}_min']=min(vals); feats[f'{v}_max']=max(vals)
            feats[f'{v}_mean']=sum(vals)/len(vals)
            feats[f'{v}_slope']=(vals[-1]-vals[0])/(s[-1][0]-s[0][0]) if s[-1][0]>s[0][0] else 0.0
            feats[f'{v}_n']=len(s); feats[f'{v}_hrs_since']=t_end-s[-1][0]
        else:
            for k in ('last','min','max','mean','slope','n','hrs_since'): feats[f'{v}_{k}']=math.nan
    for v in LABS:
        s=series(v)
        if s:
            vals=[x[1] for x in s]
            feats[f'{v}_last']=vals[-1]; feats[f'{v}_min']=min(vals); feats[f'{v}_max']=max(vals)
            feats[f'{v}_n']=len(s); feats[f'{v}_hrs_since']=t_end-s[-1][0]
        else:
            for k in ('last','min','max','n','hrs_since'): feats[f'{v}_{k}']=math.nan
    # clinical scores at cutoff (last observed in window)
    g=lambda c: (series(c)[-1][1] if series(c) else math.nan)
    hr,resp,temp,sbp,o2,fi,wbc=g('HR'),g('Resp'),g('Temp'),g('SBP'),g('O2Sat'),g('FiO2'),g('WBC')
    sirs=(0 if math.isnan(temp) else (temp>38 or temp<36))+(0 if math.isnan(hr) else hr>90)+(0 if math.isnan(resp) else resp>20)+(0 if math.isnan(wbc) else (wbc>12 or wbc<4))
    feats['SIRS']=sirs
    feats['qSOFA']=(0 if math.isnan(resp) else resp>=22)+(0 if math.isnan(sbp) else sbp<=100)
    feats['NEWS']=news(hr if not math.isnan(hr) else 75, resp if not math.isnan(resp) else 16, temp if not math.isnan(temp) else 37, sbp if not math.isnan(sbp) else 120, o2 if not math.isnan(o2) else 98, fi if not math.isnan(fi) else 0.21)
    plt_,bili,mapv,crea=g('Platelets'),g('Bilirubin_total'),g('MAP'),g('Creatinine')
    feats['SOFA_partial']=sofa_partial(plt_ if not math.isnan(plt_) else 200, bili if not math.isnan(bili) else 0.5, mapv if not math.isnan(mapv) else 80, crea if not math.isnan(crea) else 0.9)
    return feats,label
def run(setdir,out):
    files=sorted(os.listdir(setdir))
    keys=None; n=0; excl=0
    with open(out,'w',newline='') as fo:
        w=None
        for fn in files:
            feats,lab=extract(os.path.join(setdir,fn))
            if feats is None: excl+=1; continue
            if w is None:
                keys=['pid']+list(feats.keys())+['label']
                w=csv.DictWriter(fo,fieldnames=keys); w.writeheader()
            feats['pid']=fn[:-4]; feats['label']=lab
            w.writerow(feats); n+=1
    print(out,'patients',n,'excluded',excl)
if __name__=='__main__':
    run(sys.argv[1],sys.argv[2])
