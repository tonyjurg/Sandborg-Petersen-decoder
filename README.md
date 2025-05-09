[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14551056.svg)](https://doi.org/10.5281/zenodo.14551056) [![SWH](https://archive.softwareheritage.org/badge/origin/https://doi.org/10.5281/zenodo.14551056/)](https://archive.softwareheritage.org/browse/origin/?origin_url=https://doi.org/10.5281/zenodo.14551056) [![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)

# Sandborg-Petersen Morphology Decoder

The morphological decoder provided here is a lightweight decoder for the Sandborg-Petersen Morphology which is primarily tailored for Koine Greek, especially as it appears in New Testament studies and similar texts.

An online version of the decoder is available [here](https://tonyjurg.github.io/Sandborg-Petersen-decoder/).

# Decoder formats

Two functionaly equivalent coding implementations are stored on this repository:

   - [HTML with javascript](javascript/SP-Morph-decode.html)
   - [Python](python/SP-Morph-decode.py)

# Definitional document
 
[Parsing information](https://github.com/biblicalhumanities/Nestle1904/blob/master/morph/parsing.txt).

# Integrating in HTML page

If you have Javascript enabled you can use this HTML implementation. Either in the &lt;HEADER&gt; or &lt;BODY&gt; section define the following small script:

``` html
 <script>
    function openMinimalWindow() {
      window.open(
        'https://tonyjurg.github.io/Sandborg-Petersen-decoder/',
        '_blank',
        'toolbar=no,location=no,status=no,menubar=no,scrollbars=yes,resizable=yes,width=800,height=600'
      );
    }
  </script>
```
 In the &lt;BODY&gt; section include the following:
 
 ``` html
 <button onclick="openMinimalWindow()">Open Morph decoder</button>
 
 ```

This will put a button on your page similair to the image below:

<img src='images/button.jpg'>

When no scripting is enabled, you can just add a direct HTML link:

```html
  <A HREF="https://tonyjurg.github.io/Sandborg-Petersen-decoder/" TARGET="_blank">Open Morph decoder</A>
```

# Tag validation agains MACULA GNT dataset

 - See notebook: [Check SP-Morphs in MACULA XML dataset against documentated tags](testing/SP-Morphs-used-in-MACULA.ipynb).

# Acknowledgements

- ['Parsing Information for Robinson-like parsing tags Adapted from Ulrik Sandborg-Petersen's Description for Tischendorf 8th'](https://github.com/biblicalhumanities/Nestle1904/blob/master/morph/parsing.txt).
