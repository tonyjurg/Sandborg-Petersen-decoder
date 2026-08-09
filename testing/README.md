# MACULA SP morph tag verification

Verification of the decode-ability of SP Morph tagging as found in the [MACULA XML source data](https://github.com/Clear-Bible/macula-greek/tree/main/Nestle1904/lowfat) on which we based our [N1904 Text-Fabric](https://centerblc.github.io/N1904/) dataset. The basic idea is to check if there are tags that can not be decoced.

## Automated tests

Run the Python decoder tests with:

```shell
python -B -m unittest testing/test_python_decoder.py
```

Browser behavior for both HTML decoders is tested with Playwright and Chromium.
After installing pnpm, install the project dependencies and browser once:

```shell
pnpm install
pnpm exec playwright install chromium
```

Then run the browser tests with:

```shell
pnpm run test:browser
```

Use `pnpm test` to run both the Python and browser suites. GitHub Actions runs
both suites automatically for pushes and pull requests targeting `main`.
