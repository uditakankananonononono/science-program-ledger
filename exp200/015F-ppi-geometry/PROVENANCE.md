# PROVENANCE — DOC-1-015F
- 015 inputs reused in-repo: exp200/015-ppi-interfaces/data (DeepPPISP data_cache, hash-verified
  per 015's PROVENANCE) + results/dset*_residues.npz (ESM-2 320d + PSSM 20d + labels + offsets).
- Structures: RCSB search API v2 (search.rcsb.org/rcsbsearch/v2/query, sequence service,
  identity>=0.95, evalue<=1e-20, first result_set entity — locked rule), queries 12:29-12:37;
  mmCIFs files.rcsb.org/download/{PDB}.cif, 303 unique PDBs downloaded 12:38-12:40.
- Mapping/coverage tallies: map 360/418; coverage guard 40 dropped; final pools 56/123/141.
- All processing code: /home/sandbox/geo015/{map_structures.py,extract_geo.py} (workspace);
  deliverable pipeline in tools/.
