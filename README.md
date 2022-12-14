# rfc2bib

## Usage

### Generate single RFC BibTeX

```sh
./rfc2bib.py rfc7777
```

```bibtex
@techreport{rfc7777,
  title  = {Advertising Node Administrative Tags in OSPF},
  author = {{S. Hegde} and {R. Shakir} and {A. Smirnov} and {Z. Li} and {B. Decraene}},
  year   = {2016},
  month  = {3},
  url    = {https://www.ietf.org/rfc/rfc7777},
}
```

### Generate multiple RFC BibTeX and save

```sh
./rfc2bib.py rfc5555 rfc6666 rfc7777 -o my-rfcs.bib
```
