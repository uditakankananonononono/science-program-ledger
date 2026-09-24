# DOC-1-017 PROVENANCE
- Grammar: hand-locked from literature (GATES.md cites Woolfson 2021; Hecht binary patterning; Richardson & Richardson caps). No learned model in the designer.
- s4pred v1.2.4: github.com/psipred/s4pred (run_model.py, network.py, utilities.py from master) + weights.tar.gz from bioinfadmin.cs.ucl.ac.uk/downloads/s4pred/weights.tar.gz; MD5 e04ad7d10b61551f7e07a86b65bb88dc matches the published checksum. Moffat & Jones, Bioinformatics 2021;37(21):3744.
- ESM-2 esm2_t6_8M_UR50D (Lin et al., Science 2023) pseudo-PLL: R=8 replicates, 15% masking, seeds 7.
- Natural reference: 200 reviewed Swiss-Prot entries (rest.uniprot.org query reviewed:true AND length:[24 TO 200], RNG seed 45), fragments length-matched to designs.
- Sets: 200 designed (seed 42), 200 composition-matched shuffles (seed 43). All sequences in results/*.fasta.
