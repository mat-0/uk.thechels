---
layout: post
title: "Building Cheltenham Open Data - why tools beat blog posts"
date: 2026-08-19 23:00
type: blog
seo: "Cheltenham Open Data: local fuel price comparison, open data tools, and classifieds for Cheltenham — built without big tech clutter."
syndicate:
    - mastodon
    - bluesky
---

[Cheltenham Open Data](https://cheltenham-od.uk/) is now on Version 2.0 -- a design refresh on the front end, and a fair bit of unglamorous work behind the scenes to improve scalability as the site grows.

## Why I started with tools, not articles

One of the earliest lessons from running websites, including the first iteration of this site covering football statistics to 5 million page views and 180,000 twitter followers - the glory days - is that news articles or blog posts alone aren't enough to build something people come back to. There are millions of blogs out there, all chasing Google and now the AI crawlers, fighting over the same long-tail keywords and tiny niches for scraps of traffic.

If you're building a local website, people need a reason to return. That means building with data and keeping it genuinely current rather than publishing another opinion piece that goes stale in a week.

## The first tool: fuel prices

The first real test of this idea was fuel prices.

I'd seen that the UK Government had opened a beta fuel price API. I signed up, started poking at the data, and quickly realised there was something useful here. Plenty of sites now do fuel comparisons but most are bloated, ad-heavy, or nationwide and generic.

My version pulls in [over 100 of the nearest petrol stations to Cheltenham](https://cheltenham-od.uk/cheltenham-fuel-prices) and presents the data in a sortable, no-nonsense table and the headlines prices for the cheapest fuel prices by type.

- A Python script connects to the Government's fuel price API on a schedule.
- Data is pulled and cached locally rather than queried live on every page load.
- Prices are filtered to stations around Cheltenham and ranked by fuel type and cost as well as the date they last submitted their prices (cheap but stale data is no good once you get there and it's expensive not is it not cost effective, it erodes trust).

Wars and thus spiking fuel prices were dominating the news, so there was real appetite for a tool that answered "who's cheapest, right now, near me" without wading through ads.

## Community feedback shaped the roadmap

I shared the [fuel prices page](https://cheltenham-od.uk/cheltenham-fuel-prices) on a local Cheltenham subreddit. The response was immediate  and useful and some quick changes were implemented immediately.

## Where the project has gone since

Since the fuel tool, I've expanded into other open data sources such has ONS House prices and tools relevant to people actually living in Cheltenham:

- More open data integrations beyond fuel -- [see the full list of tools](https://cheltenham-od.uk/)
- Local classifieds and adverts - built deliberately without the tracking-heavy data-harvesting, "you are the product" model that dominates big tech site marketplaces and seem full of AI scams. I only use a small analytics tracker for page views and to spot errors.
- I plan to add many more too

## The philosophy has always been local stuff for local people

The bottom line throughout all of it has been my annoyance and disdain for intrusive ads, the dark patterns to keep you scrolling. I just want useful, current, local data that is presented plainly, updated properly, and free to use from someone who lives in the community for the community.

If you're in or around Cheltenham, the fuel price comparison is still the best entry point: [cheltenham-od.uk/cheltenham-fuel-prices](https://cheltenham-od.uk/cheltenham-fuel-prices), can I tempt you to get an EV with Octopus Energy? [install a charger and get a £25 visa gift card](https://tech.referrals.octopus.energy/ulLGI6SC).
