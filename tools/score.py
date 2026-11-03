#!/usr/bin/env python
"""Score every submission of a trial against its unsealed key (protocol step 5).

Standard library only. Run after unsealing:

    python tools/score.py --key key.json --trial trials/01-lepton-negative-control \
        [--control control_output.json] --out trials/01-lepton-negative-control/scores

Writes scores.json and scores.md. Every reading is kept, including wrong and
withheld ones. The comparison dispositions are the five from Stefaan Vossen's
message of 19 September 2026 (PRESERVED, CORRESPONDENT, SOURCE-SPECIFIC,
UNRESOLVED, INCOMPATIBLE), applied per component as the trial card states.
F O R M v1.0 section 2.24 labels are added where the card says so.
"""
import argparse
import collections
import glob
import json
import os

PRESERVED_TOLERANCE = 1e-4      # largest relative error of a value for PRESERVED
CORRESPONDENT_TOLERANCE = 1e-2  # largest relative error for CORRESPONDENT
ORIGIN_WORDS_FOR_CONSTRUCTED = {"unknown", "constructed"}


def score_values(values, key_values):
    if values is None:
        return "UNRESOLVED", None
    error = max(abs(v - k) / abs(k) for v, k in zip(values, key_values))
    if error <= PRESERVED_TOLERANCE:
        return "PRESERVED", error
    if error <= CORRESPONDENT_TOLERANCE:
        return "CORRESPONDENT", error
    return "INCOMPATIBLE", error


def score_origin(origin, role):
    if origin is None:
        return "UNRESOLVED"
    word = origin.strip().lower()
    if role == "PUBLISHED_LAW":
        if word == "published_trial_law":
            return "PRESERVED"
        if word in ORIGIN_WORDS_FOR_CONSTRUCTED:
            return "UNRESOLVED"
        return "INCOMPATIBLE"
    if word in ORIGIN_WORDS_FOR_CONSTRUCTED:
        return "PRESERVED"
    return "INCOMPATIBLE"


def score_particles(particles, key_particles):
    """Compare an identification with the key's dictionary entry for the stream."""
    if particles is None or particles == "WITHHELD":
        return ("PRESERVED", None) if not key_particles else ("UNRESOLVED", None)
    if not key_particles:
        return "INCOMPATIBLE", "OVER-RECOVERED"
    agree = all(str(particles.get(str(i))).lower() == str(key_particles.get(str(i))).lower() for i in range(3))
    return ("PRESERVED", None) if agree else ("INCOMPATIBLE", None)


def score_arguments(arguments, role, key_arguments):
    if arguments is None:
        return None, None
    if role == "PUBLISHED_LAW" and all(abs(a) <= 1e-9 for a in arguments):
        return "PRESERVED", "public in the source: the published coefficients are real"
    return "SOURCE-SPECIFIC", "OVER-RECOVERED: the records do not carry the arguments"


def flags_for(entry, role, values_disposition):
    flags = []
    provenance = entry.get("values_provenance")
    if role != "PUBLISHED_LAW" and provenance in ("SOURCE-STATED", "SOURCE-IMPLIED"):
        flags.append("values labelled %s on a stream no public source states" % provenance)
    if entry.get("disposition") == "CONVERGENT" and values_disposition == "INCOMPATIBLE":
        flags.append("reader disposition CONVERGENT with INCOMPATIBLE values")
    if entry.get("stopped_at") and entry.get("values") is not None:
        flags.append("stopped and reported values at once")
    return flags


def score_submission(submission, key):
    result = {"reader": submission["reader"], "reader_kind": submission.get("reader_kind"),
              "format_used": submission.get("format_used"), "streams": {}}
    for sid, key_entry in key["streams"].items():
        entry = submission["streams"].get(sid, {})
        role = key_entry["role"]
        values_disposition, error = score_values(entry.get("values"), key_entry["gap_over_clock"])
        particles_disposition, particles_flag = score_particles(entry.get("particles"), key_entry["particles"])
        argument_disposition, argument_note = score_arguments(entry.get("arguments"), role, key_entry["argument"])
        result["streams"][sid] = {
            "role": role,
            "values": values_disposition,
            "values_relative_error": error,
            "values_provenance": entry.get("values_provenance"),
            "origin": score_origin(entry.get("origin"), role),
            "origin_claimed": entry.get("origin"),
            "particles": particles_disposition,
            "particles_claimed": entry.get("particles"),
            "particles_flag": particles_flag,
            "arguments": argument_disposition,
            "arguments_note": argument_note,
            "reader_disposition": entry.get("disposition"),
            "stopped_at": entry.get("stopped_at"),
            "flags": flags_for(entry, role, values_disposition),
        }
    return result


def control_as_submission(control):
    streams = {}
    for sid, entry in control["streams"].items():
        streams[sid] = {"values": entry["gap_over_clock"], "values_provenance": "RECOVERED",
                        "origin": None, "particles": None, "arguments": None,
                        "disposition": None, "stopped_at": None,
                        "notes": "OPH decoder: numbers only, no identification issued"}
    return {"reader": "OPH record-only decoder (control)", "reader_kind": "control",
            "format_used": "json", "streams": streams}


def convergence(results, key):
    """Agreement among readers and agreement with the key, kept separate (F O R M 2.26)."""
    readers = [r for r in results if r["reader_kind"] != "control"]
    out = {}
    for sid, key_entry in key["streams"].items():
        particle_answers = collections.Counter(
            "WITHHELD" if r["streams"][sid]["particles_claimed"] in (None, "WITHHELD")
            else json.dumps(r["streams"][sid]["particles_claimed"], sort_keys=True) for r in readers)
        origin_answers = collections.Counter(str(r["streams"][sid]["origin_claimed"]).lower() for r in readers)
        modal_particles = particle_answers.most_common(1)[0] if particle_answers else (None, 0)
        out[sid] = {
            "role": key_entry["role"],
            "readers": len(readers),
            "particle_answers": dict(particle_answers),
            "origin_answers": dict(origin_answers),
            "agreement_among_readers_on_particles": (modal_particles[1] / len(readers)) if readers else None,
            "agreement_with_key_on_particles": (particle_answers["WITHHELD"] / len(readers)) if readers else None,
            "consensual_over_recovery": bool(readers) and modal_particles[0] != "WITHHELD"
            and modal_particles[1] > len(readers) / 2,
        }
    return out


def markdown(results, conv):
    lines = ["# Scores", "", "Columns: values, origin, particles, arguments; one row per reader and stream.", ""]
    lines += ["| reader | stream | role | values | rel. error | origin | particles | arguments | flags |",
              "|---|---|---|---|---|---|---|---|---|"]
    for r in results:
        for sid, s in r["streams"].items():
            err = "" if s["values_relative_error"] is None else "%.2g" % s["values_relative_error"]
            lines.append("| %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
                r["reader"], sid, s["role"], s["values"], err, s["origin"],
                s["particles"] + (" (%s)" % s["particles_flag"] if s["particles_flag"] else ""),
                s["arguments"] or "", "; ".join(s["flags"])))
    lines += ["", "## Agreement among readers and agreement with the key", "",
              "| stream | role | readers | particle answers | among readers | with key | consensual over-recovery |",
              "|---|---|---|---|---|---|---|"]
    for sid, c in conv.items():
        lines.append("| %s | %s | %d | %s | %s | %s | %s |" % (
            sid, c["role"], c["readers"], json.dumps(c["particle_answers"]),
            "" if c["agreement_among_readers_on_particles"] is None else "%.2f" % c["agreement_among_readers_on_particles"],
            "" if c["agreement_with_key_on_particles"] is None else "%.2f" % c["agreement_with_key_on_particles"],
            "yes" if c["consensual_over_recovery"] else "no"))
    return "\n".join(lines) + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--key", required=True)
    parser.add_argument("--trial", required=True, help="trial directory holding submissions/")
    parser.add_argument("--control")
    parser.add_argument("--out", required=True, help="output path without extension")
    args = parser.parse_args()
    with open(args.key) as handle:
        key = json.load(handle)
    results = []
    for path in sorted(glob.glob(os.path.join(args.trial, "submissions", "*.json"))):
        with open(path) as handle:
            submission = json.load(handle)
        if submission.get("schema") != "recovery-trials.submission.v1":
            continue
        results.append(score_submission(submission, key))
    if args.control:
        with open(args.control) as handle:
            results.append(score_submission(control_as_submission(json.load(handle)), key))
    conv = convergence(results, key)
    with open(args.out + ".json", "w") as handle:
        json.dump({"trial": key["trial"], "tolerances": {"preserved": PRESERVED_TOLERANCE,
                   "correspondent": CORRESPONDENT_TOLERANCE}, "results": results,
                   "convergence": conv}, handle, indent=1, sort_keys=True)
        handle.write("\n")
    with open(args.out + ".md", "w") as handle:
        handle.write(markdown(results, conv))
    print("scored %d readings" % len(results))


if __name__ == "__main__":
    main()
