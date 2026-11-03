# Submissions

One JSON file per reader, named after the reader, in the format of
`../submission_template.json`. Check it before sending:

    python tools/check_submission.py --streams trials/01-lepton-negative-control/streams.json \
        trials/01-lepton-negative-control/submissions/<handle>.json

Send it as a pull request, or by email to the trial authors if you prefer
that your reading is published only at unsealing. A Markdown file of the same
name may accompany it with the reasoning, the stop points and anything the
JSON fields do not hold.
