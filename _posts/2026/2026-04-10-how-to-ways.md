---
layout: post
title: How to use ways
seo: Ways - A guide to using ways
date: 2026-04-10
type: ways
pinned: true

---

Ways are a slash pages format for documenting processes, workflows, and procedures. They are designed to be easy to read and follow, on how to do things. They happen to include a link to the official manual or service where possible, but there should be enough detail to follow steps without needing to click through.

1. Create a new markdown file in the `_posts/[year]` directory. The filename should be descriptive of the process you are documenting, for example `yyyy-mm-dd-how-to-use-ways.md`.
2. Start the file with the following front matter:

   ```markdown
   ---
   layout: post
   title: How to use ways
   seo: Ways - A guide to using ways
   type: ways
   permalink: /how-to-use-ways/
   date: 2026-04-10
   pinned: true/false
   syndicate:
     - (target)
   ---
   ```

3. Customize the front matter with the appropriate title, SEO description, type, permalink, and date for your specific way.
4. Use pinned as true if you want the way to be featured at the top of the ways archive page, otherwise set it to false or omit it.
5. Add the class field with a value of indie if the post is suitable for the indieNews site. This is handled in the post layout using webmentions. We don't want to spam them with every post.
6. After the front matter, you can start writing your content. Use lists as how-to guides are often a series of steps to follow. Bullets or numbered lists can help break down the information into manageable parts.
7. Save the file and commit it to your repository. The new way will be available at the specified permalink, in this case `/how-to-use-ways/`.

_I've refrained from using screenshots of apps or tools in ways as apps and designs can change frequently, whereas functionality, hopefully, persists._

I had originally updated the Jekyll config to include `_ways` as a collection, so one could use the site data variables to access all the ways in the templates, layouts, and metadata-like front matter so counting items was easy as `site.ways | size`. However, I have since changed this to be a type of post with the relevant front matter. I'm then able to include/exclude ways from loop pages or rss feeds as needed. See each feed xml file code for more details. This just makes it easier as all post content is in the same folder and upstream tools like Drafts Actions are easy to work with.
