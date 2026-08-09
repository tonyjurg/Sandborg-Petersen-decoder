# Publishing a version

Version publication is automated from Git tags. A tag matching `vMAJOR.MINOR`
or `vMAJOR.MINOR.PATCH` runs the Python and browser test suites, validates the
release metadata, builds and verifies the Python wheel and source distribution,
publishes them to PyPI, and publishes a GitHub Release with generated notes.
GitHub also provides source ZIP and TAR archives for the tagged revision.

The Python package version is derived from the Git tag by `hatch-vcs`; there is
no separate package version string to update.

## Release procedure

1. Update `version` and `date-released` in `CITATION.cff`, retain `license: MIT`,
   then merge that change into `main`.
2. Verify the intended tag locally:

   ```shell
   python scripts/validate_release.py --tag v1.2
   python -m build
   python -m twine check dist/*
   pnpm test
   ```

3. Create and push an annotated tag from the updated `main` branch:

   ```shell
   git switch main
   git pull --ff-only
   git tag -a v1.2 -m "Release v1.2"
   git push origin v1.2
   ```

The `Publish version` workflow performs these steps in order:

1. Run the complete test workflow.
2. Build and verify the PyPI distributions against the tag.
3. Publish the package through PyPI Trusted Publishing.
4. Create the GitHub Release with generated notes.
5. Let the enabled Zenodo GitHub integration ingest that release.

The GitHub Release is deliberately created only after PyPI succeeds. After
publication, verify both the PyPI project and the new Zenodo record and DOI
metadata. The software record should identify MIT as the package license; the
repository `NOTICE.md` separately preserves the CC BY 4.0 terms and attribution
for MACULA-derived validation data.
