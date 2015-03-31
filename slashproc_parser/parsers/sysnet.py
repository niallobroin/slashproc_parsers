#!/usr/bin/env python

from slashproc_parser.basic_parser import BasicSPParser
from parse_helpers import traverse_directory


class Net(BasicSPParser):

    NET = "/proc/sys/net"

    @staticmethod
    def get_groups():
        """Enumerates groups depending on number of directories in /proc/sys/net.

        Returns:
            groups (dict): parsed variables groups
        """
        _, parents, all_variables = traverse_directory(Net.NET)

        # no need to take into account variables
        for var in all_variables:
            del parents[var]

        groups = {'sysnet': {'label': 'Network system variables', 'parents': ['root']}}

        for i in parents.keys():
            groups[Net.key_format(i)] = {
                'label': i,
                'desc': '',
                'parents': parents[i]
            }

        return groups

    @staticmethod
    def get_vars():
        """Enumerates system variables in /proc/sys/net and its subdirectories.

        Returns:
            thevars (dict): parsed system variables with their descriptions
        """

        thevars = dict()
        _, parents, all_variables = traverse_directory(Net.NET)

        for var in all_variables:
            thevars[Net.key_format(var)] = {
                'label': var,
                'unit': '',
                'parents': parents[var]
            }

        # TODO: fill with variables and appropriate descriptions
        descs = {
            'dev_weight': {
                'desc': "Work quantum for packet processing scheduler. The default value is 64",
                'label': "Work Quantum for Packet Processing Scheduler",
                'parents': ['Net']
            },

            'divert_version': {
                'desc': 'Frame diverter version string. Exists only if frame diverter (CONFIG_NET_DIVERT) is compiled in',
                'label': "Frame Diverter Version",
                'parents': ['Net']
            },

            'message_burst': {
                'desc': 'Used to limit the warning messages written to the kernel log from the networking code (together with message_cost parameter). It enforces a rate limit to make a denial-of-service (DoS) attack impossible. Message_burst controls when messages will be dropped. The default value is 10',
                'label': "Warning Messages Limit",
                'parents': ['Net']
            },

            'message_cost': {
                'desc': 'Rate limit the number of network warning messages to one every message_cost seconds. The default value is 5',
                'label': "Warning Message Rate Limit",
                'parents': ['Net']
            },

            'netdev_budget': {
                'desc': 'Net device budget. The default value is 300',
                'label': "Net Device Budget",
                'parents': ['Net']
            },

            'netdev_max_backlog': {
                'desc': 'Maximum number of packets, queued on the input side, when the interface receives packets faster than kernel can process them. Applies to non-NAPI devices only. The default value is 1000',
                'label': "Net Device Maximum BackLog",
                'parents': ['Net']
            },

            'optmem_max': {
                'desc': 'Maximum ancillary buffer size allowed per socket. Ancillary data is a sequence of struct cmsghdr structures with appended data. The default size is 10240 bytes.',
                'label': "Maximum Acillary Buffer Size",
                'parents': ['Net']
            },

            'rmem_default': {
                'desc': 'The default setting of the socket receive buffer in bytes',
                'label': "Socket Receive Buffer Default",
                'parents': ['Net']
            },

            'rmem_max': {
                'desc': 'The maximum receive socket buffer size in bytes. The default value is 131072 bytes',
                'label': "Maximum Receive Socket Buffer",
                'parents': ['Net']
            },

            'somaxconn': {
                'desc': 'Limit of socket listen() backlog, known in userspace as SOMAXCONN. Defaults to 128',
                'label': "Listen() Socket Limit",
                'parents': ['Net']
            },

            'wmem_default': {
                'desc': 'The default setting of the socket send buffer in bytes.',
                'label': "Socket Send Buffer Default",
                'parents': ['Net']
            },

            'wmem_max': {
                'desc': 'The maximum send socket buffer size in bytes. The default value is 131072 bytes',
                'label': "Maximum Send Socket Buffer",
                'parents': ['Net']
            },

            'xfrm_aevent_etime': {
                'desc': 'Used to provide default values for the XFRMA_ETIMER_THRESH in incremental units of time of 100ms. The default value is 10 (1 second)',
                'label': "XFRMA ETIMER THRESH default",
                'parents': ['Net']
            },

            'xfrm_aevent_rseqth': {
                'desc': 'Used to provide default values for XFRMA_REPLAY_THRESH parameter in incremental packet count. The default value is 2 packets',
                'label': "XFRMA REPLAY THRESH default",
                'parents': ['Net']
            },

            'accept_redirects': {
                'desc': 'Accept ICMP redirect messages.',
                'label': "Accept Redirects",
                'parents': ['Net']
            },

            'accept_source_route': {
                'desc': 'Accept packets with SRR option. conf/all/accept_source_route must also be set to 1 to accept packets with SRR option on the interface',
                'label': "Accept Source Route",
                'parents': ['Net']
            },

            'arp_accept': {
                'desc': 'Defines behavior when gratuitous ARP replies are received',
                'label': "Accept ARP",
                'parents': ['Net']
            },

            'arp_announce': {
                'desc': 'Defines different restriction levels for announcing the local source IP address from IP packets in ARP requests sent on interface',
                'label': "Announce ARP",
                'parents': ['Net']
            },

            'arp_filter': {
                'desc': 'Enables and disables arp_filter for the interface. Will be enabled if at least one of conf/{all,interface}/arp_filter is set to 1, it will be disabled otherwise.',
                'label': "Filter ARP",
                'parents': ['Net']
            },

            'arp_ignore': {
                'desc': 'Defines different modes for sending replies in response to received ARP requests that resolve local target IP addresses',
                'label': "Ignore ARP",
                'parents': ['Net']
            },

            'bootp_relay': {
                'desc': 'Accept packets with source address 0.b.c.d destined not to this host as local ones. It is supposed, that BOOTP relay daemon will catch and forward such packets',
                'label': "BootP Relay",
                'parents': ['Net']
            },

            'disable_policy': {
                'desc': 'Disable IPSEC policy (SPD) for this interface',
                'label': "Disable IPSEC Policy",
                'parents': ['Net']
            },

            'disable_xfrm': {
                'desc': 'Disable IPSEC encryption on this interface, whatever the policy',
                'label': "Disable IPSec Encryption",
                'parents': ['Net']
            },

            'force_igmp_version': {
                'desc': 'Force IGMP protocol version.',
                'label': "Force IGMP Version",
                'parents': ['Net']
            },

            'forwarding': {
                'desc': 'Enable IP forwarding on this interface.',
                'label': "IP Forwarding",
                'parents': ['Net']
            },

            'log_martians': {
                'desc': 'Log packets with impossible addresses to kernel log',
                'label': "Log Impossible Adresses Packets",
                'parents': ['Net']
            },

            'mc_forwarding': {
                'desc': 'Do multicast routing. The kernel needs to be compiled with CONFIG_IP_MROUTE and a multicast routing daemon is required',
                'label': "Multicast Routing",
                'parents': ['Net']
            },

            'medium_id': {
                'desc': 'Used to change the proxy_arp behavior: the proxy_arp feature is enabled for packets forwarded between two devices attached to different media',
                'label': "Proxy_ARP Behaviour",
                'parents': ['Net']
            },

            'promote_secondaries': {
                'desc': 'If this is enabled, and primary address of an interface gets deleted, an alias of the interface (secondary) will be upgraded to become primary. The default is to purge all the secondaries when you delete the primary',
                'label': "Reserve Primariy Address with Secondary ",
                'parents': ['Net']
            },

            'proxy_arp': {
                'desc': 'Do proxy ARP',
                'label': "Proxy ARP",
                'parents': ['Net']
            },

            'rp_filter': {
                'desc': 'Prevents spoofing attacks against your internal networks (external addresses can still be spoofed), without the need for additional firewall rules',
                'label': "RP Filter",
                'parents': ['Net']
            },

            'secure_redirects': {
                'desc': 'Accept ICMP redirect messages only for gateways, listed in default gateway list',
                'label': "Secure Redirects",
                'parents': ['Net']
            },

            'send_redirects': {
                'desc': 'Send redirects, if router. Send_redirects for the interface will be enabled if at least one of conf/{all,interface}/send_redirects is set to 1, it will be disabled otherwise',
                'label': "Send Redirects",
                'parents': ['Net']
            },

            'shared_media': {
                'desc': 'Send(router) or accept(host) RFC1620 shared media redirects. If it is not set the kernel does not assume that different subnets on this device can communicate directly. Overrides secure_redirects',
                'label': "Send and Accept Shared Media",
                'parents': ['Net']
            },

            'tag': {
                'desc': 'Allows to write a number, which can be used as required. The default value is 0',
                'label': "Tag",
                'parents': ['Net']
            },

            'icmp_echo_ignore_all': {
                'desc': 'Turns on (1) or off (0), if the kernel should ignore all ICMP ECHO requests. Off by default',
                'label': "Ignore ICMP ECHO",
                'parents': ['Net']
            },

            'icmp_echo_ignore_broadcasts': {
                'desc': 'Turn on (1) or off (0), if the kernel should ignore all ICMP ECHO and TIMESTAMP requests to broadcast and multicast addresses. Off by default',
                'label': "Ignore ICMP ECHO and TIMESTAMP",
                'parents': ['Net']
            },

            'icmp_errors_use_inbound_ifaddr': {
                'desc': 'If zero (the default), ICMP error messages are sent with the primary address of the exiting interface. If non-zero, the message will be sent with the primary address of the interface that received the packet that caused the ICMP error',
                'label': "ICMP ERRORS ROUTING",
                'parents': ['Net']
            },

            'icmp_ignore_bogus_error_responses': {
                'desc': 'Specifies kernel not to give bogus responses to broadcast frames warnings, which will avoid log file clutter.',
                'label': "Ignore Bogus Error Responses",
                'parents': ['Net']
            },

            'icmp_ratelimit': {
                'desc': 'Limit the maximal rates for sending ICMP packets whose type matches icmp_ratemask to specific targets. 0 to disable any limiting, otherwise the maximal rate in jiffies',
                'label': "ICMP Framelimit",
                'parents': ['Net']
            },

            'icmp_ratemask': {
                'desc': 'Mask made of ICMP types for which rates are being limited. Significant bits: IHGFEDCBA9876543210. Default mask: 0000001100000011000 (6168)',
                'label': "ICMP Rate Mask",
                'parents': ['Net']
            },

            'igmp_max_memberships': {
                'desc': 'Changes the maximum number of multicast groups we can subscribe to. The default value is 20.',
                'label': "Maximum number of Multicast Groups",
                'parents': ['Net']
            },

            'igmp_max_msf': {
                'desc': 'Limit on the number of multicast source filter. The default value is 10',
                'label': "Multicast Source Filter Limit",
                'parents': ['Net']
            },

            'inet_peer_gc_maxtime': {
                'desc': 'Maximum interval between garbage collection passes. This interval is in effect under low (or absent) memory pressure on the pool. Measured in jiffies',
                'label': "Maximum Interval Between Garbage Collection",
                'parents': ['Net']
            },

            'inet_peer_gc_mintime': {
                'desc': 'Minimum interval between garbage collection passes. This interval is in effect under high memory pressure on the pool. Measured in jiffies',
                'label': "",
                'parents': ['Net']
            },

            'inet_peer_maxttl': {
                'desc': 'Maximum time-to-live of entries. Unused entries will expire after this period of time if there is no memory pressure on the pool (i.e. when the number of entries in the pool is very small). Measured in jiffies.',
                'label': "Maximum Time-To-Live of Entries",
                'parents': ['Net']
            },

            'inet_peer_minttl': {
                'desc': 'Minimum time-to-live of entries. Should be enough to cover fragment time-to-live on the reassembling side',
                'label': "Minimum Time-To-Live of Entries",
                'parents': ['Net']
            },

            'inet_peer_threshold': {
                'desc': 'The approximate size of the storage. Starting from this threshold entries will be thrown aggressively. This threshold also determines entries. Time-to-live and time intervals between garbage collection passes. More entries, less time-to-live, less GC interval',
                'label': "Approximate Size of The Storage",
                'parents': ['Net']
            },

            'ip_autoconfig': {
                'desc': 'Contains the number one if the host received its IP configuration by RARP, BOOTP, DHCP or a similar mechanism. Otherwise it is zero',
                'label': "IP AutoConfig",
                'parents': ['Net']
            },

            'ip_conntrack_max': {
                'desc': 'The number of separate connections that can be tracked with netfilter conntrack (NAT layer). Defaults to a percentage of your total memory size. This percentage is geared towards a "general use" workstation with lots more memory (and fewer connections to track) than a typical special-purpose firewall box',
                'label': "Separate Connections Tracked With NetFilter",
                'parents': ['Net']
            },

            'ip_default_ttl': {
                'desc': 'TTL (time-to-live) for IPv4 interfaces. This is simply the maximum number of hops a packet may travel. The default value is 64',
                'label': "Default TTL for IPv4",
                'parents': ['Net']
            },            

            'ip_dynaddr': {
                'desc': 'If set non-zero, enables support for dynamic addresses. If set to a non-zero value larger than 1, a kernel log message will be printed when dynamic address rewriting occurs. The default value is 0',
                'label': "Support Of Dynamic Addressess",
                'parents': ['Net']
            },            

            'ip_forward': {
                'desc': 'Forward packets between interfaces if enabled (1). Disabled (0) by default',
                'label': "Forward Packets",
                'parents': ['Net']
            },            

            'ip_local_port_range': {
                'desc': 'Defines the local port range that is used by TCP and UDP to choose the local port. The first number is the first, the second the last local port number. The default value depends on the amount of memory available on the system: > 128MB 32768 - 61000, < 128MB 1024 - 4999 or even less',
                'label': "IP Local Port Range",
                'parents': ['Net']
            },            

            'ip_no_pmtu_disc': {
                'desc': 'Disable Path MTU Discovery (if set non-zero). By default, PMTU discovery is enabled (0)',
                'label': "Disable Path MTU Discovery",
                'parents': ['Net']
            },            

            'ip_nonlocal_bind': {
                'desc': 'Allows processes to bind() to non-local IP addresses, which can be quite useful, but may break some applications. The default value is 0',
                'label': "IP Nonlocal Bind",
                'parents': ['Net']
            },            

            'ipfrag_high_thresh': {
                'desc': 'Maximum memory used to reassemble IP fragments. When ipfrag_high_thresh bytes of memory is allocated for this purpose, the fragment handler will toss packets until ipfrag_low_thresh is reached. The default value is 262144 bytes (256 KB)',
                'label': "Maximum Memory To Reassemble IP Fragments",
                'parents': ['Net']
            },            

            'ipfrag_low_thresh': {
                'desc': 'Minimum memory used to reassemble IP fragments',
                'label': "Minimum Memory To Reassemble IP Fragments",
                'parents': ['Net']
            },            

            'ipfrag_max_dist': {
                'desc': 'A non-negative integer value which defines the maximum "disorder" which is allowed among fragments which share a common IP source address. Note that reordering of packets is not unusual, but if a large number of fragments arrive from a source IP address while a particular fragment queue remains incomplete, it probably indicates that one or more fragments belonging to that queue have been lost',
                'label': "IP Fragment Maximum Disorder",
                'parents': ['Net']
            },            

            'ipfrag_secret_interval': {
                'desc': 'Regeneration interval (in seconds) of the hash secret (or lifetime for the hash secret) for IP fragments. The default value is 600 seconds',
                'label': "Hash Secret Regeneration Interval",
                'parents': ['Net']
            },            

            'ipfrag_time': {
                'desc': 'Time in seconds to keep an IP fragment in memory. The default value is 30 seconds',
                'label': "IP Fragment LifeTime",
                'parents': ['Net']
            },            

            'error_burst': {
                'desc': 'Used to limit how many ICMP destination unreachable to send from the host in question. ICMP destination unreachable messages are sent when we can not reach the next hop, while trying to transmit a packet. It will also print some error messages to kernel logs if someone is ignoring our ICMP redirects',
                'label': "Error Burst",
                'parents': ['Net']
            },            

            'error_cost': {
                'desc': 'Used to limit how many ICMP destination unreachable to send from the host in question. ICMP destination unreachable messages are sent when we can not reach the next hop, while trying to transmit a packet. It will also print some error messages to kernel logs if someone is ignoring our ICMP redirects.',
                'label': "Error Cost",
                'parents': ['Net']
            },            

            'flush': {
                'desc': 'Flush of the routing cache',
                'label': "Routing Cache Flush",
                'parents': ['Net']
            },            

            'gc_elasticity': {
                'desc': 'Used to control the frequency and behavior of the garbage collection algorithm for the routing cache. Aggressive cache reduction triggers when the average entry list exceeds this length',
                'label': "Garbage Collection Elasticity",
                'parents': ['Net']
            },            

            'gc_interval': {
                'desc': 'Used to control the frequency and behavior of the garbage collection algorithm for the routing cache. This parameter defines route table garbage collection interval',
                'label': "Garbage Collection Interval",
                'parents': ['Net']
            },            

            'gc_min_interval': {
                'desc': 'gc_min_interval is deprecated and replaced by gc_min_interval_ms',
                'label': "Garbage Collection Minimum Interval",
                'parents': ['Net']
            },            

            'gc_min_interval_ms': {
                'desc': 'Used to control the frequency and behavior of the garbage collection algorithm for the routing cache. This parameter defines minimum interval between garbage collector runs',
                'label': "Garbage Collection Minimum Interval",
                'parents': ['Net']
            },            

            'gc_thresh': {
                'desc': 'Used to control the frequency and behavior of the garbage collection algorithm for the routing cache. Garbage collector starts when route table grows to this size',
                'label': "Garbage Collection Thresh",
                'parents': ['Net']
            },            

            'gc_timeout': {
                'desc': 'Used to control the frequency and behavior of the garbage collection algorithm for the routing cache. An entry expires after this time',
                'label': "Garbage Collection Timeout",
                'parents': ['Net']
            },            

            'max_delay': {
                'desc': 'Maximal delay for flushing the routing cache. The default value is 10 seconds.',
                'label': "Routing Cache Flushing Delay Maximum",
                'parents': ['Net']
            },            

            'max_size': {
                'desc': 'Maximum size of the routing cache. Old entries will be purged once the cache has reached this size',
                'label': "Routing Cache Max Size",
                'parents': ['Net']
            },            

            'min_adv_mss': {
                'desc': 'The advertised MSS depends on the first hop route MTU, but will never be lower than this setting',
                'label': "Minimum Advertised MSS",
                'parents': ['Net']
            },            

            'min_delay': {
                'desc': 'Minimal delay for flushing the routing cache. The default value is 2 seconds',
                'label': "Flushing Routing Cache Minimal Delay",
                'parents': ['Net']
            },            

            'min_pmtu': {
                'desc': 'Minimum discovered Path MTU. The default value is 552 bytes',
                'label': "Minimum Discovered Path MTU",
                'parents': ['Net']
            },            

            'mtu_expires': {
                'desc': 'Time, in seconds, that cached PMTU information is kept. The default value is 600 seconds.',
                'label': "MTU Expire Time",
                'parents': ['Net']
            },            

            'redirect_load': {
                'desc': 'One of the factors which determine if more ICMP redirects should be sent to a specific host. No redirects will be sent once the load limit has been reached',
                'label': "Redirect Load",
                'parents': ['Net']
            },            

            'redirect_number': {
                'desc': 'One of the factors which determine if more ICMP redirects should be sent to a specific host. No redirects will be sent once the maximum number of redirects has been reached',
                'label': "Redirect Number",
                'parents': ['Net']
            },            

            'redirect_silence': {
                'desc': 'Timeout for redirects. After this period redirects will be sent again, even if this has been stopped, because the load or number limit has been reached',
                'label': "Redirect Timeout",
                'parents': ['Net']
            },            

            'secret_interval': {
                'desc': 'The interval between cache flushes. The default value is 600 seconds',
                'label': "Cache Flushes Interval",
                'parents': ['Net']
            },            

            'tcp_abc': {
                'desc': 'Controls Appropriate Byte Count defined in RFC3465. If set to 0 then does congestion avoid once per ACK. 1 is conservative value, and 2 is more aggressive. The default value is 1',
                'label': "Appropriate Byte Count Control",
                'parents': ['Net']
            },            

            'tcp_abort_on_overflow': {
                'desc': 'If listening service is too slow to accept new connections, reset them. Not enabled by default. It means that if overflow occurred due to a burst, connection will recover',
                'label': "TCP Abort On OverFlow",
                'parents': ['Net']
            },            

            'tcp_adv_win_scale': {
                'desc': 'Scaling factor for calculating application portion of window. Count buffering overhead as bytes / 2 ^ tcp_adv_win_scale (if tcp_adv_win_scale > 0) or bytes - bytes / 2 ^ (-tcp_adv_win_scale), if it is <= 0. The default value is 2',
                'label': "TCP Application Portion of Window",
                'parents': ['Net']
            },            

            'tcp_app_win': {
                'desc': 'Scale factor for portion of window reserved for buffering overhead. Reserve max(window / 2 ^ tcp_app_win, mss) of window for application buffer. Value 0 is special, it means that nothing is reserved. The default value is 31',
                'label': "TCP Window Reserved Buffering",
                'parents': ['Net']
            },            

            'tcp_base_mss': {
                'desc': 'Lower bound for TCP path MTU discovery probing. The default value is 512 bytes',
                'label': "TCP MTU Discovery Lower Bound",
                'parents': ['Net']
            },            

            'tcp_congestion_control': {
                'desc': 'Set the congestion control algorithm to be used for new connections. The algorithm "reno" is always available, but additional choices may be available based on kernel configuration',
                'label': "TCP Congestion Control",
                'parents': ['Net']
            },            

            'tcp_dsack': {
                'desc': 'Allows TCP to send "duplicate" SACKs. Enabled (1) by default',
                'label': "TCP Duplicate SACKs",
                'parents': ['Net']
            },            

            'tcp_ecn': {
                'desc': 'Enable Explicit Congestion Notification in TCP. Enabled (1) by default',
                'label': "TCP Explicit Congestion Notification",
                'parents': ['Net']
            },            

            'tcp_fack': {
                'desc': 'Enable FACK congestion avoidance and fast retransmission. Forward ACKnowledgement is a special algorithm that works on top of the SACK options, and is geared at congestion controlling. The value is not used if tcp_sack is not enabled. Enabled (1) by default',
                'label': "FACK Congestion Avoidance",
                'parents': ['Net']
            },            

            'tcp_fin_timeout': {
                'desc': 'Time to hold socket in state FIN-WAIT-2, if it was closed by our side. Peer can be broken and never close its side, or even die unexpectedly. The default value is 60 seconds',
                'label': "TCP Fin Timeout",
                'parents': ['Net']
            },            

            'tcp_frto': {
                'desc': 'Enables F-RTO, an enhanced recovery algorithm for TCP retransmission timeouts. It is particularly beneficial in wireless environments where packet loss is typically due to random radio interference rather than intermediate router congestion. Disabled (0) by default',
                'label': "Enable F-RTO",
                'parents': ['Net']
            },            

            'tcp_keepalive_intvl': {
                'desc': 'Specifies how frequently the keepalive probes are sent out. Multiplied by tcp_keepalive_probes it is time to kill not responding connection, after probes started. The default value is 75 seconds i.e. connection will be aborted after ~ 11 minutes of retries',
                'label': "TCP Keep-Alive Probes Frequency",
                'parents': ['Net']
            },            

            'tcp_keepalive_probes': {
                'desc': 'Specifies how many keepalive probes TCP sends out, until it decides that the connection is broken. The default value is 9',
                'label': "TCP Keep-Alive Probes Count",
                'parents': ['Net']
            },            

            'tcp_keepalive_time': {
                'desc': 'Specifies how often TCP sends out keepalive messages when keepalive is enabled. The default value is 7200 seconds (2 hours)',
                'label': "TCP Keep-Alive Messages Frequency",
                'parents': ['Net']
            },            

            'tcp_low_latency': {
                'desc': 'If set, the TCP stack makes decisions that prefer lower latency as opposed to higher throughput. By default, this option is not set meaning that higher throughput is preferred. An example of an application where this default should be changed would be a Beowulf compute cluster',
                'label': "TCP Low Latency",
                'parents': ['Net']
            },            

            'tcp_max_orphans': {
                'desc': 'Maximal number of TCP sockets not attached to any user file handle, held by system. If this number is exceeded orphaned connections are reset immediately and warning is printed',
                'label': "TCP Max Orphans",
                'parents': ['Net']
            },            

            'tcp_max_syn_backlog': {
                'desc': 'Maximal number of remembered connection requests, which still did not receive an acknowledgement from connecting client. The default value is 1024 for systems with more than 128 MB of memory, and 128 for low memory machines. If server suffers of overload, try to increase this number',
                'label': "Remembered Connection Request Maximal Number",
                'parents': ['Net']
            },            

            'tcp_max_tw_buckets': {
                'desc': 'Maximal number of timewait sockets held by system simultaneously. If this number is exceeded TIME_WAIT socket is immediately destroyed and warning is printed. This limit exists only to prevent simple DoS attacks, you must not lower the limit artificially, but rather increase it (probably, after increasing installed memory), if network conditions require more than default value (180000)',
                'label': "Maximal Number of TimeWait Sockets",
                'parents': ['Net']
            },            

            'tcp_mem': {
                'desc': 'Vector of 3 integers: min, pressure, max that describe the amount of pages allocated by TCP',
                'label': "TCP Memory",
                'parents': ['Net']
            },            

            'tcp_moderate_rcvbuf': {
                'desc': 'If set (1) TCP automatically adjusts the size of the socket receive window based on the amount of space used in the receive queue. Enabled by default',
                'label': "TCP Moderate RCV Buffer",
                'parents': ['Net']
            },            

            'tcp_mtu_probing': {
                'desc': 'Enable TCP Packetization Layer Path MTU Discovery. Disabled (0) by default',
                'label': "TCP MTU Probing",
                'parents': ['Net']
            },            

            'tcp_no_metrics_save': {
                'desc': 'Normally, TCP will remember some characteristics about the last connection in the flow cache. If tcp_no_metrics_save is set, then it does not. Useful for benchmarks or other tests',
                'label': "TCP No Metrics",
                'parents': ['Net']
            },            

            'tcp_orphan_retries': {
                'desc': 'Specifies how many times to retry before killing TCP connection, closed by our side. The default value of 7 corresponds to ~ 50 seconds - 16 minutes, depending on RTO. If your machine is loaded web server, you should think about lowering this value, such sockets may consume significant resources',
                'label': "TCP Orphan Retries",
                'parents': ['Net']
            },            

            'tcp_reordering': {
                'desc': 'Maximal reordering of packets in a TCP stream. The default value is 3',
                'label': "TCP Packets Maximal Reordering",
                'parents': ['Net']
            },            

            'tcp_retrans_collapse': {
                'desc': 'Bug-to-bug compatibility with some broken printers. On retransmit try to send bigger packets to work around bugs in certain TCP stacks. Enabled (1) by default.',
                'label': "TCP Retransmission Collapse",
                'parents': ['Net']
            },            

            'tcp_retries1': {
                'desc': 'Specifies how many times to retry before deciding that something is wrong and it is necessary to report this suspicion to network layer. Minimal RFC value is 3, it is also the default value, which corresponds to ~ 3 seconds - 8 minutes, depending on RTO',
                'label': "Number of TCP Retries Before Warning",
                'parents': ['Net']
            },            

            'tcp_retries2': {
                'desc': 'Specifies how many times to retry before killing alive TCP connection. RFC1122 says that the limit should be longer than 100 sec. It is too small number. The default value of 15 corresponds to ~ 13 - 30 minutes, depending on RTO',
                'label': "Number of TCP Retries Before Disconnection",
                'parents': ['Net']
            },            

            'tcp_rfc1337': {
                'desc': 'If set, the TCP stack behaves conforming to RFC1337. If unset (the default), we are not conforming to RFC, but prevent TCP TIME-WAIT assassination',
                'label': "TCP FRC 1337",
                'parents': ['Net']
            },            

            'tcp_rmem': {
                'desc': 'Specifies buffer used by TCP sockets',
                'label': "TCP Socket Memory",
                'parents': ['Net']
            },            

            'tcp_sack': {
                'desc': 'Enable Selective ACKnowledgement (SACK) Option for TCP. Enabled (1) by default',
                'label': "TCP Selective Acknowledgement",
                'parents': ['Net']
            },            

            'tcp_stdurg': {
                'desc': 'Use the host requirements interpretation of the TCP urg pointer field. Most hosts use the older BSD interpretation, so if you turn this on Linux might not communicate correctly with them. Disabled (0) by default',
                'label': "Host Requirements Interpretation",
                'parents': ['Net']
            },            

            'tcp_syn_retries': {
                'desc': 'Number of times initial SYNs for an active TCP connection attempt will be retransmitted. Should not be higher than 255. The default value is 5, which corresponds to ~ 180 seconds.',
                'label': "TCP SYN Retries",
                'parents': ['Net']
            },            

            'tcp_synack_retries': {
                'desc': 'Number of times SYNACKs for a passive TCP connection attempt will be retransmitted. Should not be higher than 255. The default value is 5, which corresponds to ~ 180 seconds.',
                'label': "TCP SYNACK Retries",
                'parents': ['Net']
            },            

            'tcp_syncookies': {
                'desc': 'Send out syncookies when the syn backlog queue of a socket overflows. This is to prevent against the common "syn flood attack". Disabled (0) by default',
                'label': "TCP SYN Cookies",
                'parents': ['Net']
            },            

            'tcp_timestamps': {
                'desc': 'Enable timestamps as defined in RFC1323. Enabled (1) by default',
                'label': "TCP TimeStamps",
                'parents': ['Net']
            },            

            'tcp_tso_win_divisor': {
                'desc': 'Allows control over what percentage of the congestion window can be consumed by a single TSO frame. The setting of this parameter is a choice between burstiness and building larger TSO frames. The default value is 3',
                'label': "TCP TSO Window Divisor",
                'parents': ['Net']
            },            

            'tcp_tw_recycle': {
                'desc': 'Enable fast recycling of sockets in TIME-WAIT status. The default value is 0 (disabled). It should not be changed without advice/request of technical experts',
                'label': "TCP Fast Socket Recycling",
                'parents': ['Net']
            },            

            'tcp_tw_reuse': {
                'desc': 'Allows to reuse TIME-WAIT sockets for new connections when it is safe from protocol viewpoint. The default value is 0. It should not be changed without advice/request of technical experts',
                'label': "TCP Time-Wait Socket Reuse",
                'parents': ['Net']
            },            

            'tcp_window_scaling': {
                'desc': 'Enable window scaling as defined in RFC1323. Enabled (1) by default',
                'label': "TCP Window Scaling",
                'parents': ['Net']
            },            

            'tcp_wmem': {
                'desc': 'Specifies memory allowed for send buffers for TCP socket ',
                'label': "TCP Socket Memory ",
                'parents': ['Net']
            },            

            'tcp_workaround_signed_windows': {
                'desc': 'If set (1), assume no receipt of a window scaling option means the remote TCP is broken and treats the window as a signed quantity. If unset (0), this is default, assume the remote TCP is not broken even if we do not receive a window scaling option from them',
                'label': "TCP Work-Around Signed Windows",
                'parents': ['Net']
            },            

            'max_dgram_qlen': {
                'desc': 'Limits how many datagrams can be queued on a unix domain sockets (SOCK_DGRAM) receive buffer. If a sender tries to send more datagrams, it blocks (in a blocking sendto) or returns error (in a non-blocking sendto). The default value is 10',
                'label': "Maximum Length of Datagram Queue",
                'parents': ['Net']
            },            
          
        }

        return thevars

    @staticmethod
    def get_data(verbose=False):
        """Parse /proc/sys/net directory and its subdirs.

        Each non-directory file name is treated as variable name. Accordingly,
        file's content is treated as variable value. All groups in result
        dictionary preserve parent-child relations.

        Returns:
            tree (dict): nested dictionaries with system variables
        """

        tree, _, _ = traverse_directory(Net.NET, verbose=verbose)
        return tree


if __name__ == "__main__":
    n = Net()
    n.test_parse()
