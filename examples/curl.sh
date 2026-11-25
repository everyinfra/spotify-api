#!/usr/bin/env bash
# Spotify API 的 curl 示例：所有能力都发到同一个地址，只换 action 和 params。
# curl examples for the Spotify API: every capability uses the same URL; only action and params change.
#
#   export EVERYINFRA_API_KEY=<your API key>
#   bash examples/curl.sh search "lofi beats"
#   bash examples/curl.sh track "<track url>"                                           # search 结果里的 url / the url from a search result
#   bash examples/curl.sh album <album id>                                              # track 结果里的 album_id / the album_id from a track result
#   bash examples/curl.sh artist https://open.spotify.com/artist/06HL4z0CvFAxyc27GXpf02
set -euo pipefail
: "${EVERYINFRA_API_KEY:?Set EVERYINFRA_API_KEY first: https://everyinfra.com/docs#quickstart}"
action=${1:?"usage: bash examples/curl.sh <search|track|album|artist> <value>"}
value=${2:?"value: a keyword, an open.spotify.com link or an ID"}

case "$action" in
  search)                 params="{\"keyword\":\"$value\"}" ;;
  track | album | artist) params="{\"url\":\"$value\"}" ;;
  *) echo "unknown action: $action (use search, track, album or artist)" >&2; exit 2 ;;
esac

curl -sS -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"platform\":\"spotify\",\"action\":\"$action\",\"params\":$params}"
echo
