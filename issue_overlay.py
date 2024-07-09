from unittest import result

from iiif_prezi3 import Manifest, config
from PIL import Image, ImageDraw
import requests
import pprint
import json
import re
import os
from dotenv import load_dotenv
import argparse
# THIS IS PARTICULAR TO THE INTERNET ARCHIVE FORMAT

#CLI stuff
parser = argparse.ArgumentParser()
parser.add_argument("-mu", "--manifest_url", help="The manifest of an issue e.g. https://iiif.archive.org/iiif/3/sim_manifesto_1878-05_8_5/manifest.json")
parser.add_argument("-su", "--search_url", help="The url of a Viral Texts elastic search query e.g. https://es.viral-texts.software.ncsa.illinois.edu/viral-texts-test/_search?size=100&q=issue:sim_manifesto_1878-05_8_5%20AND%20day:1878-05-01")

args = parser.parse_args()

issue_url = args.search_url
manifest_url = args.manifest_url


load_dotenv()
# get the viral texts data for a single issue
#issue_url = "https://es.viral-texts.software.ncsa.illinois.edu/viral-texts-test/_search?size=100&q=issue:sim_manifesto_1878-05_8_5%20AND%20day:1878-05-01"

password = os.environ.get("password")
username = os.environ.get("username")

issue_json = requests.get(issue_url, auth=(username, password)).json()

# archive.org manifest for the issue in question
#manifest_url = "https://iiif.archive.org/iiif/3/sim_manifesto_1878-05_8_5/manifest.json"

response = requests.get(manifest_url)

data_dict = {}

CANVAS_WIDTH = 0
CANVAS_HEIGHT = 0


# add page to canvas
def add_to_canvas(page, canvas_page):
    page_dict[page] = manifest.make_canvas_from_iiif(
        url=canvas_page,
        id=canvas_page,
        label="Shaker",
        anno_id=canvas_page,
        anno_page_id=canvas_page,
    )


def pct_string_to_xywh(url):
    regex_pattern = "https://iiif.archive.org/iiif/.*/pct:(.*),(.*),(.*),(.*)/full"
    results = re.search(regex_pattern, url)
    pct_x, pct_y, pct_w, pct_h = (
        results.group(1),
        results.group(2),
        results.group(3),
        results.group(4),
    )

    p_x = round(float(pct_x) * 0.01 * CANVAS_WIDTH)
    p_y = round(float(pct_y) * 0.01 * CANVAS_HEIGHT)
    p_w = round(float(pct_w) * 0.01 * CANVAS_WIDTH)
    p_h = round(float(pct_h) * 0.01 * CANVAS_HEIGHT)

    return "xywh=" + str(p_x) + "," + str(p_y) + "," + str(p_w) + "," + str(p_h)


# add annotation to canvas
def add_ann_to_page(page, cluster_id, url):
    xywh_string = pct_string_to_xywh(url)
    value_string = "<p><a href='https://orca-app-ibxg3.ondigitalocean.app/cluster/" + str(cluster_id) + "'>See cluster: " + str(cluster_id) + "</a></p>"
    page.make_annotation(
        id=url,
        motivation="commenting",
        body={
            "type": "TextualBody",
            "language": "en",
            "format": "text/html",
            "value": value_string,
        },
        target=page.id + "#" + xywh_string,
        anno_page_id=url,
    )

#get the manifest data
if response.status_code == 200:
    manifest_data = response.json()
    children = manifest_data.get("sequences", [])
    for child in children:
        items = child.get("items")
        height = []
        width = []
        for item in items:
            height.append(canvas.get("height"))
            width.append(canvas.get("width"))
        width = max(width)
        height = max(height)

CANVAS_WIDTH = manifest_data["items"][0]["width"]
CANVAS_HEIGHT = manifest_data["items"][0]["height"]



config.configs["helpers.auto_fields.AutoLang"].auto_lang = "en"

label_text = manifest_data["label"]["none"][0]

manifest = Manifest(
    id=manifest_url,
    label={"en": [label_text]},
    behavior=["paged"],
)

# populate the data dict
for id_num, child in enumerate(manifest_data["items"]):
    canvas_page = child["items"][0]["items"][0]["body"]["service"][0]["id"]
    data_dict[id_num] = {}
    data_dict[id_num]["canvas_page"] = canvas_page
    data_dict[id_num]["annotations"] = []


# add annotations to dict using the issue json
for cluster_annotation in issue_json["hits"]["hits"]:
    if cluster_annotation["_source"]["issue"] == "sim_manifesto_1878-05_8_5":
        archive_url = cluster_annotation["_source"]["url"]
        page_num = re.search(
            r"https:\/\/archive\.org\/details\/.*\/page\/n([0-9]*)\/mode", archive_url
        ).group(1)
        data_dict[int(page_num)]["annotations"].append(
            {
                "_id": cluster_annotation["_id"],
                "cluster": cluster_annotation["_source"]["cluster"],
                "image_data": cluster_annotation["_source"]["page_image"],
            }
        )


# dict containing the page manifests
page_dict = {}

for page in data_dict:
    add_to_canvas(page, data_dict[page]["canvas_page"])


for page in data_dict:
    for annotation in data_dict[page]["annotations"]:
        url = annotation["image_data"]
        coords = pct_string_to_xywh(url)

        pattern = r"\$(\d{1,3})"
        regex_page = re.search(pattern, url).group(1)
# TODO: add annotations to canvases


# for page in page_dict.keys():
#    page_dict[page].make_annotation(
#        id="https://iiif.io/api/cookbook/recipe/0021-tagging/annotation/p0003-tag",
#        motivation="tagging",
#        body={
#            "type": "TextualBody",
#            "language": "en",
#            "format": "text/plain",
#            "value": "Here is another annotation",
#        },
#        target=page_dict[page].id + "#xywh=265,661,1260,1239",
#        anno_page_id="https://www.loc.gov/resource/sn96061150/1889-10-20/ed-1/seq-2/",
#    )

for page in data_dict:
    for annotation in data_dict[page]["annotations"]:
        add_ann_to_page(page_dict[page], annotation["cluster"], annotation["image_data"])


# ann1 = add_ann_to_page(page_dict[0], "asdfasdfhljk", "https://iiif.archive.org/iiif/sim_manifesto_1878-05_8_5$20/pct:7.642726,13.902292,73.572744,76.145959/full/0/default.jpg")


with open("output.json", "w") as outfile:
    outfile.write(manifest.json(indent=2))
