# dot-files

Install bitwarden-cli

    nix-env -i bitwarden-cli jq
    bw login
    bw list items --search "ssh private key thinkpad" | jq .
    bw get attachment <attachmentid> --output ssh.tar --itemid <item-id>
    
https://www.atlassian.com/git/tutorials/dotfiles

    alias dotfiles='/usr/bin/git --git-dir=$HOME/.dotfiles/ --work-tree=$HOME'
    echo ".dotfiles" >> ~/.gitignore
    git clone --bare <git-repo-url> $HOME/.dotfiles
    dotfiles checkout
    dotfiles config --local status.showUntrackedFiles no
    
