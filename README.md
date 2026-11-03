# Recovery trials

Reading exercises with a sealed key. A trial publishes records produced by a
declared instrument, seals the key that says where each record came from, and
asks independent readers to write down what the records entitle them to
recover. After the deadline the key is unsealed and every reading is scored
against it, the wrong ones and the withheld ones included.

The records of the first trial come from the executable model of Observer
Patch Holography (OPH). The reading vocabulary is F O R M v1.0 and the
transformation sequence M → ⊙ → R → PH → M₁ is MORPH, both by Stefaan Vossen.
Each component keeps its own identity. OPH answers for the instrument and the
records, F O R M for the standing of each reading, MORPH for what survived the
transformation. A trial validates none of the three. It shows whether a step
from records to names is licensed by the records or added by the reader.

## Trials

| trial | object | state |
|---|---|---|
| [01-lepton-negative-control](trials/01-lepton-negative-control/) | six record streams from the clocked lepton history of OPH release r2060; one of them is the published trial law whose particle identification was tested and excluded | sealed, open for readings |

## How a trial runs

The five steps are in [PROTOCOL.md](PROTOCOL.md).

1. M. The trial authors publish the records, a one-page card, and SHA-256
   commitments to the sealed key.
2. ⊙. Readers work from the records and the card alone and state the operation
   they performed.
3. R. Each reader writes down what the records entitle them to recover, with a
   provenance label on every component and a disposition on the reading.
   Withholding is a valid entry.
4. Control. The authors' own record-only decoder runs on the same records. Its
   output is sealed with the key.
5. PH → M₁. The key is unsealed and a script scores every reading. The
   successor record keeps all of them.

## Taking part

Read the trial's card, take the streams, fill in the submission template,
check it with `tools/check_submission.py`, and send it as a pull request.
Human readers, AI readers and mixed teams are welcome; the submission says
which.

## Attribution

Protocol and trial 01: Bernhard Mueller. F O R M v1.0
(https://zenodo.org/records/22875795) and the MORPH sequence are Stefaan
Vossen's and are used unchanged. The five comparison dispositions are from his
message of 19 September 2026 to the Information Physics Institute list. The
stop rule (FER) is Diana Haskins's, as cited in F O R M. The instrument is
from the Observer Patch Holography repository,
https://github.com/FloatingPragma/observer-patch-holography.

Code is under the MIT licence, documents and data under CC BY 4.0. See
[LICENSE](LICENSE).
