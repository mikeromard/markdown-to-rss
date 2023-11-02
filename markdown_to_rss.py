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

#rewrite test_feed.xml
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
        rss_file_out.write(f'\t\t{etree.tostring(item_tree, encoding="unicode")}\n')
    rss_file_out.write("\t</channel>\n")
    rss_file_out.write("</rss>")

#update test_rss_feed.xml
rss_out_tree = etree.parse("test_rss_feed.xml")
rss_out_root = rss_out_tree.getroot()
for pubDate in rss_out_root.findall("./channel/pubDate"):
    pubDate.text = str(timestamp)
rss_out_tree.write("test_rss_feed.xml") 
