# Contributing to Pyventory

## How to…
* [Propose a Feature](#propose-a-feature)
* [File a Bug](#file-a-bug)
* [Change the Code](#change-the-code)
* [Change the Docs](#change-the-docs)
* [Get Support](#get-support)

## Propose a Feature

* Open an issue here: https://github.com/lig/pyventory/issues/new.
* Describe a feature you are proposing in a free form.
* Provide one or more real-life use cases.
* If there are other tools that already has the feature describe the way it works there.

## File a Bug

* Open an issue here: https://github.com/lig/pyventory/issues/new.
* Provide the output of `ansible --version`.
* Provide the Pyventory version you have. It could be usually obtained with something like `pip show pyventory`.
* Provide the part of your inventory causing problems. Feel free to reduce it to a minimum required to reproduce the issue.
* Describe steps needed to reproduce the issue.
* Provide the output having error messages if applicable.

## Change the Code

> Note: the main integration branch in Pyventory repo is `main`.

* You need [`poetry`](https://python-poetry.org/docs/#installation) and [`pre-commit`](https://pre-commit.com/#install) to be installed in your local environment. 
* Fork the project on GiHub: https://github.com/lig/pyventory/fork.
* Clone the project locally.
* In the root dir of the local copy run:
  - `poetry install`
  - `pre-commit install`
* Create a new branch (in case you'll need to make another change before this one is merged upstream).
* Make changes to the code.
* Ensure tests are passing (it's a good idea to add some): `poetry run pytest tests/`.
* Push you changes.
* Open a PR.
* Be ready to address maintaners' comments after they review you code.
* Respect the [Code of Conduct](CODE_OF_CONDUCT.md).

## Change the Docs

Follow the steps in [Change the Code](#change-the-docs) except you won't need to run the tests.

## Get Support

Whilst it's possible to use GitHub issues to ask a question the best way to get the support for Pyventory is to use the [`pyventory` tag on Stack Overflow](https://stackoverflow.com/questions/tagged/pyventory).
