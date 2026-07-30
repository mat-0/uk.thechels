---
layout: post
title: How to Generate a Menu From a Jekyll Collection
seo: Ways - how to create make generate a menu from a jekyll collection
date: 2026-07-29 18:00
type: ways
syndicate: false
---

Creating a menu as a list in Jekyll from a collection is as easy as defining the item `title` and `url` as yaml in either the `config.yml` or in an object in the `_data` folder

```yaml
navigation_header:
  - url: "/about"
    title: "About"
    label: "Visit About page"
```

In this example I am using the navigation_header in the config.yml and it's then simply a case of iterating over the list with a for loop. Each menu item is assigned to the `item` object and they have values for the `title` and `url` as per the yaml, they could also include more data such as a label, an icon, class, or follow/nofollow attributes.

```html
{% raw %}
<ul class="list  list--nav">
  {% for item in site.navigation_header %} {% if item.url contains '://' %} {%
  assign url = item.url %} {% else %} {% assign url = item.url | relative_url %}
  {% endif %}

  <li
    class="item  item--nav{% if item.url == page.url %}  item--current{% endif %}"
  >
    <a href="{{ url }}">{{ item.title }}</a>
  </li>
  {% endfor %}
</ul>
{% endraw %}
```
