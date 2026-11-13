---
name: find-references
description: Finds reference images for a new look from the person's own finds and open sources, lets them pick, and groups the picks into directions so Style drafts differ. Use when the user wants inspiration, references or a moodboard for a Style, brings finds from Pinterest, Mobbin or Are.na, or says their drafts all look alike. Testing the drafts is styles; one image is asset-generator.
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

No `find_references` among your tools (search for it first if tools load on demand)? Follow Without the finder, below. In a brand, pass the same `brandId` on every call.

1. **Ask first.** In one message: what the look is for, which sources they already use (Pinterest, Mobbin, Are.na, Cosmos, sites they admire), and whether they have images or links of looks they love, or don't. Take what they give as the table below says. A board or page link isn't an image: an Are.na channel goes to the finder (step 3); for any other (a Pinterest board, a Cosmos cluster, a Dribbble shot), ask them to upload the images they want from it, or bring them through their connector for that site (step 2). Never open, read or scrape those pages yourself. Nothing to give? Go on to step 3.
2. **Use the connectors they already have.** Where the host has their own connectors (Mobbin's MCP, a Pinterest connector, web search), search them for the look, as step 3 words it. They're signed in already: never ask for a password, key, token or cookie, and never put one in a call. A connector that isn't connected is theirs to connect in their app, or they upload instead. Each find is theirs: keep the page it came from as `sourceUrl` and the connector in `note`, and say where each came from when you show it. Leave out web search results from Pinterest, Cosmos, Savee, Dribbble or Behance; those come in only through the person's own connector, an upload or a link they paste. What each source is good for and asks: [Sources](references/sources.md).
3. **Search the open sources.** `find_references` with a `query` that names a look, not a subject: medium, technique, light, palette, texture, era ("risograph print, two colours, heavy grain", not "coffee shop"). Leave `sources` out to ask Pexels, Openverse and Wikimedia Commons; pass `arenaChannel` with an Are.na channel link or slug they pasted. Keep `count` at its default 12, so three rounds fit one board, and set `orientation` when the Style is for one shape. Say in one line which sources answered and which were skipped and why, from its `sources`.
4. **Save the round, then show it.** Look at the contact sheet, and leave out near-duplicates and misses. `save_reference_board` with a fresh UUID `requestId`, and, on the first round, a `name` and a `brief` (the look and what it's for); on later rounds the `boardId` it returned. `items` is everything you'll show this round, as the table below says. Show the person each item under the board's number for it, as the host shows images (its thumbnail as a Markdown image, or a link), with its `attribution` under each found one. Ask which feel right and which don't.
5. **Record what they said.** `react_to_references` with the `boardId` and the numbers they named as `likes` and `dislikes`. Only their words; leave the rest undecided. Their own images count as likes when they brought them as the look they want.
6. **Vary the next search from the likes.** Say in one line what the likes share ("all flat colour with heavy grain"), then search again with a query that keeps that, changes one other thing, and steers clear of what the dislikes share. Not `page: 2` of the same query; that is more of the same. Steps 4 and 5 again, on the same board. Two or three rounds at most; stop sooner once the likes make two directions.
7. **Group the likes into 2 to 4 directions.** Each differs from the first in one thing (the medium, the palette, the light, the texture or the era), named in its label, holds 2 to 5 liked pictures, and shares none with another. Show the directions with their labels and numbers, change them if the person says so, then `react_to_references` with `directions: [{ label, items }]`.
8. **Hand off to the `styles` skill, one direction per draft.** `get_reference_board` for every item's fields. Each direction becomes one draft labelled like it, whose `inputs` are its pictures with their source fields copied from the board (the table below): five at most, none in two drafts. Then follow the `styles` skill: its prompts, the credit total said before anything runs, and the person's pick per prompt.
9. **Report.** The `boardId`, each direction and the draft it became, and the sources, licences and attribution behind them. Attribution stays with each reference, and `get_style` shows it; it isn't put in images.

## What each reference carries

Every item keeps where it came from, from the board to the draft. Pass its `source` and `suppliedBy` on the board item and on the Style input, and `licence` and `author` whenever the source states them.

| It is | Board item | Style input | `source` | `suppliedBy` |
|---|---|---|---|---|
| A `find_references` candidate | its fields as returned | `{ kind: "url", url: imageUrl }` | its own | `"agent"` |
| Their file | `{ uploadId }` from `create_upload_link` | `{ kind: "upload", uploadId }` | `"upload"` | `"person"` |
| Their public image link | `{ url, sourceUrl }` | `{ kind: "url", url }` | `"link"` | `"person"` |
| A connector's find | `{ url, sourceUrl, note }`, or `{ uploadId, sourceUrl, note }` | as above | `"other"` | `"person"` |

- **Uploads:** one `create_upload_link`; with a shell and the file on this machine, `direct: true` and run its `upload.curl`; otherwise the person drops the file on its `pageUrl` and `get_upload_link` gives the `uploadId`.
- **A link that expires, carries a signature or needs their login** (Mobbin's `image_url` lasts 30 days) goes in as an upload, with its page as `sourceUrl`. With no shell, the person saves it and drops it on the upload page.
- **Inputs** also carry `source`, `sourceUrl`, `licence`, `author`, `note` and `suppliedBy`, so `get_style` keeps them with each reference.

## Without the finder

For a host that doesn't have `find_references` or the board tools yet. The same loop by hand:

- Steps 1 and 2 as written. The open sources come in only through their web search or links, each with its page as `sourceUrl` and the licence the page states. From an Are.na channel, ask for the images they want as links or uploads.
- Keep the board in the chat: a numbered list of each picture's link, source, licence and the person's reaction. Group the directions the same way.
- Hand off the same way: one direction per draft, five pictures at most, none shared, with each input's source fields. Put the sources and licences in your report.

## Known failures

- **Reshuffling one set.** Drafts made from subsets of the same few pictures converge, and the trial shows the same image in each column. Each draft gets its own pictures. With fewer than four likes, search again before planning drafts.
- **A connector's images with no source.** Every connector find keeps its page as `sourceUrl` and the connector in `note`, and the person hears where each came from. When Mobbin's answer carries an `ai_usage_notice`, show its text word for word.
- **Search terms that name a subject.** "Coffee shop" finds coffee shops, and the subject leaks into every image. Name the look; the subject goes in the trial's prompts.
- **Licences ignored.** Keep `licence`, `author` and `sourceUrl` on every reference. Pexels: a link to Pexels (its `sourceUrl`) stays with the photo, and its photographer is credited where shown. CC BY and CC BY-SA: the author, the licence and a link. A find with no stated licence (Are.na, a connector, a link) is used under its source's terms: say so, and leave it out if the person isn't sure they may use it.
- **More than five references in a draft.** It's refused. Keep the five that show the direction best, or split it into two directions.
- **Asking for a connector's password or key.** Never, for any service, and never put one into a call; if they paste one, don't use it. The person connects their own apps; you use what is connected.
- **Fetching from a site we don't use.** Don't open, search or scrape Pinterest, Cosmos, Savee, Dribbble or Behance with a web fetch or browser, and don't pass their page links to our tools.
- **Reactions the person didn't give.** Record only the likes and dislikes they named. If they ask you to choose, say which and why, and record them once they agree.
- **Mixing up numbers.** `react_to_references` takes the board's numbers, not the finder's. Ask by the board's numbers, and match anything named from the finder's sheet by its image.
- **A timed-out save.** Send it again with the same `requestId`: a new one adds the items twice.
- **A stale upload.** Uploads work for 24 hours. For a trial started later, ask for the file again.

## Limits

- `find_references` searches Pexels, Openverse and Wikimedia Commons, and reads an Are.na channel the person pastes (50 items at most). Pexels is skipped, with a note, when the service has no Pexels key. 1 to 24 candidates a call (default 12), 30 calls a minute per person; a contact sheet holds 20 tiles.
- We fetch nothing from Pinterest, Cosmos, Savee, Dribbble or Behance: they come in only through the person's own connector, uploads or links they paste. Unsplash and Brave image search aren't in the finder.
- A board holds 60 items. A Style or draft keeps 5 references at most; a trial has 6 drafts.
- It finds and groups references. Making and testing the Styles is the `styles` skill.
