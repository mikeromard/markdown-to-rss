# Product updates

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

## Testing this automation again

Test

This is some text. It's not particularly exciting text.

## Proof of concept just failed in live demo

Oops

There seems to be an issue, possibly caused by not including more than one line of text between headings. The XML file did update, but only the timestamp, after the last two merges.

So I've added a second line of text to the entry that only had one, and I've added this entry as well.

## Test 2

Test

Test text

## Test 1

Test text

Test test test

## Write-Only Memory

New feature

We've added Write-Only Memory (WOM) to all servers. WOM is used to store data that you are required to archive, but will never actually need to access again. 

## O7 November 2023 part 2

Test

Updating `markdown_to_rss.py` script because it inserted the first `<item>` before the `<atom:link>`.

## 07 November 2023

Test

Testing to see if the workflow is triggered and runs successfully when I update this file.

First attempt failed on `pip install -r requirements`. That command is missing the file extension (the file is `requirements.txt`, not `requirements`). Trying again.

Second attempt, the workflow completed without error, but didn't update `test_rss_feed.xml`. Trying to add `git push` to the workflow.

Third attempt, looks like a permissions issue on the `git push`. Trying to give the workflow write permissions.

## 03 November 2023

Alpha

Lorem ipsum dolor sit amet! Consectetur adipiscing elit!

* Sed do eiusmod tempor incididunt ut labore, et
* dolore magna aliqua

### Ut enim ad minim veniam

1. quis nostrud exercitation ullamco
2. laboris nisi ut aliquip ex ea commodo consequat

Duis aute irure dolor in `reprehenderit` in voluptate velit. [Esse cillum dolore](https://example.com) eu fugiat nulla pariatur.

## 01 November 2023

Fix

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.

Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

## 31 October 2023

New, Beta

Lorem ipsum [dolor sit amet](https://example.com), consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua: 

* ut enim ad minim veniam 
* quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat

## 18 October 2023

Improved

Duis aute irure dolor in `reprehenderit in voluptate` velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
