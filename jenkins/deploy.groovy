withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
    sh '''
    commit_hash=$(cat commit_hash.txt)
    branch=$(cat branch.txt)

    namespace="ancillary-services"
    container="pelorus-pastdue"
    image="sccity/pelorus-pastdue"

    if [ "$branch" = "dev" ]; then
        exit 0
    elif [ "$branch" = "prod" ]; then
        DEPLOYMENT="pelorus-pastdue"
    else
        echo "Error: Unknown branch '$branch'. Skipping deployment."
        exit 1
    fi

    curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
    chmod +x kubectl

    ./kubectl get deployments -n $namespace

    ./kubectl -n $namespace \
        set image "deployment/$DEPLOYMENT" \
        "$container=$image:$commit_hash-$branch"

    if [ $? -ne 0 ]; then
        echo "Error: Kubernetes Update Failed!"
        exit 1
    fi

    ./kubectl -n $namespace \
        rollout status deployment/$DEPLOYMENT \
        -n $namespace

    if [ $? -ne 0 ]; then
        echo "Error: Kubernetes Rollout Failed!"
        exit 1
    fi
    '''
}