To upload your project to GitHub while excluding unnecessary files like your `myenv` virtual environment, follow these steps:

---

### 1. **Initialize a Git Repository**
Navigate to your project folder and initialize a Git repository:

```bash
cd /path/to/your/project
git init
```

---

### 2. **Create a `.gitignore` File**
To exclude the `myenv` directory and other unnecessary files (like temporary files), create a `.gitignore` file in your project root:

```bash
touch .gitignore
```

Add the following content to `.gitignore`:

```
# Exclude the virtual environment
myenv/

# Python-related files
*.pyc
*.pyo
__pycache__/

# Logs and temporary files
*.log
*.tmp

# macOS-specific files
.DS_Store

# Environment and credentials files (example)
.env
```

---

### 3. **Stage and Commit Your Files**
Stage the files for the first commit:

```bash
git add .
```

Make your initial commit:

```bash
git commit -m "Initial commit"
```

---

### 4. **Create a GitHub Repository**
1. Go to [GitHub](https://github.com).
2. Click the **New Repository** button.
3. Provide a repository name and description, then click **Create Repository**.

---

### 5. **Push Your Code to GitHub**
Follow the instructions from GitHub to push your local repository to the remote one:

```bash
# Add the GitHub repository as a remote
git remote add origin https://github.com/username/repository-name.git

# Push the code to GitHub
git branch -M main
git push -u origin main
```

Replace `username` with your GitHub username and `repository-name` with the name of your repository.

---

### 6. **Verify Your Repository**
Go to your GitHub repository URL to confirm your project has been uploaded. 🎉

---

### Notes
- **Share Dependencies Without Including `myenv`**:
  Create a `requirements.txt` file to list your project dependencies:
  ```bash
  pip freeze > requirements.txt
  ```

  Other developers can recreate the environment using:
  ```bash
  python3 -m venv myenv
  source myenv/bin/activate
  pip install -r requirements.txt
  ```


#

Yes, the code snippet will work on a MacBook M2, but with a few considerations:

### Key Points
1. **Python Version**:
   - Ensure you are using the correct version of Python installed on your MacBook. macOS often has a system version of Python (e.g., Python 2.7 or an older version), which may not be what you want to use. Verify your Python version using:
     ```bash
     python --version
     ```
     or
     ```bash
     python3 --version
     ```

2. **Correct `pip` Command**:
   - The `os.system('python -m pip install pyyaml')` command assumes `python` is linked to your intended Python interpreter. On macOS, you might need to use `python3` instead:
     ```python
     os.system('python3 -m pip install pyyaml')
     ```

3. **Rosetta Compatibility**:
   - MacBook M2 uses the ARM architecture, which can sometimes lead to compatibility issues with certain Python libraries. PyYAML and pyotp are generally ARM-compatible, but ensure you're using a Python environment compiled for ARM (e.g., from [python.org](https://www.python.org) or via Homebrew).

4. **Permissions**:
   - If you encounter permission issues, you might need to run the pip command with `--user` or use a virtual environment to avoid requiring admin privileges.

### Updated Code for macOS
Here’s a slightly modified version that ensures better compatibility:

```python
import os

try:
    import yaml
except ImportError:
    os.system('python3 -m pip install --user pyyaml')
    import yaml  # Try importing again after installation

try:
    import pyotp
except ImportError:
    os.system('python3 -m pip install --user pyotp')
    import pyotp  # Try importing again after installation
```

### Recommendation: Use a Virtual Environment
For better control of dependencies, consider using a virtual environment:

```bash
python3 -m venv myenv
source myenv/bin/activate
pip install pyyaml pyotp
```

Then run your script within this environment. This avoids polluting your system Python installation and ensures compatibility.


#

To read the `Config.yaml` file, you can use a library like **PyYAML** in Python. Here's a step-by-step guide:

### 1. Install PyYAML
If you don't have the library installed, use the following command to install it:

```bash
pip install pyyaml
```

### 2. Read the YAML File
Use the following code to read the `Config.yaml` file:

```python
import yaml

# Specify the path to the file
config_path = '/Users/swapnilk/Desktop/GITHUB/Config.yaml'

# Read the YAML file
try:
    with open(config_path, 'r') as file:
        config_data = yaml.safe_load(file)

    # Print the contents
    print(config_data)

except FileNotFoundError:
    print(f"File not found: {config_path}")
except yaml.YAMLError as e:
    print(f"Error reading YAML file: {e}")
```

### Explanation
1. **File Path**: Make sure the file path is correct. Update `config_path` to point to the exact location of your file.
2. **`safe_load`**: This method safely loads the YAML file content into a Python dictionary.
3. **Error Handling**: Handles errors like file not found or YAML parsing errors.

### Sample `Config.yaml` File
If your `Config.yaml` file looks like this:

```yaml
database:
  host: localhost
  port: 3306
  user: root
  password: secret
```

The `config_data` dictionary will look like this:

```python
{
  "database": {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "secret"
  }
}
```

You can then access individual values like this:

```python
host = config_data['database']['host']
port = config_data['database']['port']
print(f"Host: {host}, Port: {port}")
```

#

Creating a virtual environment in Windows is straightforward. Follow these steps:

---

### 1. **Open Command Prompt or PowerShell**
You can use either Command Prompt or PowerShell. To open:
- Press `Win + R`, type `cmd`, and hit Enter.
- Or search for PowerShell in the Start menu and open it.

---

### 2. **Navigate to Your Project Directory**
Use the `cd` command to go to your project folder. For example:

```bash
cd C:\path\to\your\project
```

---

### 3. **Create the Virtual Environment**
Run the following command to create a virtual environment:

```bash
python -m venv myenv
```

Here:
- `python` refers to the Python executable. Use `python3` if your Python installation is named that.
- `myenv` is the name of the virtual environment. You can choose a different name.

---

### 4. **Activate the Virtual Environment**
After creating the environment, activate it:

- **Command Prompt**:
  ```bash
  myenv\Scripts\activate
  ```

- **PowerShell**:
  ```bash
  .\myenv\Scripts\Activate
  ```

You should see the name of the virtual environment (e.g., `(myenv)`) prefixed in your terminal, indicating it is active.

---

### 5. **Install Packages in the Virtual Environment**
Once the virtual environment is active, you can install packages using `pip`:

```bash
pip install package_name
```

For example, to install `PyYAML`:

```bash
pip install pyyaml
```

---

### 6. **Deactivate the Virtual Environment**
To deactivate the virtual environment when you're done, simply type:

```bash
deactivate
```

---

### Tips
- **Check Python Version**:
  Ensure you're using the correct Python version:
  ```bash
  python --version
  ```

- **Install Dependencies from `requirements.txt`**:
  If you have a `requirements.txt` file, you can install all dependencies at once:
  ```bash
  pip install -r requirements.txt
  ```

- **Delete the Virtual Environment**:
  If you no longer need the environment, just delete the `myenv` folder:
  ```bash
  rmdir /s /q myenv
  ```


# AngelOneApiSetup

## Angel Broking Smart API Setup Guide with Full Python API Source

1. Open Angel One Account
2. Register For Angel One SmartAPI
```
https://smartapi.angelbroking.com/signup
```
3. Enable TOTP from the top menu and copy 
4. Create An app to get API from smartapi in angel broking.
```
Go to My profile > My API > Create an app
```
```
Now here you need to fill in information Like

Select: Trading
App name: anything you want
URL : https://smartapi.angelbroking.com/
POST URL: https://smartapi.angelbroking.com/
Angel Client ID : Optional
```

5. Download your Favorite python code editor or use VS Code 

6. Now Open VS Code terminal in your directory and run these Python commands.
```
pip install smartapi-python
pip install websocket-client
```


```
k7?i9xUI5c-KCp4k8A%ZX.X*rGX4oHBn
```