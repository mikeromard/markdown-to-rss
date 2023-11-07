# markdown-to-rss

This is a proof-of-concept for updating an RSS feed from a markdown file that serves as a project updates (or changelog, or release notes) page.

## How it works:

1. The workflow (`.github/workflows/markdown_to_rss.yml`) starts when a push is made to the `main` branch that includes an update to `test_product_updates.md`.
2. The workflow sets up python 3.9, installs the packages listed in `requirements.txt`, and then runs the `markdown_to_rss.py` script.
3. The `markdown_to_rss.py` script does the following:
    1. Creates a timestamp that is a valid [RFC-822](http://www.faqs.org/rfcs/rfc822.html) date-time.
    2. Converts the content of `test_product_updates.md` from markdown to HTML.
    3. Wraps that HTML in an `<rss>` element and uses a regex to extract the entries (all text from the start of an h2 element to the end of an h2 or rss element) from that element into a list.
    4. Update the `<pubDate>` element in `test_rss_feed.xml` with the value of the timestamp from step 1.
    5. For each entry in the list from step 3:
        1. Format the entry into an `<item>` with a `<title>` (from the item's `<h2>` element), and a `<category>` (from the first `<p>`). 
        2. Checks to see if the item title text already exists in `test_rss_feed.xml`. If it does, it does nothing else for that item. If it does not, it adds these elements: 
            * `<pubDate>` (from the timestamp in step 1) 
            * `<link>` (appends the `<title>` to `https://github.com/mikeromard/markdown-to-rss/blob/main/test_product_updates.md#`, but replace spaces with `-`) 
            * `<guid>` (same as `<link>`) 
            * `<description>` (outputs a string of what's left from the entry after removing the `<title>` and `<category>` elements)
        3. Inserts the `<item>` after the `<pubDate>` element.
        4. Writes the changes to `test_rss_feed.xml`.
4. Commit and push the changes from step 3 to the `main` branch.


## Current known limitations and issues:

* The timestamp uses GMT, because when I was testing this on my laptop I found that my local timezone wasn't allowed in RFC-822. That said, when I look at the feed in NetNewsWire, the time displayed per item seems to be correct, so this may not be a significant issue. If it is though, the script will need some logic for determining the time offset from UTC (in ±HHMM) and outputting that instead of `GMT`.
* The `markdown_to_rss.py` script has no logic for updating an existing `<item>`. So if you update an existing entry in `test_product_updates.md` (for example, to fix a typo), the update is not output to `test_rss_feed.xml` unless you first manually remove the corresponding `<item>`. 
    * One possible exception to this is that if you update the header for the entry. I haven't tested this, but the script uses the header text to determine if the entry already exists in `test_rss_feed.xml`, so if it doesn't find an exact match for the header text it should treat the entry as being new.
* If `markdown_to_rss.py` finds more than one new entry in `test_product_updates.md`, it makes no effort to sort them. The sample entries in `test_product_updates.md` are from most recent to oldest, and they are processed in that order. 
    * For example, if both the first and second entries in `test_product_updates.md` are new, the first entry gets added as the first `<item>` in `test_rss_feed.xml`, and then the second entry gets added as the first `<item>`, meaning that the first entry is now the second `<item>`. This could be handled better by reversing the order of the list of entries before processing them. 
    * Both entries would also have identical timestamps in their `<pubDate>` elements. It may be a good idea to update the timestamp when processing each entry, and introduce a 1 second delay to ensure that each timestamp is unique. If this is implemented, the last timestamp should also be used to update the `<pubDate>` for the feed itself, since it should presumably not be older than any of the `<pubDate>` timestamps in the `<item>` elements. 
* Where a new `<item>` is inserted is hard-coded. It would be good if the script could determine the index of the first `<item>` and insert each new `<item>` at that index, rather than relying on the number of elements before the first `<item>` staying the same.