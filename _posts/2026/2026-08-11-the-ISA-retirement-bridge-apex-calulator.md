---
layout: post
date: 2026-08-11 21:00
type: blog
title: "The Road to FIRE - Building the ISA Bridge Apex Calculator"
tags: [finance]
seo: "A free tool to find your own ISA bridge apex - the point your ISA can bridge you from early retirement to pension access."
permalink: "/fire-isa-bridge-apex-calculator"
syndicate:
  - mastodon
  - bluesky
  - textlog
---

I recently wrote about [the ISA bridge and the idea of an "apex"](/the-ISA-retirement-bridge) - the point where an ISA has grown large enough to carry you from the day you stop work to the day a pension becomes accessible. That post worked through my own numbers: £147k in the ISA, £20k a year going in, a £36k/year target, and a handful of tables showing what the apex looks like at different ages and growth rates.

Tables are fine for one scenario. They fall apart the moment someone wants to plug in their own numbers. So I've built a small calculator that does the same maths, for anyone's figures. It uses client side calculations so no data leaves your browser/device.

You can try it now at [the ISA Bridge Calculator](https://tools.thechels.uk/the-ISA-retirement-apex-bridge-tool) - sitting on my toolkit subdomain.

## You give it 4 things

- Your current age and ISA balance
- What you're contributing each year
- What you'd want to withdraw each year during the bridge (in today's money)
- The age the bridge needs to reach - 58 for private pension access, 68 for the State Pension, or another age.

Then you pick a real growth rate - 2% to 8% - with a note on what "real" means (market return minus inflation and fees, so 8% market growth at 3% inflation/fees nets out to roughly 5% real). It defaults to 5%. Most investment products tend to be conservative as it's always better to over deliver.

### I know my target FIRE age

Give it the age you're aiming for, and it tells you the required apex, your projected ISA at that age, and the surplus or shortfall between the two. If there's a shortfall, it also works out roughly what your annual contribution would need to rise to in order to hit that age,warning if you go above the annual ISA allowance of £20k you might need to look at changing your plans, or using a GIA (and the associated taxes come into play).

### Solve for my earliest FIRE age

Don't specify an age at all, and it searches for the earliest one where your projected ISA actually covers the required bridge.

The chart shows your selected growth rate plus one point either side of it (so 5% comes with 4% and 6% for context), with the apex marked on each line. In solve mode, each rate line solves independently - a higher growth rate can genuinely bring the apex forward, though sometimes a 1% difference isn't enough to shift the whole year answer, even though the underlying numbers have moved. Where that happens the summary spells out the fractional difference (e.g. 49 years 5 months vs 49 years 11 months) rather than letting two different growth rates look identical.

## Assumptions

To keep this usable rather than another spreadsheet, the calculator doesn't touch pensions; neither DC, DB, or state pensions. This is purposely a bridge until pensions become available. If you have a surplus at this point good for you and you can buy me a [Ko-fi](https://ko-fi.com/thechelsuk).

We've ignored emergency funds and the good practices needed before investing we assume you have these in place, and that they won't impact your retirement.

We've assumed a consistent 5% growth rate, or whatever percentage you chose, [growth is, in reality, inconsistent and volatile](/cash-is-risky-stocks-are-volatile), some years the markets are up 25%, or down 10%, you may get back less than you invest, value can go up as a well as down, capital at risk. You are responsible for your own investment choices etc. etc. So actual figures will vary, seek financial advice from a regulated professional.
