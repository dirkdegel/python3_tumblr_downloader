import os, sys
from shutil import copyfileobj
from urllib.request import urlopen
from xml.etree import ElementTree as ET

tumblr_name = "enter_the_mane_of_the_tumblr"
api_endpoint = 'http://%s.tumblr.com/api/read' % tumblr_name
start = 0
num = 50
post_count = 1

while post_count:
    resp = urlopen("%s?type=photo&start=%s&num=%s" % (api_endpoint, start, num))
    content = resp.read()
    tree = ET.fromstring(content)
    post_tags = tree.findall(".//post")
    post_count = len(post_tags)
    for post_tag in post_tags:
        post_id = post_tag.attrib['id']
        post_date = post_tag.attrib['date-gmt'].split(" ")[0]
        outname = "%s-%s-%s.jpeg" % (tumblr_name, post_date, post_id)
        if os.path.exists(outname):
            print("%s already downloaded" % outname)
            continue
        for photo_tag in post_tag.findall(".//photo-url"):
            if photo_tag.attrib['max-width'] == "1280":
                photo_url = photo_tag.text
                resp = urlopen(photo_url)
                outfile = open(outname, 'wb')
                copyfileobj(resp, outfile)
                outfile.close()
                print("Downloaded %s to %s" % (photo_url, outname))
    start += num
