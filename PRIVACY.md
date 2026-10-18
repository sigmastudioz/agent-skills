# Data handling

Publisher: Lex from SigmaStudioz. Applies to the domain-driven-design skill and its optional
local Claude handoff helper in this repository.

This plugin provides instructions and a local Python helper. It has no publisher-hosted backend,
account system, telemetry endpoint or network calls. The publisher receives no automatic usage
reports from the plugin.

The coding agent reads project files and uses the tools permitted by its host. The optional
handoff helper reads the host-provided session transcript locally to check explicit teammate
limits, reads the installed baseline, and returns handoff instructions to the local agent runtime.
It does not upload transcript contents to the publisher. The agent provider may process project
context and prompts according to the user's account settings and that provider's terms.

The skill asks agents to keep credentials and private payloads out of handoff notes. Users remain
in control of host permissions and which repositories the agent can access. Installing the plugin
does not silently install global rules or enable the optional helper; see [setup](SETUP.md).

Support is through [GitHub Issues](https://github.com/sigmastudioz/agent-skills/issues). Issues are
public; do not include credentials, private source, personal records or raw agent session logs.
This notice describes this plugin's behavior; it does not replace the host provider's policies.
