---
name: find-references
description: Finds reference images for a new look from the person's own finds and open sources, lets them pick, and groups the picks into directions so Style drafts differ. Use when the user wants inspiration, references or a moodboard for a Style, brings Pinterest, Mobbin or Are.na finds to base a look on, or says their drafts all look alike. Testing the drafts is styles; one image is asset-generator.
---

# Find references

Reference images for a new look: the person's own finds and open sources, chosen by the person and grouped into directions, one direction per Style draft.

**The rule: every draft gets references of its own, and the person picks them.** Drafts that reshuffle the same five pictures converge.

## Numbers

Measured on Blueprint Studio's MCP server.

- On 25 Styles run through the production generation path (12 to 13 Nov 2026), Styles made from reference images alone put the reference's subject into 42% of images. So pick references that share a look across different subjects, and search for the look, not the subject.
- Bad reference links were the most common external error, `INVALID_REFERENCE_IMAGE` and `REFERENCE_URL_UNREACHABLE` (28 Sep to 16 Oct 2026). Pass an image's own link, never the page it sits on.
- The finder and boards are new (Nov 2026): nothing measured on them yet.

## Steps

No `find_references` among your tools (search for it first if tools load on demand)? Follow Without the finder, below; with it but no `save_reference_board`, keep the board in the chat as that section says. In a brand, pass the same `brandId` on every call.

1. **Ask first.** In one message: what the look is for, which sources they already use (Pinterest, Mobbin, Are.na, Cosmos, sites they admire), and whether they have images or links of looks they love, or ones they don't. Take what they give as the table below says, noting where each came from. A page isn't an image. An Are.na channel goes to the finder (step 3). From Pinterest, Cosmos, Savee, Dribbble or Behance, never open the page: ask them to upload what they want from it, paste each image's own link, or bring it through their own connector for that site (step 2). Any other page you may open to find the image's own link, or ask for the image. Nothing to give? Go on to step 3.
2. **Use the connectors they already have.** Where the host has their own connectors (a Pinterest connector, Mobbin's MCP, web search), search them for the look, worded as in step 3. Mobbin is screens of real apps: use it when the look is for an interface, search the kind of screen as Mobbin asks, and pick by look from what it shows; for illustration or photography, skip it and say why. They're signed in already: never ask for a password, key, token or cookie, and never put one in a call. A connector that isn't connected is theirs to connect in their app, or they upload instead. From web search, leave out anything on the five sites in step 1. Show the finds you keep in step 4. Per source: [Sources](references/sources.md).
3. **Search the open sources.** `find_references` with a `query` that names a look, not a subject: medium, technique, light, palette, texture, era ("risograph print, two colours, heavy grain", not "coffee shop"). Leave `sources` out to ask Pexels, Openverse and Wikimedia Commons. Keep `count` at its default 12, so three rounds fit one board, and set `orientation` when the Style is for one shape. Read an Are.na channel they pasted in a call of its own: `arenaChannel` with its link or slug and no `query`, and `page` for its next items. Say in one line which sources answered and which were skipped and why, from its `sources`.
4. **Save the round, then show it.** Look at the contact sheet, and leave out near-duplicates, misses and anything already on the board (the same `sourceUrl`). `save_reference_board` with a fresh UUID `requestId` and the candidates you kept as `items`; on the first round also a `name`, a `brief` (the look and what it's for) and the person's own files and links; on later rounds the `boardId` it returned. Show the new finds in one message: the candidates under the board's numbers, and connector finds as C1, C2… with where each came from (each Mobbin screen as a link to its `mobbin_url`). Where Markdown images render, each thumbnail as one; in a terminal, a numbered list of links. Each candidate's `attribution` goes under it. Not the finder's own sheet: its numbers aren't the board's. Ask which feel right and which don't.
5. **Record what they said.** Connector finds they liked go on the board first: `save_reference_board` with a fresh `requestId`, the `boardId` and just those. Then `react_to_references` with the `boardId` and the board numbers they named as `likes` and `dislikes`, the connector likes included. Their own images are likes when they brought them as the look they want, dislikes when they brought them as what to avoid. Only their words; leave the rest undecided.
6. **Vary the next search from the likes.** Say in one line what the likes share ("all flat colour with heavy grain"), then search again with a query that keeps that, changes one other thing, and steers clear of what the dislikes share. Not `page: 2` of the same query; that is more of the same. Steps 4 and 5 again, on the same board. Two or three rounds at most; stop sooner once the likes make two directions. After three rounds with fewer than four likes, ask for their own images, or go on with what there is; a fourth round only if they ask.
7. **Group the likes into 2 to 4 directions.** Each differs from the first in one thing (the medium, the palette, the light, the texture or the era), named in its label, holds 2 to 5 liked pictures, and shares none with another. Too few likes for two: one direction is one draft, and the `styles` skill plans the others (with text, or from an existing Style). Show the directions with their labels and numbers, change them if the person says so, then `react_to_references` with `directions: [{ label, items }]`.
8. **Hand off to the `styles` skill, one direction per draft.** `get_reference_board` for every item's fields. Each direction becomes one draft labelled like it, whose `inputs` are its pictures, five at most and none in two drafts: each in the input form, `source` and `suppliedBy` the table gives its kind, with `sourceUrl`, `licence`, `author` and `note` copied from the board (or from your notes, where the board didn't keep one). The one shared set the `styles` skill may add is a direction's twin with text, to test the text. Then follow the `styles` skill: its prompts, the credit total said before anything runs, and the person's pick per prompt.
9. **Report.** The `boardId`, each direction and the draft it became, and the sources, licences and attribution behind them. Attribution stays with each reference, and `get_style` shows it; it isn't put in images.

## What each reference carries

Every reference keeps where it came from, from the board to the draft: `source` and `suppliedBy` as below on the board item and the Style input, a `sourceUrl` (the page it came from, else its own link), and `licence` and `author` whenever the source states them. A `sourceUrl` is only recorded, never fetched, so any page can be one.

| It is | Board item | Style input | `source` | `suppliedBy` |
|---|---|---|---|---|
| A `find_references` candidate | its fields as returned, without `number`, and its `attribution` as `note` | `{ kind: "url", url: imageUrl }` | its own | `"agent"` |
| Their file | `{ uploadId }`, with `sourceUrl` and a `note` naming the site when they say where it's from | `{ kind: "upload", uploadId }` | `"upload"` | `"person"` |
| Their public image link | `{ url, sourceUrl }` | `{ kind: "url", url }` | `"link"` | `"person"` |
| An image from their library | `{ url: imageUrl }` | `{ kind: "url", url: imageUrl }` | `"library"` | `"person"` |
| A connector find they liked | `{ url, sourceUrl, note }` or `{ uploadId, sourceUrl, note }`, `note` naming the connector | `{ kind: "url", url }` or `{ kind: "upload", uploadId }` | `"other"` | `"person"` |

- **A link** must be a public https PNG, JPEG or WebP. Anything else is uploaded.
- **Uploads:** one `create_upload_link` per file. With a shell and the file on this machine, `direct: true`, run its `upload.curl`, and use its `upload.uploadId`; otherwise the person drops the file on its `pageUrl` and `get_upload_link` gives the `uploadId`.
- **A link that expires or carries a signature** (Mobbin's `image_url` lasts 30 days): with a shell, download it and upload the file; with none, the person saves it and drops it on the upload page. One behind their login: the person saves and uploads it; never fetch it with their session or cookies.

## Without the finder

For a host that doesn't have `find_references` or the board tools yet. The same loop by hand:

- Steps 1 and 2 as written. The open sources come in only through their web search or links, each with its page as `sourceUrl` and the licence the page states. From an Are.na channel, ask for the images they want as links or uploads.
- Keep the board in the chat: a numbered list of each picture's link, source, licence and the person's reaction. Group the directions the same way.
- Hand off the same way: one direction per draft, five pictures at most, none shared, with each input's source fields. Put the sources and licences in your report.

## Known failures

- **Reshuffling one set.** Drafts made from subsets of the same few pictures converge, and the trial shows the same image in each column. Each draft gets its own pictures. With fewer than four likes, search again before planning drafts (three rounds at most, step 6).
- **A connector's images with no source.** Every connector find keeps its page as `sourceUrl` and the connector in `note`, and the person hears where each came from. When Mobbin's answer carries an `ai_usage_notice`, show its text word for word and follow it: if it limits AI use of the screens, keep them off the board and out of Styles, and say why.
- **Search terms that name a subject.** "Coffee shop" finds coffee shops, and the subject leaks into every image. Name the look; the subject goes in the trial's prompts.
- **Licences ignored.** Keep `licence`, `author` and `sourceUrl` on every reference. Pexels: a link to Pexels (its `sourceUrl`) stays with the photo, and its photographer is credited where shown. CC BY and CC BY-SA: the author, the licence and a link; CC BY-SA also asks that changed versions be shared under the same licence, so say so when one is picked. A find with no stated licence (Are.na, a connector, a link) is used under its source's terms: say so, and leave it out if the person isn't sure they may use it.
- **More than five references in a draft.** It's refused. Keep the five that show the direction best, or split it into two directions.
- **Asking for a connector's password or key.** Never, for any service, and never put one into a call. If they paste one, don't use it: tell them keys don't belong in the chat and to revoke that one. They connect their own apps; you use what is connected.
- **Browsing a site we don't search.** Never open, search or scrape Pinterest, Cosmos, Savee, Dribbble or Behance yourself (a web fetch, a browser, your own web search), and never pass a page or image from them that you found as a `url`, `query` or `arenaChannel`. What the person brings from them, through their own connector, an upload or an image link they paste, is theirs.
- **Reactions the person didn't give.** Record only the likes and dislikes they named. If they ask you to choose, say which and why, and record them once they agree.
- **Mixing up numbers.** The finder numbers its candidates and the board its items. Ask and record by the board's.
- **A full board.** A board holds 60 items. Before a save would pass that, say so and ask which of the new ones to leave out.
- **A timed-out save.** Send it again with the same `requestId`: a new one adds the items twice.
- **A stale upload.** Uploads work for 24 hours. For a trial started later, ask for the file again.

## Limits

- `find_references` searches Pexels, Openverse and Wikimedia Commons, and reads an Are.na channel the person pastes (50 items at most). Pexels is skipped, with a note, when the service has no Pexels key. 1 to 24 candidates a call (default 12), 30 calls a minute per person; a contact sheet holds 20 tiles.
- We never search or browse Pinterest, Cosmos, Savee, Dribbble or Behance; what's from there comes in only as the person's own. Unsplash and Brave image search aren't in the finder.
- A board holds 60 items. A Style or draft keeps 5 references at most; a trial has at most 6 drafts.
- It finds and groups references. Making and testing the Styles is the `styles` skill.
