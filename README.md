# dot-files

Install bitwarden-cli
nix-env -i bitwarden-cli jq
bw login
bw list items --search "ssh private key thinkpad" | jq .
bw get attachment <attachmentid> --output ssh.tar --itemid <item-id>
