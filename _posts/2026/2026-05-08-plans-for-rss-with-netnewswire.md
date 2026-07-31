---
layout: post
syndicate: true
date: 2026-05-08 22:10
title: Plans for RSS with NetNewsWire
type: blog
---

The recent update to NNW has resulted in a huge sense of speed and performance improvements for me. The app loads quickly and syncing of new content seems super fast (assume 1500 feeds).

I've been developing my own themes, in which I have used some JavaScript to rewrite some URLs to make YouTube links open in my favourite video player and I have more plans like this. I recently extracted my mastodon and Bluesky follows and converted these to RSS feeds and an OPML file. I then imported this into NNW in a 'socials' folder. I then spent some time deduplicating.

The only issue with using an RSS reader for these sorts of feeds is the link goes to the social site rather than say the source if the post contains a link - so yhis could be a two hop to get there. In fact the links in the 'body' are not rendered as links at all when it comes from bluesky.

My plan, therefore, is to use more JS to extract links from social feed items and putpose all items, and append them all as a bullet list as clickable links in the footer of the item.
