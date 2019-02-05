#!/usr/bin/env bash
# This script resizes all the images it finds in a folder (and its subfolders) and resizes them
# The resized image is placed in the /resized folder which will reside in the same directory as the image
#
# Usage: > ./batch_resize.sh

initial_folder="prints" # You can use "." to target the folder in which you are running the script for example
resized_folder_name="resized"

all_images=$(find -E ${initial_folder} -iregex ".*\.(jpg|gif|png|jpeg)")

while read -r image_full_path; do
    filename=$(basename "$image_full_path");
    source_folder=$(dirname "$image_full_path");
    destination_folder=${source_folder}"/"${resized_folder_name}"/";
    destination_full_path=${destination_folder}${filename};

    if [[ ! -z "$image_full_path" && "$image_full_path" != " " ]] &&
        # Do not resize images inside a folder that was already resized
        [[ "$(basename "$source_folder")" != "$resized_folder_name" ]]; then

        mkdir "$destination_folder";
        # If you are not using this in an OSX system, you can use imagemagick's "convert" command instead (http://www.imagemagick.org/script/convert.php)
        sips -Z 640 "$image_full_path" --out "$destination_full_path";

    fi

done <<< "$all_images"

