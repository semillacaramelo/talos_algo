
import os
import json
import ast
from typing import Dict, List, Any

def extract_python_imports(content: str) -> List[str]:
    """Extract Python imports using AST for more accurate parsing."""
    imports = []
    try:
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    imports.append(f"import {name.name}")
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ''
                names = [n.name for n in node.names]
                imports.append(f"from {module} import {', '.join(names)}")
    except:
        # Fallback to basic parsing if AST fails
        imports = [line.strip() for line in content.splitlines() 
                  if line.strip().startswith(('import ', 'from '))]
    return imports

def analyze_codebase() -> None:
    """Analyze the codebase structure and dependencies."""
    project_structure: Dict[str, Any] = {
        'files': {},
        'summary': {
            'total_files': 0,
            'total_size': 0,
            'languages': {},
            'file_types': {}
        }
    }

    excluded_dirs = {
        '.git', '__pycache__', 'node_modules', '.pytest_cache',
        '.pythonlibs', '.upm', '.config', 'attached_assets',
        'build', 'dist', '*.egg-info', '.coverage', 'htmlcov',
        '.replit_cache', '.local', '.cache'
    }

    # Only analyze files in project structure defined in README
    included_dirs = {
        'config', 'docs', 'logs', 'src', 'tests',
        'static', 'templates'
    }
    
    for root, dirs, files in os.walk('.'):
        # Skip excluded directories and only include project directories
        base_dir = root.split(os.sep)[1] if len(root.split(os.sep)) > 1 else root
        if base_dir.startswith('.') or base_dir in excluded_dirs:
            dirs[:] = []
            continue
            
        if base_dir not in included_dirs and root != '.':
            dirs[:] = []
            continue
            
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in excluded_dirs]
        
        for file in files:
            file_path = os.path.join(root, file)
            file_ext = os.path.splitext(file)[1]
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    contents = f.read()
                
                file_size = os.path.getsize(file_path)
                imports = []
                
                # Language-specific analysis
                if file.endswith('.py'):
                    imports = extract_python_imports(contents)
                elif file.endswith('.js'):
                    imports = [line.strip() for line in contents.splitlines() 
                             if line.strip().startswith('import ') or 
                                line.strip().startswith('require(')]
                
                # Update project structure
                project_structure['files'][file_path] = {
                    'imports': imports,
                    'size': file_size,
                    'lines': len(contents.splitlines()),
                    'type': file_ext
                }
                
                # Update summary statistics
                project_structure['summary']['total_files'] += 1
                project_structure['summary']['total_size'] += file_size
                project_structure['summary']['file_types'][file_ext] = \
                    project_structure['summary']['file_types'].get(file_ext, 0) + 1
                
            except (UnicodeDecodeError, IOError):
                continue
    
    # Save analysis results
    with open('code_analysis.json', 'w', encoding='utf-8') as json_file:
        json.dump(project_structure, json_file, indent=2)
    
    # Print summary
    print(f"\nAnalysis complete!")
    print(f"Total files analyzed: {project_structure['summary']['total_files']}")
    print(f"Total codebase size: {project_structure['summary']['total_size'] / 1024:.2f} KB")
    print("\nFile types distribution:")
    for ext, count in project_structure['summary']['file_types'].items():
        print(f"{ext or 'no extension'}: {count} files")

if __name__ == '__main__':
    analyze_codebase()
