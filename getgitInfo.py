import subprocess

# Get the current Git repository name
git_repo = subprocess.check_output(['git', 'rev-parse', '--show-toplevel']).strip().decode('utf-8')

# Get the Git repository server URL
git_remote_url = subprocess.check_output(['git', 'config', '--get', 'remote.origin.url']).strip().decode('utf-8')
git_remote_url_replace = git_remote_url.replace('.git', '')
# Get the Git SHA
git_sha = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip().decode('utf-8')

# Get the Git run number
git_run_number = subprocess.check_output(['git', 'rev-list', '--count', 'HEAD']).strip().decode('utf-8')
separator = "/"
value_list = [git_remote_url_replace, "commit", git_sha]
# Print the results
print("Git repository name:", git_repo)
print("Git repository server URL:", git_remote_url_replace)
print("Git SHA:", git_sha)
print("Git run number:", git_run_number)
url = separator.join(value_list)
print(url)