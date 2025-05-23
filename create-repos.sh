#!/bin/bash

# Function to create a clean git repository
create_clean_repo() {
    mkdir "$1"
    cd "$1" || exit
    git init
    touch README.md
    git add README.md
    git commit -m "Initial commit"
    cd ..
}

# Function to create a git repository with untracked files
create_untracked_repo() {
    mkdir "$1"
    cd "$1" || exit
    git init
    touch README.md
    cd ..
}

# Function to create a git repository with modified files
create_modified_repo() {
    mkdir "$1"
    cd "$1" || exit
    git init
    touch README.md
    git add README.md
    git commit -m "Initial commit"
    echo "Some changes" > README.md
    cd ..
}

# Function to create a git repository with staged changes
create_staged_repo() {
    mkdir "$1"
    cd "$1" || exit
    git init
    touch README.md
    git add README.md
    git commit -m "Initial commit"
    echo "Some changes" > README.md
    git add README.md
    cd ..
}

# Function to create a git repository with unmerged paths
create_unmerged_repo() {
    mkdir "$1"
    cd "$1" || exit
    git init
    touch README.md
    git add README.md
    git commit -m "Initial commit"
    git checkout -b feature
    echo "Feature changes" > README.md
    git add README.md
    git commit -m "Feature commit"
    git checkout main
    echo "Main changes" > README.md
    git add README.md
    git commit -m "Main commit"
    git merge feature || true
    cd ..
}

# Function to create a git repository ahead of remote
create_ahead_repo() {
    git clone https://github.com/jlopezr/docker-ffmpeg-hw.git "$1"
    cd "$1" || exit
    touch TOUCHED.md
    git add TOUCHED.md
    git commit -m "TOUCHED"    
    cd ..
}

# Function to create a git repository behind remote
create_behind_repo() {
    git clone https://github.com/jlopezr/docker-ffmpeg-hw.git "$1"
    cd "$1" || exit
    # Remove the next commit from the history
    git reset --hard HEAD~1
    cd ..
}

# Function to create a git repository that has diverged
create_diverged_repo() {
    git clone https://github.com/jlopezr/docker-ffmpeg-hw.git "$1"
    cd "$1" || exit
    # Remove the next commit from the history
    git reset --hard HEAD~1
    touch TOUCHED.md
    git add TOUCHED.md
    git commit -m "TOUCHED"    
    cd ..
}

# Main script
# create_clean_repo "Clean"
# create_untracked_repo "Untracked_Files"
# create_modified_repo "Modified_Files"
# create_staged_repo "Staged_Changes"
create_unmerged_repo "Unmerged_Paths"
# create_ahead_repo "Ahead_of_Remote"
# create_behind_repo "Behind_Remote"
# create_diverged_repo "Diverged"

# echo ""
# echo ""
# echo "Repositories created with the following statuses:"
# echo "1. Clean"
# echo "2. Untracked Files"
# echo "3. Modified Files"
# echo "4. Staged Changes"
# echo "5. Unmerged Paths"
# echo "6. Ahead of Remote"
# echo "7. Behind Remote"
# echo "8. Diverged"