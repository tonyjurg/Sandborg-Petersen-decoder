[![Project Status: Active – The project has reached a stable, usable state and is being actively developed.](https://www.repostatus.org/badges/latest/active.svg)](https://www.repostatus.org/#active) [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.14551057.svg)](https://doi.org/10.5281/zenodo.14551057) [![License: CC BY 4.0](https://img.shields.io/badge/License-CC_BY_NC-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)


# Sandborg-Petersen Morphology Decoder

The morphological decoder provided here is a lightweight decoder for the Sandborg-Petersen Morphology which is primarily tailored for Koine Greek, especially as it appears in New Testament studies and similar texts.

An online version of the decoder is available [here](https://tonyjurg.github.io/Sandborg-Petersen-decoder/).

# Decoder formats

Three functionaly equivalent coding implementations are stored on this repository:

   - [HTML with javascript](javascript/SP-Morph-decode.html)
   - [Python](python/SP-Morph-decode.py)

# Definitional document
 
[Parsing information](https://github.com/biblicalhumanities/Nestle1904/blob/master/morph/parsing.txt).

# Integrating in HTML page

The HTML implementation depends on Javascript being enabled. Either in the &lt;HEADER&gt; or &lt;BODY&gt; section define the following small script:

``` html
 <script>
    function openMinimalWindow() {
      window.open(
        'yourPage.html',
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
