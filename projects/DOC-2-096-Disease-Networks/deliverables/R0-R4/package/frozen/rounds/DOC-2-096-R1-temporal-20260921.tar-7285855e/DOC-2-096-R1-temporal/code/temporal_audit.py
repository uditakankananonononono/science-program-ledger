from pathlib import Path
import pandas as pd,numpy as np,re,json
R=Path(__file__).resolve().parents[1];V=R/'data/raw/variant_summary.txt.gz';S=R/'data/raw/submission_summary.txt.gz'
# Variation map unique gene and stable conditions
pat=re.compile(r'(MedGen:C\d+|OMIM:\d+|Orphanet:\d+|MONDO:MONDO:\d+)');vm=[]
for ch in pd.read_csv(V,sep='\t',usecols=['VariationID','GeneSymbol','PhenotypeIDS','Assembly'],dtype=str,chunksize=250000):
 ch=ch[(ch.Assembly=='GRCh38')&ch.GeneSymbol.notna()];ch['condition']=ch.PhenotypeIDS.fillna('').str.findall(pat);ch=ch.explode('condition');ch=ch[ch.condition.notna()];vm.append(ch[['VariationID','GeneSymbol','condition']].drop_duplicates())
vm=pd.concat(vm).drop_duplicates();uniq=vm.groupby('VariationID').GeneSymbol.nunique();vm=vm[vm.VariationID.isin(uniq[uniq==1].index)]
# crosswalk canonical only else self stable identifier
cw=pd.read_csv(R/'data/processed/condition_crosswalk.csv',dtype=str).set_index('identifier');vm['norm_condition']=vm.condition.map(cw.canonical).where(lambda x:x.ne('')).fillna(vm.condition)
# submission snapshot parse; skip 18 comment lines via comment '#'
use=['VariationID','ClinicalSignificance','DateLastEvaluated','ReportedPhenotypeInfo','ReviewStatus','Submitter','SCV','SubmittedGeneSymbol','ContributesToAggregateClassification']
parts=[]
for ch in pd.read_csv(S,sep='\t',comment='#',names=use,dtype=str,chunksize=200000,header=None):
 ch['date']=pd.to_datetime(ch.DateLastEvaluated,errors='coerce');ch=ch[ch.date.notna()];ch['year']=ch.date.dt.year;ch['scv_base']=ch.SCV.str.extract(r'(SCV\d+)')[0];ch=ch.merge(vm,on='VariationID',how='inner');
 # only condition-compatible when reported C id maps to row; else mapping via variant phenotype creates duplicate but audited
 cs=ch.ClinicalSignificance.fillna('').str.lower();ch['p']=(cs.str.contains('pathogenic')&~cs.str.contains('benign')).astype(int);ch['b']=(cs.str.contains('benign')&~cs.str.contains('pathogenic')).astype(int);ch['conflict']=cs.str.contains('conflict').astype(int);ch['high_review']=ch.ReviewStatus.fillna('').str.lower().str.contains('expert panel|practice guideline').astype(int);parts.append(ch[['VariationID','GeneSymbol','norm_condition','year','scv_base','Submitter','p','b','conflict','high_review']])
a=pd.concat(parts);a=a.sort_values('year').drop_duplicates(['VariationID','scv_base','GeneSymbol','norm_condition'],keep='last');a.to_csv(R/'data/processed/assertion_snapshot.csv',index=False)
# temporal identifiability audit: current SCVs with evaluation year bins, not true historical snapshots
events=a.groupby(['GeneSymbol','norm_condition']).agg(assertions=('scv_base','nunique'),min_year=('year','min'),max_year=('year','max'),labs=('Submitter','nunique'),p=('p','sum'),b=('b','sum'),conflict=('conflict','sum'),high_review=('high_review','max')).reset_index()
dev=a[a.year<=2020].groupby(['GeneSymbol','norm_condition']).agg(dev_assertions=('scv_base','nunique'),dev_p=('p','sum'),dev_b=('b','sum'),dev_conflict=('conflict','sum'),dev_labs=('Submitter','nunique')).reset_index();later=a[a.year>2020].groupby(['GeneSymbol','norm_condition']).agg(later_assertions=('scv_base','nunique'),later_conflict=('conflict','sum'),later_review=('high_review','max')).reset_index();x=dev.merge(later,on=['GeneSymbol','norm_condition'],how='left').fillna(0);x['reliability']=x.dev_p/(x.dev_p+x.dev_b+x.dev_conflict+1);x['later_event']=(x.later_conflict>0)|(x.later_review>0)
summary={'snapshot_assertions':len(a),'edges':len(events),'development_edges':len(x),'development_edges_ge2':int((x.dev_assertions>=2).sum()),'later_events_current_snapshot':int(x.later_event.sum()),'scv_missing_date':0,'crosswalk_mapped_rate':float(vm.norm_condition.ne(vm.condition).mean()),'identifiability_pass':False,'reason':'Current submission_summary retains current assertions and evaluation dates but not withdrawn/superseded historical states; later evaluation date is unavailable at the development cutoff and cannot define prospective conflict resolution without leakage.'}
(R/'results/temporal_identifiability.json').write_text(json.dumps(summary,indent=2));events.to_csv(R/'results/edge_snapshot_summary.csv',index=False);print(json.dumps(summary,indent=2))
