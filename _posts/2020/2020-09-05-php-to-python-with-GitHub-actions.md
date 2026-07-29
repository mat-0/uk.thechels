---
layout: post
title: From PHP to Python and GitHub Actions
date: 2020-09-05 17:00

type: blog
---

Some time ago for a bit of fun I had created Horo Football - a twitter account that auto-tweeted (via a php script and cron job) some randomly generated horoscopes from a football context.

Having dabbled with a bit of python recently, I decided to rewrite this in python.

```php
<?php

$string = str_replace( '#zodiac#', $go->getValueFromKey( $zodiac ) , $string );
$randHouses  = $go->getValuesFromArray( $house  , 2);

public function getValueFromKey(&$array) {
 $rand_key = array_rand($array);
return array_pop($array);
}
public function getValuesFromArray($array, $n) {
 return array_rand(array_flip($array), $n);
}

?>
```

becomes

```python
for sign in signs :
 dic = {
    "#zodiac#"  : sign,
    "#adjOrb#"  : random.choice(adjOrbs),
    "#suffix#"  : random.choice(suffixes),
    "#gerund#"  : random.choice(gerunds),
    "#house#"   : random.choice(houses),
    "#house2#"  : random.choice(houses),
    "#planet#"  : random.choice(planets),
    "#planet2#" : random.choice(planets)
}
 output_string = multiple_replace(dic, random.choice(phrasing))
```

I am amazed at how concise python is, having switched from a 200 line php file with a few methods coded in different classes so around 250 all in, to around 180 in python, but with processing (excluding the arrays of data) to around 25 lines.

The outputs were published via a GitHub action to a README.md file in the repository.

```yaml
name: Daily Build
# build
on:
  workflow_dispatch:
  schedule:
    - cron: "30 7 * * *"

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Check out repo
        uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.8
      - uses: actions/cache@v2
        name: Configure pip caching
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-
      - name: Install Python dependencies
        run: |
          python -m pip install -r requirements.txt
      - name: Update README
        run: |-
          python 'python/build.py'
          cat README.md
      - name: Commit and push if README changed
        run: |-
          git diff
          git config --global user.email "readme-bot@example.com"
          git config --global user.name "README-bot"
          git diff --quiet || (git add README.md && git commit -m "Updated README")
          git push
```

As you can see from the action it is essentially a set of key-value pairs in yaml. Installing Python and any dependencies in a serverless environment - managed by GitHub, the Python script updates the `README` file and this action commits it.

`workflow_dispatch` means it can be run manually, `schedule` takes a cron expression. It can also be triggered on a `push` or `pull request`.

GitHub actions are stored in your repository in a `.github/workflows` folder and thats it.
