withCredentials([usernamePassword(credentialsId: 'docker-hub', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
    sh '''
    commit_hash=$(cat commit_hash.txt)
    branch=$(cat branch.txt)

    if [ -z "$commit_hash" ]; then
        echo "Error: Commit hash file is missing!"
        exit 1
    fi

    echo "Using Commit Hash: $commit_hash for Docker build"
    echo "$DOCKER_PASSWORD" | docker login -u "$DOCKER_USERNAME" --password-stdin

    docker build --platform linux/x86_64 -t sccity/pelorus-pastdue:$commit_hash --push .

    if [ $? -ne 0 ]; then
        echo "Error: Docker latest tag push failed!"
        exit 1
    fi
    '''
}