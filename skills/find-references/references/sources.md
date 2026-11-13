# Sources

Where references come from: what each source is good for, what its licence and attribution ask, and its limits. `find_references` reaches the first four. The person brings the rest, through their own uploads, links and connectors.

Taking a picture into a Style is still use under its source's terms; "only a reference" doesn't change that. So every reference keeps its `source`, `sourceUrl`, `licence` and `author`, and `get_style` returns them, which is also how one can be found and taken out if its owner asks.

## Open sources, through `find_references`

### Pexels (`source: "pexels"`)

- **Good for:** photography. Light, colour grading, materials, interiors, places, product and lifestyle looks. Little illustration.
- **Licence:** the Pexels License. Free to use and to modify, and attribution isn't required. Not allowed: identifiable people shown in a bad light or offensively, unaltered copies sold (as posters, prints or products), implying that people or brands in a photo endorse a product, and redistributing the photos on other stock or wallpaper sites.
- **Attribution:** Pexels' API guidelines ask for a prominent link to Pexels wherever its results are shown, and credit to the photographer when possible. Show each Pexels candidate with its `attribution` ("Photo by {author} on Pexels", linked to its `sourceUrl`), and keep `sourceUrl` with the reference.
- **Limits:** the service's key allows 200 requests an hour and 20,000 a month, shared by everyone, so results are cached for 10 minutes. Without a key on the service, Pexels is skipped and `sources` says so.

### Openverse (`source: "openverse"`)

- **Good for:** illustration, prints, paintings, posters, graphic design and photography gathered from many collections (Flickr, museums, Wikimedia and others).
- **Licence:** per item, Creative Commons or public domain. The finder asks only for licences that allow commercial use and changes: CC0, the public domain mark, CC BY and CC BY-SA. Openverse says it can't vouch for the licence information and that each work's licence should be checked: open `sourceUrl` before anything that matters.
- **Attribution:** CC BY and CC BY-SA ask for the title, the author, a link to the source and the licence; the candidate's `attribution` has them. CC0 and public domain ask for none; keep the credit anyway.
- **Limits:** anonymous use, with low rate limits. Quality varies more than on Pexels: look at the sheet before showing it.

### Wikimedia Commons (`source: "commons"`)

- **Good for:** art history, old prints and posters, botanical and scientific illustration, maps, type specimens, architecture and textures.
- **Licence:** the finder keeps CC0, CC BY, CC BY-SA and public domain only. A file's licence covers copyright: trademarks, and the likeness of people shown, can still restrict use.
- **Attribution:** the author, the licence and a link to the file page (`sourceUrl`), as the candidate's `attribution` gives them.
- **Limits:** search reads file titles and descriptions, so mood words find little. Name the medium, the technique or the movement: "woodcut", "Bauhaus poster", "cyanotype".

### Are.na (`source: "arena"`, through `arenaChannel`)

- **Good for:** a channel the person, or someone whose taste they trust, has collected. The closest thing to their own moodboard.
- **Licence:** Are.na doesn't license what's on it; each block belongs to whoever made it. `licence` is what the block's source says, often nothing. Tell the person, keep `sourceUrl`, and leave out what they aren't sure they may use.
- **Limits:** only a channel the person pastes (its link or slug), at most 50 items. Never a search across Are.na and never a bulk pull, as its terms ask.

## The person's own

- **Uploads** (`source: "upload"`) and **public image links** (`source: "link"`): always welcome, as theirs. The person answers for having the right to use them.
- **Their library** (`source: "library"`): images they made or saved earlier. A saved image's `imageUrl` is a link input.
- **Connectors in their AI app** (`source: "other"`, `suppliedBy: "person"`, the connector named in `note`). The agent uses them with the person's own sign-in and never asks for or handles a password, key or token.
  - **Mobbin's MCP:** screens of real apps and websites. Good for the look of an interface, not for illustration. Keep each screen's `mobbin_url` as `sourceUrl` and cite it as a link. Its `image_url` expires after 30 days, so with a shell download it and upload it (`create_upload_link`); without one, the person saves it and drops it on the upload page. When an answer carries an `ai_usage_notice`, show its text word for word. Screens carry other companies' names and logos, which can leak into images: leave out those where the brand is what stands out.
  - **A Pinterest connector:** pins the person saved or searched with their account. Keep the pin's page as `sourceUrl`.
  - **Web search:** images from anywhere. Keep the page as `sourceUrl` and the licence it states. Leave out results from the sites below.

## Not fetched by us

The finder never reaches these, and the agent never opens, searches or scrapes them with a web fetch or a browser, or passes their page links to our tools. What the person brings from them through their own connector, an upload or an image link they paste is theirs, like any other.

| Site | Why |
|---|---|
| Pinterest | Its developer guidelines bar scraping, data extraction, AI training and storing API data, and new apps may be refused board data. |
| Cosmos, Savee, Dribbble, Behance | No public API, or their terms bar programmatic access. |

Not in the finder yet: Unsplash and Brave image search, which wait for written confirmation that AI use is allowed. Google's and Bing's image search APIs are closed.
