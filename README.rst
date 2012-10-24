==========================
Zen
==========================


Set up the redis for auto suggest
-----

1. Install the `redis`_.

2. Install the `redis-py`_.

3. Run the command to fill the redis with prefixes::

    python suggest/filler.py


Set up the crawler
-----

.. _redis-py: http://github.com/andymccurdy/redis-py/
.. _redis: http://redis.io/download
