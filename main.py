"""Spotify API 示例（Spotify API in Python）。

  python main.py search "lofi beats" --out tracks.csv                                              # 按关键词搜 / search
  python main.py track "<单曲链接>"                                                                # 单曲详情 / track detail
  python main.py album <专辑 ID> --out album.json                                                  # 专辑 / album
  python main.py artist "https://open.spotify.com/artist/06HL4z0CvFAxyc27GXpf02" --out artist.json # 艺人资料 / artist profile
"""
import argparse

from everyinfra import fetch, report

CONTENT_TYPES = ["albums", "artists", "playlists", "tracks"]


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("search", help="按关键词搜 / search by keyword")
    s.add_argument("keyword")
    s.add_argument("--content-type", choices=CONTENT_TYPES, help="tracks / artists / albums / playlists")
    t = sub.add_parser("track", help="单曲详情 / one track")
    t.add_argument("url")
    al = sub.add_parser("album", help="专辑 / one album")
    al.add_argument("url")
    ar = sub.add_parser("artist", help="艺人资料 / artist profile")
    ar.add_argument("url")
    for x in (s, t, al, ar):
        x.add_argument("--out", help="存成 .csv 或 .json / write .csv or .json")
    a = p.parse_args()

    if a.cmd == "search":
        params = {"keyword": a.keyword, **({"content_type": a.content_type} if a.content_type else {})}
        rows, charged = fetch("search", params)
    elif a.cmd == "track":
        rows, charged = fetch("track", {"url": a.url})
    elif a.cmd == "album":
        rows, charged = fetch("album", {"url": a.url})
    else:
        rows, charged = fetch("artist", {"url": a.url})
    report(rows, charged, a.out)


if __name__ == "__main__":
    main()
