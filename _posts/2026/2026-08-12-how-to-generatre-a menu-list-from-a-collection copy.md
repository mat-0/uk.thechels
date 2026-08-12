---
layout: post
title: How to find Broken Front Matter in Jekyll Posts
seo: Ways - How to find Broken Front Matter in Jekyll Posts
date: 2026-08-12 15:00
type: ways
---

Occasionally I discover I have created some blog posts with the incorrect or missing front matter.

This bash script searches through all my `_posts/` including my subfolders (one per year) and writes the path to a file.

I can then go file by file and check for issues, in this code snippet I am looking for missing `layout` keys. This results in the plain text being shown in the browser.

```bash
{% raw %}
for f in _posts/*/*.md; do
  awk 'NR==1{if($0!~/^---/){exit 1}} /^---/{c++} c==2{exit 0} /^layout:/{found=1} END{exit !found}' "$f" \
    || echo "$f"
done > missing.txt
wc -l missing.txt
{% endraw %}
```

Alternatively I could set a default layout in my `_config.yml` file and not worry, but I sometimes in other use cases want to iterate over the front matter locally, so I much prefer fixing at source.
