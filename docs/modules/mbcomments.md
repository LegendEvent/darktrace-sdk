# MBComments Module

> ⚠️ **BREAKING CHANGE**: SSL verification default changed from `False` to `True` in v0.9.0. If using self-signed certificates, you must either add them to your system trust store or set `verify_ssl=False` explicitly.


The MBComments (Model Breach Comments) module wraps the `/mbcomments` endpoint, which returns all comments across model breaches, or the comments of one specific model breach. The module also offers `post()` as a convenience for adding a comment to a breach.

## Initialization

```python
from darktrace import DarktraceClient

client = DarktraceClient(
    host="https://your-darktrace-instance",
    public_token="YOUR_PUBLIC_TOKEN",
    private_token="YOUR_PRIVATE_TOKEN"
)

# Access the mbcomments module
mbcomments = client.mbcomments
```

## Methods Overview

- **`get()`** - Retrieve model breach comments (`GET /mbcomments`)
- **`post()`** - Add a comment to a model breach (`POST /modelbreaches/<pbid>/comments`)

## Methods

### Get Comments

Retrieve comments across model breaches, optionally filtered by time range or by a single model breach.

```python
# Get comments (count defaults to 100)
all_comments = mbcomments.get()

# Get comments for a specific model breach
breach_comments = mbcomments.get(pbid=12345)

# Get comments within a time range (epoch milliseconds)
time_filtered = mbcomments.get(
    starttime=1597795200000,
    endtime=1597881599000
)

# Limit the number of comments
recent_comments = mbcomments.get(count=50)

# Restrict the response to one top-level field
messages = mbcomments.get(pbid=12345, responsedata="message")
```

#### Parameters

- `starttime` (int, optional): Start time of data to return, in milliseconds since epoch (UTC)
- `endtime` (int, optional): End time of data to return, in milliseconds since epoch (UTC)
- `responsedata` (str, optional): The name of ONE top-level field or object; restricts the returned JSON to only that field or object (a comma-separated list is not supported)
- `count` (int, optional): Number of comments to return (default 100). It only limits the number of comments within the specified timeframe
- `pbid` (int, optional): Only return comments for the model breach with this ID
- `timeout` (float or tuple, optional): Request timeout in seconds
- Additional query parameters via `**params`

There is no per-comment endpoint: passing `comment_id` raises `ValueError`. Use `pbid`, `starttime`/`endtime` or `count` to filter.

#### Response Structure

A list of comment objects:

```python
[
  {
    "time": 1597837975000,       # time the comment was posted (epoch ms)
    "pbid": 1432,                # policy breach ID of the model breach commented on
    "username": "lryan",         # user who made the comment
    "message": "Investigation completed",  # comment text
    "pid": 17,                   # policy ID of the model breach
    "name": "Compliance::Messaging::Facebook Messenger"  # name of the model that was breached
  },
  {
    "time": 1586937600000,
    "pbid": 1329,
    "username": "ajohnston",
    "message": "Concerning behavior. Investigating possible compromise.",
    "pid": 52,
    "name": "Anomalous File::Masqueraded File Transfer"
  }
]
```

### Add Comment

Add a comment to a model breach. The API guide documents `/mbcomments` as GET only; comments are added with `POST /modelbreaches/<pbid>/comments` and a JSON body `{"message": "..."}`. `post()` does exactly this (it is equivalent to `client.breaches.add_comment`).

```python
response = mbcomments.post(
    breach_id=12345,
    comment="Initial triage complete. Proceeding with detailed analysis."
)
```

#### Parameters

- `breach_id` (str or int, required): The model breach ID (pbid) to add the comment to
- `comment` (str, required): The comment text (sent as `message`)
- `timeout` (float or tuple, optional): Request timeout in seconds
- `**params` is accepted but ignored: the guide states that this POST takes no parameters

#### Response

The guide's example response for this endpoint is the list of comments on the breach (fields `message`, `username`, `time`, `pid`); `post()` returns the parsed JSON as received. See the API guide for the full schema.

## Examples

### Latest Comment per Breach

```python
import datetime

# Comments from the last 24 hours
end = datetime.datetime.now()
start = end - datetime.timedelta(hours=24)

comments = client.mbcomments.get(
    starttime=int(start.timestamp() * 1000),
    endtime=int(end.timestamp() * 1000)
)

latest = {}
for c in comments:
    pbid = c["pbid"]
    if pbid not in latest or c["time"] > latest[pbid]["time"]:
        latest[pbid] = c

for pbid, c in latest.items():
    when = datetime.datetime.fromtimestamp(c["time"] / 1000)
    print(f"Breach {pbid} ({c['name']}): {c['username']} at {when:%Y-%m-%d %H:%M}")
    print(f"  {c['message']}")
```

### Investigation Timeline for One Breach

```python
import datetime

pbid = 12345  # Replace with actual breach ID

comments = client.mbcomments.get(pbid=pbid)
if not comments:
    print(f"No comments found for breach {pbid}")
else:
    for i, c in enumerate(sorted(comments, key=lambda x: x["time"]), 1):
        when = datetime.datetime.fromtimestamp(c["time"] / 1000)
        print(f"{i}. {when:%Y-%m-%d %H:%M:%S} - {c['username']}: {c['message']}")
```

### Comment Search and Reporting

```python
import datetime
from collections import Counter

end = datetime.datetime.now()
start = end - datetime.timedelta(days=7)

comments = client.mbcomments.get(
    starttime=int(start.timestamp() * 1000),
    endtime=int(end.timestamp() * 1000),
    count=1000
)

# Filter by text (done client-side)
term = "false positive"
matches = [c for c in comments if term in c["message"].lower()]
print(f"{len(matches)} of {len(comments)} comments mention '{term}'")

# Comments per user and per breach
print(Counter(c["username"] for c in comments).most_common(5))
print(f"Breaches with comments: {len({c['pbid'] for c in comments})}")
```

### Adding a Comment

```python
response = client.mbcomments.post(
    breach_id=12345,
    comment="Confirmed legitimate backup process. Marking as resolved."
)
print(response)
```

## Error Handling

```python
import requests

try:
    comments = client.mbcomments.get(pbid=12345)
    for c in comments:
        print(f"{c['username']}: {c['message'][:100]}")
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
    if e.response is not None:
        print(f"Status code: {e.response.status_code}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Notes

- **Time parameters**: `starttime`/`endtime` are epoch milliseconds (UTC). `count` (default 100) only limits the number of comments within the specified timeframe. The guide does not state a default time window.
- **Breach association**: each comment carries the `pbid` of its model breach and the `pid`/`name` of the model.
- **`responsedata`**: takes the name of one top-level field or object (for example `"message"`), not a list.
- **Adding comments**: handled by `POST /modelbreaches/<pbid>/comments` with JSON body `{"message": ...}`; no parameters are supported.
