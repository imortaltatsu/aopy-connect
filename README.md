# AO Connect Python Backend - Cloning Guide

A robust Python wrapper for AO Connect using Node.js bridges. This guide will help you clone, set up, and use the repository.

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/imortaltatsu/aopy-connect.git
cd aopy-connect
```

### 2. Install Dependencies
```bash
# Install Python package
pip install -e .

# Install npm dependencies (required)
npm install -g @permaweb/aoconnect
```

### 3. Verify Installation
```python
from aopy_connect import AOConnectWrapper
print("✅ Package imported successfully!")
```

## Installation Methods

### Method 1: Direct Git Clone (Development)
```bash
git clone https://github.com/imortaltatsu/aopy-connect.git
pip install aopy-connect
```


### Method 3: Local Development Setup
```bash
git clone https://github.com/imortaltatsu/aopy-connect.git
cd aopy-connect
pip install -e .
npm install -g @permaweb/aoconnect
```

## Requirements

- **Python 3.7+**
- **Node.js** (for AO Connect bridge)
- **npm package `@permaweb/aoconnect`**

## Usage Example

```python
from aopy_connect import AOConnectWrapper

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

## Project Structure

```
aopy-connect/
├── setup.py                    # Package configuration
├── pyproject.toml             # Build configuration
├── README.md                  # This file
├── LICENSE                    # MIT License
├── aopy_connect/              # Main package
│   ├── __init__.py           # Package initialization
│   ├── ao_connect_wrapper.py # Main wrapper class
│   └── node_scripts/         # Node.js bridge scripts
├── examples/                  # Usage examples
├── tests/                     # Test files
└── node_scripts/             # Node.js scripts
```

## Development Setup

### 1. Clone and Setup
```bash
git clone https://github.com/imortaltatsu/aopy-connect.git
cd aopy-connect
```

### 2. Install in Development Mode
```bash
pip install -e .
```

### 3. Install npm Dependencies
```bash
npm install -g @permaweb/aoconnect
```

### 4. Run Tests
```bash
python -m pytest tests/
```

### 5. Run Examples
```bash
python examples/basic_usage.py
```

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'aopy_connect'**
   - Make sure you're in the correct directory
   - Try: `pip install -e .`

2. **npm not found**
   - Install Node.js from https://nodejs.org/
   - Then run: `npm install -g @permaweb/aoconnect`

3. **@permaweb/aoconnect not found**
   - Run: `npm install -g @permaweb/aoconnect`

### Verification Commands

```bash
# Check Python package
python -c "import aopy_connect; print('✅ Python package OK')"

# Check npm
npm --version

# Check AO Connect
npm list -g @permaweb/aoconnect
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Test: `python -m pytest tests/`
5. Commit: `git commit -m "Add feature"`
6. Push: `git push origin feature-name`
7. Create a Pull Request

## License

MIT License - Use it however you want!

## Support

- **Issues**: https://github.com/imortaltatsu/aopy-connect/issues
- **Repository**: https://github.com/imortaltatsu/aopy-connect 