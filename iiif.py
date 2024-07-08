from iiif_prezi3 import Manifest, config
import json, requests

url = 'https://www.loc.gov/item/sn96061150/1889-10-20/ed-1/manifest.json'

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    children = data.get('sequences', [])
    for child in children:
        canvases = child.get('canvases')
        height = []
        width = []
        for canvas in canvases:
            height.append(canvas.get("height"))
            width.append(canvas.get("width"))
        width = max(width)
        height = max(height)

            
config.configs['helpers.auto_fields.AutoLang'].auto_lang = "en"

manifest = Manifest(id="https://iiif.io/api/cookbook/recipe/0021-tagging/manifest.json",
                    label={"en": ["The daily morning Astorian. [volume], October 20, 1889"]},
                    behavior=["paged"])

canvas1 = manifest.make_canvas_from_iiif(url="https://tile.loc.gov/image-services/iiif/service:ndnp:oru:batch_oru_hufnagel_ver02:data:sn96061150:00200298111:1889102001:0368",
                                         id="https://iiif.io/api/cookbook/recipe/0009-book-1/canvas/p1",
                                         label="The daily morning Astorian. [volume], October 20, 1889",
                                         anno_id="https://iiif.io/api/cookbook/recipe/0009-book-1/annotation/p0001-image",
                                         anno_page_id="https://iiif.io/api/cookbook/recipe/0009-book-1/page/p1/1")


canvas2 = manifest.make_canvas_from_iiif(url="https://tile.loc.gov/image-services/iiif/service:ndnp:oru:batch_oru_hufnagel_ver02:data:sn96061150:00200298111:1889102001:0369",
                                         id="https://iiif.io/api/cookbook/recipe/0009-book-1/canvas/p2",
                                         label="The daily morning Astorian. [volume], October 20, 1889",
                                         anno_id="https://iiif.io/api/cookbook/recipe/0009-book-1/annotation/p0002-image",
                                         anno_page_id="https://iiif.io/api/cookbook/recipe/0009-book-1/page/p2/1")

anno2 = canvas2.make_annotation(id="https://iiif.io/api/cookbook/recipe/0021-tagging/annotation/p0003-tag",
                              motivation="tagging",
                              body={"type": "TextualBody",
                                    "language": "en",
                                    "format": "text/plain",
                                    "value": "Here is another annotation"},
                              target=canvas2.id + "#xywh=265,661,1260,1239",
                              anno_page_id="https://www.loc.gov/resource/sn96061150/1889-10-20/ed-1/seq-2/")

canvas3 = manifest.make_canvas_from_iiif(url="https://tile.loc.gov/image-services/iiif/service:ndnp:oru:batch_oru_hufnagel_ver02:data:sn96061150:00200298111:1889102001:0370",
                                         id="http://127.0.0.1:9200/search/_doc/SZL_J5ABBoOnO3giCKwt",
                                         label="The daily morning Astorian. [volume], October 20, 1889",
                                         anno_page_id="https://www.loc.gov/resource/sn96061150/1889-10-20/ed-1/seq-3/")

anno1 = canvas3.make_annotation(id="https://www.loc.gov/resource/sn96061150/1889-10-20/ed-1/seq-3/p0002-tag",
                              motivation="commenting",
                              body={"type": "TextualBody",
                                    "language": "en",
                                    "format": "text/html",
                                    "value": "<p>Here is a sample annotation that can link back to a stable url<a href='https://de.wikipedia.org/wiki/G%C3%A4nseliesel-Brunnen_(G%C3%B6ttingen)'>Gänseliesel Brunnen <img src='https://en.wikipedia.org/static/images/project-logos/enwiki.png' alt='Wikipedia logo'></a></p>"},
                              target=canvas3.id + "#xywh=265,661,1260,1239",
                              anno_page_id="https://www.loc.gov/resource/sn96061150/1889-10-20/ed-1/seq-3/")

anno2 = canvas3.make_annotation(id="https://www.loc.gov/resource/sn96061150/1889-10-20/ed-1/seq-3/p0003-tag",
                              motivation="commenting",
                              body={"type": "TextualBody",
                                    "language": "en",
                                    "format": "text/plain",
                                    "value": "Here is another sample annotation that can link back to a stable <a href=nothing> url</a>"},
                              target=canvas3.id + "#xywh=2665,1861,160,439",
                              anno_page_id="https://www.loc.gov/resource/sn96061150/1889-10-20/ed-1/seq-3/")



canvas4 = manifest.make_canvas_from_iiif(url="https://tile.loc.gov/image-services/iiif/service:ndnp:oru:batch_oru_hufnagel_ver02:data:sn96061150:00200298111:1889102001:0371",
                                         id="https://iiif.io/api/cookbook/recipe/0009-book-1/canvas/p4",
                                         label="Blank page",
                                         anno_id="https://iiif.io/api/cookbook/recipe/0009-book-1/annotation/p0004-image",
                                         anno_page_id="https://iiif.io/api/cookbook/recipe/0009-book-1/page/p4/1")

# # canvas5 = manifest.make_canvas_from_iiif(url="https://iiif.io/api/image/3.0/example/reference/59d09e6773341f28ea166e9f3c1e674f-gallica_ark_12148_bpt6k1526005v_f22",
# #                                          id="https://iiif.io/api/cookbook/recipe/0009-book-1/canvas/p5",
# #                                          label="Bookplate",
# #                                          anno_id="https://iiif.io/api/cookbook/recipe/0009-book-1/annotation/p0005-image",
# #                                          anno_page_id="https://iiif.io/api/cookbook/recipe/0009-book-1/page/p5/1")

print(manifest.json(indent=2))
