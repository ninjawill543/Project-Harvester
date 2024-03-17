#!/bin/bash
API_KEY=$(cat key.txt)

video_save=""
while true
do
    curl_output=$(curl -G -s "https://www.googleapis.com/youtube/v3/search" \
        -d channelId="UCLVMKLtleeiKs0Oqp86ApTQ" \
        -d key="$API_KEY" \
        -d part="snippet" \
        -d order="date")
    newest_video_url=$(echo "$curl_output" | jq -r '.items | sort_by(.snippet.publishedAt) | last | .snippet.thumbnails.high.url')
    if [[ $newest_video_url == $video_sav ]]
    then
        echo "Newest video already seen"
    else
        echo "New video thumbnai: $newest_video_url"
        video_save=$newest_video_url
    fi
    sleep 10
done