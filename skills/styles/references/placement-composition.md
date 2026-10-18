# Placement composition

For a hero, a call-to-action background, a card, or any image that must work inside a page. The goal is an image that works with its content, not a good picture on its own.

## Look at the slot first

Look at the rendered section and its source. Note the desktop and mobile sizes, the real copy, how the image is fitted, and which parts stay in code (type, buttons, gradients, masks). If another agent owns the page, hand over the images and a preview you can undo instead of editing over its work.

## Separate three things

- **Treatment:** camera language, materials, palette, light, texture. This is the Style candidate.
- **Subject:** what the image shows. Change it to test whether the Style holds.
- **Placement:** where the focus sits, the quiet area for copy, the crop, the mobile version. Keep this in each image's prompt, not in the Style, or every image the Style makes will be empty on the same side.

A reference can give treatment, structure or an exact identity. Say which. One well-chosen reference often gives more control than a mixed pool; try a wider pool when variety is the point. Crop browser bars and library chrome out of screenshots before using them. Keep logos and ordinary type in code when that gives the result.

## Compare honestly

Start with a small comparison that answers the current question, and keep a baseline. If several variables changed, say so: an art-direction comparison doesn't show that one model or quality setting is better.

## Check it in place

Put the candidate behind the real copy at its real size. Judge desktop and mobile separately. Look for bright lights, rooflines or window bars crossing text; missing faces or hands; subjects that only work at one crop; overlays that hide the image. Fix layout in code and the scene in the image. A local scrim keeps both text and light; darkening the whole picture usually loses its point.

If a wide image can't keep its subject and copy area on mobile, make a portrait companion from the chosen image: an edit (`parentAssetId`) when you mean the same picture, a new image with it as a reference when an adaptation is fine. Serve the right one per screen size, and check the portrait actually loads.

## Before calling it done

Test the treatment on a different subject. Write down what failed. Hand over the originals, sized files with real dimensions, crop or focal notes for desktop and mobile, the overlay treatment in code, each image's `assetId`, the exact prompts and references, and why you recommend the one you chose.
