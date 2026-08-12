---
layout: post
date: 2025-06-19
title: "Context Rot from AI"
type: linked
cited: Simon Willison
link: https://simonwillison.net/2025/Jun/18/context-rot/#atom-everything
seo: ""
---

Via Simon Willison, a quote from a comment on Hacker News by Workaccount2. Sharing here as I've found that I have inadvertently been doing this myself when wanting to move on with an agent and not have it carry existing context into a new request.

> They poison their own context. Maybe you can call it context rot, where as context grows and especially if it grows with lots of distractions and dead ends, the output quality falls off rapidly. Even with good context the rot will start to become apparent around 100k tokens (with Gemini 2.5).
>
> They really need to figure out a way to delete or "forget" prior context, so the user or even the model can go back and prune poisonous tokens.
>
> Right now I work around it by regularly making summaries of instances, and then spinning up a new instance with fresh context and feed in the summary of the previous instance.
> — Workaccount2 on Hacker News, coining "context rot"
