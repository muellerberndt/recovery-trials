#!/usr/bin/env python
"""Run OPH's record-only decoder on every stream of a trial (protocol step 4).

The decoder is `infer_ratios` in model/common_source/chiral_candidate/history.py
of the pinned release. It sees the record probabilities and the clock
calibration, and nothing else. Its output is sealed with the key and scored
like any other reading after unsealing.

    PYTHONPATH=<oph> <oph>/.venv/bin/python tools/control_decode.py --oph <oph> \
        --streams trials/01-lepton-negative-control/streams.json --out control_output.json
"""
import argparse
import json
import sys

PHASE_CONTRACT = {
    "pair_phases_principal_branch_proved_for_declared_trial": True,
    "basis": "the trial card states that every stream satisfies the window "
             "0 < pair phase < 1/4; the pinned release proves it for the published "
             "trial law and the trial authors assert it for the sealed streams",
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--oph", required=True)
    parser.add_argument("--streams", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    sys.path.insert(0, args.oph)
    from model.common_source.chiral_candidate import history

    with open(args.streams) as handle:
        streams = json.load(handle)
    calibration = streams["instrument"]["clock_calibration"]
    out = {
        "schema": "recovery-trials.control.v1",
        "trial": streams["trial"],
        "decoder": "model.common_source.chiral_candidate.history.infer_ratios at "
                   + streams["instrument"]["commit"],
        "phase_contract": PHASE_CONTRACT,
        "streams": {},
    }
    for sid, entry in streams["streams"].items():
        probabilities = {tuple(int(ch) for ch in record): p for record, p in entry["records"].items()}
        decoded = history.infer_ratios(probabilities, calibration, PHASE_CONTRACT)
        out["streams"][sid] = {
            "gap_over_clock": decoded["native_family_order_gap_over_clock"],
            "pair_phases": decoded["measured_pair_phases"],
            "clock_phase": decoded["measured_clock_phase"],
        }
        print(sid, ["%.9g" % v for v in decoded["native_family_order_gap_over_clock"]])
    with open(args.out, "w") as handle:
        json.dump(out, handle, indent=1, sort_keys=True)
        handle.write("\n")


if __name__ == "__main__":
    main()
