alias npr='f() { git checkout -b $1; git push --set-upstream origin $1; }; f'

# source: https://spencer.wtf/2026/02/20/cleaning-up-merged-git-branches-a-one-liner-from-the-cias-leaked-dev-docs.html
alias ciaclean='git branch --merged origin/main | grep -vE "^\s*(\*|main|develop)" | xargs -n 1 git branch -d'
