# CS-2110-blackjack-project

# Git Crash Course

Run these in Terminal from inside the project folder.

```Bash
cd Documents/CS-2110-blackjack-project
```

Makes sure you always check to see what branch you are in 

## Every time you work

1. `git pull` to get the latest changes
2. `git add .` to add your edits
3. `git commit -m "what you changed"` to save them
4. `git push` to upload

`git status` shows what's changed at any point.

## Branches (copies)

| Command | What it does |
| --- | --- |
| `git checkout -b name` | Create a branch and move to it |
| `git switch main` | Go back to main |
| `git branch` | To see current branches |


## Merge conflicts

Open the file, keep the code you want, and delete the `<<<<<<<`, `=======` and `>>>>>>>` lines. Then add, commit and push.

Never use `git push --force` on main.
