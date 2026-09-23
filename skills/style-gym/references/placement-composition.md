# Placement composition

Use a real interface placement to develop a reusable visual treatment. The deliverable is an image that works with its surrounding content, not merely an attractive isolated picture.

Inspect the current rendered section and its source. Record desktop/mobile geometry, actual copy, image fitting, and which elements remain editable. If another agent owns the page, hand off assets and a reversible in-context preview instead of editing over its work.

Separate three inputs:

- **Treatment:** camera language, materials, palette, lighting, texture. This is the reusable Style candidate.
- **Subject:** what the image depicts. Change this for a holdout test.
- **Placement:** focal position, quiet area for copy, crop, and mobile composition. Keep these in the task prompt rather than making every future Style output empty on the same side.

A reference can supply treatment, structure, or an exact identity. State which role it serves. A narrowly chosen image often gives more control than a mixed pool; compare wider pools when variety is the actual objective. Remove screenshot browser/library bars before they enter the generation inputs. Keep original logos and ordinary type, buttons, gradients and masks in code when that gives the intended result.

Start with a small comparison that answers the current design question. Keep a baseline. Record when multiple variables change: an art-direction comparison is not evidence that a model or quality setting is superior. Use the live tool's supported model/settings rather than copying settings from an old case study.

Composite the candidate with real copy at its intended dimensions. Judge desktop and mobile independently. Look for bright lights, rooflines or window mullions intersecting text; missing faces or hands; crop-dependent subjects; and overlays that obscure the image. Fix layout issues in code and scene issues in the image. A localized scrim can preserve both readability and light; a uniformly darkened picture often loses its point.

If a wide composition cannot retain its subject and copy area on mobile, make a companion portrait using the selected image as the visual anchor. Use an exact-parent edit when available and intended; a fresh generation with a reference is an adaptation, not an edit-thread continuation. Use responsive image selection in the final page and verify the actual portrait loads.

Before endorsing a Style, test the treatment on a different subject. Record failures and limitations. If the authoring tool saves only text, do not claim it saved the reference pool or formal lineage. Category and thumbnail are separate library metadata; verify them through the Style tools. Keep the specific reference handles in the experiment record and call out missing authoring controls.

Follow [the durable MCP contract](../../asset-generator/references/mcp-contract.md): retain the request and job IDs, poll the returned job in the same workspace until terminal, and reuse the request ID only for an identical transport retry. A timeout or unknown outcome is not proof of failure or a refund. If polling must stop, hand off the unresolved handle; do not automatically repeat a paid generation.

Hand off original outputs, optimized files with actual dimensions, desktop/mobile crop or focal guidance, the editable overlay treatment, asset/receipt IDs where exposed, exact prompts and references, and the reason for the recommended choice. Mark proposed copy and preview-only actions. A browser mockup does not establish that the production wallet or navigation flow has been wired.
