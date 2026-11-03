# Trial 01: lepton negative control

Protocol version 1.0. Sealed 3 November 2026.

Six record streams from the clocked lepton history of Observer Patch
Holography, release r2060. One stream is the published trial mass law whose
identification with the electron, muon and tau was tested and excluded in
that release. The other five were constructed by the trial authors from sealed
coefficients. The card says what the instrument is and what a reader is asked
to recover. The key says which stream is what and is sealed until the
deadline.

The question of this trial: can independent readers recover the numerical
content of the records and withhold a physical identification the records do
not license?

## Files

| file | what it is |
|---|---|
| [CARD.md](CARD.md) | the one page a reader works from: instrument, record format, source statements, what to recover, scoring |
| [streams.json](streams.json) | the six streams: 64 record probabilities each, plus the instrument description and clock calibration |
| [streams.csv](streams.csv) | the same numbers, to the same digit, as a flat table |
| [submission_template.json](submission_template.json) | the submission format |
| [submissions/](submissions/) | the readings, one file per reader |
| [COMMITMENT.md](COMMITMENT.md) | the pinned instrument, the hashes of the sealed files, the timestamp proofs |
| [MANIFEST.sha256](MANIFEST.sha256) | hashes of the published files at sealing |

## Taking part

1. Read [CARD.md](CARD.md).
2. Work from `streams.json` or `streams.csv`. Use whatever you like, including
   the instrument's own code in the pinned release. Note which file you used.
3. Copy `submission_template.json` to `submissions/<your handle>.json` and fill
   it in. The fields:

   - `values`: the three pair gaps in clock units, in record order, or null.
   - `uncertainty`: three numbers or null.
   - `values_provenance`, `origin_provenance`, `particles_provenance`: one of
     SOURCE-STATED, SOURCE-IMPLIED, RECOVERED, EVALUATOR-INFERRED, or null.
   - `origin`: `published_trial_law`, `unknown`, `constructed`, or other text.
   - `particles`: `"WITHHELD"`, or `{"0": name, "1": name, "2": name}` naming
     a measured particle for each record position.
   - `arguments`: the three coefficient arguments if you claim them, else null.
   - `disposition`: one of the F O R M 2.24 dispositions for the reading.
   - `stopped_at`: null, or the unstated bridge at which you stopped.
   - `notes`: anything else, including numerical observations you make
     without carrying them into an identification.

4. Check the file:

       python tools/check_submission.py --streams trials/01-lepton-negative-control/streams.json \
           trials/01-lepton-negative-control/submissions/<handle>.json

5. Send it as a pull request. A Markdown file of the same name may carry the
   reasoning. Readers who prefer their reading published only at unsealing
   send it by email to the trial authors; it is hashed on receipt and the hash
   is recorded in this folder.

Readers do not exchange readings before the deadline.

## Deadline and unsealing

The deadline is set on the Information Physics Institute list once the
protocol is agreed, and recorded here. At the deadline the key and the control
output are published in this folder, their hashes are checked against
[COMMITMENT.md](COMMITMENT.md), and `tools/score.py` writes `scores.json` and
`scores.md` next to the submissions.
