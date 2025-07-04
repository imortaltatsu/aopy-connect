#!/usr/bin/env python3
"""
Post-install script for aopy_connect package.
Installs npm dependencies required for AO Connect.
"""

import subprocess
import sys
import os

def install_npm_dependencies():
    """Install npm dependencies after Python package installation"""
    print("🔍 Checking npm dependencies for AO Connect...")
    
    try:
        # Check if npm is available
        npm_version = subprocess.run(["npm", "--version"], check=True, capture_output=True, text=True)
        print(f"✅ npm version: {npm_version.stdout.strip()}")
        
        # Check if @permaweb/aoconnect is installed
        result = subprocess.run(
            ["npm", "list", "-g", "@permaweb/aoconnect"], 
            capture_output=True, 
            text=True
        )
        
        if "@permaweb/aoconnect" not in result.stdout:
            print("⚠️  @permaweb/aoconnect not found. Installing...")
            install_result = subprocess.run(
                ["npm", "install", "-g", "@permaweb/aoconnect"],
                capture_output=True,
                text=True
            )
            
            if install_result.returncode == 0:
                print("✅ @permaweb/aoconnect installed successfully")
                return True
            else:
                print(f"❌ Failed to install @permaweb/aoconnect: {install_result.stderr}")
                print("Please install manually: npm install -g @permaweb/aoconnect")
                return False
        else:
            print("✅ @permaweb/aoconnect is already installed")
            return True
            
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ npm not found. Please install Node.js from https://nodejs.org/")
        print("Then run: npm install -g @permaweb/aoconnect")
        return False
    except Exception as e:
        print(f"❌ Error during npm installation: {e}")
        print("Please install manually: npm install -g @permaweb/aoconnect")
        return False

if __name__ == "__main__":
    install_npm_dependencies() 