#!/usr/bin/env python
"""Generate or verify the record streams of a trial from its key.

The key is sealed until the trial is unsealed; before that only the trial
authors can run this. After unsealing anyone can regenerate the streams and
compare them with the published file.

Needs the pinned OPH release on the path. Run with that repository's Python:

    PYTHONPATH=<oph> <oph>/.venv/bin/python tools/generate.py --oph <oph> \
        --key key.json --out trials/01-lepton-negative-control/streams.json

    ... --key key.json --verify trials/01-lepton-negative-control/streams.json

The instrument is model/common_source/chiral_candidate/history.py of the
pinned release: `_dense_probe` runs the clocked history for one coefficient
triple and returns the 64 record branches.
"""
import argparse
import json
import math
import sys

RECORD_BITS = [
    "pair0_read", "pair1_read", "pair2_read", "pair1_reread", "clock_X", "clock_Y",
]


def stream_table(history, experiment, coefficients, backend):
    branches, _, calibration, _, _, _ = history._dense_probe(coefficients, backend=backend)
    records = {"".join(map(str, key)): experiment.norm(state) for key, state in branches.items()}
    return {key: records[key] for key in sorted(records)}, calibration


def build(key, history, experiment):
    out = {
        "schema": "recovery-trials.streams.v1",
        "trial": key["trial"],
        "instrument": {
            "source": "model/common_source/chiral_candidate/history.py, function _dense_probe",
            "release": key["rer_release"],
            "commit": key["rer_commit"],
            "backend": key["backend"],
            "record_bits": RECORD_BITS,
            "bit_convention": "pair reads: 0 empty, 1 occupied; clock reads: 0 plus, 1 minus",
            "interval": key["interval"],
            "window": key["window"],
        },
        "streams": {},
    }
    calibration = None
    for sid in sorted(key["streams"], key=lambda s: int(s[1:])):
        coefficients = [complex(re, im) for re, im in key["streams"][sid]["coefficients"]]
        records, calibration = stream_table(history, experiment, coefficients, key["backend"])
        out["streams"][sid] = {
            "records": records,
            "total_probability": math.fsum(records.values()),
        }
    out["instrument"]["clock_calibration"] = calibration
    return out


def write_csv(streams, path):
    with open(path, "w") as handle:
        handle.write("stream,record,probability\n")
        for sid, entry in streams["streams"].items():
            for record, probability in entry["records"].items():
                handle.write("%s,%s,%r\n" % (sid, record, probability))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--oph", required=True, help="path of the pinned OPH checkout")
    parser.add_argument("--key", required=True)
    parser.add_argument("--out")
    parser.add_argument("--csv")
    parser.add_argument("--verify", help="existing streams.json to compare against")
    parser.add_argument("--tolerance", type=float, default=1e-12)
    args = parser.parse_args()
    sys.path.insert(0, args.oph)
    from model.common_source.chiral_candidate import history
    from model.common_source.mass_response import experiment

    with open(args.key) as handle:
        key = json.load(handle)
    streams = build(key, history, experiment)
    if args.verify:
        with open(args.verify) as handle:
            published = json.load(handle)
        worst = 0.0
        for sid, entry in streams["streams"].items():
            for record, probability in entry["records"].items():
                worst = max(worst, abs(probability - published["streams"][sid]["records"][record]))
        print("largest difference to the published table: %.3g" % worst)
        if worst > args.tolerance:
            sys.exit("the regenerated streams differ from the published table")
        print("the published table regenerates from the key")
    if args.out:
        with open(args.out, "w") as handle:
            json.dump(streams, handle, indent=1, sort_keys=True)
            handle.write("\n")
    if args.csv:
        write_csv(streams, args.csv)


if __name__ == "__main__":
    main()
