# Data handling

Publisher: Lex from SigmaStudioz. Applies to Principal Driven Domain Design, SigmaStudioz Visualizer,
SigmaStudioz Video Analysis, Engineering Spikes and UI Foundation Reuse, including the optional local helpers shipped
with the applicable plugins in this repository.

These plugins provide instructions and optional local Python/Node.js helpers. There is no publisher-hosted
backend, account system or telemetry endpoint. Shipped helpers do not send media or project data to
the publisher. The Video Analysis sampler invokes existing local FFmpeg/ffprobe; it does not install
dependencies or download speech models. No hooks automatically register these media helpers.

The host agent may use local or external rendering, transcription or generation tools authorized
by the user. Those providers may process supplied content under their own terms/settings. Selecting
a skill does not authorize uploading private media, publishing an analysis or creating paid jobs.
Keep private reference media, transcripts and extracted evidence out of public export packages.

Engineering Spikes has no executable helper, publisher service or required external connector.
During a user-requested investigation, the host agent may read supplied tickets, findings and
permitted repository files, then create local stakeholder and technical documents, evidence
records or isolated experiment artifacts. These can contain personal or confidential information.
Local retention and deletion remain under the user's control; the publisher receives and retains
none of these artifacts through a publisher service.

Optional research and experiments use only tools and destinations authorized by the user. A host
browser or research provider may process search queries or other content deliberately supplied
to it; the applicable provider depends on the user's tools and account settings. No external
research provider, experiment service or Confluence connection is required by this package.
Review the chosen provider's privacy policy before sharing restricted evidence. Invoking the
skill does not authorize uploading private files, spending money, or publishing pages or attachments.

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
This notice describes these plugins' behavior; it does not replace the host provider's policies.

UI Foundation Reuse reads its local runtime metadata/archive and a selected app manifest,
then copies a checksum-verified archive into that app's vendor directory. It does not
download code, install dependencies, send data or modify package manifests. A separately
authorized package-manager install can access its configured registries for external peers.
Visualizer's optional local renderer reads user-controlled scene/font files and invokes
local FFmpeg to write video, captions and posters; no publisher service receives them.
