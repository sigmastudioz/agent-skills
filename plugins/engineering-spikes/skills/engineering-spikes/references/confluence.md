# Confluence delivery

Use this reference when producing the final pair of documents. Formatting readiness is separate
from permission to publish and from proof that the investigation's claims are correct.

## Portable output

- Deliver two distinct documents/pages, one per audience. Give each a title, shared spike ID,
  status/date and companion link. Keep filenames and titles stable across revisions.
- For file delivery, use simple standalone HTML that renders locally: semantic headings,
  paragraphs, lists, ordinary links, basic tables and `pre`/`code` for engineering snippets.
  Escape source text rather than interpreting it as HTML. Do not include scripts or remote trackers.
- Tell the user to open the HTML and copy its **rendered content**, rather than paste HTML source.
  Editable Markdown variants are useful, but raw Markdown is not a universal bulk-import format.
- Use shallow headings, short paragraphs and narrow tables with header rows. Split wide tables;
  avoid merged/nested cells, layout tables, raw wiki macros and dependence on custom CSS.
- Keep references meaningful after paste: use accessible source URLs. Local artifact links must be
  attached or replaced with destination links when publication is authorized; do not expose private
  filesystem paths or advertise inaccessible links as working Confluence references.

## Workflows and code

Choose a diagram only if it explains an important interaction, branch, ownership boundary or
failure path better than prose. Skip it when a few sentences suffice.

Mermaid source can be an editable engineering asset. Use a rendered image with caption/alt text
and an equivalent short numbered flow unless the target space's diagram support is verified.
Use a host-authorized renderer if available; do not upload private architecture to an external
rendering service or install an app just to complete a diagram. If rendering is unavailable,
deliver the textual flow and label the diagram source as unrendered. Do not claim native Mermaid
support merely because a fenced block displays in another Markdown viewer.

Keep code confined to the technical document and use Confluence code elements when editing the
actual page. Avoid code inside table cells. Give proposed snippets a purpose and validation state.

## Verification and publication

Preview both outputs locally. Check headings, table wrapping, source links, special characters,
image readability and technical code formatting. Compare both audience versions for substantive
agreement. Remove template guidance; explicitly retain genuine unknowns rather than blank answers.

If the user authorized a Confluence destination and access exists, test the rendered paste in that
destination's editor before claiming target compatibility. Publishing or attaching restricted
evidence needs the corresponding authorization. Without target access, report **local preview
verified; Confluence paste unverified**. Do not turn that limitation into a claim of a successful
live publication or a request to change unrelated account permissions.

## Primary references

Checked 2026-10-22; recheck when target editor behavior matters or changes:

- [Atlassian: legacy wiki/Markdown markup](https://support.atlassian.com/confluence-cloud/docs/insert-confluence-wiki-markup/) distinguishes legacy markup insertion from the cloud editor.
- [Atlassian: available Markdown commands](https://support.atlassian.com/confluence-cloud/docs/available-markdown-commands/) describes editing shortcuts, not a guarantee that arbitrary Markdown or Mermaid renders on bulk paste.
