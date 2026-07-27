---
layout: post
title: How to add a jekyll collection
seo: Ways - how to add a jekyll collection
date: 2026-07-27 13:00
type: ways
syndicate: true
---

Jekyll considers collections as a type, like posts and pages, by adding the collection to the `config.yml` it can operate in the same way as posts, making listing, sorting, and counting easy. To add a collection, you need to update several places, these code examples use the `ride` collection.

First of all we need to register the collection in the `_config.yml` file

```markdown
collections:
rides:
output: true
sort_by: date
permalink: ./rides/:title
```

In order to make the most of a new collection, I add a count of items in my directory template which shows a count of all the types and data objects in the site.

```liquid
{{ site.rides | size }}.
```

I also need to add the collection to the sitemap, so the new pages get picked up by search engines.

```xml
<!-- rides -->
{% assign links = site.rides %}
{% for link in links %}
<url>
<loc>{{ link.url | replace:'/index.html','/' | absolute_url | xml_escape }}</loc>
{% if link.last_modified_at or link.date %}
<lastmod>{{ link.last_modified_at | default: link.date | date_to_xmlschema }}</lastmod>
<changefreq>weekly</changefreq>
<priority>0.8</priority>
{% endif %}
</url>
{% endfor %}
```

I also create an xml file for the RSS Feed, and if appropriate add the collection to the main page so it appears in the 'firehose'

```xml
---
layout: empty
permalink: /rides.xml
---
<?xml version="1.0" encoding="utf-8"?>
{% assign pub_date = site.time | date: "%Y-%m-%dT%H:%M:%SZ" %}
<feed xmlns="http://www.w3.org/2005/Atom" xml:lang="en">
<title>{{ site.owner.name }} - {{ site.title }} Rides only</title>
<subtitle type="html">{{ site.description }}</subtitle>
<link rel="self" type="application/atom+xml" href="{{ site.url }}/rides.xml" />
<link rel="alternate" type="text/html" href="{{ site.url }}" />
<generator>Jekyll</generator>
<rights>{{ site.owner.name }}</rights>
<updated>{{ pub_date }}</updated>
<author>
<name>{{ site.owner.name }}</name>
<email>{{ site.owner.email }}</email>
<uri>{{ site.owner.uri }}/</uri>
</author>
<id>{{ site.url }}/</id>
{% assign posts = site.rides %}
{% for post in posts %}
{% assign build_date = post.date | date: "%Y-%m-%dT%H:%M:%SZ" %}
{% assign updated_date = post.modified | date: "%Y-%m-%dT%H:%M:%SZ" %}
    <entry>
        <title type="html"><![CDATA[{{ post.title | cdata_escape }}]]></title>
        <link rel="alternate" type="text/html" href="{{ site.url }}{{ post.url }}" />
        <id>{{ site.url }}{{ post.id }}</id>
        <published>{{ build_date }}</published>
        <updated>{% if post.modified %}{{ updated_date }}{% else %}{{ build_date }}{% endif %}</updated>
        <author>
        <name>{% if post.cited %}Quoting {{ post.cited }}{% else %}{{ site.owner.name }}{% endif %}</name>
        <uri>{% if post.link %}{{ post.link }}{% else %}{{ site.url }}/{{ post.url }}{% endif %}</uri>
        </author>
        <content type="html"><![CDATA[
        {{ post.content }}
        {% include footer_for_feeds.html %}
        ]]></content>
    </entry>
{% endfor %}
</feed>
```

And the json equivalent feed

```json
"items": [
    {%- assign rides = site.rides -%}
    {%- assign posts = site.posts -%}
    {%- assign posts = posts | concat: rides -%}
    {%- assign posts = posts | sort: "date" | reverse -%}
    {% for post in posts %}
    {
    "id": "{{ post.url | escape }}",
    "url": "{{ site.url | append: post.url | escape }}",
    "title": "{{ post.title | escape }}",
    "content_html": "{{ post.content | strip_html | normalize_whitespace | escape }}
    {% include footer_for_feeds.html %}
    ]]>",
    "date_published": "{{ post.date | date_to_rfc822 }}",
    "author": {
    "name": "{% if post.cited %}Quoting {{ post.cited }}{% else %}{{ site.owner.name }}{% endif %}",
    "uri": "{{ post.link | default: post.url }}"
    }
    }{% unless forloop.last %},{% endunless %}
    {% endfor %}
    ]
```

And finally, to make sure the collection appears in the main page, I add it to the main feed code which makes use of the `concat` filter to merge the two collections together, and then sort them by date.

```liquid
{% assign rides = site.rides %}
{% assign posts = site.posts | where_exp: "post", "post.show != false" %}
{% assign posts = posts | concat: rides %}
{% assign posts = posts | sort: "date" | reverse %}
```

This ensures the content appears where it should.
