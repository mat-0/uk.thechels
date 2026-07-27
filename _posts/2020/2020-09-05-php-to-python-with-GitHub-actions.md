---
layout: post
title: From PHP to Python and GitHub Actions
date: 2020-09-05 17:00

type: blog
---

Some time ago for a bit of fun I had created Horo Football - a twitter account that auto-tweeted (via a php script and cron job) some randomly generated horoscopes from a football context.

Having dabbled with a bit of python recently, I decided to rewrite this in python.

<script src="https://gist.github.com/thechelsuk/891bc8cff9235edb3479776eb706fa38.js"></script>

becomes

<script src="https://gist.github.com/thechelsuk/01a0143f6f61c52b5523647205e44ebd.js"></script>

I am amazed at how concise python is, having switched from a 200 line php file with a few methods coded in different classes so around 250 all in, to around 180 in python, but with processing (excluding the arrays of data) to around 25 lines.

The outputs were published via a GitHub action to a README.md file in the repository.

<script src="https://gist.github.com/thechelsuk/314fc390936e862bc4c264e1e1cc57d0.js"></script>

As you can see from the action it is essentially a set of key-value pairs in yaml. Installing Python and any dependencies in a serverless environment - managed by GitHub, the Python script updates the `README` file and this action commits it.

`workflow_dispatch` means it can be run manually, `schedule` takes a cron expression. It can also be triggered on a `push` or `pull request`.

GitHub actions are stored in your repository in a `.github/workflows` folder and thats it.
