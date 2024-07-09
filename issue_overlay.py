from iiif_prezi3 import Manifest, config
from PIL import Image, ImageDraw
import requests
import pprint
import json
import re

#THIS IS PARTICULAR TO THE INTERNET ARCHIVE FORMAT

#get the viral texts data for a single issue
issue_url = 'https://es.viral-texts.software.ncsa.illinois.edu/viral-texts-test/_search?size=100&q=issue:sim_manifesto_1878-05_8_5%20AND%20day:1878-05-01'
username = 'elastic'
password = '1%Zlbf7936cDGgK4'
issue_json = requests.get(issue_url, auth=(username, password)).json()

#archive.org manifest for the issue in question
manifest_url = 'https://iiif.archive.org/iiif/3/sim_manifesto_1878-05_8_5/manifest.json'

response = requests.get(manifest_url)

data_dict = {}

#add page to canvas
def add_to_canvas(canvas_page):
	manifest.make_canvas_from_iiif(url=canvas_page,
                                         id=canvas_page,
                                         label="Shaker",
                                         anno_id=canvas_page,
                                         anno_page_id=canvas_page)
#add annotation to canvas
def add_ann_to_page(page):
    page.make_annotation(id=page,
                                  motivation="tagging",
                                  body={"type": "TextualBody",
                                        "language": "en",
                                        "format": "text/plain",
                                        "value": "Here is another annotation"},
                                  target=page.id + "#xywh=265,661,1260,1239",
                                  anno_page_id=page)


if response.status_code == 200:
    manifest_data = response.json()
    children = manifest_data.get('sequences', [])
    for child in children:
        items = child.get('items')
        height = []
        width = []
        for item in items:
            height.append(canvas.get("height"))
            width.append(canvas.get("width"))
        width = max(width)
        height = max(height)

            
config.configs['helpers.auto_fields.AutoLang'].auto_lang = "en"

manifest = Manifest(id="https://iiif.archive.org/iiif/3/sim_manifesto_1878-05_8_5/manifest.json",
                    label={"en": ["Shaker blah blah"]},
                    behavior=["paged"])

#populate the data dict
for id_num, child in enumerate(manifest_data["items"]):
	canvas_page = child["items"][0]["items"][0]["body"]["service"][0]["id"]
	data_dict[id_num] = {}
	data_dict[id_num]["canvas_page"] = canvas_page
	data_dict[id_num]["annotations"] = []


#add annotations to dict using the issue json
for cluster_annotation in issue_json["hits"]["hits"]:
	if cluster_annotation["_source"]["issue"] == "sim_manifesto_1878-05_8_5":
		archive_url = cluster_annotation["_source"]["url"]
		page_num = re.search(r"https:\/\/archive\.org\/details\/.*\/page\/n([0-9]*)\/mode", archive_url).group(1)
		data_dict[int(page_num)]["annotations"].append({"_id": cluster_annotation["_id"], "cluster": cluster_annotation["_source"]["cluster"], "image_data": cluster_annotation["_source"]["page_image"]})


#dict containing the page manifests
page_dict = {}

for page in data_dict:
    page_dict[page] = add_to_canvas(data_dict[page]["canvas_page"])

#TODO: add annotations to canvases



print(manifest.json(indent=2))
