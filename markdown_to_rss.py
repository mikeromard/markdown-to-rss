#! /usr/bin/python3

import markdown
from markdown.treeprocessors import etree
import re
import datetime

timestamp = datetime.datetime.now().strftime("%d %b, %Y %H:%M")

with open("test_product_updates.md", "r") as md_file:
    md_text = md_file.read()
    
xml_out = f"<rss>{markdown.markdown(md_text)}</rss>"

items = re.findall("(<h2>[\S \n]*?)(?=\n<h2|<\/rss)",xml_out)

#rewrite test_feed.xml - this section can be dropped, aside from the for loop, which will be needed in the next section
with open("test_feed.xml","w",encoding="utf-8") as rss_file_out:
    rss_file_out.write('<rss version="2.0" encoding="utf-8">\n')
    rss_file_out.write("\t<channel>\n")
    rss_file_out.write("\t\t<title>Test changelog</title>\n")
    rss_file_out.write("\t\t<link>example.com</link>\n")
    rss_file_out.write("\t\t<description>Testing a markdown to RSS script.</description>\n")
    rss_file_out.write("\t\t<language>en-us</language>\n")
    rss_file_out.write(f"\t\t<pubDate>{timestamp}</pubDate>\n")
    for item in items:
        item = f"<item>\n{item}\n</item>"
        item_tree = etree.fromstring(item)
        item_tree[0].tag = "title"
        item_tree[1].tag = "category"
        pubDate = etree.Element("pubDate")
        item_tree.insert(2, pubDate)
        pubDate.text = str(f"{timestamp}")
        rss_file_out.write(f'\t\t{etree.tostring(item_tree, encoding="unicode")}\n')
    rss_file_out.write("\t</channel>\n")
    rss_file_out.write("</rss>")

#update test_rss_feed.xml
rss_out_tree = etree.parse("test_rss_feed.xml")
rss_out_root = rss_out_tree.getroot()
for pubDate in rss_out_root.findall("./channel/pubDate"):
    pubDate.text = str(timestamp)
rss_out_tree.write("test_rss_feed.xml") 
with open("test_rss_feed.xml","r") as rss_feed_file:
    rss_feed_text = rss_feed_file.read()
#print(rss_feed_text)
for item in items:
    item = f"<item>{item}</item>"
    item_tree = etree.fromstring(item)
    item_tree[0].tag = "title"
    item_tree[1].tag = "category"
    pubDate = etree.Element("pubDate")
    item_tree.insert(2, pubDate)
    pubDate.text = str(f"{timestamp}")
    if str(item_tree[0].text) in rss_feed_text: #this one seems to be working
        pass
    else:
        new_item = etree.Element("item")
        rss_out_root[0].insert(5,new_item) #inserting empty <item> in the right place! need to figure out how to add content
rss_out_tree.write("test_rss_feed.xml") 
