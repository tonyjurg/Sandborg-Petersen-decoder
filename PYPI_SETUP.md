# PyPI package setup

The installable package is developed on the `pypi-setup` branch. Do not create a
release tag from this branch. Merge it into `main` only after its API, metadata,
documentation, and licence are ready for the first public package release.

## Package identity

- Distribution: `sandborg-petersen-decoder`
- Import package: `sp_morph_decoder`
- Command: `sp-morph-decode`
- Version source: annotated Git tags through `hatch-vcs`
- Supported Python versions: 3.9 and newer

The proposed distribution name returned as unregistered on PyPI when this setup
was created. PyPI names are global, so confirm availability again when configuring
the pending publisher.

## One-time Trusted Publisher registration

PyPI Trusted Publishing uses short-lived GitHub Actions credentials and requires
no stored PyPI API token.

Before the first release, sign in to PyPI and register a pending GitHub publisher
at <https://pypi.org/manage/account/publishing/> with:

- PyPI project name: `sandborg-petersen-decoder`
- GitHub owner: `tonyjurg`
- GitHub repository: `Sandborg-Petersen-decoder`
- Workflow filename: `publish-version.yml`
- GitHub environment: `pypi`

Create or review the `pypi` environment in the GitHub repository settings. A
required maintainer approval is recommended for the publishing job; omit that
rule only if completely unattended publication is preferred.

## Publication pipeline

A pushed `vMAJOR.MINOR` or `vMAJOR.MINOR.PATCH` tag runs the
`.github/workflows/publish-version.yml` workflow. It tests the repository, builds
the wheel and source distribution, verifies their metadata and version, publishes
them to PyPI with an OIDC Trusted Publisher, and then creates the GitHub Release.

The PyPI action creates digital publish attestations by default. The repository
does not need a `PYPI_API_TOKEN` secret.

If the repository is enabled in the Zenodo GitHub integration, the resulting
GitHub Release is ingested automatically. Zenodo enablement remains a one-time
external repository setting and should be verified before the release tag is
pushed.

## Pre-release decisions

The repository currently declares CC BY 4.0 for software and data. Creative
Commons recommends a software-specific licence for code. Confirm whether the
code should remain CC BY 4.0 or be offered under a software licence before the
first PyPI release; changing or dual-licensing requires the agreement of the
relevant rights holder.
