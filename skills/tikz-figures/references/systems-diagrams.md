# Systems Diagrams

Load this reference only when `.writing/metadata.yaml` sets `writing_profile: systems` and the figure is a structural diagram.

## Figure brief gate

Read `.writing/figures/<fig_id>.brief.yaml` before choosing a layout or writing TikZ. Stop and list the missing fields when the file is absent or incomplete.

Require:

- `figure_id`, matching `<fig_id>`
- one primary analytical `question`
- one primary claim ID in `claim`
- a non-empty `sources` list with at least one `type: artifact` or `type: citation` entry and a locatable `ref`
- non-empty `conditions` stating scope, trust domain, protocol phase, or other boundaries needed to read the structure correctly
- one `family`, `order`, `encoding`, and non-empty `caption_facts`
- `interpretation_location: body`
- `route: tikz-figures` for routine diagrams

Allow `family: other` only with `family_reason`. Require `route_reason` whenever a built-in family's default route changes. Keep routine diagrams with a clear direction in TikZ.

Treat venue rules as higher priority than this reference. Record any width, font, or color departure under `venue_overrides` in the brief.

## Structural figure families

### `layered-architecture`

Use to answer what the architecture is, where responsibilities sit, or where a trust boundary lies.

- Arrange the primary execution or data path from left to right unless the domain convention requires another direction.
- Use spatial groups, labeled lanes, and explicit boundaries for machines, privilege levels, administrative domains, or trust zones.
- Place each real component in exactly one primary domain. Represent a cross-domain service explicitly rather than letting a box straddle an unlabeled border.
- Distinguish control, data transfer, computation, and return paths with arrow labels and line styles. Keep a small legend when the distinction is not obvious.
- Draw trust boundaries as labeled enclosing or separating geometry. Do not imply trust through color alone.
- Use a stable component and stage order matching the paper's prose and protocol description.
- Include only artifacts and relations supported by the brief's sources. Do not invent hidden services, links, or guarantees for visual completeness.

### `overlap-timeline`

Use to answer how protocol phases, requests, or resources overlap over time.

- Put time on the horizontal axis and actors, resources, or pipeline lanes on the vertical axis.
- Keep lane order stable and match it to the order used in the text or protocol.
- Align shared events vertically. Show causality with arrows only when the sources establish it; use alignment without arrows for mere simultaneity.
- Distinguish execution, waiting, transfer, and idle intervals with line style, fill pattern, or boundary treatment that survives grayscale.
- Mark synchronization points, barriers, and phase boundaries explicitly.
- Show whether lengths are measured, proportional, or schematic. Do not imply quantitative duration with arbitrary widths.
- For repeated or pipelined work, label the iteration or request and make overlap visually traceable across lanes.

## Lane, domain, and arrow grammar

- Use lanes for repeated actors, resources, protocol parties, or time-aligned stages.
- Use enclosing zones or divider lines for deployment and trust domains; label every non-obvious boundary.
- Favor one dominant left-to-right path. Route secondary control or return paths so they do not compete with it.
- Use solid arrows for the primary path. Use dashed or dotted arrows only with a defined meaning recorded in the brief and caption.
- Label arrows when payload, control action, or synchronization meaning is material to the claim.
- Make every arrow a continuous path from source to target. Avoid crossings and box penetration; use the TikZ skill's canonical routing and validation rules.
- Do not encode a relation only through proximity or color when a boundary, label, line style, or arrow can state it precisely.

## Semantic color and grayscale redundancy

Allow a small set of colors only for semantic roles that stay stable across stages, such as control, transfer, compute, return, or trust domain.

- Pair color with line style, boundary style, label, shape, or spatial grouping.
- Keep primary structure readable in grayscale.
- Preserve one semantic meaning per color throughout the paper.
- Use neutral fills for containers and reserve accents for paths or roles that the claim requires readers to track.
- Do not copy a palette or hex table from an external package. Use the existing TikZ color and accessibility guidance.
- Inspect a grayscale rendering at the final single-column or full-width size. Treat merged domains, paths, or phase types as a blocking defect.

Record the redundant mapping in the brief's `encoding.grayscale_redundancy` field, even when the main diagram uses semantic color.

## Caption facts

Write a fact-complete caption that can be understood without searching the body for structural definitions. Include:

- what the architecture, lanes, phases, or panels depict
- stage, lane, component, or method order
- scope, deployment setting, trust domains, protocol phase, and other relevant conditions
- meanings of boundaries, zones, arrow styles, fills, symbols, and abbreviations
- whether timeline lengths are measured, proportional, or schematic

Allow facts directly visible in the diagram. Keep causal explanations, security arguments, and broader design implications in the body near the first substantive reference. Keep `interpretation_location: body` in the brief.

## Final checks

- Compare every component, phase, boundary, and arrow against the recorded artifacts or citations.
- Check order and terminology against the manuscript.
- Inspect the rendered output in color and grayscale at its final placement size.
- Run the TikZ skill's compile, geometry, overlap, and visual-review checks.
- Stop rather than inventing missing components, relations, trust assumptions, or caption facts.
