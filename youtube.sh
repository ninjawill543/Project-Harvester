#!/bin/bash
API_KEY=$(cat key.txt)



video_save=""
while true
do
    curl_output=$(curl -G -s "https://www.googleapis.com/youtube/v3/search" \
        -d channelId="UCOeYVWZgw08tDMqm7Fk4Wvw" \
        -d key="$API_KEY" \
        -d part="snippet" \
        -d order="date")
    newest_video_url=$(echo "$curl_output" | jq -r '.items | sort_by(.snippet.publishedAt) | last | .snippet.thumbnails.high.url')
    if [[ $newest_video_url == $video_save ]]
    then
        echo "Newest video already seen"
    else
        echo "New video thumbnail: $newest_video_url"
        wget -O "$(dirname "$(readlink -f "$0")")/command.jpg" $newest_video_url
        echo "Command is: " && zbarimg --quiet "$(dirname "$(readlink -f "$0")")/command.jpg" | cut -c 9-
        video_save=$newest_video_url
    fi
    sleep 10
done