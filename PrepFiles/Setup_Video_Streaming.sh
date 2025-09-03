#!/usr/bin/env bash


# taken from https://github.com/UmakantKulkarni/multipath-routing/blob/main/ExpJan/ecmp/src/medias.sh
# updated by sripath

# checking for arguments
DIR="../data/video_streaming/"
# convert DIR to absolute path
DIR="$(cd "$(dirname "$DIR")" && pwd)/$(basename "$DIR")"


[ -d "$DIR" ] || {
  printf 'Directory not found: %s\n' "$DIR"
  exit 1
}

printf 'Working directory: %s\n' "$DIR"
cd "$DIR"


ffmpeg -i big_buck_bunny_streaming.mp4 -c copy -f flv big_buck_bunny_reference.mp4
ffmpeg -i ed_streaming.mp4 -c copy -f flv ed_streaming_reference.mp4

mkdir -p adaptive
cd $DIR/adaptive
ffmpeg -y -copyts -start_at_zero -noaccurate_seek -i $DIR/big_buck_bunny_streaming.mp4 \
    -keyint_min 48 -g 48 -frag_duration 0.4 -sc_threshold 0 -c:v libx264 \
    -profile:v main -crf 20 -c:a aac -ar 48000 -f dash -dash_segment_type mp4 \
    -map v:0 -movflags frag_keyframe -s:0 426x240 \
    -map v:0 -movflags frag_keyframe -s:1 640x360 \
    -map v:0 -movflags frag_keyframe -s:2 854x480 \
    -map v:0 -movflags frag_keyframe -s:3 1024x600 \
    -map v:0 -movflags frag_keyframe -s:4 1280x720 \
    -map v:0 -movflags frag_keyframe -s:5 1600x900 \
    -map v:0 -movflags frag_keyframe -s:6 1920x1080 \
    -map 0:a \
    -init_seg_name chunk\$RepresentationID\$-index.mp4 -media_seg_name chunk\$RepresentationID\$-\$Number%05d\$bb.mp4 \
    -use_template 0 -use_timeline 0 \
    -seg_duration 4 -adaptation_sets "id=0,streams=v id=1,streams=a" \
    big_buck_bunny.mpd

ffmpeg -y -copyts -start_at_zero -noaccurate_seek -i $DIR/ed_streaming.mp4 \
    -keyint_min 48 -g 48 -frag_duration 0.4 -sc_threshold 0 -c:v libx264 \
    -profile:v main -crf 20 -c:a aac -ar 48000 -f dash -dash_segment_type mp4 \
    -map v:0 -movflags frag_keyframe -s:0 426x240 \
    -map v:0 -movflags frag_keyframe -s:1 640x360 \
    -map v:0 -movflags frag_keyframe -s:2 854x480 \
    -map v:0 -movflags frag_keyframe -s:3 1024x600 \
    -map v:0 -movflags frag_keyframe -s:4 1280x720 \
    -map v:0 -movflags frag_keyframe -s:5 1600x900 \
    -map v:0 -movflags frag_keyframe -s:6 1920x1080 \
    -map 0:a \
    -init_seg_name chunk\$RepresentationID\$-index.mp4 -media_seg_name chunk\$RepresentationID\$-\$Number%05d\$ed.mp4 \
    -use_template 0 -use_timeline 0 \
    -seg_duration 4 -adaptation_sets "id=0,streams=v id=1,streams=a" \
    ed.mpd