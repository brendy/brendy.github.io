''' Updates the staging repo from the main development site'''

import shutil
import os
from sys import exit
from os.path import getmtime # modification time

reeborg_age = getmtime("../reeborg/reeborg.html")
build_age = getmtime("../reeborg/build/reeborg.js")
reeborg_offline_age = getmtime("../reeborg/reeborg_offline.html")

if (reeborg_age > reeborg_offline_age) or (build_age - reeborg_offline_age > 60):
    print("Offline version too old; need to run make in main repo.")
    print("reeborg_age:", reeborg_age)
    print("reeborg_offline_age", reeborg_offline_age, reeborg_offline_age-reeborg_age)
    print("build_age", build_age, build_age-reeborg_offline_age)
    exit()

#===========================
# IMPORTANT: a file named .nojekyll must be in the staging repository
# This file can be empty.
#===========================

# Everything is going to be served from the github site; we
# thus use the offline version (which includes all relevant libraries
# in the repository instead of using CDN versions) and rename it so
# that it is recognized as the default page by Github Pages.
shutil.copy2("../reeborg/reeborg_offline.html", "index.html")

# other single main file
shutil.copy2("../reeborg/build/reeborg.js", "build/reeborg.js")

# We use shutil to copy entire directories.
# However, shutil.copytree requires that no such directory exist already;
# so, we start by removing the old one with the same nome,
# not worrying if it did not exists before

def update_dir(name):
    reeborg = "../reeborg/"
    print("Updating directory", name)
    try:
        shutil.rmtree(name)
    except FileNotFoundError:
        print("Warning:", name, "could not be found and removed")

    try:
        shutil.copytree(reeborg + name, name)
    except FileExistsError:
        print("Error:", name, "already exists and could not be copied.")

update_dir("offline/")
update_dir("src/blockly/")
update_dir("src/blockly_msg/")
update_dir("src/css/")
update_dir("src/images/")
update_dir("src/libraries/")
update_dir("src/python/")
update_dir("src/sounds/")
update_dir("worlds/")

os.system('git add *')
os.system('git commit -m "automatic update"')
os.system('git push')
