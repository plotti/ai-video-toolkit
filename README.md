# AI Video Toolkit

A **Claude skill** for evidence-based explainer videos. You tell Claude your topic and your theses; Claude does the research, fact-checks every number against the original study, and hands you everything you need to shoot and edit:

- a **teleprompter script** where every claim has a source, with a sources table and a list of corrections
- **study slides** with the original charts rebuilt as editable data
- **video quotes** (O-Töne) from YouTube, parliaments or your own archive, cut to the exact sentence
- a clickable **cut mockup**: slide left, speaker right, quotes full screen, script read by a text-to-speech voice
- a **preview MP4** of the whole video before you record a single take
- every quote as a **1080p clip with 5 s handles** plus a cut list for your editor
- a **rights traffic light** for every quote (quotation law CH/DE, not legal advice)

![Cut mockup](docs/mockup.png)

You don't run any of this yourself. You talk to Claude; Claude runs the scripts that come with the skill.

---

## Install

### Claude Code

```
/plugin marketplace add plotti/ai-video-toolkit
/plugin install ai-video-toolkit@ai-video-toolkit
```

Or from the terminal: `claude plugin marketplace add plotti/ai-video-toolkit` then `claude plugin install ai-video-toolkit@ai-video-toolkit`.

### Claude app (claude.ai, desktop)

1. Download [`studien-video-workflow.zip`](dist/studien-video-workflow.zip).
2. In Claude, open **Customize → Skills**, click **+ → Upload a skill**, choose the ZIP.
3. Make sure code execution (**Create and edit files**) is on in Settings → Capabilities.

---

## Use it

Just describe your video. The skill kicks in on its own, or call it explicitly with `/ai-video-toolkit:studien-video-workflow` (Claude Code) or by name ("use the studien-video-workflow skill").

> Make a 8-minute YouTube video on why trust in parliaments is falling. My notes and the studies I want to use are attached. Channel "Losdemokratie", speaker Thomas.

Claude will:

1. read your notes, check every number against the original paper and open a teleprompter doc you can edit,
2. suggest video quotes for each chapter and ask you to pick,
3. build the slide deck in your design (attach a template slide),
4. publish the cut mockup, then render the preview MP4,
5. on request, export all quotes in 1080p and produce the rights table.

Things you can say along the way:

| You say | Claude does |
|---|---|
| "Take quote 8 out, move the Robert quote to chapter 1" | edits the script, rebuilds the mockup |
| "Slide 12 doesn't work, find a better chart" | researches, rebuilds the slide, updates the sources |
| "What's the weakest part of the script?" | critiques and proposes a rewrite |
| "Render me a preview" | `out/<Title>_Preview.mp4` |
| "Give me all clips in 1080p with 5 s padding" | `out/schnitt_1080/` + `Schnittliste.csv` |
| "Can I use these clips?" | rights traffic light per quote |
| "Give me the sources for the YouTube description" | copy-ready list with DOIs |

The skill's instructions are in German (it was built for a German-language channel) but it works for videos in any language. Tell Claude which language and voice you want.

### Downloading YouTube clips

YouTube blocks cloud servers. In Claude Code on your own machine this just works. In the Claude app, link a folder on your computer (desktop app) so Claude can run the download there, or run the one command Claude gives you.

### Requirements on the machine that runs the scripts

Python 3.10+, ffmpeg, poppler, `pip install pillow piper-tts`, and `yt-dlp` for online clips. Claude installs what's missing. On a Mac: `brew install python ffmpeg poppler yt-dlp`.

---

## What's inside

```
.claude-plugin/marketplace.json          marketplace entry (for /plugin marketplace add)
plugins/ai-video-toolkit/
  .claude-plugin/plugin.json
  skills/studien-video-workflow/
    SKILL.md                             the workflow Claude follows
    references/                          project format, slides, rights, quote sources
    scripts/                             tts, mockup, preview, clip fetching, rights
    examples/demo/                       smallest working project
    examples/demokratiekrise/            real project: 26 slides, 19 quotes
dist/studien-video-workflow.zip          the same skill for upload to the Claude app
```

The scripts also work on their own (`python scripts/build_mockup.py <project>`); see [`references/toolkit.md`](plugins/ai-video-toolkit/skills/studien-video-workflow/references/toolkit.md) for the project format.

## License

MIT. Video quotes belong to their owners; the example project contains only references and timecodes, no footage.
