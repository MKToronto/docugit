from git import Repo, GitCommandError
from datetime import datetime
from pathlib import Path
from dateutil.relativedelta import relativedelta
import sys
import time
from operator import attrgetter
import yaml

with open('config.yaml') as config_file:
    config = yaml.safe_load(config_file)

repositories = config['repositories']
new_reports_dir = Path(config['new_reports_dir']) / datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
start_date = datetime.strptime(config['start_date'], '%Y-%m-%d')
start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)  # Ensure it starts at midnight
end_date = datetime.now() if config['end_date'] == 'now' else datetime.strptime(config['end_date'], '%Y-%m-%d')
period = config.get('period', 'monthly')
# Determine the period delta
if period == 'weekly':
    period_delta = relativedelta(weeks=1)
elif period == 'bi-weekly':
    period_delta = relativedelta(weeks=2)
elif period == 'monthly':
    period_delta = relativedelta(months=1)
elif period == 'quarterly':
    period_delta = relativedelta(months=3)
elif period == 'yearly':
    period_delta = relativedelta(years=1)
else:
    raise ValueError("Invalid period specified. Please choose from 'weekly', 'bi-weekly', 'monthly', 'quarterly', or 'yearly'.")


file_types = config['file_types']
ignore_file_names = config['ignore_file_names']
ignore_file_types = config['ignore_file_types']
ignore_folders = config['ignore_folders']

# Function to handle index.lock file using pathlib
def handle_lock_file(repo_path):
    lock_file = repo_path / ".git" / "index.lock"
    print(f"Checking for lock file: {lock_file}")
    while lock_file.exists():
        print(f"Removing lock file: {lock_file}")
        try:
            print(f"Removing lock file: {lock_file}")
            lock_file.unlink()
            print("Lock file removed.")
        except Exception as e:
            print(f"Failed to remove lock file: {e}")
        
        if lock_file.exists():
            print("Lock file still exists.")
            time.sleep(1)
        else:
            print("Lock file removed.")
            break



def save_code_state(repo_name, period_folder, file_path, commit):
    """Save the state of a file at a specific commit with optional description."""
    output_file_path = Path(f"{period_folder}/{repo_name}/{file_path.name}/code_state_{file_path.stem}.txt")
    output_file_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with file_path.open('r') as file:
            contents = file.read()
        with output_file_path.open('w') as output_file:
            output_file.write(f"Contents of {file_path} as of commit {commit.hexsha}:\n{contents}")
    except FileNotFoundError:
        with output_file_path.open('w') as output_file:
            output_file.write(f"File {file_path} not found in the repository at commit {commit.hexsha}.")


# Function to write commit information to files by file
def write_commit_info_to_files(repo_name, commit_info_dict, period_folder):
    for file_name, info_blocks in commit_info_dict.items():
        output_dir = Path(f'{period_folder}/{repo_name}')
        output_dir.mkdir(parents=True, exist_ok=True)
        file_index = 1
        current_file_path = output_dir / f'{Path(file_name)}/{Path(file_name).stem}_part{file_index}.txt'

        current_file_path.parent.mkdir(parents=True, exist_ok=True)
        output_file = open(current_file_path, 'w')
        current_line_count = 0


        for block in info_blocks:
            # print(f"Block: {block}")
            lines = block.split('\n')
            for line in lines:
                # print(f"Line: {line}")
                # print(f"Current Line Count: {current_line_count}")
                

                # if current_line_count >= 2000 and ('def ' in line.strip() or line.strip() == '') :
                if current_line_count >= 2000 and ('def ' in line.strip() ) :

                    # print("Function definition detected. Splitting file.")
                    output_file.write('\n\n-------------------\n\n')
                    output_file.close()
                    # print(f"closing file {current_file_path}")
                    file_index += 1
                    current_file_path = output_dir / f'{Path(file_name)}/{Path(file_name).stem}_part{file_index}.txt'
                    current_file_path.parent.mkdir(parents=True, exist_ok=True)

                    output_file = open(current_file_path, 'w')
                    current_line_count = 0
                    # print(f"New file: {current_file_path}")
                    # print(f"Current Line Count: {current_line_count}")
                
                
                output_file.write(line + '\n')
                current_line_count += 1
                
                
                
        if current_line_count > 0:
            output_file.write('\n\n-------------------\n\n')
        output_file.close()



    

# Inside your loop, update the current_end_date calculation
# Iterate over commits in the specified period and write commit information

def handle_checkout(repo, commit_sha):
    try:
        repo.git.checkout(commit_sha)
    except GitCommandError as e:
        if "untracked working tree files would be overwritten by checkout" in e.stderr:
            print("Handling untracked files...")
            # Extract all file paths from the error message
            untracked_files = [line.split()[-1] for line in e.stderr.split('\n') if line.strip().startswith('barcode_production/')]
            # Filter to get paths in '_production' directories
            production_files = [file for file in untracked_files if '_production' in file]
            # Update .gitignore if needed
            update_gitignore(repo.working_dir, production_files)
            # Attempt to checkout again if necessary
            try:
                repo.git.checkout(commit_sha)
                print("Checkout successful after checking and updating if necessary .gitignore.")
            except GitCommandError:
                print("Checkout failed even after updating .gitignore. Please handle manually.")



def update_gitignore(repo_dir, file_paths):
    gitignore_path = Path(repo_dir) / '.gitignore'
    need_to_update = False

    if gitignore_path.exists():
        existing_ignore = gitignore_path.read_text()
        with gitignore_path.open('a') as file:
            for file_path in file_paths:
                if file_path not in existing_ignore:
                    need_to_update = True
                    file.write(f'\n{file_path}')
    else:
        need_to_update = True
        with gitignore_path.open('w') as file:
            for file_path in file_paths:
                file.write(f'{file_path}\n')

    if need_to_update:
        print(f"Updated .gitignore with paths: {file_paths}")
    else:
        print("No update needed for .gitignore.")

def check_uncommitted_changes(repo):
    # Check for uncommitted changes including untracked files
    if repo.is_dirty(untracked_files=True):
        raise Exception("There are uncommitted changes. Please commit or stash them before running this script.")


for repo_string, branch in repositories.items():
    print(f"Processing repository: {repo_string} on branch {branch}")
    print(f"Processing repository: {repo_string}")
    repo_path = Path(repo_string)
    repo = Repo(repo_path)
    try:
        original_branch = repo.git.symbolic_ref('HEAD', quiet=True).strip().split('/')[-1]
    except GitCommandError:
        original_branch = branch  # Fallback to the specified branch if in detached HEAD

    # Process commits...
    try:
        check_uncommitted_changes(repo)
    except Exception as e:
        print(e)
        sys.exit("Stopping script due to uncommitted changes.")

 
    current_start_date = start_date
    while current_start_date < end_date:
        initial_commit = None
        initial_commit_empty = False
        # current_end_date = current_start_date + timedelta(days=7)
        # current_end_date = current_start_date + relativedelta(months=1)
        current_end_date = current_start_date + period_delta


        # Get commits within the specified period and sort them
        period_folder = f"{new_reports_dir}/{current_start_date.strftime('%Y_%m_%d')}_to_{current_end_date.strftime('%Y_%m_%d')}"
        print(f"From: {current_start_date.strftime('%Y-%m-%d %H:%M:%S')} To: {current_end_date.strftime('%Y-%m-%d %H:%M:%S')}")
        
        commits_in_period = list(repo.iter_commits(branch, since=current_start_date.strftime('%Y-%m-%d %H:%M:%S'), until=current_end_date.strftime('%Y-%m-%d %H:%M:%S')))

        if len(commits_in_period) < 1:
            print("Not enough commits in the period to perform a meaningful diff.")
            current_start_date = current_end_date
            continue

        commits_in_period.sort(key=attrgetter('committed_date'))
        last_commit = commits_in_period[-1]
        commits_in_period_previous = list(repo.iter_commits(branch, until=current_start_date.strftime('%Y-%m-%d %H:%M:%S')))
        if commits_in_period_previous:
            commits_in_period_previous.sort(key=attrgetter('committed_date'))
            initial_commit = commits_in_period_previous[-1]
            print("Commits found in the previous period.")
        else:
            initial_commit = last_commit
            initial_commit_empty = True
            print("No previous commits found in the period. Using empty tree SHA.")
   



        

        # Checkout to the initial commit and gather all relevant files
        # repo.git.checkout(initial_commit.hexsha)
        handle_checkout(repo, initial_commit.hexsha)
        initial_files = [f for f in repo_path.glob('**/*') if ((f.suffix in file_types or f.name == 'Dockerfile') and f.name not in ignore_file_names and not any(f.suffix == ign for ign in ignore_file_types)) and ("_production" not in str(f) and
        not any(ignored in f.parts for ignored in ignore_folders))]

        # Checkout to the last commit
        # repo.git.checkout(last_commit.hexsha)
        handle_checkout(repo, last_commit.hexsha)

        # Initialize dictionary to store diffs
        commit_info_dict = {}

        # Generate diffs for each file
        for file_path in initial_files:
            print(f"Checking file: {file_path}")
            # If file exists in the last commit, diff it against the initial commit
            if file_path.exists():
                if initial_commit_empty:
                    print("Initial commit. Using empty tree SHA.")
                    empty_tree_sha = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"
                    diff = repo.git.diff(empty_tree_sha, last_commit.hexsha, file_path)                    
                else:
                    diff = repo.git.diff(initial_commit.hexsha, last_commit.hexsha, file_path)
                if diff:  # If there is a difference
                    print(f"Changes in: {file_path}")
                    commit_info_dict[file_path.name] = [f"Changes in: {file_path}\n{diff}\n"]
                    if not initial_commit_empty:
                        save_code_state(repo_path.name, period_folder, file_path, initial_commit)
        # Write the commit information to files
        
        if not initial_commit_empty:
            initial_files_set = set(initial_files)
            for diff_file in repo.git.diff(initial_commit.hexsha, last_commit.hexsha, name_only=True).split('\n'):
                file_path = repo_path / diff_file
                if file_path not in initial_files_set:
                    print(f"New file in last commit: {file_path}")
                    if file_path.suffix in file_types and file_path.name not in ignore_file_names and not any(file_path.suffix == ign for ign in ignore_file_types) and "_production" not in str(file_path) and not any(ignored in file_path.parts for ignored in ignore_folders):
                        diff = repo.git.diff(initial_commit.hexsha, last_commit.hexsha, '--', file_path)
                        if diff:
                            print(f"Diff exists for New file in last commit: {file_path}")
                            commit_info_dict[file_path.name] = [f"Changes in: {file_path}\n{diff}\n"]
        # Debugging print statements
        print("Commit Info Dict Contents:")
        for k, v in commit_info_dict.items():
            # print(f"{k}: {v}")
            print(f"{k}: {len(v)}")
            
        write_commit_info_to_files(repo_path.name, commit_info_dict, period_folder)
        current_start_date = current_end_date

        


# After operations, checkout back
    repo.git.checkout(original_branch)


