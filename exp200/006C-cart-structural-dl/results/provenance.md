# Provenance (006C)
- Train: 16 curated Ab-Ag complexes from 006B (RCSB URLs + SHA-256 in exp200/006B-cart-interface/results/provenance.md).
- Frozen external test: https://files.rcsb.org/download/6AL5.pdb
  SHA-256 88e69511d994d69ff398f2d8d55fa9f187bc111c61e283a8d731bea0b7996e51
  (Teplyakov A, Obmolova G, Luo J, Gilliland GL. Proteins 2018;86:495-500, doi:10.1002/prot.25485)
- 6AL5 history: 006B computed features/labels as prep but never fit/selected/tuned/scored
  any model on it (006B WRITEUP: G2 NOT RUN). 006C re-featurized under its own locked spec.
- Environment: torch 2.14.0+cpu, sklearn 1.7.2; all seeds frozen (20260924).
