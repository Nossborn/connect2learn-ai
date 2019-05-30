#!/bin/bash

srcdir="./"
destdir="./"
reopt="^-"
redocstart="^<doc"
redocend="^</doc"
while [[ "$1" =~ $reopt && ! "$1" == "--" ]]; do case "$1" in
    -s | --srcdir )
        shift; srcdir="$1"
        ;;
    -d | --destdir )
        shift; destdir="$1"
        ;;
    * )
        echo "Usage: $0 [-s|--srcdir PATH] [-d|--destdir PATH] [-h|--help]"
        exit
esac; shift; done
if [[ "$1" == "--" ]]; then shift; fi

if [[ ! -e "$srcdir" ]]; then
    echo "Directory $srcdir doesnt exist"
    exit
fi

[[ -e "$destdir" ]] || mkdir -p "$destdir"

i=0
for f in $srcdir/*; do
    [[ -e "$f" ]] || continue
    while read -r line || [[ -n "$line" ]]; do
        if [[ "$line" =~ $redocstart ]]; then
            OUT="$destdir/wiki_${i}"
            echo "$OUT"
            s=""
            continue
        fi
        if [[ "$line" =~ $redocend ]]; then
            echo "$s" >"$OUT" && ((++i)) && continue
        fi
        s+="$line" && s+=$'\n'
    done <"$f"
done