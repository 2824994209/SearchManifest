#!/bin/bash

# Traverse all subdirectories in the current directory
for dir in */ ; do
    if [ -d "$dir" ]; then
        # Check for subdirectories within this directory
        if find "$dir" -mindepth 1 -type d | read; then
            echo "Subdirectory with nested directories: $dir"
	        rm -rf $dir
        fi
    fi
done

echo "Review the directories listed above that contain further subdirectories."

