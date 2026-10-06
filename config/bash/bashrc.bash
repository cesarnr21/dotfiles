# Example .bashrc file


# -------------------------------------- added by cesar --------------------------------------

# set vim as the default editor for everything
export VISUAL=vim
export EDITOR=vim

function parse_git() {
    git branch 2> /dev/null | sed -e '/^[^*]/d' -e 's/* \(.*\)/ (\1)/'
}

# user@hostname (blue): home/path (yellow) git-branch (red) for main
export PS1="\[\033[34;1m\]\u@\h:\[\033[33;1m\]\w\[\033[31m\]\$(parse_git) \[\033[m\]\$ "

# without git_parse
export PS1="\[\033[01;32m\]\u@\h:\[\033[34m\]\w \[\033[m\]$ "

# for other systems
# for some setups, for example virtual machines, the full hostname would better than the shorted version, so use `u@\H:` instead of `u@\h:`
export PS1="\[\033[01;32m\]\u@\h:\[\033[34m\]\w\[\033[31m\]\$(parse_git) \[\033[m\]\$ "

alias rebash='echo "Resourcing bash";source ~/.bashrc'

# show all files, in long format, with sizes in more modern units 
alias ll="ls -alhF"

alias bat="/usr/bin/batcat"

# set bat as the manpager
# for debian and ubuntu, use "batcat" and "bat" for other distros (MacOS, arch, fedora, etc)
# export MANPAGER="sh -c 'col -bx | batcat -l man -p'"

# autojump for linux
# WARNING: keep in mind that this file may be named a little differently, ie `autojump.bash` or something similar
. /usr/share/autojump/autojump.sh


## Set up SSH Agent
SSH_ENV="$HOME/.ssh/environment"

function start_agent {
     echo "Initialising new SSH agent..."
     /usr/bin/ssh-agent | sed 's/^echo/#echo/' > "${SSH_ENV}"
     echo succeeded
     chmod 600 "${SSH_ENV}"
     . "${SSH_ENV}" > /dev/null
     /usr/bin/ssh-add;
}

# Source SSH settings, if applicable
if [ -f "${SSH_ENV}" ]; then
     . "${SSH_ENV}" > /dev/null
     ps -ef | grep ${SSH_AGENT_PID} | grep ssh-agent$ > /dev/null || {
         start_agent;
     }
else
     start_agent;
fi

# -------------------------------------- end by cesar --------------------------------------

