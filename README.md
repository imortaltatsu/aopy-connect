# AOConnect Python Backend

A robust, simple Python wrapper for interacting with AO Connect using Node.js bridges. This package is intended as a backend utility for higher-level AO Connect integrations (such as `pyaoconnect`).

## Installation

```bash
pip install git+https://github.com/imortaltatsu/aopy-connect.git
```

## Usage Example

```python
from aopy_connect.ao_connect_wrapper import AOConnectWrapper

# Initialize the wrapper
ao = AOConnectWrapper()

# Generate a wallet
wallet = ao.generate_wallet()
print("Wallet:", wallet)

# Spawn a process (replace with your process source)
process_id = ao.spawn_process(source="your_process_hash", tags=["MyApp"], scheduler="", data="")
print("Process ID:", process_id)

# Send a message
result = ao.send_message(process_id, "Hello AO!")
print("Message result:", result)

# Evaluate code
eval_result = ao.send_eval(process_id, "print('Hello from backend!')")
print("Eval result:", eval_result)

# Read results
results = ao.read_results(process_id)
print("Results:", results)

# Dry run
dry_run_result = ao.dry_run(process_id, "print('Test!')")
print("Dry run:", dry_run_result)
```

## Requirements
- Python 3.7+
- Node.js (for the underlying AO Connect bridge)
- npm package `@permaweb/aoconnect` (installed automatically during package installation)

## Features
- Simple Python interface to AO Connect
- Wallet generation and management
- Process spawning and messaging
- Code evaluation and result reading
- Dry run/testing support

## License
MIT License - Use it however you want! 