# Commitment: trial 01

Sealed 3 November 2026 by Bernhard Mueller.

## Pinned instrument

Observer Patch Holography, https://github.com/FloatingPragma/observer-patch-holography,
release r2060, commit `ebb4ebb21753f90a4055259afbef4cfce3112449` (2 November 2026).

SHA-256 of the files at that commit:

| hash | file |
|---|---|
| `265e73ac87321ebd514b97af2c7c4c0bb376144f60e53d10bfd46662ce2d8db4` | `model/common_source/chiral_candidate/history.py` (instrument and decoder) |
| `1ffdf1a680763d52d0841636aee3dc05a51a16487a5770b2e7208dcb3dbdaacf` | `model/common_source/mass_response/model.py` (clock and carrier parameters) |
| `4a440b7802543789a706434232663b213b39ba7fd317603b9b14de067a113662` | `model/common_source/chiral_candidate/results.json` (the published law's receipt) |
| `5cc000a374aa5523e2ba1fa32bf68b346f65111b94ff8c293815879a638964aa` | `model/common_source/chiral_candidate/ACTION.md` (rows 1, 2, 6) |
| `05e6cfec98103d6c78f1f15d1da2f2a59906efa946e13c16ef5de683fbbee56c` | `model/common_source/chiral_candidate/README.md` (rows 3, 4, 5) |
| `1f4b6305f1c137219262d9c144ac9660b1f69284e9b7352e089af1c2cb476a72` | `model/common_source/particle_identification/SM_MATCH.md` (row 1) |
| `3837d50595bc66801658a1caca430af74201a284dd7f4bfb5405ae075577a4bf` | `docs/research/OPH_PARTICLE_MASS_RESPONSE.md` (rows 5, 6) |
| `026c1d7923a1fe347a1bf3fa6e678c814e89142f1efc332c62808983564badb7` | `docs/EMPIRICAL_STATUS.md` (row 7) |
| `413236fdc23d9f9a30e080dd63c2a28325b926cd9e3a3aaf7d62a778f756c90c` | `docs/POSTDICTION_LEDGER.md` (row 7) |
| `fe37b164c7396111b615c8ffad399ee93ddddfaf653dc954b83f63973ab6292b` | `docs/FROZEN_PREDICTION_LADDER.md` (row 7) |

Row 8 of the card is from OPH issue 1143 and the authors' list message of
1 November 2026.

The published stream regenerates from the pinned code with
`tools/generate.py`; its table agrees with the receipt in `results.json` to
1e-14.

## Sealed files

| SHA-256 | file | content |
|---|---|---|
| `605ad07f2beade0f013061d69a346b692510034f115e54068c92a4b35bfcb8fb` | `key.json` | the role of each stream, the coefficients, the construction rule, the seed and its rule, the authors' dictionary |
| `b3e36927ac5faab594af2ff570a6d6e533f2705e71a1f09be45feca86eebc2a1` | `control_output.json` | OPH's record-only decoder run on `streams.json` (protocol step 4) |
| `f4765d08dea42b5805a8120325d700f1ca13d89cce7d5c5b1a563fdc8f4173c9` | `make_key.py` | the script that wrote `key.json` |

The same three lines are in [SEALED.sha256](SEALED.sha256), and
`SEALED.sha256.ots` is its OpenTimestamps proof. The published files are
listed in [MANIFEST.sha256](MANIFEST.sha256) with `MANIFEST.sha256.ots`.

An OpenTimestamps proof is complete once the calendar's Bitcoin transaction
is confirmed; `ots upgrade <file>.ots` fetches the completed proof and
`ots verify <file>.ots` checks it against the file.

## At unsealing

The three sealed files are added to this folder. Anyone can check their
hashes against the table above, regenerate `streams.json` with
`tools/generate.py --verify`, and rerun `tools/score.py`.
