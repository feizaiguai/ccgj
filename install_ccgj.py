#!/usr/bin/env python3
"""
ccgj One-Click Installer
Install all 9 AI development tools with a single command

Usage:
    python install_ccgj_english.py
"""

import os
import sys
import json
import hashlib
import subprocess
import tempfile
import requests
import shutil
from pathlib import Path
from datetime import datetime

class CCGJInstaller:
    """ccgj One-Click Installer"""

    def __init__(self):
        self.master_password = "datouguai"
        self.master_hash = hashlib.sha256(self.master_password.encode()).hexdigest()
        self.install_dir = Path.home() / "ccgj"
        self.tools = {
            "gongju0": {
                "name": "Orchestrator",
                "desc": "Chief Architect",
                "repo": "https://github.com/feizaiguai/gongju0.git",
                "install_path": "orchestrator"
            },
            "gongju1": {
                "name": "SpecFlow",
                "desc": "Requirements Tool",
                "repo": "https://github.com/feizaiguai/gongju1.git",
                "install_path": "specflow"
            },
            "gongju2": {
                "name": "TechFlow",
                "desc": "Design Tool",
                "repo": "https://github.com/feizaiguai/gongju2.git",
                "install_path": "techflow"
            },
            "gongju3": {
                "name": "CodeFlow",
                "desc": "Code Generation",
                "repo": "https://github.com/feizaiguai/gongju3.git",
                "install_path": "codeflow"
            },
            "gongju4": {
                "name": "TestFlow",
                "desc": "Testing Tool",
                "repo": "https://github.com/feizaiguai/gongju4.git",
                "install_path": "testflow"
            },
            "gongju5": {
                "name": "ReviewFlow",
                "desc": "Code Review",
                "repo": "https://github.com/feizaiguai/gongju5.git",
                "install_path": "reviewflow"
            },
            "gongju6": {
                "name": "DocFlow",
                "desc": "Documentation",
                "repo": "https://github.com/feizaiguai/gongju6.git",
                "install_path": "docflow"
            },
            "gongju7": {
                "name": "DeployFlow",
                "desc": "Deployment",
                "repo": "https://github.com/feizaiguai/gongju7.git",
                "install_path": "deployflow"
            },
            "gongju8": {
                "name": "FixFlow",
                "desc": "Auto Fix",
                "repo": "https://github.com/feizaiguai/gongju8.git",
                "install_path": "fixflow"
            }
        }

    def show_banner(self):
        """Display installation banner"""
        print("""
==================================================
              ccgj AI Development Toolchain
==================================================

  AI: 9 tools working together
  Fast: One command installation
  Smart: Requirements to deployment

  Password: datouguai
==================================================
        """)

    def verify_password(self):
        """Verify master password"""
        print("Enter installation password (hint: datouguai):")

        try:
            import getpass
            password = getpass.getpass("Password: ")
        except ImportError:
            password = input("Password: ")

        password_hash = hashlib.sha256(password.encode()).hexdigest()

        if password_hash == self.master_hash:
            print("Password verification passed")
            return True
        else:
            print("Password incorrect")
            return False

    def check_system(self):
        """Check system requirements"""
        print("Checking system environment...")

        # Check Python version
        if sys.version_info < (3, 8):
            print("ERROR: Python 3.8+ required")
            return False
        print("Python version:", sys.version.split()[0])

        # Check Git
        try:
            subprocess.run(["git", "--version"], check=True, capture_output=True)
            print("Git is installed")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("ERROR: Git not installed")
            return False

        # Check network
        try:
            response = requests.get("https://github.com", timeout=10)
            if response.status_code == 200:
                print("Network connection OK")
            else:
                print("WARNING: Network connection issue")
        except:
            print("ERROR: Network connection failed")
            return False

        return True

    def create_install_directory(self):
        """Create installation directory"""
        print(f"Creating install directory: {self.install_dir}")

        try:
            self.install_dir.mkdir(parents=True, exist_ok=True)
            print("Install directory created successfully")
        except Exception as e:
            print(f"ERROR: Failed to create install directory: {e}")
            return False

        return True

    def install_tool(self, tool_id, tool_info):
        """Install single tool"""
        print(f"Installing {tool_info['name']} ({tool_info['desc']})...")

        tool_dir = self.install_dir / tool_info['install_path']

        try:
            # Clone repository
            if tool_dir.exists():
                print(f"  {tool_info['name']} exists, updating...")
                subprocess.run(["git", "pull"], cwd=tool_dir, check=True, capture_output=True)
            else:
                print(f"  Cloning {tool_info['name']}...")
                subprocess.run([
                    "git", "clone",
                    tool_info['repo'],
                    str(tool_dir)
                ], check=True, capture_output=True)

            # Install dependencies
            req_file = tool_dir / "requirements.txt"
            if req_file.exists():
                print(f"  Installing {tool_info['name']} dependencies...")
                subprocess.run([
                    sys.executable, "-m", "pip", "install", "-r", str(req_file)
                ], check=True, capture_output=True)

            # Create basic main.py if not exists
            main_file = tool_dir / "src" / "main.py"
            if not main_file.exists():
                main_file.parent.mkdir(parents=True, exist_ok=True)
                with open(main_file, 'w') as f:
                    f.write(f'''#!/usr/bin/env python3
"""
ccgj {tool_info['name']} Main Module
"""

def main():
    print(f"ccgj {tool_info['name']} - {tool_info['desc']}")
    print("Tool is ready to use")

if __name__ == "__main__":
    main()
''')

            print(f"  {tool_info['name']} installation complete")
            return True

        except subprocess.CalledProcessError as e:
            print(f"  ERROR: {tool_info['name']} installation failed: {e}")
            return False
        except Exception as e:
            print(f"  ERROR: {tool_info['name']} installation error: {e}")
            return False

    def create_master_script(self):
        """Create master launcher script"""
        master_script = self.install_dir / "ccgj.py"

        script_content = '''#!/usr/bin/env python3
"""
ccgj Toolchain Launcher
Usage: python ccgj.py <tool_name>

Available tools:
    orchestrator - Chief Architect
    specflow     - Requirements Analysis
    techflow     - Technical Design
    codeflow     - Code Generation
    testflow     - Automated Testing
    reviewflow   - Code Review
    docflow      - Documentation
    deployflow   - Deployment
    fixflow      - Auto Fix
"""

import sys
import os
from pathlib import Path

def show_help():
    print("ccgj AI Development Toolchain")
    print("=" * 40)
    print("Available tools:")
    print("  orchestrator - Chief Architect (gongju0)")
    print("  specflow     - Requirements Analysis (gongju1)")
    print("  techflow     - Technical Design (gongju2)")
    print("  codeflow     - Code Generation (gongju3)")
    print("  testflow     - Automated Testing (gongju4)")
    print("  reviewflow   - Code Review (gongju5)")
    print("  docflow      - Documentation (gongju6)")
    print("  deployflow   - Deployment (gongju7)")
    print("  fixflow      - Auto Fix (gongju8)")
    print("")
    print("Usage:")
    print("  python ccgj.py <tool_name>")
    print("")
    print("Example:")
    print("  python ccgj.py specflow")

def main():
    if len(sys.argv) < 2:
        show_help()
        return

    tool_name = sys.argv[1].lower()
    install_dir = Path(__file__).parent

    # Tool mapping
    tool_mapping = {
        "orchestrator": "orchestrator",
        "specflow": "specflow",
        "techflow": "techflow",
        "codeflow": "codeflow",
        "testflow": "testflow",
        "reviewflow": "reviewflow",
        "docflow": "docflow",
        "deployflow": "deployflow",
        "fixflow": "fixflow"
    }

    if tool_name not in tool_mapping:
        print(f"ERROR: Unknown tool: {tool_name}")
        show_help()
        return

    # Run tool
    tool_script = install_dir / f"{tool_mapping[tool_name]}.py"

    if tool_script.exists():
        os.execv(sys.executable, [sys.executable, str(tool_script)])
    else:
        print(f"ERROR: Tool not installed: {tool_name}")

if __name__ == "__main__":
    main()
'''

        with open(master_script, 'w', encoding='utf-8') as f:
            f.write(script_content)

        # Set executable permission
        if os.name != 'nt':
            os.chmod(master_script, 0o755)

    def create_batch_files(self):
        """Create Windows batch files"""
        # Create main batch file
        batch_file = self.install_dir / "ccgj.bat"

        batch_content = '''@echo off
REM ccgj Toolchain Launcher for Windows

set "INSTALL_DIR=%~dp0"
set "PYTHON_PATH=python"

if "%1"=="" goto :show_help
goto :run_tool

:show_help
echo ccgj AI Development Toolchain
echo ================================
echo Available tools:
echo   orchestrator - Chief Architect
echo   specflow     - Requirements Analysis
echo   techflow     - Technical Design
echo   codeflow     - Code Generation
echo   testflow     - Automated Testing
echo   reviewflow   - Code Review
echo   docflow      - Documentation
echo   deployflow   - Deployment
echo   fixflow      - Auto Fix
echo.
echo Usage:
echo   ccgj.bat <tool_name>
echo.
echo Example:
echo   ccgj.bat specflow
goto :end

:run_tool
set "TOOL_NAME=%1"
set "TOOL_PATH=%INSTALL_DIR%\\%TOOL_NAME%"

if exist "%TOOL_PATH%" (
    echo Starting ccgj %TOOL_NAME%...
    cd /d "%TOOL_PATH%"
    %PYTHON_PATH% src\\main.py
) else (
    echo ERROR: Tool not installed: %TOOL_NAME%
)
goto :end

:end
'''

        with open(batch_file, 'w', encoding='utf-8') as f:
            f.write(batch_content)

    def save_config(self):
        """Save configuration file"""
        config = {
            "version": "1.0.0",
            "installed_at": datetime.now().isoformat(),
            "master_password_hash": self.master_hash,
            "tools": self.tools,
            "install_directory": str(self.install_dir),
            "password": self.master_password
        }

        config_file = self.install_dir / "config.json"
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

    def show_success_message(self):
        """Display success message"""
        print("""
==================================================
                    Installation Complete!
==================================================

Install directory: """ + str(self.install_dir) + """

Usage:
  cd """ + str(self.install_dir) + """
  python ccgj.py <tool_name>

Available tools:
  orchestrator - Chief Architect
  specflow     - Requirements Analysis
  techflow     - Technical Design
  codeflow     - Code Generation
  testflow     - Automated Testing
  reviewflow   - Code Review
  docflow      - Documentation
  deployflow   - Deployment
  fixflow      - Auto Fix

Quick start:
  cd """ + str(self.install_dir) + """
  python ccgj.py specflow

For more help: https://github.com/feizaiguai/ccgj
        """)

    def install(self):
        """Execute full installation"""
        self.show_banner()

        # Verify password
        if not self.verify_password():
            return False

        # Check system
        if not self.check_system():
            return False

        # Create install directory
        if not self.create_install_directory():
            return False

        print("\nStarting installation of 9 AI tools...")
        print("=" * 50)

        # Install all tools
        success_count = 0
        for tool_id, tool_info in self.tools.items():
            if self.install_tool(tool_id, tool_info):
                success_count += 1

        print("\n" + "=" * 50)
        print(f"Installation result: {success_count}/{len(self.tools)} tools installed")

        if success_count == len(self.tools):
            # Create master script
            self.create_master_script()

            # Create batch files for Windows
            self.create_batch_files()

            # Save configuration
            self.save_config()

            # Show success message
            self.show_success_message()
            return True
        else:
            print(f"Installation failed: only {success_count}/{len(self.tools)} tools installed")
            return False


def main():
    """Main function"""
    installer = CCGJInstaller()
    installer.install()


if __name__ == "__main__":
    main()