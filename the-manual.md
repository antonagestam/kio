# How to parse the Apache Kafka® Protocol

## Version range specifiers

### Inferring field-level valid versions

Fall back to `"taggedVersions"` if `"versions"` is missing.

https://github.com/apache/kafka/pull/13680

## Common structs

Starting in version 3.5, `AddPartitionsToTxnResponse` introduced forward references in
common structs. Regardless of whether this was intentional, it complicates parsing the
schema a bit.

## "Flexibility"

Changes two things in parsing behavior: tagged fields, and string and array
serialization formats.

### Inferring flexibility

Model-level flexibility and field-level flexibility.

### Tagged fields

### "Compact" strings and arrays

## KIP-893 Nullable entity fields

## Undocumented special cases

### ControlledShutdownRequest non-standard request header

> Version 0 of ControlledShutdownRequest has a non-standard request header which does
> not include clientId. Version 1 of ControlledShutdownRequest and later use the
> standard request header.

https://github.com/apache/kafka/blob/38103ffaa962ef5092baffb884c84f8de3568501/generator/src/main/java/org/apache/kafka/message/ApiMessageTypeGenerator.java#L342-L350

###

> ApiVersionsResponse always includes a v0 header. See KIP-511 for details.

https://github.com/apache/kafka/blob/38103ffaa962ef5092baffb884c84f8de3568501/generator/src/main/java/org/apache/kafka/message/ApiMessageTypeGenerator.java#L335-L341
