if status is-interactive
    # Commands to run in interactive sessions can go here

    # set autojump file
    set --local AUTOJUMP_PATH /usr/share/autojump/autojump.fish
    if test -e $AUTOJUMP_PATH
        source $AUTOJUMP_PATH
    end
end

set -gx EDITOR /usr/bin/vim
set -gx DOCKER_BUILDKIT 1


# -----------------------setup SSH Agent ------------------------
set SSH_ENV $HOME/.ssh/agent-environment

function start_agent
    echo "Initialising new SSH agent..."
    ssh-agent -c | sed 's/^echo/#echo/' >$SSH_ENV
    echo Success!
    chmod 600 $SSH_ENV
    . $SSH_ENV >/dev/null
    ssh-add
end

# Source SSH settings, if applicable
if test -e $SSH_ENV
    . $SSH_ENV >/dev/null
    ps -ef | grep $SSH_AGENT_PID | grep ssh-agent >/dev/null || start_agent
else
    start_agent
end



# ----------------------- set prompt color ------------------------
function fish_prompt
    # 1. Conda Environment
    #if set -q CONDA_DEFAULT_ENV
    #    set_color -o green
    #    echo -n "("(basename $CONDA_DEFAULT_ENV)") "
    #    set_color normal
    #end
    if set -q SSH_CONNECTION; or set -q SSH_CLIENT
        # SSH remote color (e.g., red/orange for safety/awareness)
        set user_color green
        set dir_color blue
    else
        # Local color (e.g., green/cyan)
        set user_color blue
        set dir_color yellow
    end

    set_color $user_color
    #set_color --bold $user_color
    # https://stackoverflow.com/questions/24581793/ps1-prompt-in-fish-friendly-interactive-shell-show-git-branch
    echo -n (whoami)'@'(prompt_hostname)':'
    set_color $dir_color
    # show up to 3 full directories
    echo -n (prompt_pwd --full-length-dirs 3)
    set_color red
    set -l git_branch (git branch 2>/dev/null | sed -n '/\* /s///p')

    if string length -q -- $git_branch
        echo -n " ($git_branch)"
    end
    set_color normal
    echo -n ' ❯ '
end

set -gx LD_LIBRARY_PATH $LD_LIBRARY_PATH $HOME/.local/lib /usr/local/lib
fish_add_path $HOME/.local/bin /usr/local/bin
fish_add_path /var/lib/flatpak/exports/bin
# add homebrew installed commands
#eval "$(/opt/homebrew/bin/brew shellenv)"

# get codes from: https://geoff.greer.fm/lscolors/
set -gx LS_COLORS 'di=34:ln=35:so=31:pi=33:ex=32:bd=34;46:cd=34;43:su=30;41:sg=30;46:tw=30;42:ow=30;43'

alias rebash='echo "reloading fish shell";source ~/.config/fish/config.fish'
alias ll="ls -alFhS"

alias gs="git status"

# >>> conda initialize >>>
# !! Contents within this block are managed by 'conda init' !!
if test -f /home/cesar/miniforge3/bin/conda
    eval /home/cesar/miniforge3/bin/conda "shell.fish" "hook" $argv | source
else
    if test -f "/home/cesar/miniforge3/etc/fish/conf.d/conda.fish"
        . "/home/cesar/miniforge3/etc/fish/conf.d/conda.fish"
    else
        set -x PATH "/home/cesar/miniforge3/bin" $PATH
    end
end
# <<< conda initialize <<<

