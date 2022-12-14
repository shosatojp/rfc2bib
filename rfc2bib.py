#!/usr/bin/env python3
from typing import Any, Dict
import time
import requests


def get_metadata(doc_id: str) -> Dict[str, Any]:
    url = f"https://www.ietf.org/rfc/{doc_id}.json"
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f"failed to get metadata from {url}")

    try:
        return res.json()
    except Exception as e:
        raise e


def generate_bibtex(citekey: str, metadata: Dict[str, Any]) -> str:
    txt = ""
    txt += f"@techreport{{{citekey},\n"
    if "title" in metadata:
        txt += f"  title = {{{metadata['title']}}},\n"
    if "authors" in metadata:
        authorlist = " and ".join(
            ["{" + author + "}" for author in metadata["authors"]]
        )
        txt += f"  author = {{{authorlist}}},\n"
    if "pub_date" in metadata:
        pub_date = time.strptime("March 2016", "%B %Y")
        txt += f"  year = {{{pub_date.tm_year}}},\n"
        txt += f"  month = {{{pub_date.tm_mon}}},\n"
    txt += f"  url = {{https://www.ietf.org/rfc/{metadata['doc_id'].lower()}}},\n"
    txt += "}"

    return txt


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("doc_id", help="e.g. rfc7777")
    args = parser.parse_args()

    metadata = get_metadata(args.doc_id)
    txt = generate_bibtex(args.doc_id.lower(), metadata)
    print(txt)
