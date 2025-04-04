
import os
import json
import ast
import sys
import re
import pkg_resources
from typing import Dict, List, Any, Set, Tuple

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

def get_stdlib_modules() -> Set[str]:
    """Get a set of standard library module names."""
    # Common standard library modules that might not be captured automatically
    common_stdlib = {
        'abc', 'argparse', 'asyncio', 'base64', 'collections', 'concurrent', 
        'contextlib', 'copy', 'csv', 'ctypes', 'datetime', 'decimal', 'difflib', 
        'email', 'enum', 'fileinput', 'fnmatch', 'functools', 'glob', 
        'hashlib', 'heapq', 'hmac', 'html', 'http', 'imaplib', 'importlib', 
        'inspect', 'io', 'ipaddress', 'itertools', 'json', 'logging', 'math', 
        'mimetypes', 'multiprocessing', 'netrc', 'numbers', 'operator', 'os', 
        'pathlib', 'pickle', 'pkgutil', 'platform', 'pprint', 'queue', 
        'random', 're', 'reprlib', 'secrets', 'selectors', 'shutil', 'signal', 
        'smtplib', 'socket', 'sqlite3', 'ssl', 'stat', 'string', 'struct', 
        'subprocess', 'sys', 'tempfile', 'textwrap', 'threading', 'time', 
        'timeit', 'tkinter', 'token', 'traceback', 'types', 'typing', 'unicodedata', 
        'unittest', 'urllib', 'uuid', 'warnings', 'wave', 'weakref', 'webbrowser', 
        'xml', 'xmlrpc', 'zipfile', 'zipimport', 'zlib',
    }
    
    # Builtin modules
    stdlib = set(sys.builtin_module_names)
    stdlib.update(common_stdlib)
    
    # Add modules from the standard library path
    try:
        std_lib_path = os.path.dirname(os.__file__)
        import pkgutil
        stdlib.update([
            name for _, name, _ in pkgutil.iter_modules([std_lib_path])
        ])
    except (ImportError, AttributeError, NameError):
        pass
    
    return stdlib

def extract_root_package_names(import_statements: List[str]) -> Set[str]:
    """Extract the root package names from import statements."""
    package_names = set()
    
    for statement in import_statements:
        if statement.startswith('import '):
            # Handle 'import pkg' or 'import pkg.subpkg'
            packages = statement[7:].split(',')
            for pkg in packages:
                pkg = pkg.strip().split(' as ')[0].split('.')[0]
                if pkg:
                    package_names.add(pkg)
        elif statement.startswith('from '):
            # Handle 'from pkg import x' or 'from pkg.subpkg import x'
            parts = statement.split(' import ')[0][5:].strip()
            if parts and parts != '.':  # Skip relative imports
                root_pkg = parts.split('.')[0]
                package_names.add(root_pkg)
    
    # Filter out standard library modules
    stdlib_modules = get_stdlib_modules()
    
    # Return non-stdlib packages
    return package_names - stdlib_modules

def get_installed_packages() -> Dict[str, str]:
    """Get a dictionary of installed Python packages and their versions."""
    try:
        return {pkg.key: pkg.version for pkg in pkg_resources.working_set}
    except:
        return {}

def analyze_requirements_file() -> Dict[str, str]:
    """Extract packages and their versions from requirements.txt if it exists."""
    required_packages = {}
    req_file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'requirements.txt')
    
    if os.path.exists(req_file_path):
        with open(req_file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Check if there's a version constraint
                    match = re.match(r'([a-zA-Z0-9_\-\.]+)([<>=~].+)?', line)
                    if match:
                        package_name = match.group(1).strip()
                        version_constraint = match.group(2).strip() if match.group(2) else ""
                        required_packages[package_name] = version_constraint
    
    return required_packages

def generate_dependency_report(used_packages: List[str], installed_packages: Dict[str, str], 
                              required_packages: Dict[str, str], missing_packages: List[str],
                              unused_packages: List[str]) -> str:
    """Generate a detailed dependency report."""
    report = []
    report.append("# Dependency Analysis Report\n")
    
    report.append("## Summary")
    report.append(f"- Used packages: {len(used_packages)}")
    report.append(f"- Installed packages: {len(installed_packages)}")
    report.append(f"- Required packages (requirements.txt): {len(required_packages)}")
    report.append(f"- Missing packages: {len(missing_packages)}")
    report.append(f"- Unused packages: {len(unused_packages)}\n")
    
    report.append("## Used Packages")
    for pkg in sorted(used_packages):
        version = installed_packages.get(pkg, "Not installed")
        report.append(f"- {pkg}: {version}")
    report.append("")
    
    if missing_packages:
        report.append("## Missing Packages")
        for pkg in sorted(missing_packages):
            report.append(f"- {pkg}")
        report.append("")
    
    if unused_packages:
        report.append("## Unused Packages")
        for pkg in sorted(unused_packages):
            version = installed_packages.get(pkg, "Unknown")
            report.append(f"- {pkg}: {version}")
        report.append("")
    
    report.append("## Requirements.txt")
    if required_packages:
        for pkg, version in sorted(required_packages.items()):
            installed_version = installed_packages.get(pkg, "Not installed")
            if pkg in used_packages:
                status = "✓ Used"
            else:
                status = "✗ Unused"
            report.append(f"- {pkg}{version}: {installed_version} ({status})")
    else:
        report.append("- No requirements.txt file found or file is empty")
    
    return "\n".join(report)

def analyze_codebase() -> None:
    """Analyze the codebase structure and dependencies."""
    project_structure: Dict[str, Any] = {
        'files': {},
        'summary': {
            'total_files': 0,
            'total_size': 0,
            'languages': {},
            'file_types': {}
        },
        'dependencies': {
            'used_packages': set(),
            'installed_packages': {},
            'required_packages': [],
            'missing_packages': [],
            'unused_packages': []
        }
    }
    
    # Count files by directory for better insights
    dir_counts = {}

    excluded_dirs = {
        '.git', '__pycache__', 'node_modules', '.pytest_cache',
        '.pythonlibs', '.upm', '.config', 'attached_assets',
        'build', 'dist', '.coverage', 'htmlcov',
        '.replit_cache', '.local', '.cache'
    }
    
    print("Starting code analysis...")
    
    # Start at project root, not current directory
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    print(f"Project root: {project_root}")
    
    for root, dirs, files in os.walk(project_root):
        # Remove excluded directories from the walk
        dirs[:] = [d for d in dirs if not (d.startswith('.') or 
                                         d.endswith('.egg-info') or 
                                         d in excluded_dirs)]
        
        # Track file counts by directory
        rel_dir = os.path.relpath(root, project_root)
        dir_counts[rel_dir] = dir_counts.get(rel_dir, 0) + len(files)
        
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
                    # Extract package names from imports
                    if imports:
                        packages = extract_root_package_names(imports)
                        project_structure['dependencies']['used_packages'].update(packages)
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
    
    # Get installed packages
    project_structure['dependencies']['installed_packages'] = get_installed_packages()
    
    # Get packages from requirements.txt
    project_structure['dependencies']['required_packages'] = analyze_requirements_file()
    
    # Convert used packages to list for JSON serialization
    used_packages = list(project_structure['dependencies']['used_packages'])
    project_structure['dependencies']['used_packages'] = used_packages
    
    # Identify local modules based on directories
    local_modules = set()
    for dir_path in dir_counts:
        if dir_path != '.' and not dir_path.startswith('.'):
            # Get top level directory
            top_dir = dir_path.split('/')[0]
            if top_dir:
                local_modules.add(top_dir)
    
    print("\nDetected local modules:")
    for module in sorted(local_modules):
        print(f"  - {module}")
    
    # Essential packages that might not be directly imported but are required
    essential_packages = {
        'pip', 'setuptools', 'wheel', 'pytest', 'gunicorn', 
        'flask', 'psycopg2-binary', 'email-validator'  # Keep project-specific essentials
    }
    
    # Find missing packages (used but not installed)
    project_structure['dependencies']['missing_packages'] = [
        pkg for pkg in used_packages 
        if pkg not in project_structure['dependencies']['installed_packages'] and
           pkg not in local_modules  # Exclude local modules
    ]
    
    # Find unused packages (installed but not used)
    project_structure['dependencies']['unused_packages'] = [
        pkg for pkg in project_structure['dependencies']['installed_packages']
        if pkg not in used_packages and
           pkg not in essential_packages  # Keep essential packages
    ]
    
    # Save analysis results
    analysis_file = os.path.join(project_root, 'code_analysis.json')
    with open(analysis_file, 'w', encoding='utf-8') as json_file:
        json.dump(project_structure, json_file, indent=2)
    print(f"Analysis JSON saved to: {analysis_file}")
    
    # Generate and save the dependency report
    report = generate_dependency_report(
        used_packages,
        project_structure['dependencies']['installed_packages'],
        project_structure['dependencies']['required_packages'],
        project_structure['dependencies']['missing_packages'],
        project_structure['dependencies']['unused_packages']
    )
    report_file = os.path.join(project_root, 'dependency_report.md')
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"Dependency report saved to: {report_file}")
    
    # Print summary
    print(f"\nAnalysis complete!")
    print(f"Total files analyzed: {project_structure['summary']['total_files']}")
    print(f"Total codebase size: {project_structure['summary']['total_size'] / 1024:.2f} KB")
    
    print("\nFile types distribution:")
    for ext, count in project_structure['summary']['file_types'].items():
        print(f"{ext or 'no extension'}: {count} files")
        
    print("\nFiles by directory:")
    # Sort directories by count for better visibility
    sorted_dirs = sorted(dir_counts.items(), key=lambda x: x[1], reverse=True)
    for dir_path, count in sorted_dirs[:15]:  # Show top 15 directories
        print(f"{dir_path}: {count} files")
    
    print("\nPackage Analysis:")
    print(f"Used packages: {len(used_packages)}")
    print(f"Installed packages: {len(project_structure['dependencies']['installed_packages'])}")
    
    if project_structure['dependencies']['missing_packages']:
        print("\nMissing packages (used but not installed):")
        for pkg in project_structure['dependencies']['missing_packages']:
            print(f"  - {pkg}")
            
        print("\nInstallation commands:")
        print("# To install missing packages:")
        print(f"pip install {' '.join(project_structure['dependencies']['missing_packages'])}")
    
    if project_structure['dependencies']['unused_packages']:
        print("\nUnused packages (installed but not detected in imports):")
        for pkg in project_structure['dependencies']['unused_packages']:
            print(f"  - {pkg}")
            
        print("\nUninstallation commands:")
        print("# To uninstall unused packages (USE WITH CAUTION):")
        print(f"pip uninstall -y {' '.join(project_structure['dependencies']['unused_packages'])}")
        
    print("\nNote: Review the dependency_report.md file for more detailed information.")

if __name__ == '__main__':
    try:
        import pkgutil
        analyze_codebase()
    except Exception as e:
        print(f"Error analyzing codebase: {e}")
