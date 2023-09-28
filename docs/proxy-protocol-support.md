# Support for PROXY protocol

The proxy protocol allows an intermediate proxying server speaking proxy protocol (ie. HAProxy) between the server and the ultimate client (i.e. mysql client etc) to provide the source client address to the server, which normally would only see the proxying server address instead.

As the proxy protocol amounts to spoofing the client address, it is disabled by default, and can be enabled on per-host or per-network basis for the trusted source addresses where trusted proxy servers are known to run. Unproxied connections are not allowed from these source addresses.

!!! note

    Ensure that proper firewall access control lists (ACL) are in place when this feature is enabled.

Proxying is supported only for TCP over IPv4 and IPv6 connections. The UNIX socket connections can not be proxied and do not fall under the effect of using the asterisk symbol (*).

You cannot have a proxied IP address that is `127.0.0.1` or `::1`, even if the IP address is in the proxy_protocol_networks.

## Version specific information

* 8.0.12-1: The feature was ported from *Percona Server for MySQL* 5.7.

## System variables

### `proxy_protocol_networks`

| Option       | Description    |
|--------------|----------------|
| Command-line | Yes            |
| Config file  | Yes            |
| Scope        | Global         |
| Dynamic      | No             |
| Default      | (empty string) |

This variable is a global-only, read-only variable, which is either an asterisk symbol(*), or a list of comma-separated IPv4 and IPv6 network and host addresses. For security reasons we do not recommend using an asterisk symbol for the IP address. This symbol causes the server to accept the proxy protocol from any host. Network addresses are specified in CIDR notation, i.e. `192.168.0.0/24`. To prevent source host spoofing, the setting of this variable must be as restrictive as possible to include only trusted proxy hosts.

## Related reading

* [PROXY protocol specification](https://www.haproxy.org/download/1.5/doc/proxy-protocol.txt)
