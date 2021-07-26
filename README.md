# jsonl-fields

## Usage

```
python3 jsonl-fields <input_file>
```

## Summary

This tool loads the supplied JSONL file into memory, and emits a CSV-formatted content to standard output consisting of the `profileId` and any `note` fields for each record.

Note that for extremely large JSONL files, the current implementation may not work if it does not all fit into memory. A future extension could handle larger files if needed.

A message summarizing the total number of records processed is output to standard error.