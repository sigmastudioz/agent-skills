# Collection catalog trace

## DDD guidance-only marketplace package — November 13

DDD-PKG-01 (integration gap): the existing DDD plugin includes an optional Python
handoff guard and its executable regressions, although the current directory accepts
only guidance/listing files from an unverified publisher. The human supplied the exact
current file-type refusal after authenticated browser control became unavailable.
This is a package-boundary issue, not a guard algorithm failure or human rejection.

Move the real guard and its regressions to tools/handoff-guard, outside every plugin.
The guard implementation remains byte-identical to public378be95, SHA-256
0e3ef2edb9ad8a492aac35899f886d707b75ca413c9338097d8d5b35d883c023. It still trusts only
SKILL.md beside the installed scripts directory; source execution from the tools folder
is deliberately unsupported. Tests now construct private installed layouts instead of
depending on the public plugin carrying executable code. SETUP.md retains the same
user-installed hook path and documents the explicit opt-in copy. No installer, auto-fetch,
MCP server or hook is added to the marketplace package. Existing global files are untouched.

| Cluster | Entry, effects and trace | Closure evidence / boundary |
| --- | --- | --- |
| Guidance discovery | existing catalog → four manifests → skills/domain-driven-design/SKILL.md → local handoffs/architecture/verification references | Guidance/JSON handoff contract remains usable without code; no script link or runtime download. Package allowlist, UTF-8/NUL/shebang and registration regressions. |
| Optional guard | user-authorized setup → separately reviewed tools/handoff-guard source → copy into installed skill/scripts → existing PreToolUse hook → baseline identity/budgets/isolated brief → accepted/rejected invocation | Same runtime bytes and hook path; temporary installed-layout subprocess regressions exercise all existing behavior. No agent/provider efficacy or actual global installation claimed. |
| Collection consumers | tests/test_handoff_guard.py → moved regressions → isolated full skill copy + guard | Repository test discovery and documented standalone command use the same guard suite; historical evidence remains historical. |
| Release | public378be95 → DDD1.4.6 and19-file package → regenerated release hashes → complete plugin ZIP | Eight other plugin inventories, including concurrent Visualizer1.4.5, must remain byte-identical. No new catalog identity or held-back additions. |

Rollback: inverse move of the two Python sources, reverting setup/test-loader links and
guard-free guidance/version metadata; preserve newer source edits before rollback.
Historical DDD1.4.5 release and installed helper paths remain available unchanged. The
marketplace plugin legitimately ships no program; code is neither renamed as text nor
fetched/executed indirectly. Remote policy/scan outcome and DDD native activation remain
unverified until the existing submission detects this patch. No new identity/declarations.
No schema, app mount, scheduler or permission change; those edges are not applicable.

Final runtime/content checks: standalone moved guard suite58 passed in9.538s; collection
`python3 -B -m unittest discover -s tests` passed200 in53.115s, no skips. Metadata validator
and targeted native validator pass; only the existing README install-line advice remains.
All eight other release inventories match378be95, and the moved guard bytes match the
original SHA-256 above. These prove local boundary/compatibility, not a remote policy pass.

Concurrent public PR30/8d2beee updated Visualizer to1.4.6 and its root demo assets after the
initial gate. Merged that public base without conflicts; DDD package and guard bytes are
unchanged. The final release preserves all eight other inventories against8d2beee, including
Visualizer1.4.6. Recheck the final merged tree before publication; no other skill is republished
by this task. The initial378be95/Visualizer1.4.5 comparison above remains historical evidence.

## Credential boundaries — November 13

CRED-01 (bug, fixed-and-verified): the storyboard and media-in-3D CLIs passed
the full caller environment to FFmpeg/ffprobe. No credential transmission was observed,
but child tools unnecessarily received host keys, proxy/authentication settings and
Python/loader/report overrides. Existing sound children used an allowlist; its remaining
OS/temp/locale reads were not credential reads, but the provider labels sound_design.py
as MCP_FORWARDS_CREDENTIAL_ENV. All three now reuse scripts/tool_runtime.py. It constructs
an environment from selected tool directories, OS defaults, fixed locale and no-user-site
settings; sound adds fixed offline flags. No caller environment values are copied.

| Cluster | Connected path and failure boundary | Evidence / remaining scope |
| --- | --- | --- |
| Media child environment | documented render.py / media_in_3d.py CLI → selected local FFmpeg/ffprobe → shared tool environment → encode/probe result or existing process failure | Real child sentinel tests and storyboard encode cover credential exclusion and preserved output; media composition rendering retains existing behavior tests. Fresh full media-in-3D export is not claimed. |
| Sound runtime | documented config/doctor/generate/mix → pinned local tool validation → shared environment + fixed offline flags → subprocess → result/provenance | Existing revision/rights/output/decoder/proxy tests plus real child tests; no fresh live Openverse, Earshot or Real SFX operation. |
| UI native configuration | marketplace entry → .claude-plugin/plugin.json → empty inline MCP server map → no registered server, env, hook or secret input | CRED-02 below; native validator and regression assertions. UI staging helper reads only local metadata/archive/app manifest and has no network/process/env API. Existing archive/staging checks reused only if runtime bytes match. |
| Distribution | nine existing identities → two version bumps → four host manifests each → release.json → self-contained ZIPs | Other seven inventories must remain byte-identical; helper must ship beside all three callers. No installed/global/development checkout change. |

CRED-02 (unverified provider finding): UI1.2.2/583d79b and Visualizer1.4.3/e9ce3d0
both name .claude-plugin/plugin.json for MCP_FORWARDS_CREDENTIAL_ENV. Those exact JSON
manifests contain only listing metadata: no server, env, hook, interpolation or credential.
The former has one warning; the latter also names the sound script. Inspected UI archive
has no process.env or token/API-key lookup; explicit browser image CORS options are app
configuration, not native host credential forwarding. No confirmed manifest credential
defect exists. Empty mcpServers maps make absence explicit without inventing a credential
request or service. Only a new provider scan/reviewer can establish warning removal.

Consumer/registration, default, rejection, snapshot and package edges require the final
checks below. No app mount, persistence/schema, recurring cadence, webhook or legal change.
Windows system-directory lookup uses the native OS API; Windows runtime is unavailable
and remains unverified. Keep real scripts/runtime archive and cross-host manifests.

Verification on the final runtime/manifest content: `python3 -B -m unittest discover -s tests`
passed 198 tests in 44.357s, no skips. Both targeted `claude plugin validate` commands passed,
with only the existing README install-line advice. Real baseline children launched by the
old sound default runner and media runner inherited a synthetic credential; patched real
children do not. The storyboard CLI's actual FFmpeg wrapper records no sentinel credential,
proxy, Python-path or FFREPORT settings while producing the expected frames/audio/captions.
The existing sound configured-child, anonymous downloader, decoder/rights/output rejection
tests pass. UI archive SHA-256 stays a433d9eea8e91681cf8c1e7af86d520f0979840b900887a71b82942772b02d1a;
all seven other plugin inventories match public b661947 exactly. Caller/registration/default
and rejection edges pass; Windows and remote directory scan remain unverified, not green.

## Delegating to Agents local contract — November 13

DEL-01 (integration gap): the 1.0.0 skill's operative handoff links fetched mutable remote
instructions. The public skills.sh Snyk audit reports W012/medium for that dependency.
Entrypoint -> local references/handoff-contract.md -> authorized brief/isolation/reporting;
README and the two section links now resolve inside the installed package. The bundled
versioned adaptation derives from unchanged DDD1.4.5; its source identity/hash is recorded
in the reference. No guard, executable, account or service is added. Host authorization,
budgets and existing engineering baselines remain controlling. The other eight public
plugin inventories and upstream MIT attribution/licenses remain unchanged. Existing1.0.0
release and the single AgenticSkills intake remain historical/complete, never overwritten
or resubmitted. Provider warning clearance and native activation require fresh observations.


## Directory package boundaries — November 13

Scope: existing Claude feedback for DDD, UI Foundation Reuse, Does It Make Sense?,
Visualizer and Video Analysis. Base bb410682f70c9621e480eba6ff8588ddafccf73d includes
nine public identities; preserve the concurrent Delegating to Agents publication.

DIR-01 (integration gap): DDD/UI/Sense installed skill folders included synthetic
application fixtures, so their application package.json scripts/dependencies and source
files were also scanned as plugin runtime. Move all 61 fixture files, without byte changes,
to collection-owned tests/fixtures/<skill>. Historical scenario summaries stay packaged;
their current links reach the collection fixtures and their original paths/dates/hashes
remain explicitly historical. No collection runner imports those old fixture paths.

Trace: plugin manifests -> catalog builder -> release inventory and full-plugin ZIP ->
marketplace install boundary. Separate scenario path: packaged tests/README -> public
collection fixture -> isolated authorized evaluation workspace. Preserve the DDD handoff
guard, UI staging helper/runtime archive/source/licenses and all runtime instructions.
No new feature, model evaluation, global installation or application change is included.

DIR-02 (external policy): real DDD/UI/Visualizer/Video code and the UI archive still require
Anthropic's Verified-organization allowance. The portal says Anthropic chooses those
organizations and has no application route yet. Do not remove or disguise runtime files.
The existing verification inquiry remains sent once. Current UI/Visualizer manifests have
no MCP/env/hook declarations; Visualizer's real subprocess callers already use an explicit
allowlisted environment and its downloader is anonymous. No new reachable credential
forwarding defect was established; conditional provider warnings require provider review.

Validation: 193 collection tests pass, no skips (42.070s); the three skill metadata checks,
native nine-plugin validator and catalog/hash checks pass. All 61 moved files match the
base byte for byte; all six untargeted plugin inventories and actual runtime files are unchanged.
No new causal efficacy, visual rendering or provider approval claim is made.

Verification and publication identities are recorded in the owning human-task receipt;
remote approval, warning clearance and native activation require fresh provider evidence.


## Maintained skill releases — November 1

Scope: synchronize four maintained skills from the existing six-plugin collection at
571947f. Release DDD 1.4.0, Visualizer 1.3.1, UI Foundation Reuse 1.1.1 and Does It Make
Sense? 1.0.1. Engineering Spikes and Video Analysis retain exact prior inventories.
No new catalog identity, native submission, source check, legal acceptance or support message.

| Cluster | Trace, review and verification | Remaining boundary |
| --- | --- | --- |
| DDD guidance and guard | Entrypoint -> focused architecture/handoff/tracing/verification references -> documented PreToolUse matcher -> coding request/session offer/proposal/start -> cumulative budget and validated brief -> reminder. Corrected setup matcher to register the added desktop tool. All packaged guard regressions run through the collection gate. | Only the named host tool is supported; permissions, real isolation and natural-language intent remain host/coordinator responsibilities. No global hook settings changed. |
| Visualizer | Stable interactive/data/R3F entrypoints retained; local video guidance rebased into video.md -> sound/storyboard/dependency references -> size parser/layout -> encoder/captions/poster. Corrected two relative script links and isolated test imports to preserve root discovery. Real encode/full decode and existing sound namespace protections pass. | No new rich-scene, subjective listening, external sound service or model-efficacy claim. |
| UI reuse | Expanded guide -> all 85 existing runtime export entries -> unchanged 0.7.0 archive/source/types/notices -> app-local staging helper. All guide entries present in the bundled package; integrity, contained targets, conflict/idempotency/symlink checks pass. | Runtime was not rebuilt because its bytes/API are unchanged; consuming apps remain pinned. Native rendering not rerun. |
| Outcome review | Request authority -> existing goal -> terminal consumer -> bounded recommendation. Recorded refund scenario exposed quoted-ticket ambiguity; clarified that quoted stakeholder text does not grant user authorization. Existing implicit discovery made explicit in metadata. | The narrow clarification was reviewed but not retested with a fresh model; historical scenarios retain their original tested hashes. |
| Portable scenarios | Eight synthetic tasks/fixture folders and summarized historical comparisons included. Raw sessions, host paths/configuration and the duplicated host-only generator excluded. Historical baseline contamination and no-difference cases retained. | These are repeatable inputs and limited historical evidence, not fresh causal efficacy scores. No agents spawned. |
| Distribution | Four native/portable manifests per changed plugin -> unchanged six-entry registry -> generated release inventory -> four complete ZIPs. Unchanged plugins and existing media compared by hash. | Native directory activation and skills.sh backing snapshots remain separate provider observations. No installs/telemetry or marketplace requests repeated. |

Validation: 119 collection tests passed, no skips; 29 distributed renderer/sound tests passed,
no skips. Four skill validators passed; 88 relative skill links resolve inside the repository.
Claude native validation passed with the existing 12 nonblocking icon/documentationUrl warnings.
JSON, Python syntax, runtime integrity/exports, unique identities and excluded-skill checks pass.
The first suite attempt exposed imported test-directory shadowing; the test loader path is now
restored after importing the renderer, and the full suite then passed. No unrelated applications,
private source media, model installations or operational records were changed.


## Visualizer 1.3.0 release review — 2026-10-29

Human authorized review, push to the main collection, a Visualizer release and one
skills.sh refresh while preserving existing marketplace identities. Review found a
blocking output collision: a fresh MP4 name could overwrite an approved same-basename
WAV/report through upstream FFmpeg `-y`. `sound_design.mix_output` now rejects existing
stem/report/work namespaces before launching the mixer. Sixteen guard tests include
seven existing-sidecar cases and a non-MP4 rejection. The installed-skill reproduction
was rerun after this fix and retained −16.0 LUFS / −3.6dBTP with speech-keyed ducking.

Release trace: Visualizer1.3.0 portable + three native manifests -> unchanged six-entry
registry -> generated hashes -> self-contained versioned ZIP -> main/release/index
verification. Only Visualizer's plugin inventory changes; the other five inventories
remain byte-identical. Root privacy documentation now describes optional Openverse
requests/downloads and project-local sound records. No source media, model/runtime
payloads, private config, new directory intake or legal reacceptance is included.
Official provider approval/activation remains separate from this release.


## 2026-10-29 installed sound runtime and end-to-end test (local, unreleased)

The subsequent human request explicitly authorized installing and integrating all
three tools and testing a short film. This supersedes the earlier documentation-only
scope below; it does not change any published version or marketplace receipt.

| Module/consumer | Connected trace and checks | Status / boundary |
| --- | --- | --- |
| scripts/sound_design.py | Skill -> sound-runtime.md -> CLI doctor/search/fetch/generate/mix -> pinned isolated runtime -> final playable export | SOUND-01 fixed-and-verified on this host; identical standalone and Visualizer adapters, 14 guard tests |
| Openverse adapter | HTTPS query/filter -> saved result ID -> reviewed original CC0 item -> bounded download -> ffprobe/hash/provenance -> cue | SOUND-02 supported filtered-browse/download route verified live; keyword searches time out externally and remain an explicit limitation, never silently relabeled as matches |
| Earshot adapter | Revision/dirty-tree check -> offline model-free bank render -> recipe/seed/audited WAV -> provenance -> mixer | SOUND-03 verified 0.4.0 / 591fa3e028032e6dce56620a20e932e35667e8d8; original whoosh clean, no optional analysis models fetched |
| Real SFX adapter | Validated picture/cue/asset snapshot -> project-local config and explicit files -> plan -> speech-keyed mix/stems -> AAC -> decoded export | SOUND-04 verified edbefcbc3474869e6cc1e8a7ca583b0efd0dab7e; no automatic cue snapping, destructive stem extraction or tonal fitting. Origin metadata distinguishes generated files from upstream generic “library” labels |
| Revision/rights/failure contracts | Reject stale picture, changed assets, missing clearance/origin, duplicate IDs, nonfinite time, ambiguous audio preservation, double base/stems and existing output; bounded download/retry | SOUND-05 verified by 14 guard tests and actual short-video invocation; unsupported optional drawtext/rubberband paths remain reported |
| 12-second test film | Openverse CC0 pop + Earshot whoosh + local narration -> authored cues -> Real SFX -> 360 H.264 frames/AAC -> final metrics/ASR/visual frames | SOUND-06 technical pass: cue peaks +6.94ms/+8.31ms, voice-keyed SFX attenuation 5.96dB, −16.0 LUFS / −3.6dBTP. All narration words recovered; exact final AAC payload matches analyzed draft. Listening/taste approval remains unclaimed |
| Installed/distribution consumers | Standalone skill -> Codex/Claude aliases and separate Cursor copy; Visualizer video mode -> same self-contained refs/script -> catalog hashes | SOUND-07 13-file installed copies and ZIP byte-verified, 20/34 local links valid, schemas pass, 8 catalog tests, native catalog validation passes with existing metadata warnings; installed-skill reproduction also passes |

Local task artifacts live outside this public repository in the owning task's
`outputs/visualization-sound-e2e/`: verified-demo.mp4, editable storyboard/plan,
rights/provenance, separate effects/stems, reproduce.py and e2e-verification.json.
The final video SHA-256 is
`a17e45830c7063eaaf3c926babbe73635d51d8fea275932e6db9a8bb51e5a4bb`.
The audio ends at 11.908s, leaving 92ms within the intentional silent picture tail.
No private/runtime paths or third-party tool repositories are bundled in the skill.
Openverse is a remote API client, not a locally hosted service. Native agent skill
selection on other hosts, optional model analysis and subjective listening are not
established by these checks. No release, push or duplicate submission was performed.

## 2026-10-29 sound-design guidance update (local, unreleased)

Scope: human-authorized visualization-videos sound pass and verified optional tools;
no renderer changes, tool installation, release or marketplace action. The installed
standalone skill, shared archive and Visualizer video consumer carry the same sound
references. Existing publication receipts still describe their published revisions.

| Path/consumer | Trace and check | Result/limit |
| --- | --- | --- |
| visualization-videos SKILL.md / Visualizer references/video.md | Audio route -> sound-design.md -> sound-tools.md -> original timeline/assets/mixer -> encoded export | Connected local reference links: 15 standalone, 29 Visualizer; no broken targets |
| sound-design.md | Cues with intent/quiet decisions -> cleared assets or recipes -> processed audible anchors -> speech-safe mix -> mux -> measured/listening review | Manual scenario review: silent brief, 2.000 s cue minus .320 s peak, missing tools/rights, no clean stems, narration masking and unjustified score-driven density; no rendered efficacy test claimed |
| sound-tools.md | Openverse official API/terms; Clipwing source edbefcbc3474869e6cc1e8a7ca583b0efd0dab7e; Earshot source 591fa3e028032e6dce56620a20e932e35667e8d8 / 0.4.0 | Docs/source verified; API query timed out; external tools not installed/executed. Asset rights, provisioned environment and final listening remain task-specific |
| Installed copies / standalone archive | Canonical skill -> existing Codex/Claude symlinks; separate Cursor copy refreshed; ZIP -> byte comparison with source | 10 installed files hash-verified across two existing folders; 11-file ZIP round-trip verified, no caches |
| Collection integration | Video reference -> self-contained sound references -> release.json hashes | Both skill schemas pass; 8 catalog tests pass; generated catalogs/hashes pass --check. No new version/release/native activation claim |

The optional tools complement existing project mechanics. Real SFX voice-safe and
music-led duck flags have different directions; arbitrary combined tracks cannot be
assumed cleanly separable. Earshot metering/model evidence is not taste, speech
transcription or licensing clearance. These limits are carried into the instructions.

Scope: adding future independently versioned plugins to the SigmaStudioz collection. Reviewed
2026-10-18. This record covers catalog tooling, not universal skill efficacy or an official listing.

| Module/path | Entry/consumers | Dependencies/effects | Evidence | Finding/status |
| --- | --- | --- | --- | --- |
| catalog.json | Maintainer -> build_catalogs.render | Plugin names, contained paths, owner and display label | Actual registry plus two-plugin test | COLL-01 fixed-and-verified: one inventory serves three hosts |
| tools/build_catalogs.py | CLI -> build -> render | Registry and four manifests per plugin -> three host catalogs and per-plugin release hashes | Six tests; actual --check and native Claude catalog validation | COLL-02 fixed-and-verified: preserve independent versions; reject duplicate names, traversal and native drift |
| Three generated catalogs | Claude / Cursor / Codex discovery | Contained ./plugins paths -> native/portable package -> skills | Registry equality checks and source containment; native Claude validation | COLL-03 verified file/schema integration; live store installation is a separate boundary |
| release.json | Maintainer verification | Each plugin version plus hashes of its files | Two-plugin test verifies versions 1.0.0 and 2.3.4 coexist | COLL-04 fixed-and-verified: avoid a forced shared release version |
| tests/test_catalogs.py | Standard-library unittest | Temporary independent plugin fixtures; read-only stale check | 6 tests pass, including no output on duplicate rejection | verified |
| README / CONTRIBUTING / SETUP | New user / maintainer | Select plugins, add entries, opt into native global instructions | Source/path review; no placeholder skill folders created | static-only user instructions; each new plugin needs its own efficacy checks |
| Repository publication | GitHub creation form -> public repository | Selected organization, name, visibility and license -> remote creation/upload | Public snapshot 6451d807f6c7f77e36ecf105af0237d5acf125f2; 26 files match reviewed bundle; native catalog validation and 6 tests pass in fresh clone | COLL-05 fixed-and-verified: MIT root/plugin notices, clean direct-install collection published; see ../publication.json |
| Initial DDD skill | Installed/native agent -> module changes | Global baseline, optional Claude hook, handoffs and checks | Cursor fresh coding 16/16 + 2/2; fresh Claude 1.0.5: 16/16 + 2/2 with one teammate; 21 guard tests | fixed-and-verified for the scoped native test; desktop/cloud/performance remain outside coverage |

Inventory: 8 review units, 8 accounted for. File/catalog checks and generated output are runtime
verified locally; user setup, official-store publication and every possible future plugin are not.
A maintainer adding a plugin must rerun catalog checks and verify that plugin's actual behavior.
Cycles are absent in the scoped flow: registry -> manifests -> catalogs/receipt; no reverse imports.

COLL-05 closure completed on 2026-10-18: MIT confirmed; public destination created; the clean
bundle and all native catalog source paths verified in a fresh public clone. The 26-file verified
snapshot is recorded in [the publication receipt](../docs/publication.json); this receipt and trace
closure are later documentation additions. No private session logs, global settings, credentials
or publisher machine paths were uploaded. Official store submissions remain a separate boundary.

Catalog-tool content revision: 2504ae7b2e3175effa18a4f21c08a091cb81b2525e97ac4cf8bb06592b86dea0 . Reopen evidence after relevant changes.

## 1.0.5 repair trace

| Module/path | Entry and effects | Evidence | Status |
| --- | --- | --- | --- |
| SKILL.md | Global routing -> original contract -> proposed brief -> worker and parent review | Core SHA in ../validation.json; full-body native child delivery before HANDOFF_JSON | fixed-and-verified: explicit injective identity and user budget precedence |
| guard_handoff.py | Native PreToolUse -> non-meta user budget -> pending/non-rejected dispatches -> handoff validation -> updated input | 21 subprocess tests; one real accepted teammate, one rejected incomplete attempt | fixed-and-verified; English explicit Use N syntax and available transcript boundary documented |
| Native consumer | Isolated worker -> parent copy/integration -> API/worker billing facade -> store/read/retry/error outcomes | 20 parent tests; 16 external feature checks; 2 original regressions | fixed-and-verified in the dependency-free fixture |
| Installed package docs | Plugin cache README -> hosted setup/privacy/validation links | Absolute repository links replace paths outside a cached plugin folder | fixed-and-verified static link/path inspection; publisher portal scans remain separate |

These additions close the observed identity-collision and excess-teammate findings for this native
run. Budget wording that cannot be recognized and unavailable native history remain coordinator
responsibilities. No transcript data is sent to a publisher service by the helper.

## 1.0.6 branding trace

The human requested Principal Driven Domain Design as the public name. Keep the package and
skill ID `domain-driven-design` for compatibility. Trace: reviewed title/UI metadata -> builder ->
portable/native manifests -> generated catalogs/release hashes -> installed aliases and local
plugin -> repository docs and directory scan. Instruction body after the H1 and optional helper
are unchanged from the tested 1.0.5 baseline. Preserve original native evidence and hashes.
Verify the 597-line folder limit, full baseline delivery before handoff, native manifest validation,
catalog drift and every published file. Directory approval and platform-derived labels remain
external; do not claim that a metadata update establishes a live listing.

## 1.1.0 user-installed instruction update

The instruction body now adds cross-module edge checks, staged-snapshot and concurrent-writer
review, candidate disproof, and early orientation versus final acceptance gates.

| Cluster | Edges checked | Evidence and limits |
| --- | --- | --- |
| Instruction delivery | Consumer, contract, registration | Stable skill ID and path; updated SKILL.md exactly matches user-installed source; full-body guard delivery unchanged; existing 21 guard tests pass |
| Distribution | Contract, back-compat, snapshot | Four manifests agree on 1.1.0; registry and three catalogs retain stable IDs; release inventory and ZIP byte hashes match; other plugins unchanged |
| Documentation | Contract, headroom | README reports 567 instruction lines / 666 skill-folder lines; earlier 597-line and native efficacy receipts remain historical, not relabeled |

No new production module, periodic task, UI component, discriminator, storage writer or persisted
key was introduced, so cadence, mount and data-migration edges have no changed runtime path.
The helper and UI metadata remain byte-identical. No fresh native-agent efficacy run was made
for 1.1.0; packaging checks do not establish instruction adherence. Reviewer activation and
blocked uploader eligibility remain external boundaries, not confirmed publication.

## Engineering Spikes 1.0.0 addition

Scope: one new, independent instruction/template plugin; no production runtime helper or global
configuration change. The 13 design gaps and scenario boundaries are recorded in
[Engineering Spikes validation](../docs/engineering-spikes-validation.md).

| Cluster | Forward / backward edges | Candidate findings and closure |
| --- | --- | --- |
| Instruction consumption | Relevant spike request -> modes -> evidence/decision -> two audience templates -> delivery reference | SP-01–12 covered; negative/blocked outcomes and recommendation versus approval explicit |
| Format delivery | Templates -> HTML artifacts -> rendered copy -> target editor | Six-column identity table replaced; Mermaid native-rendering assumption rejected; actual Confluence paste remains unverified |
| Distribution | catalog.json -> portable/native manifests -> three host catalogs -> skill/resources -> release hashes -> ZIP | SP-13; stable independent ID/version and contained paths; exact inventory checked at release preparation |
| Discovery and documentation | README install ID -> registry name -> plugin skill path -> UI metadata | No alwaysApply global rule, executable helper or forced activation; existing plugin versions/inventories preserved |

Four clusters inventoried and accounted for. No runtime storage writer, recurring process, API or
UI mount was introduced; cadence, migration and production rollback edges have no changed code.
Research access, actual agent adherence, editor paste and native directory activation remain
external/unverified boundaries. Authored scenarios and package checks do not close those claims.

## 1.2.0 final local update

Scope: publish the user-approved five-file skill snapshot, four compatible plugin manifests,
and matching setup/release documentation. No delegation, global-settings change or new runtime
service is authorized by this release task. Existing privacy, icons, demos and other plugins stay
outside the changed capability.

| Cluster | Connected paths and edge evidence | Outcome and limits |
| --- | --- | --- |
| Instruction/reference delivery | Stable skill ID -> SKILL.md routing -> references/architecture.md sections; complete reference included in release inventory | Exact local-source bytes retained; linked files/anchors checked. Tracker/evidence retention, cadence and verification guidance updated. No fresh native-agent adherence run. |
| Optional guard | Documented SETUP PreToolUse command -> guard input -> coding workspace -> native user history and cumulative budget -> handoff/isolation/baseline validation -> compact idempotent updated prompt | 51 packaged subprocess regressions pass, including malformed input/history, repeated caps, quoted/negated examples, pending/rejected/resumed calls and different-workspace declarations. Caller permissions, real isolation authority, unsupported natural language and host resume identity validation remain external responsibilities. |
| Regression ownership | tests/test_handoff_guard.py loads the packaged test class; packaged tests launch the adjacent guard with isolated fixtures | One maintained 51-test contract replaces obsolete full-baseline/reset-on-repeated-cap expectations. Repository discovery runs 70 tests successfully without launching agents or project jobs. |
| Distribution | Portable/native version1.2.0 manifests -> existing catalog generator -> three host catalogs and release.json -> ZIP inventory | Stable package/skill IDs, UI metadata and other plugin bytes preserved. Source/copy/release hashes and staged snapshot checked; independent marketplace activation remains outside local package proof. |
| Setup/documentation | README and SETUP consumers -> compact reminder, cumulative limits and explicit isolation object | Present-tense instructions describe1.2.0. Historical1.0.5 full-body guard and coding efficacy remain identified as historical; no new efficacy or universal-host guarantee. |

Consumer, contract, registration, default/back-compat, snapshot, concurrent-writer and relevant
headroom edges are covered by the named source, link, manifest, fixture and artifact checks.
Cadence changes are instruction guidance only; no scheduler runs in this plugin. Mount,
discriminator and persisted-data migration edges have no changed production implementation.
The user confirmed the local pass complete; the source is copied into an isolated release branch
and rechecked by content hashes before committing. No live writer is swept into the release.
The source entrypoint is405lines; its complete five-file folder is1348lines, including313lines of
conditional architecture guidance and406lines of guard regressions. Earlier size caps/receipts
are historical and do not describe this explicitly requested source snapshot.

Candidate disproof: the guard's smaller output and cumulative repeated cap are intended new
contracts, not regressions to repair back to old behavior. The existing root tests that required
full-body injection or reset-on-every-cap were superseded by the shipped contract tests. Multiple
semantic decision sites and legitimate runtime loops are no longer automatically classified as
bugs. No confirmed in-scope package defect remains after the listed checks. Actual provider review,
remote/cloud loading, model adherence and production runtime behavior remain unverified boundaries.

Final pre-publication revision also adds repository ownership and operational-artifact guidance in
SKILL.md and its architecture reference. Existing reference/anchor and package inventory checks
cover this prose change; guard source/configuration/tests are byte-identical to the51-test pass.

## 1.3.0 project-record convention and migration

Scope: `.principal-ddd/` discovery, one owning source of task truth, and authorized record
migrations. No application source, production configuration, scheduler, agent hook or runtime
behavior changed. The optional guard, its51tests and UI metadata remain byte-identical to1.2.0.

| Cluster | Connected paths and checked edges | Evidence / limits |
| --- | --- | --- |
| Instruction discovery | Global baseline -> owning root -> `.principal-ddd/index.md` -> existing tracker or DDD ledger; SKILL routes conditional migration detail | New project-record reference is packaged; existing trackers keep authority; no empty scaffolds, duplicate status or implicit cross-project sweep. Static behavioral scenarios checked; native model adherence not rerun. |
| Data migration | Named original ledger -> rebased relative links -> new canonical ledger -> legacy forwarding path/anchors; owning index -> migration receipt | Exact original bytes reconstruct from reversible link edits; source/destination hashes, heading preservation and unchanged target identities checked. Conflict fixture refuses an occupied destination. Pinned mode preserves original bytes. |
| Active consumers | Existing audit/evidence writer paths -> original authority; new index -> that same record | Pinned records are explicitly linked rather than relocated. Existing evidence/operational tools stay in place; no jobs or deployments triggered. |
| Distribution | Four1.3.0manifests -> current catalog generator -> three host catalogs/release inventory -> complete ZIP | Other plugin bytes, guard, tests and UI unchanged. Catalog, skill/link, native validation and package integrity checks apply to this revision; directory activation remains provider-owned. |

Candidate disproof: hiding a folder does not establish access control or build exclusion; globally
ignoring it would lose durable findings. Moving an established tracker would fork task authority.
An old-path forwarding document is insufficient for a parser/appender, so uncertain writers stay
pinned. Paths without DDD data get no directory. Historical evidence keeps its original identity.

Migration receipt `.principal-ddd/migration.json` records the exact pre-append move identity;
this section is newer canonical work, so hash-gated rollback must reconcile it rather than
overwriting it. Public product/architecture docs remain in their normal documentation locations.
No fresh agent efficacy, marketplace publication, production or universal host guarantee is implied.

## UI Foundation Reuse 1.0.0 and Visualizer 1.2.0

Scope: add one independently versioned UI Foundation Reuse plugin; update the existing
Visualizer identity with the current local visualization-videos workflow. Existing interactive,
data and R3F entry points, icons and demonstration media remain present.

| Cluster | Connected paths and checked edges | Evidence / limits |
| --- | --- | --- |
| UI reuse | Skill -> setup -> checksum manifest -> staging helper -> contained runtime archive -> public exports/types | Runtime0.5.0, 74 public export targets; exact installed-source comparison, safe archive inventory, repeated staging, conflict preservation and symlink escape tests. Source/license and CC BY geometry notices retained. |
| Visualizer video | Existing SKILL -> video routing -> art direction/storyboard/motion/shaders -> renderer -> captions/poster/FFmpeg export | Latest local helper and four references preserved; existing manual R3F frame/export guidance linked. Nine renderer regressions include real encoding, audio and full decode. Explicit scene clock is required; scene helpers do not imply arbitrary frame export. |
| Distribution | Unique catalog entry -> four plugin manifests -> three generated host catalogs -> release inventory -> separate ZIPs | Catalog duplicate/path/version tests and Claude native validation pass. Cursor schemas and contained Markdown references checked. Other plugin bytes and existing media are unchanged. |

83 repository tests passed using the bundled Python with Pillow. Skill metadata validation passes
for both packaged skills. These checks prove package and helper behavior; no fresh native-agent
efficacy or provider marketplace approval is inferred. Publication receipts remain in the owning
release tracker, separate from provider decisions.

User-requested upgrade film: existing Visualizer demo -> additional Light takes form
player -> downloadable MP4/VTT/poster -> complete editable source -> public runtime
imports -> app-owned timeline/capture adapter. Original film retained. Supplied archive
is safe and checksum-consistent; full decode/metadata and six distributed frames checked.
The original production-run claims remain identified as historical source documentation.

## Outcome review 1.0.0 and maintained skill synchronization

Scope: add Does It Make Sense?1.0.0; refresh UI Foundation Reuse to1.1.0 with the
maintained0.7.0 runtime; update Visualizer to1.2.1 with current feedback/learning guidance.
Base collection:4d691cf. DDD1.3.0, Engineering Spikes1.0.0 and Video Analysis1.0.0
release inventories remain byte-identical to that base. No application code, demos,
external marketplace submissions or publisher agreements are changed by this branch.

| Cluster | Trace and candidate disproof | Evidence / limits |
| --- | --- | --- |
| Outcome assessment | Original problem -> actual build/entry point -> state/consumer -> terminal result -> evidence -> bounded refinement. Backward component-purpose trace; defects, required gaps, optional refinements and missing proof separated. | Packaged instructions and metadata exactly match the installed source. Authored scenario review covers satisfied goals/no change, incomplete criteria, asynchronous completion, unavailable runtime proof and goal expansion requiring a decision. No fresh independent-agent efficacy claim. |
| Outcome discovery | One registry identity -> four plugin manifests -> three generated catalogs -> complete contained skill, UI metadata, original SVG and MIT notice. | Skill validation, JSON/SVG parse and contained Markdown links pass. No executable helper or hard dependency added. Repository distribution does not establish official native approval. |
| Reuse payload | Maintained installed skill -> public copy preserving author byline -> checksum metadata -> runtime archive -> public export targets -> app-local staging helper. | SHA-256 d08c4e0b447bade19f7ea77d5bf138b7e0976cd7da3d947385dc78fda96bfe2c; runtime0.7.0,2431 regular contained files,85 export entries. Existing archive/export, repeated staging, conflict preservation and symlink escape tests pass. Consumer applications remain pinned; native/visual rendering is not newly verified. |
| Visual feedback | Existing visualizer entry -> video reference -> conditional learning reference -> project feedback -> bounded supported reusable lesson. | Local video entry adapted only for its reference location; manual R3F export guidance retained. Existing interactive/data/R3F routes, renderer and demos preserved. Current request overrides past preferences; saved notes do not train a model. |
| Snapshot and distribution | Four independently versioned manifests -> catalog generator -> release hashes -> Git branch snapshot. | Catalog --check and complete repository suite83tests pass. A first run encountered three10-second subprocess timeouts in unchanged DDD tests; the focused guard suite51tests and subsequent complete83-test run both passed. Claude native validation passes with12 nonblocking icon/documentationUrl compatibility-field warnings. |

All five clusters are accounted for. Consumer, contract, registration, snapshot and
source-copy freshness are checked; no scheduler, persistence schema or production handler
changed, so cadence/migration/mount checks have no changed runtime path. A local video-only
skill is not a replacement for the broader published Visualizer: preserve its stable identity
and add only its current video guidance. Local shared discovery paths are not public package
content. Official provider activation, live user effectiveness and model adherence remain
unverified and require their own evidence. This branch does not close pending review cases.


## Published-identity update — November 11

Scope: isolate the latest five maintained updates on the November 1 public base
35e9eeadc8197347cf80f825d45e5febde0f67cd; preserve exactly six catalog identities and
Engineering Spikes' inventory. New plugin additions and their commit history are excluded.

| Cluster | Connected-path trace | Evidence / limit |
| --- | --- | --- |
| Discovery and packages | Six registry entries → portable and host manifests → generated catalogs/release hashes → complete plugin ZIPs | Catalog generation/check and native CLI validation pass; package and repository link/version tests pass. Native provider review remains separate. |
| DDD and outcome review | Existing entrypoints → handoff evidence references / requester authorization → unchanged guard and outcome consumers | Included in 139 collection tests, no skips. No fresh agent-efficacy claim. |
| Visualizer | Existing root routes → timed spec, motion/renderer references → media-in-3D CLI and its optional dependencies → export/review | Distributed adapter, renderer and sound regressions included in collection gate. Optional external model/render providers not exercised. |
| UI Foundation | Skill → bundle metadata/checksum → staging helper → bundled 0.11.0 exports/source/types and notices | Archive integrity, every public export target, idempotent staging and conflicting archive/symlink rejection verified. No agent install performed. |
| Snapshot boundary | Frozen selected plugin folders → generated per-file inventories → staged commit → release artifacts | All six folders exactly match the selected local source snapshot; Engineering Spikes exactly matches the public base. Each ZIP is re-read against release.json. |

Checks: `python3 -B -m unittest discover -s tests` — 139 passed in 14.446s, no skips;
`python3 tools/build_catalogs.py --check` — four generated files verified;
`claude plugin validate .` — passed, four nonblocking install-line suggestions;
`git diff --check` — passed. Cadence, database persistence and app mounts are not changed.
No tests or implementation for held-back plugins are included. Provider update outcomes belong
to the existing marketplace receipt, with their actual observation times preserved.

## Follow-up to the November 11 existing-skill release (local)

On top of aa78e30: ui-foundation-reuse 1.2.1 (critique loop in the skill; bundle rebuilt from ui-foundation 2530792),
video-analysis README "Python 3.10+", docs/visual-skills-validation.md spacing, catalog builder skips tool folders
(.venv, caches) with a test, .venv ignored, tools/hooks/pre-push with its PUBLISHING note. New plugins stay on the
local `new-plugins` branch. Checks: unittest discover OK; build_catalogs --check passes.

## Tony Stark and maintained-skill release — November 12

Authorized scope: six existing public plugin identities plus what-if-tony-stark-built-this.
Start from public 9593865; freeze selected development folders, preserve newer public UI
1.2.1, and integrate the earlier isolated Visualizer sound-runtime fixes as 1.4.3.
The original development checkout and other local skills are not modified or published.

| Cluster | Entry, consumers and effects | Verification and limits |
| --- | --- | --- |
| Discovery and package | catalog.json → seven portable/Claude/Cursor/Codex manifests → generated catalogs/release.json → complete plugin ZIPs | Validate identity/version/author/link/hash contracts; native review and index activation remain external. |
| Tony Stark guidance | host discovery → SKILL.md → invention-methods and optional scoped references → proposal or authorized working slice | Runtime guidance has no required service, hook or telemetry. Optional evaluation CLIs remain outside skills/; deterministic harness tests exercise matched inputs, isolation, graders and fixture failure paths. Fresh model trials are not run or claimed. |
| DDD guidance | SKILL.md → handoffs → observed batch coordination cases → actor/scope/revision checks | Preserve guard implementation and caller contract. New prose has static link/consistency coverage, not universal host adherence proof. |
| Visualizer sound | sound_design.py runtime/get/fetch/probe/mix → explicitly provisioned local tools → bounded audio and provenance | Regression tests cover child-secret isolation, anonymous proxy boundary, invalid output/code/playlist refusal and valid WAV provenance. Live providers and fresh full Earshot mixes remain outside this release check. |
| Unchanged/public reuse | public UI1.2.1 bundle → staging helper and export checks; Video/Sense/Engineering existing entrypoints | Preserve public UI inventory and earlier release identities; no global skill installation or application changes. |

Consumer, contract, registration and snapshot edges are checked by the selected tests and
release inventory verification. No app mount, schema migration or scheduled task changes;
mount/back-compat/cadence edges are not applicable. Final gate and exact revision results
are recorded below after execution. Release artifacts belong to this release checkout.

Collection gate: `python3 -B -m unittest discover -s tests` — 162 passed in 25.028s,
no skips. Native `claude plugin validate .` passed with four advisory install-line
suggestions. Initial diff check found a trailing blank line in the new Visualizer
README section; normalized before final catalog/package hashing. No live model
evaluation, provider credential flow, native publication or installation was run.

Release scope checks: exactly seven registry entries/folders, no held-back plugin files or
history; UI1.2.1, Video1.0.1, Sense1.0.2 and Engineering1.0.0 inventories match public
9593865 exactly. Four complete ZIPs are re-read against release.json, including each
file hash. Extracted Visualizer ZIP: 23 sound tests pass in 0.288s, no skips.
Tony Stark ships reusable protocols, fixtures and summarized results; raw local
evaluation-session archives are excluded. The source development folder is untouched.

## Tony Stark 2.1.0 and App Retention 1.1.0 release — November 13

Scope: start from public e9ce3d0, freeze only these two development plugins and
their Tony harness tests. Preserve the six established public plugin inventories.
Exactly eight registry identities; all other development plugins and history remain private.

| Cluster | Connected path | Evidence and boundary |
| --- | --- | --- |
| Discovery | catalog.json → portable and three host manifests → generated catalogs and release hashes → plugin ZIPs | Identity/version/author, contained paths, links, licenses and exact inventory checks. Official directory approval remains external. |
| Tony comparison | SKILL.md → comparison-runner reference and example manifest → compare_designs CLI → contained source validation and identities → worker subprocess → exact JSON correctness, separate timing/allocation trials → conservative decision → exclusive report publication | Tests cover incorrect variants, nonfinite/bool values, escapes, timeouts/crashes, memory caps, input changes, sibling imports, process cleanup, concurrent report writer and ties. Executes inspected authorized local code; process separation is not a security sandbox. No model/API trial rerun or efficacy claim. |
| Optional evaluation | README → frozen protocols/results → matched trial preparation, private evaluator checks and synthetic fixtures | The sequencing fixture retains its source hash and reference copy; its source plugin is deliberately absent. The public test now verifies frozen provenance and exclusion instead of requiring a held-back plugin. Catalog fixture still matches the included maintained tool. No raw sessions/archives ship. |
| App Retention | host discovery → SKILL.md → patterns/distribution references → product-specific implementation handoff | Guidance only, no runtime service/helper. Frontmatter, reference resolution, manifest consistency and package inventory checked; no product efficacy or native activation inferred. |

Consumer, contract, registration, default, snapshot and concurrent-writer edges are
covered by runtime/contract tests and release inventory review. No application mount,
schema migration or recurring task cadence changes. The original development tree is
read-only for this task; release edits and evidence belong to this isolated checkout.

Final behavior gate: 193 collection tests passed in 37.161s, no skips. Extracted
Tony ZIP: all 25 comparison-runner tests passed in 11.342s, no skips. Both skill
metadata validators passed with isolated PyYAML 6.0.3; native validator passed
with five advisory README installation suggestions. Final diff review normalized
one App Retention trailing blank line before regenerating its inventory and ZIP.

### Requested creative title: Returncraft

App Retention 1.1.0 was already published when the user requested a creative name.
Rename display metadata, README and skill title to Returncraft in 1.1.1, retaining
`app-retention` as the stable plugin/skill identifier. No runtime behavior changes,
new identity, or edits to the other seven plugins; historical 1.1.0 assets remain.
Trace: catalog → four native/portable display fields → skill UI metadata/title →
README and existing installation identifier. Rebuild release hashes and verify
frontmatter, independent versions, native catalogs and artifact inventory.

### Visualizer 1.4.5: data-city and explainer-control recipes

Two recipes held for the owner's approval, added to existing references (no new files): a data
city in `references/data.md` and explainer controls (cutaway, camera-shot hotkeys, rewind to a
beat, pinned notes) in `references/interactive.md`. Each was built first as a small React Three
Fiber demo outside the repository and checked in headless Chromium (React 18, Three.js 0.160,
R3F 8): three browser tests covering height/value proportion, rejected and no-data records,
picking by stable id, plan view, beat jumps, the rewind grace rule, seek determinism, cutaway,
shot keys with and without reduced motion, a note following a moving part, and the typing guard.
Two defects found in the demos shaped the text: a note anchored to a fixed point drifted off a
moving part, and notes pointed at parts hidden by the casing. Demo sources and screenshots are
not distributed with the skill. Trace: SKILL.md routing rows → data.md / interactive.md (unchanged
links) → React Three Fiber reference for capture of DOM notes. Checks on this branch:
`build_catalogs.py --check` verified, unittest discover 193 OK, `claude plugin validate` passed
for the plugin and the marketplace. Unverified: other React/Three/R3F versions, real GPUs, touch
input, screen readers, and whether an agent applies the recipes unprompted.
First prepared as 1.4.4; renumbered to 1.4.5 and re-applied on top of main after main published
its own 1.4.4 (credential-free tool environments) while this work was in progress.

### Visualizer 1.4.6: both demo films re-cut

The owner asked for the repository's Visualizer videos to show the latest work, and chose to re-cut
both films. No skill instructions change; the version moves because the plugin README does.
`assets/visualizer-r3f-demo.*` (React Three Fiber, 36 s) now shows the data-city recipe and the
explainer controls. `assets/visualizer-demo.*` (Three.js, 32 s) now shows picture on a beat grid
measured from the final mix, motion asked for by name and a four-beat looping asset. Each was
built from its existing source ZIP with the existing manual-frame export, and its poster, SRT,
VTT, validation and source ZIP were regenerated. `visual-skills-demo-source.zip` changes because
it holds the Three.js film's source; every Video Analysis file inside it is byte-identical
(`exports/video-analysis.mp4` 63ef965d…, `audio/video-analysis.wav` 078b3826…). The UI Foundation
film is untouched.

Trace per film: timeline (scenes, events, cues) → pure models → scene and in-picture type → frame
export at explicit times → encoder → MP4 → verifier (frame count, full decode, loudness, distinct
neighbouring frames; for the Three.js film also loop closure and the beat-map hash). One
independent critic, given frames and a brief only, found five material defects (a note pointing at
a hidden part, an install command drawn with one dash, list highlighting that lagged the action, a
follow-through that happened before its scene, pulsing rings too thin to see) and about two dozen
minor ones; all five and most minor ones were fixed and both films re-exported. The check after the
fixes was the author's own on decoded frames, not a second independent round. Effects were
measured against the music stem and key-press clicks raised about 10 dB.

Results: R3F 36.0 s, 2,160 frames, 10.26 MB → 6.94 MB, −15.36 LUFS, −1.63 dBTP. Three.js 32.0 s,
1,920 frames, 5.39 MB → 5.05 MB, −16.22 LUFS, −1.46 dBTP; frames one loop apart differ by 0.28
luma levels against 4.77 a quarter-loop apart; fitted 99.997 BPM, mean beat offset −6.1 ms, largest
26 ms. Both sampled with the video-analysis sampler (23 frames each at decoded timestamps); a
local transcription returned only a stock phrase on the music, consistent with no speech.
One R3F export was discarded because the canvas was resized mid-export; the exporter now holds
the export size.

Open: the README players are GitHub upload URLs, so the plugin README still plays the first R3F
cut until the owner uploads the new MP4 and replaces the URL. Unverified: listening review,
browsers other than headless Chromium on Apple M1 Max, word-level speech timing (there is no
narration), and whether either film changes how an agent uses the skill.
