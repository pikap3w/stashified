# wget -r -nc -np -A png,jpg http://ju-ju-be-prints.com/

# go to myEnvironments folder
# source jjbDjangoPy3Env/bin/activate
# python manage.py shell
# exec(open("./utils/populate_database.py").read())

import os
import re

from apps.stash_happy.models import *

url_root = "https://s3.us-west-2.amazonaws.com/tkdk-jjb/img/prints"
path_root = "/Users/pikap3w/OneDrive/_Dojo/_Projects/Python_Project/main/apps/stashified/static/stashified/img/prints"

collections_ = [
    "Classic_",
    "Onyx_",
    "Ever_",
    "Coastal_",
    "Legacy_Earth_Leather_",
    "Legacy_",
    "Nautical_",
    "Rose_",
    "XY_",
    "Tokidoki_Hello_Kitty_",
    "Tokidoki_Sanrio_",
    "Tokidoki_",
    "Hello_Kitty_",
    "Sanrio_",
    "Blizzard_WoW_",
    "Cheerios_",
]

bags = []

for dirname in os.listdir(path_root):
    if (
            (dirname.find("preview") == -1)
            and (dirname.find("accessories") == -1)
            and (dirname.find("resized") == -1)
            and (not dirname.startswith("."))
    ):
        for name in os.listdir(os.path.join(path_root, dirname)):
            if (
                    (not name.startswith("_"))
                    and (name.find("preview") == -1)
                    and (name.find("resized") == -1)
                    and (not name.startswith("."))
            ):
                bag = {"URL": os.path.join(url_root, dirname, name),
                       "URL_resized": os.path.join(url_root, dirname, "resized", name)}
                col_print_style = name.replace(".jpg", "")
                col_print_style = col_print_style.replace(".JPG", "")
                # parse dirname for (collection, print,) & year
                yr_pos = re.search(r"\d\d\d\d", dirname).start()
                bag["Date"] = dirname[yr_pos:]
                col_print = dirname[: yr_pos - 1]
                style = col_print_style.replace(col_print + "_", "")
                # Remove parentheses from style field
                paren = "("
                idx = style.find(paren)
                if idx != -1:
                    style = style[:idx]
                style = style.replace("_", " ")
                bag["Style"] = style.rstrip()  # Remove trailing whitespace
                for collection in collections_:
                    if col_print.startswith(collection):
                        print_name = col_print.replace(collection, "", 1)
                        collection = collection.replace("_", " ")
                        bag["Collection"] = collection.rstrip()
                        bag["Print"] = print_name.replace("_", " ")
                        bags.append(dict(bag))

collections = []
for collection in collections_:
    collection = collection.replace("_", " ")
    collections.append(collection.rstrip())

# print(collections)
#
# for collection in collections:
#     Collection.objects.create(name=collection)

styles = []
for bag in bags:
    style = bag["Style"]
    if style not in styles:
        styles.append(style)
        styles.sort()

# for style in styles:
#     Style.objects.create(name=style)

print(styles)

prints = []
for bag in bags:
    print_ = {"Name": bag["Print"], "Date": bag["Date"], "Collection": bag["Collection"]}
    if print_ not in prints:
        prints.append(print_)

print(prints)

# for p in prints:
#     Print.objects.create(
#         name=p["Name"],
#         release_date=p["Date"],
#         collection_id=Collection.objects.get(name=p["Collection"]).id,
#     )

for bag in bags:
    Bag.objects.create(
        print_id=Print.objects.get(name=bag["Print"]).id,
        style_id=Style.objects.get(name=bag["Style"]).id,
        image=bag["URL"],
        image_resized=bag["URL_resized"],
    )
