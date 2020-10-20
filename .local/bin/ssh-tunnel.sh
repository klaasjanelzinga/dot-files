#!/bin/sh
if [ -z "$1" ]; then
    echo "Usage: ssh-tunnel.sh tunnel_name"
    exit 1
fi

if [ -z "$SSH_AUTH_SOCK" ]; then
    echo "Please start ssh-agent first."
    exit 1
fi

exec docker run -it --rm \
    -v $SSH_AUTH_SOCK:/tmp/ssh.agent \
    -e SSH_AUTH_SOCK=/tmp/ssh.agent \
    -e SSH_HOST_KEY="$SSH_HOST_KEY" \
    -e SSH_TUNNEL_PUBLIC_PORT="$SSH_TUNNEL_PUBLIC_PORT" \
    -e SSH_TUNNEL_PRIVATE_IP="$SSH_TUNNEL_PRIVATE_IP" \
    -e SSH_TUNNEL_PRIVATE_PORT="$SSH_TUNNEL_PRIVATE_PORT" \
    -e SSH_USER="$SSH_USER" \
    -e SSH_HOST="$SSH_HOST" \
    --label tunnel=true \
    --name "$1" \
    --network ssh-tunnels \
    --ip $SSH_LOCAL_IP \
    ssh-tunnel
