def analyze_codebase():
  import os
  import json

  project_structure = {}

  for root, dirs, files in os.walk('.'):
      for file in files:
          file_path = os.path.join(root, file)
          with open(file_path, 'r', encoding='utf-8') as f:
              contents = f.read()

              # Analyze imports within the file
              imports = []
              if file.endswith('.py'):
                  # Check for Python imports
                  imports = [line for line in contents.splitlines() if line.startswith('import') or line.startswith('from')]
              elif file.endswith('.js'):
                  # Check for JavaScript imports (basic)
                  imports = [line for line in contents.splitlines() if line.startswith('import')]

              project_structure[file_path] = {
                  'imports': imports,
                  'size': os.path.getsize(file_path),
                  'lines': contents.splitlines(),
              }

  # Save the analysis result to a JSON file
  with open('code_analysis.json', 'w', encoding='utf-8') as json_file:
      json.dump(project_structure, json_file, indent=4)

if __name__ == '__main__':
  analyze_codebase()