#!/bin/bash

# Function to run make command and kill child/grandchild processes
run_make_and_cleanup() {
    make run-controlled-pcap-collection

    # Kill all child/grandchild processes
    pkill -P $$ # $$ refers to the script's own process ID
}

# Run make command 2 times
for ((i=1; i<500; i++)); do
    echo "Running make command, iteration $i"
    run_make_and_cleanup
    mv ./*.pcap ../data/collected_dataset/
done

echo "All make commands completed."
