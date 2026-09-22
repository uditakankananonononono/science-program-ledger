library(Biobase)
load('/tmp/deep-research/science-program/SP-002-research/data-feasibility/curated-full/curatedBreastDataExprSetList.rda')
keep <- c('study_16446_GPL570_all','study_20194_GPL96_all','study_22226_GPL1708_all','study_22358_GPL5325_all','study_32646_GPL570_all')
out <- '/tmp/deep-research/science-program/SP-002-research/experiment/data/breast'; dir.create(out,recursive=TRUE,showWarnings=FALSE)
for(nn in keep){
 z=curatedBreastDataExprSetList[[nn]]; x=exprs(z); fd=fData(z); pd=pData(z)
 # collapse duplicate gene symbols by median; remove empty symbols
 g=as.character(fd$gene_symbol); ok=!is.na(g)&g!=''; x=x[ok,,drop=FALSE];g=g[ok]
 ux=unique(g); m=t(sapply(ux,function(gg) apply(x[g==gg,,drop=FALSE],2,median,na.rm=TRUE)))
 colnames(m)=colnames(x); rownames(m)=ux
 write.csv(m,file.path(out,paste0(nn,'__expression.csv')),quote=FALSE)
 write.csv(pd,file.path(out,paste0(nn,'__clinical.csv')),quote=TRUE,row.names=FALSE)
}
