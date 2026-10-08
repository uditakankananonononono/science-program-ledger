# Q3 fixed full PDF parser freeze

Published prereg7a6b709 unchanged. Actual source body notparsed; onlysynthetic
ReportLab2pagefixture through nativeparser in development. Initial exactdimensions
fixture failed because renderer rounding differs1pixel; prefreeze fixed explicit
±1pixel association, and cappreflight uses(pw+1)*(ph+1)/RGBAplusoverhead so tolerance
not weakening20millionpixel/allocationbound. Renderactualdimensions separatelyrecorded.

Held original+scratch opened/read/hash+fstat beforeEACHparser and afterprocessing;
scratchpathstat bindsheldhandle. Hashcheck entire128786B/SHA256 beforefirstparse,
heldoriginal open throughout. Identityfail ZEROparser; mutation/pathstatfail removes
partialstage. atimechanges may conservativelyfail, not weakened. No freshnetwork.

pdfinfo strictoneEncrypted:no/onePages1..32. Eachpage -box preflight dimensions/
rotationstrictfinitepositivegrammar beforeanyrender; rejectunsupported/ambiguous.
Wholepdf pdftotext -layout -enc UTF-8 stdout; stricttext<=1MiB/10000lines/16384chars.
ExactlyNformfeeds and trailingemptysegment required (Popplerfinalformfeed), LFsplit
retainsblank/finalemptylines/page separators. BlankpagesflaggednotOCRrescued.
ALLpagessequential pdftoppm150dpi PNG, exactpageassociation viaindex/actualdims.
20millionpixel bound preflightBEFORErender; conservativeRGBAbytes+1MiBoverheadmust
fitremaining128MiBbudget beforeeachrender. RLIMIT_FSIZEremainingbudget eachnative
process pluspostfile/pngIHDRpixelcheck. No unlimitedstdout capture, file-backed
<=1MiBtext/info/stderr. RLIMIT_AS2GiB/CPU20s/wall30s/affinity<=2CPU/corefilesoff.
Timeout/interruptionkillsprocessgroup andwaits, finallyremovesscratch. Perprocess
limitsNOTtotalpeakmemory/diskquota universalproof;stderr+scratch/source/control
files bounded buttotalrenderbudgetonlycoversPNGs, notallfilesystembytes. No claim
hard2GiB aggregatepeak. No nativePDF maliciousinputsecurityguarantee.

Actualpdfinfo/pdftotext/pdftoppm/Pythonexecutable andlddresolvedsharedlibrarySHA256
pinned, plusPythonmodulebytes orbuiltinorigin+executablepin. Dynamicfontconfig/fonts
notcomprehensivelypinned: render reproducibility notuniversalcrosssystemproof. Fixed
PATH/LC_ALL=C, no alternativetools/OCR. Fullpdftext/images remainPRIVATE scratch,
onlyowncitedfindings/digests/parsermanifestpublished. ParseroutputsstatusPENDING
ALLPAGEPIXELREVIEW. No readyflag without actualeverypagecoverage+legibilityledger.
Nativeparsefailure exposes no partialinventory; finalstagepromotiononlyallparses.
SIGKILL/powerlossmayleavequarantined .q3-incomplete-* neverreused/notcomplete;
renamenotcrashfsyncdurability. Localconcurrentmalicioustampernotatomicallyprevented.

6tests/multiplesubcasesPASS: infoencrypted/ambiguity/pagecaps, textblank/finalformfeed/
UTF8grammar, dimensioninvalid/hugecaps, identityzeroanalysis, actual2pageblankfixture,
parserfailurecleanup. Binaryandmodulepinsverify beforeproduction. Sourcebodyparse
onlyafterexactfreezereview/publication; resultallpagevisual+manualledgerreviewbefore
publication. Noscience/model/GT/eventtime/searchcost/invention/RuleA-Bendpointcredit.
