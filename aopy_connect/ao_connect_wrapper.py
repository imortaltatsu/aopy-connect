"""
Python wrapper for @permaweb/aoconnect npm package.

This module provides a Python interface to interact with Arweave and Permaweb
through the @permaweb/aoconnect package with real on-chain operations.
"""

import json
import subprocess
from typing import Any, Dict, List, Optional
from pathlib import Path


def check_npm_dependencies():
    """Check if npm and @permaweb/aoconnect are available"""
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
            subprocess.run(["npm", "install", "-g", "@permaweb/aoconnect"], check=True)
            print("✅ @permaweb/aoconnect installed successfully")
        else:
            print("✅ @permaweb/aoconnect is already installed")
            
    except subprocess.CalledProcessError:
        print("❌ npm not found. Please install Node.js from https://nodejs.org/")
        print("Then run: npm install -g @permaweb/aoconnect")
    except FileNotFoundError:
        print("❌ npm not found. Please install Node.js from https://nodejs.org/")
        print("Then run: npm install -g @permaweb/aoconnect")


class AOConnectWrapper:
    """
    Python wrapper for @permaweb/aoconnect using a Node.js bridge script.
    """
    def __init__(self, wallet_path: Optional[str] = None):
        self.wallet_path = wallet_path
        self.node_script = str(Path(__file__).parent / "node_scripts" / "ao_connect.js")
        
        # Check npm dependencies on initialization
        check_npm_dependencies()

    def _run_node(self, command: str, **kwargs) -> Dict[str, Any]:
        args = {"command": command}
        args.update(kwargs)
        proc = subprocess.run([
            "node", self.node_script, json.dumps(args)
        ], capture_output=True, text=True)
        try:
            return json.loads(proc.stdout)
        except Exception as e:
            return {"success": False, "error": f"Failed to parse output: {e}", "raw": proc.stdout}

    def create_wallet(self) -> Dict[str, Any]:
        return self._run_node("create_wallet")

    def spawn_process(self, source: str, tags: Optional[List[Dict[str, str]]] = None, scheduler: Optional[str] = None, data: Optional[str] = None) -> Dict[str, Any]:
        if not self.wallet_path:
            raise ValueError("wallet_path required for spawn_process")
        return self._run_node("spawn", jwkPath=self.wallet_path, source=source, tags=tags or [], scheduler=scheduler, data=data)

    def send_message(self, process_id: str, message: str, tags: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        if not self.wallet_path:
            raise ValueError("wallet_path required for send_message")
        return self._run_node("message", jwkPath=self.wallet_path, processId=process_id, message=message, tags=tags or [])

    def get_results(self, process_id: str, options: Optional[dict] = None) -> Dict[str, Any]:
        return self._run_node("results", processId=process_id, options=options or {})

    def get_single_result(self, process_id: str, message_id: str) -> Dict[str, Any]:
        return self._run_node("single_result", processId=process_id, messageId=message_id)

    def dryrun(self, process_id: str, data: str = "", tags: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        """Make a dryrun using the Node.js bridge (AO Connect library)."""
        return self._run_node("dryrun", processId=process_id, data=data, tags=tags or [])


# Convenience functions

def create_ao_connect(wallet_path: Optional[str] = None) -> AOConnectWrapper:
    return AOConnectWrapper(wallet_path)

def spawn_simple_process(source: str, wallet_path: str) -> Dict[str, Any]:
    wrapper = AOConnectWrapper(wallet_path)
    return wrapper.spawn_process(source)

def send_simple_message(process_id: str, message: str, wallet_path: str) -> Dict[str, Any]:
    wrapper = AOConnectWrapper(wallet_path)
    return wrapper.send_message(process_id, message) 