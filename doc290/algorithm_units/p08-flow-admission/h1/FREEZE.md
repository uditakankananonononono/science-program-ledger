# H1 static CSV admission freeze

Prereg c57cedd published/read back;CSV sources NOT yet fetched. Exact3size+MD5
checks precede ANYUTF8/CSV/text analysis;failure produces unavailable/no analysis.
Reviewed transport no redirect/exactURL/identity/truncation/caps carried forward.
20s socket,40s between reads,not hard wall;CPU/RAM stated,not quotas/peak.

csv.reader strict=True is SYNTAX ONLY,not schema/semantic validation. Ragged/blank
records and malformed/nonfinite strings retained,not coercion/repair/suppression.
Quoted multiline fields preserved. CSV physical start/end reader.line_num explicitly
separate from raw Python splitlines ordinals,VT/FF create additional raw boundaries.
Manual citations use exact labeled coordinate convention,never assume equivalence.
API snapshot description ABSENT,not empty string;this corrects prereg shorthand,
no changed data selection/outcome. Root metadata license assertion only.

Six literal groups:transport,MD5/size,UTF8,quoted multiline+CR/CRLF/VT/FF,ragged/
nonfinite strings,malformed quote retention. No network/source execution in tests.
No inference of waveform/units/timing/experiment/controller from CSV syntax. Mandatory
manual evidence ledger over3CSVs+record metadata,not expanded source set.

After review/publication: python3 admit.py NEW_OUTPUT_DIRECTORY
Replay: python3 admit.py NEW_DIRECTORY RETAINED_SOURCES
All original bytes,inputs/inventory/manifest plus manual ledger/scoped result.
No plots,model fits,frequency estimate,RL/proxy score,invention or rights clearance.
