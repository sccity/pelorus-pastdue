withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
    sh '''
    commit_hash=$(cat commit_hash.txt)
    branch=$(cat branch.txt)

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

    ./kubectl --kubeconfig $KUBECONFIG set image deployment/$DEPLOYMENT pelorus-pastdue=sccity/pelorus-pastdue:$commit_hash -n ancillary-services

    if [ $? -ne 0 ]; then
        echo "Error: Kubernetes update failed!"
        exit 1
    fi

    ./kubectl --kubeconfig $KUBECONFIG rollout status deployment/$DEPLOYMENT -n ancillary-services

    if [ $? -ne 0 ]; then
        echo "Error: Kubernetes rollout failed!"
        exit 1
    fi
    '''
}