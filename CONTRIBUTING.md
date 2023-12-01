All contributions, bug reports, bug fixes, documentation improvements, enhancements, and ideas are welcome.

If you are simply looking to start working with the codebase, navigate to the GitHub "issues" tab and start looking through interesting issues. There are a number of issues listed under Docs and good first issue where you could start out.

Feel free to ask questions on the mailing list or on Slack.

As contributors and maintainers to this project, you are expected to abide by TransitionZero's code of conduct. More information can be found at: Contributor Code of Conduct

## Installing dev dependencies

```console
git clone https://github.com/transition-zero/feo-client.git
cd feo-client
pip install ".[dev]"
```

To install pre-commit hooks (recommended), run

```console
pre-commit install
```

Please also run mypy with

```console
pip install ".[dev]" && mypy -p feo.client
```

## Authentication

Running our test suite first requires authentication

```console
feo auth login
```

## Running tests

```console
pytest
```

After having made changes in the codebase, run `pip install ".[dev]"` to pick them up in the tests.
