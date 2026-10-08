# Q5 whole central directory scanner freeze

Publishedprereg4f8315ee. PinnedexactA2original a2-scanner-original.py copied, notruntime
importfromotherpath; scanner.py explicitlyadapted withadditionalcaps/fields/spans,
notassumedunchangedA2behavior. No boundsourceZIPscan/memberread in development.

Entireheldarchive660154652B/SHA256beforeANYparse andposthash+fstat. EOCDboundedtail
uniqueexactEOF/comment; nonZIP64/nonmultipart/bounded16MiBcentral/100kentriesbefore
ZipFile. Rawfields filename<=16384B/extra<=4096B/comment<=4096B BEFOREsliceallocation;
decodedname<=4096characters. Conservative perrecordcharge8192+64*rawvariablebytes,
aggregate<=64MiB BEFORErecordconstruction andZipFilemetadataallocation. Notempirical
Pythonheappeakproof; includesheadroom/escaping/hex/names, selectedcentral<=16MiB held
separately, semanticcapsnot2GiBaggregateRSSproof. JSONiterencode streams<=64MiBoutput
cap beforewrite, no wholeJSONstringconstruction. Single encodedpiece bounded byraw
field caps. Largevaliddirectorycanfailconservativecaps; no sourcefalsityinference.

ALLliteralcentralfields pinned: neededversion/rawDOSdate-time/disks/internalattrs
plusA2names/flags/compression/CRC/sizes/offsets/creator/extras/comments, decoded
ZipInfoordinal/date/repr. ManualscannerandZipFilemetadatafields compared. DOSdate/time
correspondencefixture coversrawliteralvalues. Central-declared minimumlocal spans
[start,start+30+rawname+centralextra+compressedsize) checkedALLwithinbeforecentral
andnonoverlapping. NO localheaderreads: actuallocalextra maydiffer, so conservative
false-rejectionpossible; doesNOTauthenticateactuallocalheaderagreement or descriptors.
Data-descriptorbytes outside minimumspanNOTvalidated, overlappingundocumentedlocal
variablefields cannotbeproved absentwithoutlocalreads. Thisunit onlycentral-declared
spanbounds, notsafeextraction/integrityproof. Rejectduplicate/symlink/encryption/
unsafeabsolute/traversal/extraambiguity/parserfielddisagreement withnopartialinventory.

9tests/multiplesubcasesPASS: ALLliteralrecordcorrespondence, rawvariable/decoded/
central/entry/aggregatecaps, sameoffsetoverlap/outside, beforeidentityzeroanalysis,
actualsamesize sourcemutationpostparse, memberopen/extract/testziptrap, ZipInfodisagree,
ZIP64/multipart/encryption/duplicates/unsafe. Initialtrapfixturebuiltinsidepatched
ZipFile.open failedfixtureconstruction; fixedprefreeze buildbeforetrap. No source
GET/localcontent/memberCRC/decompression/format/image/CSV/model/execution. Allactual
Python/zipfile/struct/hash/module/executablepin identities checkedbeforeproduction.

Failure finallydeletesscratch, nosuccesspartialpromotion. Directoryrename visibility
notcrashfsyncdurability;SIGKILLorphansquarantinedneverreused. No hostilelocalrace/atime
false-rejectionrepair/securityuniversalproof. Rawarchiveprivate/unscanned/originmosaic
limitsunchanged. Exactfreezereview/publicationBEFOREboundarchivescan. Reviewer own
boundedconfirmatoryscanner independent, not implementationreplay scienceclaim.
Resultsmanualwholemetadata ledger exactreviewbeforepublication, NEWmemberselection
prereglater. Noeventtime/GT/searchcost/calibration/endpointRuleA-B/inventioncredit.

## Prepublication repair after exactreview HOLD6185f875

Reviewer syntheticcontrols found two realgaps, no sourcearchiveparseoccurred:
extras length/ZIP64test omittedduplicateIDambiguity, andrawDOSdate/time didn'tgate
ZipInfodecodeddate. scanner.py nowrejectsANYduplicateextraID andcomputes literal
DOSexpectedtuplecomparedtoZipInfo.date_time BEFORE recordoutput. AddeddistinctA/B
ID0x0002duplicatefixture andpatchedinfolistdate-disagreement control. unittest.main
movedafterALLclasses so direct/discovery both11tests. Exactexecutablechanges disclosed;
originalA2copystaysunchangedpinnedasprovenance, adaptedscannerNEWhash. Preregunchanged,
contracts tightenednotnarrowed. Thisreplacementfreeze needsseparatereview before
publication/sourceparse; rejectedfreeze6185f875 wasneverpublished orusedon source.
