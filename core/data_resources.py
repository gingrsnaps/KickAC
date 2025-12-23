"""
core/data_resources.py
Contains static data for generating unique identifiers in the simulation.
"""

VERBS = [
    'Synthesizing', 'Compiling', 'Decrypting', 'Navigating', 'Routing',
    'Quantizing', 'Oscillating', 'Resonating', 'Amplifying', 'Diverting',
    'Injecting', 'Parsing', 'Indexing', 'Archiving', 'Deploying',
    'Mitigating', 'Isolating', 'Validating', 'Bypassing', 'Overclocking',
    'Tracing', 'Resolving', 'Switching', 'Bridging', 'Tunneling',
    'Hyperlinking', 'Caching', 'Hashing', 'Salting', 'Spoofing',
    'Rendering', 'Glitching', 'Streaming', 'Broadcasting', 'Encoding'
]

NOUNS = [
    'Mainframe', 'Protocol', 'Bandwidth', 'Latency', 'Packet', 'Payload',
    'Daemon', 'Kernel', 'Shell', 'Terminal', 'Console', 'Registry',
    'Cluster', 'Node', 'Shard', 'Replica', 'Proxy', 'Gateway', 'Firewall',
    'Bastion', 'Cipher', 'Token', 'Session', 'Socket', 'Port', 'Thread',
    'Process', 'Container', 'Pod', 'Namespace', 'Volume', 'Snapshot',
    'Artifact', 'Binary', 'Module', 'Variable', 'Constant', 'Vector'
]

# Simulated Hardware Contexts (User Agents)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
]