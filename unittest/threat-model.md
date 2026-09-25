# Threat Model for json_search()

## 1. Actors and Roles

### admin
Purpose:
- Full administrative access to network monitoring data.
- May read all fields defined in POLICY.

### operator
Purpose:
- Operate and troubleshoot network infrastructure.
- May access operational information such as managementIpAddress and issueSummary.
- Must not access apiKey.

### viewer
Purpose:
- View general monitoring and incident information.
- May access issueSummary.
- Must not access apiKey or managementIpAddress.

## 2. Sensitive Assets

The JSON data may contain sensitive information, including:

- `apiKey`: SNMP/authentication credential or community string.
- `managementIpAddress`: internal management IP address of a network device.
- Device identifiers and host information.
- Network topology and operational status information.

The `apiKey` is the most sensitive asset because disclosure may expose authentication
material used to access or manage network infrastructure.

## 3. Trust Boundary

A trust boundary exists between the caller of `json_search()` and the monitoring data.

The caller supplies:
- the requested key;
- the JSON object;
- the caller role.

If json_search() performs recursive search without checking the role before returning
a matched value, the trust boundary is bypassed and unauthorized users may receive
protected information.

## 4. Threats

### T1 - Information Disclosure
An unauthorized user such as `viewer` calls:

json_search("apiKey", data, role="viewer")

If role authorization is not enforced, the SNMP community string may be returned.

Impact:
- Disclosure of authentication credentials.
- Possible exposure of network device access information.

Mitigation:
- Check POLICY before returning any protected field.
- Return an empty list when the role is unauthorized.

### T2 - Information Disclosure
A `viewer` requests:

json_search("managementIpAddress", data, role="viewer")

Without authorization checks, the internal management address of a network device
may be disclosed.

Mitigation:
- Allow only `admin` and `operator` roles.

### T3 - Elevation of Privilege
A caller with no valid role, or a lower-privileged role, attempts to request a field
reserved for a higher-privileged role.

Impact:
- A viewer or unauthenticated caller could obtain data intended only for operators
  or administrators.

Mitigation:
- Apply a default-deny policy.
- Only explicitly authorized roles may obtain protected values.

## 5. Security Objective

json_search() must enforce the access-control policy defined in `policy.py` for every
matching result, including results found recursively inside nested dictionaries and lists.
