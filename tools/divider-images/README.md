# Section-divider art

Nearly every `lead` section-divider slide carries one image in a soft chibi anime style, placed
right after the lead comment:

```markdown
<!-- _class: lead -->

![bg right:50%](images/<id>.jpg)

# Part N — Title
```

Most decks use `bg right:50%`; the Day 16 and Day 17 metadata decks use `bg right:55%`. Match the
width the deck's other dividers already use. A comment on the slide points back to the prompt file.

Each JSON file here lists the scene prompt for every divider image in a set of decks:
`week02.json` to `week14.json` hold the first anime pass (October 27, 2026), and
`gap-fill-2026-10.json` holds the dividers that had no image after that pass, plus the Part
dividers added on October 28, 2026. The `week*.json` files record the full prompt, style suffix
included; `gap-fill-2026-10.json` records the scene prompt only, with the deck and divider title.
Every image gets the same style suffix:

> — Japanese anime illustration style, clean cel shading, expressive large eyes, gentle
> pastel-leaning colors with a few warm accents, soft lighting, calm uncluttered composition.
> Absolutely no text, words, letters or numbers anywhere in the image.

Generated with the OpenAI images skill (`gpt-image-2.5-flare`, medium quality, 1024 × 1024) and saved
into the deck's `images/` folder as JPEG at quality 85, named `<deck-prefix>-divider-<slug>.jpg`.

When writing a new prompt:

- Describe the idea of the section as a scene, not a joke or a meme. Keep it plausible for a
  geomatics class: surveying, GPS receivers, maps, field work, satellites, campus.
- Chibi helpers are welcome (cute satellites, survey instruments, the folded-map and file-folder
  mascots that recur across the decks).
- Give about half of the solo scenes a woman lead; left unspecified, the model draws men.
- Never name an instructor, and no copyrighted characters.
- Avoid screens, signs and whiteboards, which invite fake lettering. Phrase a screen as "a glowing
  map on the screen".
- Look at every image for stray lettering, garbled screens, extra fingers or a scene that does not
  read before it goes in a deck, and regenerate the ones that fail.
