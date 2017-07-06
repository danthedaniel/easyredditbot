# easyredditbot

Create a reddit bot as quickly as possible.

easyredditbot automatically handles:

* Network Errors
* Multiple Callbacks
* id blacklist (so no item is ever processed twice)

# Installation

This software can be installed through pip as the easyredditbot package:

    pip install easyredditbot

# Usage

```python
from easyredditbot import set_reddit, AllCommentsHook

set_reddit(
    client_id='...',
    client_secret='...',
    user_agent='...'
)


@AllCommentsHook
def print_comment(comment):
    if 'easyredditbot' in comment.body:
        comment.reply('Hello, world!')


AllCommentsHook.loop_forever()  # AllCommentsHook.run_once() is also available
```

All hooks available:

* `AllCommentsHook` - Read comments from /r/all
* `AllSubmissionsHook` - Read submissions from /r/all
* `InboxHook` - Read messages in your inbox (and mark them as read after)
