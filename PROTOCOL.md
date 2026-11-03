# Recovery trial protocol

Version 1.0, 3 November 2026. A trial names the protocol version it runs
under. A change to this text is a new version and applies to later trials
only.

## Purpose

A trial tests whether the step from a record to an interpretation is licensed
by the record or added by the reader. It does that with a key that exists and
is sealed before anyone reads, so that the design cannot be fitted to the
result and the result cannot be explained away.

Three things keep their own identity throughout. The source framework answers
for its instrument and its records. F O R M v1.0 supplies the provenance
labels and dispositions that record the standing of each reading. MORPH
supplies the order of the transformation. A trial does not validate any of
them. Physical validity belongs to measurement and is outside a trial.

## Roles

The trial authors hold the instrument and the key. Readers work from the
published material. The control is the authors' own record-only decoder, which
reads the same records and nothing else. A trial author cannot be a reader of
that trial.

## The five steps

### 1. M, the representation available

The authors publish:

- the record streams, with the identity of each stream removed and the order
  shuffled;
- a one-page card: what the instrument is, what each record bit means, which
  facts the source states, what a reader is asked to recover, and the scoring
  rules with their tolerances;
- the pinned commit of the instrument's repository and SHA-256 hashes of the
  files that define the instrument and the source's own status statements;
- SHA-256 hashes of the sealed files, and an OpenTimestamps proof of the file
  that lists them.

The sealed files are the key (which stream is what, how the constructed
streams were made, the random seed and its rule, the authors' own dictionary)
and the control output. Nothing in a sealed file changes after sealing. If the
authors find an error in a sealed trial, they say so in the repository and the
trial is either scored as sealed or declared void; a corrected trial is a new
trial.

### 2. ⊙, the transformation performed

A reader works from the streams and the card. Any tool is allowed, including
the instrument's own public code. The submission states the operation in the
reader's words and names the software used. Readers do not exchange readings
before the deadline.

### 3. R, what the records license

For each stream the reader writes down what the records entitle them to
recover. Every component carries one of the F O R M 2.3 provenance labels:
SOURCE-STATED, SOURCE-IMPLIED, RECOVERED or EVALUATOR-INFERRED. The reading as
a whole carries one of the 2.24 dispositions. A reader may withhold any
component; a withheld component is an entry, scored like any other. Under the
FER stop rule a step that needs an unstated bridge stops there and is recorded
as stopped, with the missing bridge named.

### 4. Control

The authors run their record-only decoder on the published streams. Its
output is hashed, listed with the sealed files, and scored at unsealing like
any other reading.

### 5. PH → M₁, unsealing and the successor record

After the deadline the authors publish the key and the control output, and a
script scores every reading. The scores, all submissions, the key and the
authors' own corrections stay in the repository. Nothing is removed.

## Scoring

Each component of a reading gets one of the five comparison dispositions from
Stefaan Vossen's message of 19 September 2026, applied against the key:

- PRESERVED: the reading and the key agree within the stated tolerance.
- CORRESPONDENT: the reading is close to the key without reaching the
  tolerance for PRESERVED, as the card defines.
- SOURCE-SPECIFIC: the reading reports a component that the key holds and the
  records do not carry, or that the records carry and the key does not hold.
- UNRESOLVED: the component is withheld, or the submission does not settle it.
- INCOMPATIBLE: the reading and the key disagree.

Where a reading attributes structure, status or origin that the key does not
hold, the scorer adds the F O R M 2.24 label OVER-RECOVERED. The card of each
trial lists the components and the tolerances; the scorer is published with
the trial, so a reader can see before submitting how each field will be
scored.

Agreement among readers and agreement with the key are reported separately
(F O R M 2.26). A majority of readers agreeing on a component the key does not
hold is recorded as CONSENSUAL OVER-RECOVERY.

## What a trial does not establish

Recovering the authors' sealed dictionary shows correspondence with a declared
reference. It does not show that the dictionary is uniquely recoverable from
the records; that needs its own argument, and reader agreement cannot supply
it. A trial also says nothing about whether the source framework's physics is
right. That is decided by measurement against predictions frozen before the
test.

## Presentation

A trial may publish the same records in several formats. Their content is
identical to the digit. A trial that withholds the card from some readers
treats that as a separate variable and says so in advance.

## Reflexivity

The protocol submits to the same reading it asks of others. Its drafting
history is the git log of this repository, the hashes are in the trial
folders, and the authors' errors stay where they were made.
