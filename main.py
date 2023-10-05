from github import Github
from github import GithubException
import os
from subprocess import Popen
import re
import click
import json


class AutoPyGitHub:
    def __init__(self):
        self.token = ""
        self.user = ""

    def create_repository(self, folder_path):
        folder_name = os.path.basename(folder_path)
        repo_name = folder_name.lower().replace(" ", "-")
        if not click.confirm(f"Create repository name as : {click.style(repo_name, 'green')}", default=True):
            folder_name = input( click.style("write name of your repo> ", "red", bold=True).strip())
       
        repo_name = folder_name.lower().replace(" ", "-")

        # Create a new repository on GitHub
        try:
            new_repo = self.user.create_repo(repo_name, auto_init=True)
        except GithubException as e:
            error = str(e).replace("422 ","")
            error = json.loads(error)
            print(click.style(f"{error['errors'][0]['message']}","red",bold=True))
            exit()

        
        print(f"Created repo: {new_repo.html_url}")

        self.rename_readme(folder_path)

        # Initialize a local Git repository
        self.initialize_local_repo(folder_path)

        # Add and commit files
        self.add_and_commit_files(folder_path)

        # Create a main branch
        self.create_main_branch(folder_path)

        # Add a remote to the local repository
        remote_url = new_repo.clone_url
        self.add_remote(folder_path, remote_url)

        # Push the local repository to GitHub
        self.push_repository(folder_path)

    def remove_url(self, text):
        brackets_pattern = r"\s*\(https:[^)]*\)"
        text_without_brackets = re.sub(brackets_pattern, "", text)
        return text_without_brackets

    def rename_readme(self, folder_path):
        files = os.listdir(folder_path)
        for file in files:
            if file == "README.md":
                readme_path = os.path.join(folder_path, file)
                with open(readme_path, "r") as f:
                    content = f.read()
                    removed_url = self.remove_url(content).replace(
                        "thepythoncode", "Iranzi Thierry"
                    )
                    with open(readme_path, "w") as f_2:
                        f_2.write(removed_url)
                break
            
    def initialize_local_repo(self, folder_path):
        files = os.listdir(folder_path)
        for file in files:
            if file == ".git":
                try:
                    os.removedirs(os.path.join(folder_path, file))
                except PermissionError as error:
                    print(error)
                except OSError as error:
                    print(error)

        with Popen(f"git init", cwd=folder_path, shell=True) as repo:
            repo.communicate(timeout=30)
        print(f"Initialized git repo: {folder_path}")

    def add_and_commit_files(self, folder_path):
        with Popen(
            f"git config --global core.autocrlf false", cwd=folder_path, shell=True
        ) as repo:
            repo.communicate(timeout=30)
        with Popen(f"git add .", cwd=folder_path, shell=True) as repo:
            repo.communicate(timeout=30)
        with Popen(
            f'git commit -m "Initial commit"', cwd=folder_path, shell=True
        ) as repo:
            repo.communicate(timeout=30)
        print(f"Committed git repo: {folder_path}")

    def create_main_branch(self, folder_path):
        with Popen(f"git branch -M main", cwd=folder_path, shell=True) as repo:
            repo.communicate(timeout=30)
        print(f"Created main branch for git repo: {folder_path}")

    def add_remote(self, folder_path, remote_url):
        with Popen(
            f"git remote add origin {remote_url}", cwd=folder_path, shell=True
        ) as remote:
            remote.communicate(timeout=30)
        print(f"Added remote: {remote_url} to local repo")

    def push_repository(self, folder_path):
        with Popen(
            f"git push -u origin main --force", cwd=folder_path, shell=True
        ) as repo:
            repo.communicate(timeout=30)
        print(f"Pushed git repo to GitHub: {folder_path}")

    def manage_folders(self, root_folder):
        folders = os.listdir(root_folder)
        basename = click.style(os.path.basename(root_folder),"green")
        only_folders = [item for item in os.listdir(root_folder) if os.path.isdir(os.path.join(root_folder, item))]
        
        if not only_folders:
            response = click.style(f"\nThere's no folders found in {basename}\nUse option 2\n","red")
            print(response)
            self.main()

        for folder in folders:
            folder_path = os.path.join(root_folder, folder)
            self.create_repository(folder_path)
    def authorize(self):
         if os.path.exists("token.txt"):
            with open ("token.txt", "r") as f:
                token = f.read()
         else:
              print(click.style("Create Github access token to be able to create repository",bold=True))
              print(click.style("Opening Github", "green", bold=True))
              with Popen(
                 f"start chrome https://github.com/settings/personal-access-tokens/new", shell=True
              )      as repo:
                 repo.communicate(timeout=30)
              token = input(
                 click.style("Enter generated token here > ", "red", bold=True).strip()
              )
              with open ("token.txt", "w") as f:
                  f.write(token)
              if not token:
                  print("Token has not provided")
                  exit(1)
         self.token = token
         g = Github(token)
         self.user = g.get_user()

    def main(self):
        print(click.style("Developed by Iranzi Dev", "green", bold=True))
        repo_name = os.path.basename(os.getcwd())
        repo_dir = os.getcwd()
        if click.confirm(f"1) Create one repository : {click.style(repo_name, 'green')}", default=True):
            self.authorize()
            self.create_repository(repo_dir)
        if click.confirm(f"2) Create many repository from : {click.style(repo_name, 'green')}", default=True):
            self.authorize()
            self.manage_folders(repo_dir)
        if click.confirm(f"3) Create repository located else where", default=True):
              self.authorize()
              example = "T:\Projects\Website>"
              root_folder = input(
                click.style(f"Enter folder path \nExample : {click.style(example, 'green')}", "red", bold=True).strip()
               )
              self.manage_folders(root_folder)

if __name__ == "__main__":
    try:
        autocreate_repo = AutoPyGitHub()
        autocreate_repo.main()
    except KeyboardInterrupt:
        print(click.style("\nBye", "green", bold=True))
