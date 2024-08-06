# DocuGit

## Overview
DocuGit is a tool designed to automatically retrieve detailed code changes in repositories over a specified period. This tool is particularly useful for generating R&D reports, which can help companies receive grants, tax incentives or cashback for employee salaries spent on research and development. The code changes can be fed into large language models (LLMs) such as ChatGPT for further analysis or report generation.

## Features
- **Automatic Code Retrieval**: Retrieves detailed code changes over a specified period.
- **Customizable**: Users can specify which file types and folders to include or ignore.
- **Time Range Specification**: Analyze changes within custom time ranges (weekly, bi-weekly, monthly, quarterly, yearly).
- **Integration with LLMs**: Output can be fed into models like ChatGPT for enhanced report generation.

## Installation

### Using Conda

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/docugit.git
    cd docugit
    ```

2. Create the Conda environment:
    ```sh
    conda env create -f environment.yaml
    ```

3. Activate the environment:
    ```sh
    conda activate docugit
    ```

### Using Pip

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/docugit.git
    cd docugit
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Configuration
Edit the `config.yaml` file to set up your repositories and other settings.

### Example `config.yaml`
```yaml
repositories:
  # Replace /path/to/repoX with actual repository paths and branchX with the corresponding branch names
  "/path/to/repo1": "branch1"  # e.g., "/Users/username/project1": "main"
  "/path/to/repo2": "branch2"  # e.g., "/Users/username/project2": "develop"

new_reports_dir: "generated_reports"
start_date: "2023-12-01"      # Format: YYYY-MM-DD
end_date: "now"               # Use "now" for the current date
period: "monthly"             # Specify the period: "weekly", "bi-weekly", "monthly", "quarterly", or "yearly"

file_types:
  - ".py"
  - ".sh"
  - ".md"
  - ".yml"
  - ".command"
  - ".svelte"
  - ".js"
  - ".json"
  - "Dockerfile"
  - ".txt"

ignore_file_names:
  - "recipe.json"

ignore_file_types:
  - ".png"
  - ".jpg"
  - ".bin"
  - ".npy"

ignore_folders:
  - "node_modules"
  - ".mypy_cache"
  - "mounted_vols"
  - "batches_test"
```

### Configuration Options

- **repositories**: A dictionary where the key is the path to the repository and the value is the branch name.  
- **new_reports_dir**: The directory where the generated reports will be saved.  
- **start_date**: The start date for analyzing changes (format: YYYY-MM-DD).  
- **end_date**: The end date for analyzing changes. Use "now" to use the current date.  
- **period**: The period for analyzing changes. Options are "weekly", "bi-weekly", "monthly", "quarterly", or "yearly".  
- **file_types**: A list of file extensions to include in the analysis.  
- **ignore_file_names**: A list of specific file names to ignore.  
- **ignore_file_types**: A list of file extensions to ignore.  
- **ignore_folders**: A list of folders to ignore. 

## Usage
Run the script to retrieve code changes for the specified repositories.

```sh
python docugit.py
```
### Example Output
The retrieved code changes will be stored in the generated_reports directory with a timestamp. Each repository's changes will be documented in separate folders within this directory. The output will include the original code from the beginning of the specified period and the code changes made during that period. These changes can then be used to produce reports by feeding them into LLMs such as ChatGPT.





## Contributing
If you would like to contribute to DocuGit, please fork the repository and create a pull request with your changes.


### Using GPT for Documenting Code Changes in Your GitHub Repository

To use GPT for generating documentation for your code changes, follow these steps. This method allows you to provide the original code and its modifications, and GPT will automatically summarize the changes for you. If the code is too large, split it into multiple sections.

### Instructions for Interacting with GPT

1. **Start the Conversation with Instructions**:
   - Inform GPT that you will provide the original state of the code with `o:` or in sections with `o1:`, `o2:`, etc.
   - Changes to the code will be provided with `c:` or in sections with `c1:`, `c2:`, etc.
   - If it is a new file, just use `c:` to indicate it is a new script.
   - GPT should automatically ask for the `c:` sections after receiving `o:` sections if not provided. If GPT does not ask for `c:` after an `o:`, stop it and remind it to ask for `c:`.
   - If you provide `o1:`, GPT should ask for `o2:`. If you provide `c1:`, GPT should ask for `c2:`.

2. **Providing Original Code**:
   - Prefix the original state of the code with `o:`. For large files, split into sections with `o1:`, `o2:`, etc.
   - GPT will request the next section automatically if not provided.

3. **GPT Requests Changed Code Sections**:
   - GPT will then ask: "Please provide the changes corresponding to the original."

4. **Providing Changed Code**:
   - Prefix the modified state of the code with `c:`. For large files, split into sections with `c1:`, `c2:`, etc.
   - If it is a new file, just use `c:` to indicate it is a new script.

5. **GPT Summarizes Changes**:
   - GPT will summarize the changes with a title "Changes to `<filename>`", focusing on the functionality, purpose, and reason for new functions and modifications to existing functions. Console statements, print statements, and general clean-up changes will be excluded.

6. **Adjusting the Level of Detail**:
   - If you need more or less detail in the summary, you can ask GPT to adjust accordingly.

### Example Interaction

**Step 1: Start with Instructions**
```plaintext
I will provide the original state of the code prefixed with `o:` or in sections `o1:`, `o2:`, etc if the code file is large. Changes will be provided with `c:` or in sections `c1:`, `c2:`, etc if the code file is large. After receiving the `o:` sections, ask for the corresponding `c:` sections if not provided. Summarize the changes with a title "Changes to `<filename>`", describing the functionality, purpose, and reason for new functions and modifications to existing functions. Do not include changes to console or print statements or general clean-up tasks. If it is a new file, just use `c:` to indicate it is a new script. If I provide `o1:`, ask for `o2:`. If I provide `c1:`, ask for `c2:`.
```

##Step 2: Provide Original Code in Sections

o1: Contents of example_file.py as of commit abc123:
```python
def calculate_sum(a, b):
    return a + b

def multiply(a, b):
    return a * b
```
o2: Contents of example_file.py as of commit abc123:
```python
def divide(a, b):
    if b == 0:
        return "Cannot divide by zero"
    return a / b
```


**Step 3: GPT Requests Changed Code Section**
GPT should then ask:
```plaintext
Please provide the changes corresponding to the original. If there are changes for multiple sections, please provide them with `c1:`, `c2:`, etc.
```
**Step 4: Provide Changed Code in Sections**


c1: Changes in: example_file.py
```python
def calculate_sum(a, b, c=0):
    return a + b + c

def multiply(a, b):
    return a * b

def subtract(a, b):
    return a - b
```

c2: Changes in: example_file.py
```python
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

**Step 5: GPT Summarizes the Changes**
GPT will then summarize:  
#### Changes to example_file.py:

1. **Function `calculate_sum`**: Added an optional third parameter `c` to allow summing three numbers instead of two.

2. **New Function `subtract`**: Introduced a new function to subtract one number from another.

3. **Enhanced Error Handling in `divide`**: Changed the error handling in the `divide` function to raise a `ValueError` instead of returning a string when division by zero is attempted.



#### GPT should then ask:


Please provide the next section of the original code or the changes if available.
#### Example for New File
If you are adding a new file, simply provide the changes using c:

c: Contents of new_file.py
```python
def new_function(x):
    return x * x

def another_function(y):
    return y + y
```

GPT will then summarize:

#### Changes to new_file.py:

1. **Function `new_function`**: Takes a single argument `x` and returns its square.
2. **Function `another_function`**: Takes a single argument `y` and returns its double.

By following these guidelines, you can efficiently use GPT to generate detailed and accurate documentation for your code changes in your GitHub repository. This process ensures that your documentation is clear, thorough, and helpful for other developers.

At any time, you can stop GPT and provide additional instructions or corrections. For example, if GPT forgot to ask for c: or you need the changes listed by functions, simply state your requirements clearly. Additionally, you can say "Give me details of the changes in text and sentences."

## Advanced Usage:

### Ensuring a Completely Clean Repository:

DocuGit will stop if there are uncommitted changes in your repository to avoid any data loss. It's crucial to ensure a clean repository before running the script to accurately track changes. Here’s why and how you can achieve a clean repository:

#### Why Ensure a Clean Repository?

- **Accurate Tracking**: Ensuring no uncommitted changes helps accurately track modifications made within the specified period.

- **Prevent Data Loss**: Committing changes ensures no work is lost inadvertently.

- **Git Checkout Requirement**: Git cannot check out an old commit if there are files with unresolved changes in the current state. Therefore, you need to commit or remove all tracked files that haven't been committed to proceed.  

#### Steps to Clean Your Repository Using GitHub Desktop:

1. **Review Changes and Decide**: Review the changes and decide what to do with each file—commit or discard.

- Open GitHub Desktop.  
- Select the repository.  
- Click on the "Changes" tab to review the modified and untracked files.  

2. **Commit Wanted Current Changes**: If you decide to keep the changes, commit them to ensure you don't lose any work.

- In the "Changes" tab, write a commit message describing your changes.
- Click "Commit to <branch name>".

3. **Discard Unwanted Changes**: If you decide not to keep some changes, discard them.

- Right-click on the files you want to discard in the "Changes" tab.
- Select "Discard Changes" to remove the changes from your working directory.

#### Using Command Line for Advanced Cleaning:
If GitHub Desktop is unsuccessful in cleaning the repository, you can use the following Git commands. Use these commands with caution as they will permanently remove uncommitted changes and untracked files.

- git reset --hard will revert the repository to the last committed state, discarding all changes in tracked files since the last commit.
- git clean -fd will remove all untracked files and directories, leaving only the files that are tracked by Git.

### Returning to the Original Branch Using GitHub Desktop:
If the script stops in the middle of running, either due to uncommitted changes or a different reason, you might need to return the repository to the original branch. This is because when git looks at the history of the code it does this by checking out commits and uses a detached headless branch for viewing the code. To return to the original branch:
- Open GitHub Desktop.
- Click on the current branch name at the top of the window.
- Select the original branch you were working on to return to it. For example, click 'master' or 'main'



