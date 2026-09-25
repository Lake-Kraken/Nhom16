# Security Requirements for json_search()

## SR-01 - Role-based access control
The json_search() function must verify the caller's role before returning values of protected fields.

## SR-02 - Protect apiKey
The field `apiKey` contains sensitive authentication information.
Only users with the `admin` role are allowed to retrieve this field.

Allowed roles:
- admin

Denied roles:
- operator
- viewer
- unspecified/invalid role

## SR-03 - Protect managementIpAddress
The field `managementIpAddress` contains internal network addressing information.
Only `admin` and `operator` roles may retrieve this field.

Allowed roles:
- admin
- operator

Denied roles:
- viewer
- unspecified/invalid role

## SR-04 - Access to issueSummary
The field `issueSummary` may be accessed by all defined roles.

Allowed roles:
- admin
- operator
- viewer

## SR-05 - Default deny
If a protected field is requested by a role that is not explicitly listed in POLICY,
json_search() must return no protected value.

## SR-06 - Recursive search must preserve authorization
Authorization checks must also apply when a protected key is located inside nested
dictionaries or lists. Recursive traversal must not bypass role checks.
