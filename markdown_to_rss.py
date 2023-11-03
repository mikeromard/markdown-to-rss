#! /usr/bin/python3

import markdown
from markdown.treeprocessors import etree
import re
import datetime

timestamp = datetime.datetime.now().strftime("%d %b, %Y %H:%M")

with open("test_product_updates.md", "r") as md_file:
    md_text = md_file.read()
    
xml_out = f"<rss>{markdown.markdown(md_text)}</rss>" #convert the md to HTML and wrap in <rss> element

items = re.findall("(<h2>[\S \n]*?)(?=\n<h2|<\/rss)",xml_out) #this finds all <item> elements

#update test_rss_feed.xml
rss_out_tree = etree.parse("test_rss_feed.xml")
rss_out_root = rss_out_tree.getroot()
for pubDate in rss_out_root.findall("./channel/pubDate"): #update the timestamp for the feed
    pubDate.text = str(timestamp)
#rss_out_tree.write("test_rss_feed.xml") 
with open("test_rss_feed.xml","r") as rss_feed_file:
    rss_feed_text = rss_feed_file.read()
for item in items:
    item = f"<item>{item}</item>"
    item_tree = etree.fromstring(item)
    item_tree[0].tag = "title"
    item_tree[1].tag = "category"
    pubDate = etree.Element("pubDate")
    item_tree.insert(2, pubDate)
    pubDate.text = str(f"{timestamp}") #update the timestamp for the item
    if str(item_tree[0].text) in rss_feed_text: # if an item with the same title as this item is already in the output file, do nothing
        pass #would be nice to update the content of item if it differs though... maybe get item's current position, extract original pubDate, and reoutput to that position with original pubDate? 
    else: #if the item is not in the output file, add it as the first <item> in <channel> after <pubDate>
        rss_out_root[0].insert(5,item_tree) 
etree.indent(rss_out_tree, space="\t") #this is what makes the output pretty
rss_out_tree.write("test_rss_feed.xml") 
