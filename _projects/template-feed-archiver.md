---
layout: projects
title: "Track a RSS/Atom feed on GitHub - Template Repo"
permalink: /projects/create-archive-of-feed-on-github-with-this-template
seo: "Create a copy of this repo to fetch and archive a feed on GitHub with this template"
class: scripts
i_name: View
i_url: "https://github.com/thechelsuk/template-feed-archiver"
summary: "A Repo template for monitoring and archiving a feed."
type: wrench
---

A GitHub template repository setup to copy an rss or atom feed into a `_data` folder in a repo for monitoring and archiving purposes.

- Simply copy the repo.
- Change the `daily.yml` action to include the feed url and the output file name
- GitHub Action runs on a daily schedule and will commit any new updates into the repo.
