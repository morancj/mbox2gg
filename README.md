# mbox2gg.py

Push mails from a local mbox file to Google Groups. Skips mails over 25MiB in size (this is a Google Groups limitation).

Can be used to migrate mails from a Google Workspace user to a group: to do so, use Google Takeout as the user to export mail to an mbox file, then run this script.

## Original authors

[pecigonzalo](https://gist.github.com/pecigonzalo/c147e3f174fca90bec66efbd9eb24ad3) from [jacksonj04](https://gist.github.com/jacksonj04/60c1da79da8c86feea1b).

## Prerequisites

- `pyenv`
- `pipenv`
- A new GCP project with Groups Migration API enabled and the necessary secrets: see [mail2gg](https://pypi.org/project/mail2gg/0.1.5/) for more.

## Notes

When prompted for OAuth2, you **must** authenticate be an admin (I've tried with fewer privs!)

## Changes

```shell
wget -O mbox2gg.py https://gist.githubusercontent.com/pecigonzalo/c147e3f174fca90bec66efbd9eb24ad3/raw/c3c1cf31b733822ad2b1ef5220e08319ea61d2f9/mbox2gg.py

2to3 --write mbox2gg.py
```

Modified to skip mails over 25MiB following [this comment](https://gist.github.com/pecigonzalo/c147e3f174fca90bec66efbd9eb24ad3#gistcomment-3313515).

## Usage

Install dependencies with: `pipenv install --python 3.8.2`

Run with: `python mbox2gg.py`
