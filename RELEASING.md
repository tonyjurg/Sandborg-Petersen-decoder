# Publishing a version

Version publication is automated from Git tags. A tag matching `vMAJOR.MINOR`
or `vMAJOR.MINOR.PATCH` runs the Python and browser test suites, validates the
release metadata, and publishes a GitHub Release with generated notes. GitHub
also provides source ZIP and TAR archives for the tagged revision.

## Release procedure

1. Update `version` and `date-released` in `CITATION.cff`, then merge that change
   into `main`.
2. Verify the intended tag locally:

   ```shell
   python scripts/validate_release.py --tag v1.2
   pnpm test
   ```

3. Create and push an annotated tag from the updated `main` branch:

   ```shell
   git switch main
   git pull --ff-only
   git tag -a v1.2 -m "Release v1.2"
   git push origin v1.2
   ```

The `Publish version` workflow publishes the release only after all checks pass.
If this repository is enabled in the Zenodo GitHub integration, Zenodo will then
ingest the GitHub Release and create the corresponding archived software version.
After publication, verify the new Zenodo record and DOI metadata.
