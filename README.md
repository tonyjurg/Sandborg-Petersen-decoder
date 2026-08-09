[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active)  [![Online Tool](https://img.shields.io/badge/online%20tool-%F0%9F%95%B9-blueviolet)](https://tonyjurg.github.io/Sandborg-Petersen-decoder/)  [![DOI](images/zenodo.14551056.svg)](https://doi.org/10.5281/zenodo.14551056) [![SWH](https://archive.softwareheritage.org/badge/origin/https://doi.org/10.5281/zenodo.14551056/)](https://archive.softwareheritage.org/browse/origin/?origin_url=https://doi.org/10.5281/zenodo.14551056) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/tonyjurg/Sandborg-Petersen-decoder)


<img src="images/logo.png" width=200>

# Sandborg-Petersen Morphology Decoder

This lightweight decoder implements the Sandborg-Petersen morphology schema for Koine Greek — especially New Testament and related texts — in a simple, browser-based tool.

You can try it online at [https://tonyjurg.github.io/Sandborg-Petersen-decoder/](https://tonyjurg.github.io/Sandborg-Petersen-decoder/). 
The online version allows also allows for prefilling the decoder with a specific tag by appending `?tag=<TAG>` (for example, <a href="https://tonyjurg.github.io/Sandborg-Petersen-decoder/?tag=N-NSF" target="_blank">`?tag=N-NSF`</a>).

# Decoder formats

Two functionaly equivalent coding implementations are stored on this repository:

   - [HTML with javascript based decoder](https://github.com/tonyjurg/Sandborg-Petersen-decoder/blob/main/javascript/SP-Morph-decode.html)
   - [Installable Python package](src/sp_morph_decoder) with a
     [compatibility script](python/SP-Morph-decode.py)

# Python package

After release 1.2 is published, install it from PyPI with:

```shell
python -m pip install sandborg-petersen-decoder
```

For development, install the current source checkout with:

```shell
python -m pip install .
```

Permissive mode is the default. It returns all fields that can be recovered and
includes an `Errors` list when validation finds a problem:

```python
from sp_morph_decoder import decode_tag

result = decode_tag("N-XYZ")
print(result["Errors"])
```

Strict mode raises `MorphologyDecodeError`. The exception retains the partial
result and the individual validation messages:

```python
from sp_morph_decoder import MorphologyDecodeError, decode_tag

try:
    result = decode_tag("N-XYZ", mode="strict")
except MorphologyDecodeError as error:
    print(error.errors)
    print(error.result)
```

The package also provides a command-line interface:

```shell
sp-morph-decode V-PAI-3S --mode strict
python -m sp_morph_decoder V-PAI-3S
```

See the [Python package guide](https://tonyjurg.github.io/Sandborg-Petersen-decoder/python-package.html)
for installation, API, strict-mode, typing, and command-line documentation.

# Definitional document
 
A descriptive document with parsing information is available via [github.com/biblicalhumanities](https://github.com/biblicalhumanities/Nestle1904/blob/master/morph/parsing.txt).

# Integrating in HTML page

## Using a JavScript generated button

Because the decoder requires JavaScript to function, it is reasonable to embed a link to it directly in any HTML page using a method depending on JavaScript as well. This approach also lets you open it in a new, resizable window of a specified size.

The first step is to add a script anywhere inside your &lt;HEAD&gt; section, or at the top of your &lt;BODY&gt; section:

``` html
 <SCRIPT>
    function openMinimalWindow() {
      window.open(
        'https://tonyjurg.github.io/Sandborg-Petersen-decoder/',
        '_blank',
        'toolbar=no,location=no,status=no,menubar=no,scrollbars=yes,resizable=yes,width=800,height=600'
      );
    }
  </SCRIPT>

```
 In the &lt;BODY&gt; section include the following:
 
 ``` html

 <BUTTON onclick="openMinimalWindow()">Open Morph decoder</button>
 
 ```

This will put a button on your page similair to the image below:

<img src='images/button.jpg'>

If JavaScript is enabled, clicking this button will launch the decoder in a new 800×600 px window without toolbars or menus.

## Adding a direct link

If you prefer a simple hyperlink that opens in a full browser tab, just use:

```html
  <A HREF="https://tonyjurg.github.io/Sandborg-Petersen-decoder/" TARGET="_blank">Open Morph decoder</A>
```

## Open decoder for a specific tags

You can also open the decoder pre-filled for a specific tag by appending a `tag` query parameter to its URL. In our HTML/JavaScript implementation, a small script reads the URL’s `tag` parameter and uses it to initialize the decoder, which is especially handy if you’ve already run your analysis in Python.

```Python
import pandas as pd
from IPython.display import HTML

base_url = "https://tonyjurg.github.io/Sandborg-Petersen-decoder/?tag="

# Simple example data
results = [
    ("Βίβλος", "N-NSF"),
    ("λόγος",  "N-NSM"),
]

# Build dataframe
df = pd.DataFrame(results, columns=["Word", "Tag"])
# Embed clickable HTML links in the 'Tag' column
df["Tag"] = df["Tag"].apply(lambda tag: f'<a href="{base_url}{tag}" target="decoder">{tag}</a>')

# Display as an HTML table with clickable links
HTML(df.to_html(escape=False, index=False))
```

This will produce the following table:

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>Word</th>
      <th>Tag</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Βίβλος</td>
      <td><a href="https://tonyjurg.github.io/Sandborg-Petersen-decoder/?tag=N-NSF" target="decoder">N-NSF</a></td>
    </tr>
    <tr>
      <td>λόγος</td>
      <td><a href="https://tonyjurg.github.io/Sandborg-Petersen-decoder/?tag=N-NSM" target="decoder">N-NSM</a></td>
    </tr>
  </tbody>
</table>


Note the use of `target="decoder"` would normally reuse a single named window. However, in a sanitized environment like Jupyter Notebook, each click opens a new window because Jupyter’s security model isolates browsing contexts. In contrast, when you save the same HTML locally (or serve it as a regular web page), clicks targeting the same window name correctly reuse that single window.

See the following small [Jupyter Notebook](create_clickable_links.ipynb) to see the code in action.

# Tag validation agains the MACULA GNT dataset

 - See notebook: [Check SP-Morphs in MACULA XML dataset against documentated tags](testing/SP-Morphs-used-in-MACULA.ipynb).

# License

The original software and associated documentation are licensed under the
[MIT License](LICENSE). MACULA-derived validation data in `testing/output/` and
data embedded in the validation notebook remain available under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) with the required
MACULA attribution. See [NOTICE.md](NOTICE.md) for the exact scope, attribution,
and historical-release information.

# Responsible disclosure

AI-assisted tools have been used in a limited capacity to audit this repository, identify possible defects, suggest improvements to the original code, and help
develop automated tests. All resulting changes are reviewed and tested by the repository maintainer before inclusion. 
Scholarly interpretation, design decisions, and final responsibility for the code remain with the human author.

# Version publication

Tagged versions are tested and prepared for automatic publication to PyPI and as
GitHub Releases. See [RELEASING.md](RELEASING.md) for the maintainer procedure,
PyPI Trusted Publishing setup, and Zenodo notes.

# Acknowledgements

- ['Parsing Information for Robinson-like parsing tags Adapted from Ulrik Sandborg-Petersen's Description for Tischendorf 8th'](https://github.com/biblicalhumanities/Nestle1904/blob/master/morph/parsing.txt).

