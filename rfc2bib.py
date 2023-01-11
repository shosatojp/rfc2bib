#!/usr/bin/env python3
import sys
from typing import Any, Dict
import time
import requests
import string


def get_metadata(doc_id: str) -> Dict[str, Any]:
    url = f"https://www.ietf.org/rfc/{doc_id}.json"
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f"failed to get metadata from {url}")

    try:
        return res.json()
    except Exception as e:
        raise e


def generate_slug(s: str) -> str:
    return "".join(
        [
            c
            for c in s.strip().lower().replace(" ", "-")
            if c in string.ascii_lowercase + string.digits + "-"
        ]
    )


def generate_bibtex(citekey: str, metadata: Dict[str, Any]) -> str:
    fields: Dict[str, str] = {}
    slug = None
    if "title" in metadata:
        fields["title"] = metadata["title"].strip()
        slug = generate_slug(metadata["title"].strip())
    if "authors" in metadata:
        fields["author"] = " and ".join(
            ["{" + author.strip() + "}" for author in metadata["authors"]]
        )
    if "pub_date" in metadata:
        pub_date = time.strptime(metadata["pub_date"].strip(), "%B %Y")
        fields["year"] = pub_date.tm_year
        fields["month"] = pub_date.tm_mon
    fields["url"] = f"https://www.ietf.org/rfc/{metadata['doc_id'].strip().lower()}.txt"

    # generate bibtex text
    max_key_length = max([len(k) for k in fields.keys()])

    INDENT = " " * 2
    txt = f"@techreport{{{citekey}{'-' + slug if slug else ''},\n"
    for k, v in fields.items():
        pad = " " * (max_key_length - len(k))
        txt += INDENT + f"{k}{pad} = {{{v}}},\n"
    txt += "}"

    return txt


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("doc_ids", nargs="+", help="e.g. rfc7777")
    parser.add_argument("--output", "-o")
    args = parser.parse_args()

    bibtex_list = []
    for doc_id in args.doc_ids:
        print(f"fetching {doc_id}", file=sys.stderr)
        metadata = get_metadata(doc_id.lower())
        bibtex = generate_bibtex(doc_id.lower(), metadata)
        bibtex_list.append(bibtex)

    bibtex_all = "\n\n".join(bibtex_list)
    if args.output:
        with open(args.output, "wt", encoding="utf-8") as fp:
            fp.write("% generated with:\n")
            fp.write(f"% {' '.join(sys.argv)}\n\n")
            fp.write(bibtex_all)
    else:
        print(bibtex_all)
