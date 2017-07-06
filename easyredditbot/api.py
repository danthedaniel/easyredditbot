"""easyredditbot is an API to create a reddit bot as quickly as possible.

Copyright (C) 2017 teaearlgraycold

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
from time import sleep
from praw import Reddit


class HookBase:
    """Abstract base class for all hook classes."""

    previous_ids = set()  # All previously seen items
    wrapped_funcs = {}  # All wrapped callback functions
    reddit = None

    def __init__(self, func):
        """Add a function to the class's list of callbacks.

        Parameters
        ----------
        func : callable
            A function to add to the callback list.
        """
        class_name = self.__class__.__name__
        current_callbacks = self.wrapped_funcs.get(class_name, [])
        self.wrapped_funcs[class_name] = current_callbacks + [func]

    @classmethod
    def run_once(cls):
        """Call each callback for this class in sequence."""
        if cls.reddit is None:
            raise ValueError('PRAW Reddit session is not set. Run set_reddit first.')

        # Invoke each callback for each item
        items = list(cls.seen_filter(cls.items()))
        for func in cls.wrapped_funcs.get(cls.__name__, []):
            for item in items:
                cls.process_return(func(item))

    @classmethod
    def loop_forever(cls):
        """Loop over all callbacks with exponential delay upon exceptions."""
        delay = 1

        while True:
            try:
                cls.run_once()
                delay = 1
            except KeyboardInterrupt as e:
                print('Reddit read loop ended.')
                return
            except Exception as e:
                print('An error occurred while reading from reddit: {}'.format(str(e)))
                sleep(delay)
                delay *= 2  # Double the delay each time run_once fails

    @classmethod
    def seen_filter(cls, items):
        """Yield the subset of items that have not previously been viewed.

        Parameters
        ----------
        items : iterable
            Items to filter through.

        Returns
        -------
        Generator yielding items who have ids not previously seen.
        """
        for item in items:
            # Only yield if this item has not yet been seen
            if item.id not in cls.previous_ids:
                yield item

        # Add all new ids to the set of previously viewed ids
        cls.previous_ids |= {item.fullname for item in items}

    @classmethod
    def process_return(cls, ret):
        """If necessary, perform processing after the wrapped function completes.

        Parameters
        ----------
        ret : object
            The value returned by the wrapped function.
        """
        pass


def set_reddit(*args, **kwargs):
    """Set all API hooks to use a single PRAW Reddit session.

    Parameters
    ----------
    args : Positional Arguments
        Positional arguments used in instantiation of a Reddit session object.
    kwargs : Keyword Arguments
        Keyword arguments used in instantiation of a Reddit session object.
    """
    HookBase.reddit = Reddit(*args, **kwargs)


class InboxHook(HookBase):
    """Hook for processing inbox messages."""

    @classmethod
    def items(cls):
        for message in cls.reddit.inbox.messages(limit=100):
            message.mark_read()
            yield message


class AllCommentsHook(HookBase):
    """Hook for processing comments from /r/all."""

    @classmethod
    def items(cls):
        return cls.reddit.subreddit('all').comments(limit=100)


class AllSubmissionsHook(HookBase):
    """Hook for processing submissions from /r/all."""

    @classmethod
    def items(cls):
        return cls.reddit.subreddit('all').submissions()
