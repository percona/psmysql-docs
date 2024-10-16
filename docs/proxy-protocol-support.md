# Support for PROXY protocol

The proxy protocol helps servers see the real client address when a proxy server sits between them. Normally, servers only see the proxy's address. For example, when HAProxy stands between a MySQL client and server, it can use the proxy protocol to show the client's true address to the server.

This protocol is off by default because it can make the server think traffic is coming from somewhere else. You can turn it on for specific hosts or networks where you trust the proxy servers. Once enabled, these addresses can only send proxied connections.

Remember to set up proper firewall rules when you use this feature.

The proxy protocol only works with TCP connections over IPv4 and IPv6. It doesn't work with UNIX socket connections. Also, you can't use localhost addresses (127.0.0.1 or ::1) as proxied IP addresses, even if they're in your allowed proxy network list.

## Version specific information

* 8.0.12-1: The feature was ported from Percona Server for MySQL 5.7.

## System variables

### `proxy_protocol_networks`

| Option       | Description    |
|--------------|----------------|
| Command-line | Yes            |
| Config file  | Yes            |
| Scope        | Global         |
| Dynamic      | No             |
| Default      | (empty string) |

This setting controls which IP addresses can use the proxy protocol. It's a global setting that you can't change while the server is running. You can set it to either a star symbol (*) or a list of specific IP addresses and networks.

For safety, we don't recommend using the star symbol. If you do, your server will accept the proxy protocol from any computer, which could be risky.

When listing networks, use CIDR notation. For example, write "192.168.0.0/24" to include all addresses from 192.168.0.0 to 192.168.0.255.

To keep your server safe from people pretending to be trusted sources, make this list as small as possible. Only include the IP addresses of proxy servers you trust.

Remember, you can list both IPv4 and IPv6 addresses. Separate each address or network with a comma.
