<p align="center">
  <img src='images/arXie_300.png'/>
</p>

# **arXie Slack Bot** [![Build Status](https://travis-ci.org/thundergolfer/arXie-Bot.svg?branch=master)](https://travis-ci.org/thundergolfer/arXie-Bot) [![Code Climate](https://codeclimate.com/github/thundergolfer/arXie-Bot/badges/gpa.svg)](https://codeclimate.com/github/thundergolfer/arXie-Bot)

### arXiv {pronounced *archive*}, arXie {pronounced... *archie*}


---------------

<p align="center">
  <a href="https://slack.com/oauth/authorize?scope=commands,bot&client_id=31179650306.145700550929">
    <img alt="Add to Slack" height="40" width="139" src="https://platform.slack-edge.com/img/add_to_slack.png" srcset="https://platform.slack-edge.com/img/add_to_slack.png 1x, https://platform.slack-edge.com/img/add_to_slack@2x.png 2x" />
  </a>
</p>

arXie is a Slack bot that browses and filters the arXiv repository for you. You're kept informed on what's happening in Machine Learning and AI with minimal effort.

This production of this bot was motivated by this question in Google Brain's [r/machinelearning AMA](https://www.reddit.com/r/MachineLearning/comments/4w6tsv/ama_we_are_the_google_brain_team_wed_love_to/?st=irvvkvu4&sh=b50d5ce3)

> How do you keep up with the vast amount of work being done on deep learning? Do each of you just focus on one thing or is everyone reading many papers daily? I'm a second year AI master student and I find it overwhelming.

I've taken all feedback from that thread and the [hacker news thread](https://news.ycombinator.com/item?id=12233289) to make the process on ingesting the massive amount of Machine Learning research relatively pain free.

## Set-Up

#### **Disclaimer:**
```
ArXie-Bot uses arxiv-sanity.com as an interface to the ArXiv papers repository.
As arxiv-sanity has a _username_, _password_ login system, Arxie-Bot is required
to either receive some existing login details from you, or ask you
to message it some fresh ones to use.

As you have probably figured, this requires messaging through Slack a password,
which is god-awful security. Though an arxiv-sanity.com account is a pretty low
value target, it is still something that needs to be fixed.

The first step will probably involve moving to a process whereby Arxie-Bot
creates an password for you on the back-end and emails you that password to a
secure email so that you may use the arxiv-sanity.com account outside of Slack.

It will be harder to facilitate the secure  passing of an existing password to
the bot, but that is a desired feature.
```

`Coming soon once I've implemented what's necessary for the "Add to Slack" button process`

## How To Basics

The following commands are available to you:

#### 1. Get Library

The "Library" is those papers that are stored for your account at *arxiv-sanity.com*, and a summary will be presented by saying things like this:

`@arxie-bot Get my library`, `@arxie-bot get library`, `@arxie-bot Fetch my library`, `@arxie-bot Get my papers library`

#### 2. Get Paper

Get a paper's summary:

`@arxie-bot Show <paper title>`

#### 3. Get Recommended

Given papers you've saved, pull a few recent papers *arxiv-sanity.com* thinks you'd like.

`@arxie-bot Get recommended papers`, `@arxie-bot I want my recommended papers`, `@arxie-bot recommended`

#### 4. Clear Library

The "Library" is those papers that are stored for you at *arxiv-sanity.com*, and they all be deleted by saying things like this:

`@arxie-bot delete library`, `@arxie-bot delete all in library`, `@arxie-bot wipe library`, `@arxie-bot clear library`

#### 5. Search

Supply a query and search against the papers in *arxiv-sanity.com*.

`@arxie-bot search for <search query>`, `@arxie-bot search <query>`

## Development

#### Installation

You can use `virtualenv arxie-env` to create a virtual environment called "arxie-env". Running `pip install -r requirements.txt`.

You will require an [*API AI*](https://api.ai/) token and a *Slack API Token* for the ArXie-Bot, which is accessible once the bot has been adding to your team ([details here for Slack](https://api.slack.com/bot-users)). Add these tokens as environment variables and the ArXie bot will pick them up.

#### Running Locally

The following environment variables must be populated:

```
APIAI_TOKEN=<GET FROM https://api.ai/>
SLACK_TOKEN=<GET A 'Bot user OAuth access token'>

ARXIE_DB_TOKEN=<ANY HIGH-ENTROPY STRING>
ENV="DEV"
```

Run `python -m bot.app`

#### Deployment and Running in 'Prod'

Arxie-bot can be deployed to the Google Cloud by following and adapting [*Build a Slack Bot with Node.js on Kubernetes*](https://codelabs.developers.google.com/codelabs/cloud-slack-bot/index.html?index=..%2F..%2Findex#4). The [`kubernetes/`](/kubernetes) folder has the config and more info.

The following environment variables must be populated:

```
APIAI_TOKEN=<GET FROM https://api.ai/>
SLACK_TOKEN=<GET A 'Bot user OAuth access token'>

ARXIE_DB_TOKEN=<ANY HIGH-ENTROPY STRING>
DEV="PROD"
PROJECT_ID=<YOUR GCLOUD PROJECT ID>
```

When in production, Arxie-bot uses [*Google Datastore*](https://cloud.google.com/datastore/) to store `arxiv-sanity.com` account details for Slack users.

### License
This project is under the [MIT License](https://opensource.org/licenses/MIT).

------
### Made With

![Imgur](http://i.imgur.com/Fd6Kk9T.png) ![Imgur](http://i.imgur.com/rikiMi0.jpg) ![Imgur](http://i.imgur.com/BwhBHyx.jpg) ![Imgur](http://i.imgur.com/k289uw5.jpg)
