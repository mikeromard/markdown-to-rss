#! /usr/bin/python3

import markdown
from markdown.treeprocessors import etree
import re
import datetime

timestamp = datetime.datetime.now().strftime(f"%a, %d %b %Y %H:%M:%S GMT") #cheated for PoC by adding GMT so that this looks like a valid RFC-822 date-time https://validator.w3.org/feed/docs/error/InvalidRFC2822Date.html

with open("test_product_updates.md", "r") as md_file:
    md_text = md_file.read()
    
xml_out = f"<rss>{markdown.markdown(md_text)}</rss>" #convert the md to HTML and wrap in <rss> element

items = re.findall("(<h2>[\S \n]*?)(?=\n<h2|<\/rss)",xml_out) #this finds all <item> elements

#update test_rss_feed.xml
rss_out_tree = etree.parse("test_rss_feed.xml")
rss_out_root = rss_out_tree.getroot()
for pubDate in rss_out_root.findall("./channel/pubDate"): #update the timestamp for the feed
    pubDate.text = str(timestamp)
with open("test_rss_feed.xml","r") as rss_feed_file:
    rss_feed_text = rss_feed_file.read()
for item in items: 
    item = f"<item>{item}</item>" 
    item_tree = etree.fromstring(item)
    item_tree[0].tag = "title"
    item_tree[1].tag = "category"
    if str(item_tree[0].text) in rss_feed_text: # if an item with the same title as this item is already in the output file, do nothing
        pass #would be nice to update the content of item if it differs though... maybe get item's current position, extract original pubDate, and reoutput to that position with original pubDate? 
    else: #if the item is not in the output file, add it as the first <item> in <channel> after <pubDate>. 
        item_out = "<item></item>"
        item_out_tree = etree.fromstring(item_out)
        item_title = etree.Element("title")
        item_out_tree.insert(0,item_title)
        item_title.text = item_tree[0].text
        item_category = etree.Element("category")
        item_out_tree.insert(1,item_category)
        item_category.text = item_tree[1].text
        item_pubDate = etree.Element("pubDate")
        item_out_tree.insert(2, item_pubDate)
        item_pubDate.text = str(f"{timestamp}") #update the timestamp for the item
        item_link = etree.Element("link")
        item_out_tree.insert(3, item_link)
        item_link.text = f"https://github.com/mikeromard/markdown-to-rss/blob/main/test_product_updates.md#{str(item_title.text).replace(' ', '-')}"
        item_guid = etree.Element("guid")
        item_out_tree.insert(4, item_guid)
        item_guid.text = f"https://github.com/mikeromard/markdown-to-rss/blob/main/test_product_updates.md#{str(item_title.text).replace(' ', '-')}"
        for title in item_tree.findall("title"):
            item_tree.remove(title)
        for category in item_tree.findall("category"):
            item_tree.remove(category)
        item_description = etree.Element("description")
        item_out_tree.insert(4, item_description)
        item_out_string = etree.tostring(item_tree, encoding="unicode").replace("<item>","").replace("</item>","")
        item_description.text = f"{item_out_string}" 
        rss_out_root[0].insert(6,item_out_tree) # insert(6 <-- update this number if any more elements are added before the first <item>
etree.indent(rss_out_tree, space="\t") #this is what makes the output pretty
rss_out_tree.write("test_rss_feed.xml") 
