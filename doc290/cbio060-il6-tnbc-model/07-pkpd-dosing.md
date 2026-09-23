---
id: P21-07
title: "Dose to Signal: Coupling Real Drug Pharmacokinetics to the IL-6 Pathway Model"
parent: "CBIO060 - A Mathematical Model of IL-6 in Breast Cancer (source abstract, 2023)"
---

# Dose to Signal

**Parent project:** CBIO060 IL-6 TNBC Model (48-ODE model of IL-6 signal transduction in triple-negative breast cancer; sensitivity analysis and virtual drug-target screening).

## Premise
The parent's virtual drug screen treats drugs as fixed-strength inhibitors. In patients, drug levels rise and fall with dosing. Ruxolitinib has a short half-life (a few hours); tocilizumab stays for weeks. Whether pathway suppression holds between doses depends on this, and it can change which drug looks best. FDA labels and published PK studies give the needed parameters.

## Hypothesis
Under clinically approved dosing, the model predicts that IL-6R antibody gives sustained pSTAT3 suppression while JAK inhibition allows rebound between doses, and that this reverses the single-dose ranking for at least one drug pair.

## Data sources (free/public)
- FDA labels (Drugs@FDA) for ruxolitinib, tocilizumab, siltuximab PK parameters.
- Published population PK models (open-access papers).
- ChEMBL IC50/Kd values to link concentration to inhibition.

## Method outline
1. Add one- or two-compartment PK models for each drug; convert plasma to free concentration with protein binding from labels.
2. Link free concentration to target inhibition (Emax model with ChEMBL potency; antibody binding kinetics for IL-6R/IL-6).
3. Simulate approved schedules for 4 weeks; track pSTAT3 and IL-6 output time courses.
4. Compare time-averaged suppression vs peak-based rankings.

## Success gates (locked before results)
- G1: PK modules reproduce label-reported Cmax/half-life within 20%.
- G2: ranking change between static and dynamic simulation reported for all drug pairs.
- G3: conclusions robust across P21-01 parameter ensemble (>= 80%).

## Expected deliverable
A PK/PD-coupled IL-6 model and schedule-dependent drug comparison plots.

## Failure/pivot rule
If PK makes no difference to rankings, report that static screens are adequate for this pathway - a useful simplification for future models.
