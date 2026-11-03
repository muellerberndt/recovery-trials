# Card: trial 01, lepton negative control

## The object

Six streams, S1 to S6. Each is a table of the 64 possible six-bit records of
one run of the instrument and the probability of each record. The
probabilities are computed exactly by the instrument's code, to double
precision; nothing is sampled. One stream is the published trial law of OPH
release r2060, run as published. The other five were produced by the same
instrument from coefficients the trial authors chose; those coefficients, the
rule that chose them and the random seed are sealed. Some constructed streams
may coincide numerically with values a reader recognises.

## The instrument

Source: `model/common_source/chiral_candidate/history.py`, function
`_dense_probe`, in the Observer Patch Holography repository at release r2060
(commit `ebb4ebb21753f90a4055259afbef4cfce3112449`). The code is public and
may be read and run. These statements are SOURCE-STATED by OPH.

Three fermion pair modes start empty. Each evolves under a pairing coupling
with its own complex coefficient v for one interval τ = 1/4 of the programmed
modular parameter. Each pair is then read: 0 empty, 1 occupied. If pair 0 read
occupied, a declared neutral phase is applied to pair 1. A second interval
follows and pair 1 is read again. A two-qubit clock has advanced through both intervals;
its X and then its Y quadrature are read: 0 plus, 1 minus. The record is the
six bits in this order:

| position | bit |
|---|---|
| 0 | pair 0 read |
| 1 | pair 1 read |
| 2 | pair 2 read |
| 3 | pair 1 re-read |
| 4 | clock X |
| 5 | clock Y |

Clock calibration: populations 1/6 and 5/6, contrast −2/3, generator
K = constant·I + log(5)·Z/2. The clock does not depend on the pair
coefficients, so its reading is the same in every stream. The clock's
parameter is a programmed modular parameter, with no physical seconds attached.

The quantity to recover for each pair is its gap in clock units, as the pinned
release defines it: the pair's phase over the first interval divided by the
clock's phase over both intervals. For the instrument above this equals the
coefficient's modulus |v| divided by log 5.

Two further facts enter any decoding of these records and are stated here so
that they carry a label. The contrast −2/3 above is SOURCE-STATED by OPH. The
window 0 < 2|v|τ < 1/4 for every pair of every stream, which makes the pair
phase unambiguous, is proved in the pinned release for the published trial law
and asserted by the trial authors for the constructed streams. A reader who
uses it labels it accordingly.

## OPH's own statements about the published law

Each row is SOURCE-STATED by OPH at r2060. The files are listed in
[COMMITMENT.md](COMMITMENT.md) with their hashes.

| # | statement | standing at r2060 |
|---|---|---|
| 1 | Trial law: one real family matrix F, with each sector's Yukawa coupling a fixed multiple of it | Assumed for the trial, not derived |
| 2 | The lepton gaps are in the ratio 1 : 1.1903 : 1.4982 | Exact algebra from row 1 |
| 3 | The law runs as a clocked history with 64 six-bit records | Executed; the full 90-mode law and the probe agree to within 2e-9 |
| 4 | The three gaps can be read back from the records | Executed from exact probabilities, using the contrast and the window above; errors from finite sampling are not certified |
| 5 | The three gaps are the electron, muon and tau masses | Tested against 1 : 206.77 : 3477 and failed; the code records `physical_units_or_observed_mass_identification: False` |
| 6 | Every law of the form uI + wF, u and w complex, fails | Proved: with muon/electron at 206.8, tau/electron is at most 543 |
| 7 | OPH derives the charged-lepton masses | No; open under OPH issue 1143 |
| 8 | The mapping from OPH defects to particles is unique and parameter-free | Expected and unproved; reader agreement cannot establish it |

## What a reader is asked

For each stream:

- `values`: the three gaps in clock units, in record positions 0, 1, 2, with
  an uncertainty, or null.
- `origin`: `published_trial_law` if you hold the stream to be the published
  r2060 law; `unknown` or `constructed` otherwise; or other text if you claim
  a different origin.
- `particles`: a measured particle for each position, or `WITHHELD`.
- `arguments`: the coefficient arguments, if you claim them.
- a provenance label on each of these, a F O R M 2.24 disposition on the
  reading, and the point at which you stopped if you stopped.

Matching a stream to the pinned release's published numbers is allowed. It is
a use of the source and carries the label SOURCE-STATED.

## Scoring

`tools/score.py` is public. Per stream and component, against the key:

- values: largest relative error over the three positions at most 1e-4 is
  PRESERVED, at most 1e-2 is CORRESPONDENT, larger is INCOMPATIBLE, null is
  UNRESOLVED.
- origin: PRESERVED when it matches the key's role; `unknown` on the published
  law is UNRESOLVED; a specific origin the key does not hold is INCOMPATIBLE.
- particles: compared with the key's dictionary for the stream. WITHHELD
  agrees with an empty entry. An identification the key does not hold is
  INCOMPATIBLE and carries OVER-RECOVERED.
- arguments: the records do not carry them. A claim is SOURCE-SPECIFIC and
  OVER-RECOVERED, except the value zero on the published law, which the source
  states.

Flags are added where a provenance label cannot be right (SOURCE-STATED on a
stream no public source states), where the reader's disposition contradicts
the scores, and where a stop and a value are reported at once.

## Sealed

`key.json` and `control_output.json`, hashed in
[COMMITMENT.md](COMMITMENT.md). The control is OPH's own decoder,
`infer_ratios` in the file above, run on the published streams.
