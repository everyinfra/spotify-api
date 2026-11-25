# Spotify API

[English](#english) · [中文](#中文)

## English

This repo reads public Spotify data with Python or curl. You can search tracks, artists, albums and playlists by keyword, and read a track, an album and an artist's profile. You need one EveryInfra API key. You do not need a Spotify account or cookie. The same API also works as an MCP tool in Claude and Cursor. Billing is per call: these 4 capabilities cost $1.39 per 1,000 calls (about $0.0014 per call). Failed calls and empty results are not charged. The EveryInfra Spotify API has 7 capabilities, all listed on the platform page: <https://everyinfra.com/en/spotify-api?utm_source=github&utm_medium=example_repo&utm_campaign=spotify-api>

### Quick start

```bash
git clone https://github.com/everyinfra/spotify-api.git
cd spotify-api
pip install -r requirements.txt
export EVERYINFRA_API_KEY=<your API key>
python main.py search "lofi beats" --out tracks.csv
python main.py track "<track url>"
python main.py album <album id> --out album.json
python main.py artist "https://open.spotify.com/artist/06HL4z0CvFAxyc27GXpf02" --out artist.json
```

- For `track`, `album` and `artist`, pass an open.spotify.com link, a spotify:type:ID URI or a bare ID. The subcommand decides what kind of object it is.
- `search` looks for tracks by default; `--content-type` switches to artists, albums or playlists.
- For `album`, you can use the `album_id` from a `track` result.
- Without `--out`, the command prints the first 3 rows as JSON. With `--out`, it saves a .csv or .json file. The CSV has a BOM, so Excel opens it without garbled text.
- Register at everyinfra.com, then create the API key in the console. Steps: <https://everyinfra.com/en/docs?utm_source=github&utm_medium=example_repo&utm_campaign=spotify-api#quickstart>

### curl

```bash
curl -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"platform":"spotify","action":"search","params":{"keyword":"lofi beats"}}'
```

All capabilities use the same URL. Change `action` and `params` to call another one. Examples for `track`, `album`, and `artist` are in [examples/curl.sh](examples/curl.sh).

### Claude and Cursor (MCP)

The remote MCP URL is <https://api.everyinfra.com/mcp>. Add the `Authorization: Bearer` header with your API key. EveryInfra runs the server, so you install no local program.

Claude Code:

```bash
claude mcp add --transport http everyinfra https://api.everyinfra.com/mcp --header "Authorization: Bearer <API Key>"
```

Cursor and other clients that read `mcp.json` ([examples/mcp.json](examples/mcp.json)):

```json
{
  "mcpServers": {
    "everyinfra": {
      "url": "https://api.everyinfra.com/mcp",
      "headers": {
        "Authorization": "Bearer <API Key>"
      }
    }
  }
}
```

Custom connectors in Claude on the web and desktop, and ChatGPT, accept only a URL. Enter <https://api.everyinfra.com/mcp/all>, sign in to EveryInfra when asked, and allow access. You do not need to enter a key. Full steps: <https://everyinfra.com/en/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=spotify-api>

### Price

| `action` | Per 1,000 calls |
|---|---|
| `search` | $1.39 |
| `track` | $1.39 |
| `album` | $1.39 |
| `artist` | $1.39 |

- Billing is per call, about $0.0014 each. Failed calls, empty results, parameter errors, and authentication failures are not charged.
- A new account gets a $1 trial allowance, valid for 24 hours. No credit card is needed. How to claim it: <https://everyinfra.com/en/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=spotify-api>
- Prices for the other 3 Spotify capabilities are on the platform page: <https://everyinfra.com/en/spotify-api?utm_source=github&utm_medium=example_repo&utm_campaign=spotify-api>

### Fields

These are the fields that the 4 capabilities returned in our test. Each meaning is the first sentence of the field's entry in the API documentation. The link under each table has the full text.

#### `search` (keyword search)

| Field | Meaning |
|---|---|
| `id` | The record's unique ID on the platform. |
| `url` | Link to the record on the platform. |
| `type` | Record type; values depend on the capability (for example video / image / text). |
| `name` | Name of the object itself, for account, product and business capabilities. |
| `artists` | List of participating artists. |
| `album_name` | Album name. |
| `image_url` | Image link. |
| `duration_ms` | Duration in **milliseconds** (not seconds; divide by 1000 for seconds). |
| `is_explicit` | Whether it contains explicit content. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |

All parameters and fields: <https://everyinfra.com/en/spotify-api/search?utm_source=github&utm_medium=example_repo&utm_campaign=spotify-api>

#### `track` (track)

| Field | Meaning |
|---|---|
| `id` | The record's unique ID on the platform. |
| `url` | Link to the record on the platform. |
| `name` | Name of the object itself, for account, product and business capabilities. |
| `artists` | List of participating artists. |
| `album_name` | Album name. |
| `duration_ms` | Duration in **milliseconds** (not seconds; divide by 1000 for seconds). |
| `play_count` | Play count. |
| `track_number` | Position of the track within the album. |
| `disc_number` | Disc number of the track within its album, from 1 (track). |
| `is_explicit` | Whether it contains explicit content. |
| `release_date` | Release date. |
| `preview_url` | Link to a 30-second preview clip; may be null. |
| `image_url` | Image link. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |
| `album_id` | Album ID. |
| `album_type` | Album type (album/single/compilation). |

All parameters and fields: <https://everyinfra.com/en/spotify-api/track?utm_source=github&utm_medium=example_repo&utm_campaign=spotify-api>

#### `album` (album)

| Field | Meaning |
|---|---|
| `id` | The record's unique ID on the platform. |
| `url` | Link to the record on the platform. |
| `name` | Name of the object itself, for account, product and business capabilities. |
| `album_type` | Album type (album/single/compilation). |
| `artists` | List of participating artists. |
| `release_date` | Release date. |
| `label` | Record label. |
| `copyright` | Copyright information. |
| `track_count` | Total number of tracks. |
| `image_url` | Image link. |
| `tracks` | List of tracks. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |

All parameters and fields: <https://everyinfra.com/en/spotify-api/album?utm_source=github&utm_medium=example_repo&utm_campaign=spotify-api>

#### `artist` (artist details)

| Field | Meaning |
|---|---|
| `id` | The record's unique ID on the platform. |
| `url` | Link to the record on the platform. |
| `name` | Name of the object itself, for account, product and business capabilities. |
| `bio` | Profile bio written by the account; may contain line breaks and emoji. |
| `monthly_listener_count` | Monthly listener count. |
| `follower_count` | Followers. null means not disclosed, not 0. |
| `world_rank` | Global rank. |
| `image_url` | Image link. |
| `header_image_url` | Profile header image. |
| `album_count` | Number of albums. |
| `single_count` | Number of singles. |
| `compilation_count` | Number of compilations. |
| `top_cities` | Cities with the most listeners. |
| `top_tracks` | Top tracks. |
| `related_artists` | Recommended related artists. |
| `platform` | Source platform identifier, the same as platform in the request (for example xiaohongshu, tiktok). |

All parameters and fields: <https://everyinfra.com/en/spotify-api/artist?utm_source=github&utm_medium=example_repo&utm_campaign=spotify-api>

### FAQ

**Do I need a Spotify account or cookie to call the API?**

No. Send the `Authorization: Bearer` header with your API key. The request body holds `platform`, `action`, and the capability parameters. You do not scan a QR code, keep a login session, or open a browser.

**How much does it cost? Are failed calls charged? Is there a free allowance?**

Billing is per call, from $1.39 per 1,000 calls. Failed calls, empty results, parameter errors, and authentication failures are not charged. A new account gets a $1 trial allowance, valid for 24 hours. No credit card is needed. How to claim it: <https://everyinfra.com/en/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=spotify-api>

**Can I connect the Spotify API to Claude or Cursor?**

Yes. The remote MCP URL is <https://api.everyinfra.com/mcp>. Add the `Authorization: Bearer` header with your API key. You install no local program. Setup for Claude, Cursor, ChatGPT, and Claude Code: <https://everyinfra.com/en/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=spotify-api>.

**What legal points apply when I use Spotify data?**

The EveryInfra Terms of Service require you to make sure your use of the data follows applicable law and the terms of the relevant platform. Do not use the data for anything illegal or anything that violates privacy or intellectual property rights. Do not use bulk scraping for harassment, fraud, or other abuse. When you use personal information such as nicknames and avatars, keep only the fields your business needs.

**Which Spotify data can I get?**

The EveryInfra Spotify API has 7 capabilities:

- profile or object details
- keyword search
- artist details
- track
- album
- playlist
- podcast

Parameters and return fields for each capability are on the platform page: <https://everyinfra.com/en/spotify-api?utm_source=github&utm_medium=example_repo&utm_campaign=spotify-api>

### Tested

Before release, we ran the 4 commands in Quick start against the live API with this repo's code.

| Command | Time (Singapore, UTC+8) | Rows | Charged |
|---|---|---|---|
| `python main.py search "lofi beats" --out tracks.csv` | 2026-11-25 13:20 | 20 | $0.001389 |
| `python main.py track "<track url>"` | 2026-11-25 13:20 | 1 | $0.001389 |
| `python main.py album <album id> --out album.json` | 2026-11-25 13:20 | 1 | $0.001389 |
| `python main.py artist "https://open.spotify.com/artist/06HL4z0CvFAxyc27GXpf02" --out artist.json` | 2026-11-25 13:20 | 1 | $0.001389 |

## 中文

本仓库用 Python 或 curl 读 Spotify 公开数据：按关键词搜歌曲、艺人、专辑和歌单，读单曲、专辑和艺人资料。只需一把 EveryInfra API Key，不用 Spotify 账号和 Cookie，也能作为 MCP 工具接进 Claude、Cursor。按调用次数计费，这 4 个能力每千次 $1.39（每次约 $0.0014），失败和空结果不收费。Spotify 共 7 个能力：<https://everyinfra.com/spotify-api?utm_source=github&utm_medium=example_repo&utm_campaign=spotify-api>

### 快速开始

```bash
git clone https://github.com/everyinfra/spotify-api.git
cd spotify-api
pip install -r requirements.txt
export EVERYINFRA_API_KEY=<你的 API Key>
python main.py search "lofi beats" --out tracks.csv
python main.py track "<单曲链接>"
python main.py album <专辑 ID> --out album.json
python main.py artist "https://open.spotify.com/artist/06HL4z0CvFAxyc27GXpf02" --out artist.json
```

- `track`、`album`、`artist` 传 open.spotify.com 链接，也可以传 spotify:类型:ID 或裸 ID；查哪类由子命令决定。
- `search` 默认搜歌曲，`--content-type` 换成 artists、albums、playlists。
- `album` 可用 `track` 结果里的 `album_id`。
- 不加 `--out` 时打印前 3 条 JSON；加 `--out` 存成 .csv 或 .json。CSV 带 BOM，Excel 直接打开不乱码。
- API Key 在 everyinfra.com 注册后到控制台创建，步骤见 <https://everyinfra.com/docs?utm_source=github&utm_medium=example_repo&utm_campaign=spotify-api#quickstart>

### 用 curl 调

```bash
curl -X POST https://api.everyinfra.com/api/v1/social \
  -H "Authorization: Bearer $EVERYINFRA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"platform":"spotify","action":"search","params":{"keyword":"lofi beats"}}'
```

所有能力都发到同一个地址，换 `action` 和 `params` 就行；`track`、`album`、`artist` 的写法见 [examples/curl.sh](examples/curl.sh)。

### 接进 Claude、Cursor（MCP）

远程 MCP 地址是 <https://api.everyinfra.com/mcp>，请求头加 `Authorization: Bearer` 和 API Key；服务器由 EveryInfra 运行，不用装本地程序。

Claude Code：

```bash
claude mcp add --transport http everyinfra https://api.everyinfra.com/mcp --header "Authorization: Bearer <API Key>"
```

Cursor 等读 `mcp.json` 的客户端（[examples/mcp.json](examples/mcp.json)）：

```json
{
  "mcpServers": {
    "everyinfra": {
      "url": "https://api.everyinfra.com/mcp",
      "headers": {
        "Authorization": "Bearer <API Key>"
      }
    }
  }
}
```

Claude 网页版和桌面版的自定义连接器、ChatGPT 只能填网址：填 <https://api.everyinfra.com/mcp/all>，连接时登录 EveryInfra 并允许，不用填 Key。完整步骤见 <https://everyinfra.com/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=spotify-api>

### 价格

| 能力 | `action` | 每千次 |
|---|---|---|
| 关键词搜索 | `search` | $1.39 |
| 单曲详情 | `track` | $1.39 |
| 专辑 | `album` | $1.39 |
| 艺人或创作者资料 | `artist` | $1.39 |

- 按调用次数计费，每次约 $0.0014；失败、空结果、参数错误和鉴权失败都不收费。
- 新账号有 $1 试用额度，24 小时内有效，不用信用卡，领取方式见 <https://everyinfra.com/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=spotify-api>
- Spotify 其他 3 个能力的单价见平台页 <https://everyinfra.com/spotify-api?utm_source=github&utm_medium=example_repo&utm_campaign=spotify-api>

### 返回字段

下面是这 4 个能力实测返回的字段，含义取自接口文档每条说明的第一句，完整说明在每张表下面的链接里。

#### `search`（关键词搜索）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `type` | 记录类型，取值随能力而定（如 video / image / text）。 |
| `name` | 名称。 |
| `artists` | 参与艺人列表。 |
| `album_name` | 专辑名称。 |
| `image_url` | 图片链接。 |
| `duration_ms` | 时长，**单位毫秒**（不是秒，除以 1000 才是秒）。 |
| `is_explicit` | 是否含限制级内容。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |

完整参数和字段：<https://everyinfra.com/spotify-api/search?utm_source=github&utm_medium=example_repo&utm_campaign=spotify-api>

#### `track`（单曲详情）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `name` | 名称。 |
| `artists` | 参与艺人列表。 |
| `album_name` | 专辑名称。 |
| `duration_ms` | 时长，**单位毫秒**（不是秒，除以 1000 才是秒）。 |
| `play_count` | 播放次数。 |
| `track_number` | 该曲在专辑中的序号。 |
| `disc_number` | 曲目在专辑里的碟号（第几张碟），从 1 开始（track）。 |
| `is_explicit` | 是否含限制级内容。 |
| `release_date` | 发行日期。 |
| `preview_url` | 30 秒试听片段链接，可能为 null。 |
| `image_url` | 图片链接。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |
| `album_id` | 专辑 ID。 |
| `album_type` | 专辑类型（album/single/compilation）。 |

完整参数和字段：<https://everyinfra.com/spotify-api/track?utm_source=github&utm_medium=example_repo&utm_campaign=spotify-api>

#### `album`（专辑）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `name` | 名称。 |
| `album_type` | 专辑类型（album/single/compilation）。 |
| `artists` | 参与艺人列表。 |
| `release_date` | 发行日期。 |
| `label` | 唱片公司。 |
| `copyright` | 版权信息。 |
| `track_count` | 曲目总数。 |
| `image_url` | 图片链接。 |
| `tracks` | 曲目列表。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |

完整参数和字段：<https://everyinfra.com/spotify-api/album?utm_source=github&utm_medium=example_repo&utm_campaign=spotify-api>

#### `artist`（艺人或创作者资料）

| 字段 | 含义 |
|---|---|
| `id` | 该记录在原平台上的唯一标识。 |
| `url` | 该记录在原平台上的可访问链接。 |
| `name` | 名称。 |
| `bio` | 个人简介，账号自己填写的文本。 |
| `monthly_listener_count` | 月听众数。 |
| `follower_count` | 粉丝数。 |
| `world_rank` | 全球排名。 |
| `image_url` | 图片链接。 |
| `header_image_url` | 主页头图。 |
| `album_count` | 专辑数量。 |
| `single_count` | 单曲数量。 |
| `compilation_count` | 合辑数量。 |
| `top_cities` | 听众最多的城市。 |
| `top_tracks` | 热门曲目。 |
| `related_artists` | 相关艺人推荐。 |
| `platform` | 数据来源平台标识，与请求里的 platform 一致（如 xiaohongshu、tiktok）。 |

完整参数和字段：<https://everyinfra.com/spotify-api/artist?utm_source=github&utm_medium=example_repo&utm_campaign=spotify-api>

### 常见问题

**调用时要不要提供 Spotify 账号或 Cookie？**

不用，请求头带 `Authorization: Bearer` 和 API Key 就能调，请求体写 `platform`、`action` 和能力参数。不用扫码、维护登录状态，也不用开浏览器。

**怎么收费？失败了收不收钱？有免费额度吗？**

按调用次数计费，每千次 $1.39 起。失败、空结果、参数错误和鉴权失败都不收费。新账号有 $1 试用额度，24 小时内有效，不用信用卡，领取方式见定价页 <https://everyinfra.com/pricing?utm_source=github&utm_medium=example_repo&utm_campaign=spotify-api>

**能把 Spotify 接口接进 Claude、Cursor 吗？**

能，远程 MCP 地址是 <https://api.everyinfra.com/mcp>，请求头加 `Authorization: Bearer` 和 API Key，不用装本地程序。Claude、Cursor、ChatGPT、Claude Code 配置见 <https://everyinfra.com/mcp-server?utm_source=github&utm_medium=example_repo&utm_campaign=spotify-api>。

**用 Spotify 数据要注意哪些合规问题？**

EveryInfra 服务条款要求你自行确保数据用法符合适用法律和相关平台条款，禁止用于违法、侵犯隐私或知识产权，或批量抓取用于骚扰、欺诈等恶意用途。用到昵称、头像等个人信息时，只留业务用得上的字段。

**可以拿到 Spotify 的哪些数据？**

Spotify 有 7 个能力：主页或对象详情、关键词搜索、艺人或创作者资料、单曲详情、专辑、播放列表、播客。每个能力的参数和返回字段见平台页 <https://everyinfra.com/spotify-api?utm_source=github&utm_medium=example_repo&utm_campaign=spotify-api>

### 实测记录

发布前用本仓的代码对线上接口跑过一遍，命令就是「快速开始」里的 4 条。

| 命令 | 时间（新加坡时间） | 返回条数 | 扣费 |
|---|---|---|---|
| `python main.py search "lofi beats" --out tracks.csv` | 2026-11-25 13:20 | 20 | $0.001389 |
| `python main.py track "<单曲链接>"` | 2026-11-25 13:20 | 1 | $0.001389 |
| `python main.py album <专辑 ID> --out album.json` | 2026-11-25 13:20 | 1 | $0.001389 |
| `python main.py artist "https://open.spotify.com/artist/06HL4z0CvFAxyc27GXpf02" --out artist.json` | 2026-11-25 13:20 | 1 | $0.001389 |

`track` 返回的一条（正文截到 60 字，作者字段没放进来）：

```json
{
  "id": "4BBVbCXtGYRkRhVtQIverK",
  "play_count": 3893
}
```

## License

MIT
