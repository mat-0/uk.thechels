---
layout: projects
title: Drafts Actions List
permalink: /projects/drafts
seo: "Drafts actions master list"
class: scripts
i_name: View
i_url: "https://actions.getdrafts.com/search?utf8=✓&q=thechelsuk"
summary: "Drafts is a Mac and iOS app made by Agile Tortoise. The app supports custom actions and scripts written in JavaScript, here is a list of actions I have created."
type: wrench
---

Drafts is a Mac and [iOS app](https://apps.apple.com/us/app/drafts/id1236254471) made by [Agile Tortoise](https://getdrafts.com). The app supports custom actions and scripts written in JavaScript, here is a [list of actions](https://actions.getdrafts.com/search?utf8=✓&q=thechelsuk) I have created.

## OMDB Film Search

- Takes the selected text in a draft and searches the OMDB API for a film result (requires OMDB API key).
- [OMDB Film Search](https://actions.getdrafts.com/a/24e) &rarr;

## Film GitHub Action

- Takes the Date, IMDBCode, and Rating, and Posts to GitHub to trigger an action to write the film data to a Yaml file. (Requires a GitHub User, Repo and Personal Access Token).
- [Film GitHub Action](https://actions.getdrafts.com/a/24f) &rarr;

## Deduplicate List

- Makes list items unique and appends deleted items in a new list at the bottom of the draft.
- [Deduplicate list](https://actions.getdrafts.com/a/21k) &rarr;

## Sort Lists

- Takes all the lists in a draft and sorts the list items alphabetically within each list.
- [Sort lists](https://actions.getdrafts.com/a/21h) &rarr;

## Timezones

- Takes a 24h time in the UK (23:45) at the start of a draft and appends a list of common time zones across the world.
- [TimeZones](https://actions.getdrafts.com/a/21g) &rarr;

## Line Quotes

- Takes a draft and prepends a `>` at the start of each line.
- [Line Quotes](https://actions.getdrafts.com/a/21f) &rarr;

## Sum Lists

- Takes a list of items and costs, and creates a new line showing the total.
- [Sum Lists](https://actions.getdrafts.com/a/21e) &rarr;

## Quote Post

- Takes a quote post, asks for Front Matter, and saves it into Working Copy.
- [Quote post](https://actions.getdrafts.com/a/21d) &rarr;

## Regular Post

- Takes a regular blog post, asks for Title and date, and saves it to Working Copy.
- [Regular Post](https://actions.getdrafts.com/a/21c) &rarr;

## Front-mattered Post

- Takes a Jekyll formatted post with front matter and copies it to Working Copy.
- [Front-mattered Post](https://actions.getdrafts.com/a/21i) &rarr;

## Header Date

- adds today's date as a h3 heading - perfect for journalling.
- [Header Date](https://actions.getdrafts.com/a/21m) &rarr;

## Get Weather

- using OpenWeather's 2.5 API (your own key required) and a city/location added as credentials to produce a date header and list of metrics for the forecast.
- [Get weather](https://actions.getdrafts.com/a/21n) &rarr;

## Quiche Browser Open Url

- Takes the selected url in a draft, and launches the url in the Quiche Browser (iOS).
- [Quiche Browser Open Url](https://actions.getdrafts.com/a/24k) &rarr;

## AI Prompt Processor

- Uses a template to create a prompt and data, the action then uses the on device model to provide an outcome.
- [AI Prompt Processor](https://actions.getdrafts.com/a/21q) &rarr;

## ISBN Search

- Uses selected text in a draft and searches ISBNsearch.org for a result.
- [ISBN Search](https://actions.getdrafts.com/a/2Rw) &rarr;

## Arc Search Selection

- Takes the selected text in a draft, and launches a search in the Arc Browser.
- [Arc Search Selection](https://actions.getdrafts.com/a/21s) &rarr;

## Duck Duck Go Search Selection

- Takes the selected text in a draft, and launches a search with Duck Duck Go.
- [Duck Duck Go Search Selection](https://actions.getdrafts.com/a/22D) &rarr;

## Bing Search Selection

- Takes the selected text in a draft, and launches a search with Bing.
- [Bing Search Selection](https://actions.getdrafts.com/a/22F) &rarr;

## Google Search Selection without AI

- Takes the selected text searches at google but appends udm=14 to the url to remove the AI overview.
- [Google Search Selection without AI](https://actions.getdrafts.com/a/24h) &rarr;

## Ecosia Search Selection

- Takes the selected text in a draft, and launches a search with Ecosia.
- [Ecosia Search Selection](https://actions.getdrafts.com/a/24j) &rarr;

## Get GitHub User ID

- Takes GitHub username and appends user id number to the draft.
- [Get GitHub user id](https://actions.getdrafts.com/a/25b) &rarr;

## Auto Post Markdown to GitHub

- Takes a draft with first line as the title, and rest as the body and posts the draft to GitHub as a markdown file with front matter in a `posts` directory. Uses GitHub API and Drafts Credential store, with these set on first use (account, repo, token). Requires a GitHub Personal Access Token with contents read/write access.
- [Get Markdown to GitHub](https://actions.getdrafts.com/a/266) &rarr;

## Super Bookmarker to GitHub

- Takes a draft with first line as the title, finds a `link: url` line and the rest as the body and posts the draft to GitHub as a markdown file with front matter in a `_bookmarks` directory/collection of a Jekyll Blog. Uses GitHub API and Drafts Credential store, with these set on first use (account, repo, token). Requires a GitHub Personal Access Token with contents read/write access. Front matter uses microformat `u-bookmark-of` format.
- [Super Bookmarker to GitHub](https://actions.getdrafts.com/a/269) &rarr;
