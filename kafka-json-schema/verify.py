from typing import Iterator

from jsonschema import validate
import pathlib
import json


def read_strip_comments(path: pathlib.Path) -> bytes:
    def read_stripped() -> Iterator[bytes]:
        with path.open("rb") as fd:
            for line in fd.readlines():
                if line.lstrip(b" ").startswith(b"//"):
                    continue
                yield line

    return b"".join(read_stripped())


meta_schema_path = pathlib.Path("meta-schema.json")
meta_schema = json.loads(meta_schema_path.read_bytes())


schema_glob = pathlib.Path("schema/3.6.0/").glob("*.json")

for schema_path in schema_glob:
    print(schema_path)
    schema = json.loads(read_strip_comments(schema_path))
    validate(
        instance=schema,
        schema=meta_schema,
    )
