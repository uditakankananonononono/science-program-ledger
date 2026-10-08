# Builder correction before freeze review or source run

Initial local a1cc629 test log showed62fixture errors:synthetic selection replacement
was rejected by real freeze-hash check before exercising identity gate. Shell pipeline
without pipefail allowed local commit despite failed tests. No freeze review/publication
or source run occurred. Corrected test harness supplies synthetic selection hash to
match its synthetic selection,leaving production hash enforcement and executable
unchanged. Binding mocked only in identity-gate fixture;separate binding group uses
real pinned metadata. New successful log replaces prior failed log at corrected tip;
failed log remains in local predecessor history. Builder correction,not reviewer request.
Subsequent test pipeline uses pipefail. No data/executable/selection change.
