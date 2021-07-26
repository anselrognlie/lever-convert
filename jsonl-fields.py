import sys
from sys import stderr
import json
import csv


ERR_GENERAL = 1

FIELD_PROFILE_ID = "profileId"
FIELD_FIELDS = "fields"
VALUE_NOTE = "note"
FIELD_TYPE = "type"
FIELD_VALUE = "value"
HEADER_NOTE_BASE = "note_"


def make_row(record, note_count):
    notes = get_notes_for_record(record)
    fields = [record.get(FIELD_PROFILE_ID)]
    fields.extend(notes)
    fields.extend([""] * (note_count - len(notes)))
    return fields


def make_header(note_count):
    fields = [FIELD_PROFILE_ID]
    fields.extend(f"{HEADER_NOTE_BASE}{i + 1}" for i in range(note_count))
    return fields


def get_notes_for_record(record):
    return [field.get(FIELD_VALUE, "") for field in record.get(FIELD_FIELDS, []) if field.get(FIELD_TYPE).lower() == VALUE_NOTE]


def count_max_notes(db):
    return max(len(get_notes_for_record(rec)) for rec in db)


def jsonl_to_csv_stream(in_file, out_file):
    writer = csv.writer(out_file)

    db = [json.loads(line) for line in in_file]

    # temp code that gathered the field types
    # 'note' was the only one
    # field_types = set()
    # for record in db:
    #     for field in record.get(FIELD_FIELDS, []):
    #         field_types.add(field.get(FIELD_TYPE))
    # print(field_types)
    # return

    max_notes = count_max_notes(db)
    writer.writerow(make_header(max_notes))
    for record in db:
        writer.writerow(make_row(record, max_notes))

    print(f"Processed {len(db)} record(s).", file=stderr)


def jsonl_to_csv(filename):
    with open(filename) as in_file, sys.stdout as out_file:
        jsonl_to_csv_stream(in_file, out_file)


def main(argv):
    if len(argv) < 1:
        print("input filename missing", file=stderr)
        return ERR_GENERAL

    jsonl_to_csv(argv[0])


if __name__ == "__main__":
    main(sys.argv[1:])
