---
layout: projects
title: "Create mta-sts.txt and subdomain on GitHub Pages - Template Repo"
permalink: /projects/create-mta-sts-txt-subdomain-on-github-pages-template
seo: "Create mta-sts.txt and subdomain on GitHub Pages with this easy to use Repo Template"
class: scripts
i_name: View
i_url: "https://github.com/thechelsuk/template-mta-sts-sub-domain"
summary: "A Repo template for creating an mta-sts.txt record and subdomain hosted on GitHub Pages using their branch deployment."
type: wrench
---

A GitHub template repository setup to quickly deploy an `mta-sts.txt` file into a `.well-known/mta-sts.txt` path on a `mta-sts.domain.tld` subdomain.

- Simply copy the template repo.
- Change the CNAME.txt file contents to mta-sts.yourdomain.tld
- Rename CNAME.txt to just CNAME1
- Change the .well-known/mta-sts.txt file to match your email MX records and version2
- Set up the DNS records to point to GitHub's IP ranges.
  - 185.199.108.153
  - 185.199.109.153
  - 185.199.110.153
  - 185.199.111.153
- Publish to GitHub Pages - using the deploy from branch fine, no actions needed.

Default mta-sts config is for Apple's MX records - change these to your provider.
