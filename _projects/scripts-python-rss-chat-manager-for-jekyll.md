---
layout: projects
title: rss.chat reply manager for Jekyll - Python Script
permalink: /projects/scripts-python-rss-chat-manager-for-jekyll
seo: "rss.chat reply manager for Jekyll - Python Script"
class: scripts
i_name: View
i_url: "https://github.com/thechelsuk/rss-chat-reply-manager-for-jekyll/"
summary: "A Python script to manage rss.chat replies for Jekyll sites."
type: wrench
---

A python script that allows you to manage rss.chat replies for Jekyll sites. The script pulls in the RSS feed of the user and matches replies to the url slug of the jekyll post. It then creates a yaml file in the `_data/replies` directory with each reply as a separate entry in the file. This exposes the replies to the Jekyll site and templating using the `site.data.replies` variable.

The project is open source and available on GitHub under an MIT licence.
