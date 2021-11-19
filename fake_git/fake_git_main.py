"""
    status           "Prints current status of fake_git"
    init             "Inits fake_git repository"
    commit           "Commits staged files"
    add <file_name>  "Stages new files"

Usage:
    fake_git status
    fake_git init
    fake_git commit
    fake_git add <file_name>
"""
from fake_git.fake_git import add, init, commit, status
import docopt


def main():
    args = docopt.docopt(__doc__)
    if args["add"]:
        add(args["<file_name>"])
    elif args["init"]:
        init()
    elif args["commit"]:
        commit()
    else:
        status()




if __name__ == '__main__':
    main()
