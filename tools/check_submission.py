#!/usr/bin/env python
"""Check a submission file before it is sent in.

    python tools/check_submission.py --streams trials/01-lepton-negative-control/streams.json \
        trials/01-lepton-negative-control/submissions/<handle>.json

Standard library only. Exit status 1 when something is wrong.
"""
import argparse
import json
import sys

PROVENANCE = {"SOURCE-STATED", "SOURCE-IMPLIED", "RECOVERED", "EVALUATOR-INFERRED"}
DISPOSITIONS = {"CONVERGENT", "PARTIAL", "NON-UNIQUE", "UNDER-RECOVERED", "OVER-RECOVERED",
                "SEMANTIC DISPLACEMENT", "INCOMPATIBLE", "UNRECONSTRUCTABLE", "JURISDICTION DRIFT",
                "CONSENSUAL OVER-RECOVERY", "UNRESOLVED"}
READER_KINDS = {"human", "ai", "human+ai"}
FORMATS = {"json", "csv"}


def triple(value):
    return isinstance(value, list) and len(value) == 3 and all(isinstance(x, (int, float)) for x in value)


def check(submission, streams):
    problems = []
    for field in ("schema", "trial", "reader", "reader_kind", "date", "format_used", "card_used",
                  "operation", "streams"):
        if field not in submission:
            problems.append("missing field: %s" % field)
    if problems:
        return problems
    if submission["schema"] != "recovery-trials.submission.v1":
        problems.append("schema must be recovery-trials.submission.v1")
    if submission["trial"] != streams["trial"]:
        problems.append("trial must be %s" % streams["trial"])
    if submission["reader_kind"] not in READER_KINDS:
        problems.append("reader_kind must be one of %s" % sorted(READER_KINDS))
    if submission["format_used"] not in FORMATS:
        problems.append("format_used must be one of %s" % sorted(FORMATS))
    if not isinstance(submission["card_used"], bool):
        problems.append("card_used must be true or false")
    if not submission["operation"].strip():
        problems.append("operation must say what was done with the records")
    for sid in streams["streams"]:
        entry = submission["streams"].get(sid)
        if entry is None:
            problems.append("%s: missing (a withheld reading is an entry too)" % sid)
            continue
        values = entry.get("values")
        if values is not None and not triple(values):
            problems.append("%s: values must be null or three numbers" % sid)
        if entry.get("uncertainty") is not None and not triple(entry["uncertainty"]):
            problems.append("%s: uncertainty must be null or three numbers" % sid)
        if entry.get("arguments") is not None and not triple(entry["arguments"]):
            problems.append("%s: arguments must be null or three numbers" % sid)
        for field in ("values_provenance", "origin_provenance", "particles_provenance"):
            if entry.get(field) is not None and entry[field] not in PROVENANCE:
                problems.append("%s: %s must be null or one of %s" % (sid, field, sorted(PROVENANCE)))
        if values is not None and entry.get("values_provenance") is None:
            problems.append("%s: values need a provenance label" % sid)
        if "origin" not in entry:
            problems.append("%s: origin is required (null, unknown, constructed, published_trial_law or text)" % sid)
        particles = entry.get("particles")
        if particles != "WITHHELD" and not (isinstance(particles, dict)
                                            and set(particles) == {"0", "1", "2"}
                                            and all(isinstance(v, str) for v in particles.values())):
            problems.append('%s: particles must be "WITHHELD" or {"0": name, "1": name, "2": name}' % sid)
        if entry.get("disposition") not in DISPOSITIONS:
            problems.append("%s: disposition must be one of %s" % (sid, sorted(DISPOSITIONS)))
        if entry.get("stopped_at") is not None and not isinstance(entry["stopped_at"], str):
            problems.append("%s: stopped_at must be null or text" % sid)
    extra = set(submission["streams"]) - set(streams["streams"])
    if extra:
        problems.append("unknown streams: %s" % sorted(extra))
    return problems


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--streams", required=True)
    parser.add_argument("submission")
    args = parser.parse_args()
    with open(args.streams) as handle:
        streams = json.load(handle)
    with open(args.submission) as handle:
        submission = json.load(handle)
    problems = check(submission, streams)
    for problem in problems:
        print(problem)
    if problems:
        sys.exit(1)
    print("submission is well formed: %d streams" % len(submission["streams"]))


if __name__ == "__main__":
    main()
