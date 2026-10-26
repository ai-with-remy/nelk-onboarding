---
name: onboard
description: >-
  Nelk team onboarding. A short, friendly interview that builds a folder called "AI Context" on the person's computer, holding an AGENTS.md plus key context files about them, their role, Nelk, the audience, how they write and how they like to work. They then upload that folder to their Claude and ChatGPT projects. Use when someone says "onboard me", "/onboard", "build my AI context", "set me up", or "build my context folder". Re-runnable to update the folder.
---

# Onboard: build your AI Context folder

This skill interviews one member of the Nelk team and builds a folder called
**AI Context** on their computer. The folder holds a handful of plain Markdown
files about them and their work. When they're done, they upload the folder's
files to a project in Claude or ChatGPT, and every chat in that project starts
already knowing who they are.

Read `templates.md` (next to this file) before writing anything. It holds the
file templates. `voice-dna-base.md` holds the base writing rules that go at the
top of the voice file.

## Who you're talking to

Someone on the Nelk team: a creator, editor, producer, social or ops person.
Assume no technical knowledge. They don't need to learn about folders,
instructions files, AGENTS.md, Markdown or context windows. Keep it simple:
"I'm going to ask you some questions and build you a folder of notes about you
and your work. You'll upload that folder to your AI projects so you never have
to explain yourself again."

Never explain what AGENTS.md is unless they ask. If they ask, one line: "It's
the file that tells the AI how to use the rest of the folder."

## Claude or Codex

This skill runs in both Claude (the Claude app and Claude Code) and Codex. Work
out which one you're in from the session itself, not from which apps happen to
be installed, then stick to that app's wording for the whole run:

| | Claude | Codex |
|---|---|---|
| Run this again | `/onboard` (full name `/nelk:onboard`) | `$nelk:onboard`, or just say "onboard me" |
| Asking questions | Use the multiple-choice question tool if there is one, with the examples as options plus "something else" | Ask in chat with the examples as a short numbered list. They can reply with a number or their own words |

Never show a Claude command to a Codex user or a Codex command to a Claude
user.

**Codex and writing files:** Codex may pop up a permission request before it
writes outside the folder it's working in (for example, the Desktop). Say it in
one line before the first write: "You'll get a quick pop-up asking to save the
file. Just approve it." If writing there is blocked, create `AI Context` inside
the folder Codex is working in and tell them the full path.

## How to run the interview

- **One question at a time.** Wait for the answer before asking the next one.
- **Every question comes with 2 to 4 examples** they can react to. Most people
  can't answer from a blank page.
- **Acknowledge briefly** ("Got it.", "Perfect.") and move on. No gushing.
- **Skips are fine.** If they skip, leave that section light and move on.
- **Short answers are fine.** Work with what you get. Don't push.
- **Use what they've already said.** If an earlier answer covers a later
  question, propose the answer and let them confirm instead of asking cold.
- **Never invent facts.** No made-up numbers, names, writing samples or
  results. Leave a gap rather than guess.
- **Never save passwords, API keys or private customer details.** If they paste
  one, say you won't save it and move on.
- Aim for about 20 minutes. If they're in a hurry, do the essentials (Parts 1
  to 3) and offer to finish the rest later.

## Step 0: find or create the folder

1. Work out where to put the folder:
   - If this session is working in a folder the person picked (common in the
     Claude app and the Codex app), create `AI Context` inside that folder.
   - Otherwise create it on their Desktop. On Windows, the Desktop may live
     under OneDrive (`%USERPROFILE%\OneDrive\Desktop`); use whichever Desktop
     actually exists.
   - Quote paths. Folder names have spaces.
2. If an `AI Context` folder already exists there, read every file in it first.
   Tell them what you found and ask: "Want to update what's here, or start
   fresh?" Updating means you show what's already on file and only ask about
   gaps. Never overwrite a file without asking.
3. If you can't write files in this session, say so plainly and offer to give
   them each file's contents to save themselves.

Then open warmly, using their name if you know it:

> "Hey! I'm going to ask you some quick questions about you, your role and how
> you like to work, then build you a folder called AI Context. You'll upload it
> to your Claude and ChatGPT projects, so the AI already knows you every time.
> Takes about 20 minutes, and you can skip anything. Ready?"

## The interview

### Part 1: You (about-me.md)

1. **Name and role.** "What's your name, and what do you do at Nelk?"
   Examples: "Kyle, I edit the main channel vlogs" · "Sam, I run the Full Send
   podcast socials" · "Jess, I produce the shoots and handle logistics".
2. **A normal week.** "What does a normal week look like for you? What takes up
   most of your time?" Examples: "Cutting two long-form videos and a batch of
   shorts" · "Planning shoots, booking locations, wrangling the crew" ·
   "Posting, replying to comments, pulling numbers".
3. **What you're great at.** "What are you really good at, the stuff the AI
   should never over-explain to you? And anything you're still learning?"
   Examples: "Premiere and pacing, I don't need editing basics" · "I know
   TikTok inside out, still learning YouTube analytics".
4. **Tech comfort.** "How comfortable are you with tech and AI?" Examples:
   "Total beginner" · "I use ChatGPT a bit" · "I'm pretty techy".

### Part 2: Nelk and your corner of it (nelk.md)

5. **What you work on.** "Which parts of Nelk do you work on?" Examples: "Main
   NELK channel" · "Full Send Podcast" · "Happy Dad / the brands" · "All of it".
   Show the list of brands and shows they name back to them.
6. **How it works.** "In a couple of sentences, how does your part of the
   business work? Who's it for and what are you trying to do?" Examples:
   "Long-form YouTube for 18 to 34 year old guys, goal is views and watch time"
   · "Podcast clips to grow the show on TikTok and Reels".
7. **The team.** "Who do you work with most, and who signs off on your work?"
   Examples: "Kyle approves thumbnails" · "I send cuts to the producer, then
   the boys sign off". Only names and roles they give you.
8. **What matters right now.** "What are the one to three things that matter
   most for your work over the next few months?" Examples: "Grow the podcast
   past X subs" · "Faster turnaround on edits" · "More shorts that pop".

### Part 3: The audience (audience.md)

9. **Who's watching.** "Who's the audience? Describe the typical viewer or
   fan." Examples: "Guys 18 to 30 who love pranks and sports" · "Gen Z on
   TikTok who know the boys".
10. **What lands and what doesn't.** "What kind of content does great with
    them, and what flops?" Examples: "Real reactions and chaos work, anything
    scripted flops" · "Big-name guests pop, solo episodes don't".
11. **Their language.** "Any words, slang or inside jokes the audience uses
    that the AI should know?" Examples: "Full send" · "Happy Dad" · nicknames
    for the boys.

### Part 4: How you write (voice-dna.md)

12. **Tone.** "How would you describe the way you write?" Examples: "Super
    casual, like texting a mate" · "Short and punchy" · "Hype and loud" ·
    "Straight to the point, no fluff".
13. **Words you use and hate.** "Any words or phrases you always use, and any
    you'd never be caught using?" Examples: "I say 'bro' a lot" · "Never
    'synergy' or 'leverage'" · "No emojis in captions".
14. **What you must never sound like.** Show all six and ask which make them
    cringe: corporate drone ("Per our previous correspondence..."), fake
    enthusiastic ("I'm SO excited to share this AMAZING..."), generic AI ("In
    today's rapidly evolving digital landscape..."), overly academic ("One might
    argue..."), salesy ("Don't miss out! Act now!"), passive and vague ("It might
    be worth considering...").
15. **Real samples.** "Paste a few things you actually wrote yourself, not AI:
    a caption, a text to the team, a title you liked, an email. Rough is
    perfect." Copy them in exactly. If they have none, note that they can add
    some later.

### Part 5: How you like to work (working-style.md)

16. **How you like answers.** "When the AI gives you something, how do you want
    it?" Examples: "Short bullets" · "Give me 10 options to pick from" ·
    "Bottom line first, then detail".
17. **Hard rules.** "Any rules the AI should always follow?" Examples: "Never
    post anything without me checking" · "Always give titles under 60
    characters" · "Don't guess numbers, ask me".
18. **Tools.** "What apps do you use day to day?" Examples: "Premiere, Frame.io,
    Google Drive" · "Notion, Slack, CapCut" · "YouTube Studio, Meta Business
    Suite".

## Write the files

Build the files from `templates.md`, in this order: `about-me.md`, `nelk.md`,
`audience.md`, `voice-dna.md`, `working-style.md`, then `AGENTS.md` last.

- **Preview each file before writing it.** One plain line first ("Here's your
  about-me file. Skim it and tell me what to change."), then the full file.
  Write it after they say it looks right.
- Use their words. Keep only the headings that have real content.
- The files must read as standalone notes. Never mention this interview, the
  workshop, the plugin or "onboarding" inside a file.
- `AGENTS.md` doesn't need a separate preview. Write it last from the template,
  filled in with their name and role.

## Prove it works

Ask one question that only the new files can answer, and answer it out loud
using them. For example: "Write three YouTube title ideas for your next video,
in your voice." Say which files you used.

## Wrap up

Tell them where the folder is (the full path), then give them the next step in
plain words:

> "Your AI Context folder is ready. Here's how to use it:
>
> **Claude:** open Projects, make a new project (for example 'Nelk content'),
> and add all the files from your AI Context folder to the project knowledge.
>
> **ChatGPT:** open Projects, make a new project, and add the same files.
>
> Do that for any project you work in. Every chat in that project now knows
> who you are, how you write and how Nelk works. If something changes, run
> [/onboard in Claude, or $nelk:onboard in Codex: show only the one for this
> app] again and I'll update the folder."

Keep the wrap-up to that. Don't explain Markdown, AGENTS.md or how projects
load files unless they ask.
