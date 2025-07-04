import os
import json
import pytest
from aopy_connect import AOConnectWrapper

WALLET_PATH = 'wallet.json'
PROCESSES_FILE = 'processes.json'

PROCESS_HASH = 'JArYBF-D8q2OmZ4Mok00sD2Y_6SYEQ7Hjx-6VZ_jl3g'

def test_create_wallet():
    wrapper = AOConnectWrapper()
    result = wrapper.create_wallet()
    print('Wallet creation result:', result)
    assert result['success']
    assert 'address' in result['wallet']
    assert 'jwk' in result['wallet']
    # Save the JWK for other tests
    with open(WALLET_PATH, 'w') as f:
        json.dump(result['wallet']['jwk'], f)
    print('Saved wallet.json')

@pytest.mark.skipif(not os.path.exists(WALLET_PATH), reason='wallet.json not found; run wallet creation first.')
def test_spawn_process():
    wrapper = AOConnectWrapper(WALLET_PATH)
    tags = [
        {"name": "Authority", "value": "fcoN_xJeisVsPXA-trzVAuIiqO3ydLQxM-L4XbrQKzY"},
        {"name": "Another-Tag", "value": "another-value"},
    ]
    scheduler = "_GQ33BkPtZrqxA84vM8Zk-N2aO0toNNu_C-l-rawrBA"  # Example scheduler address
    data = "optional initial data"
    result = wrapper.spawn_process(PROCESS_HASH, tags=tags, scheduler=scheduler, data=data)
    print('Spawn process result:', result)
    assert result['success']
    process_id = result.get('processId') or result.get('result', {}).get('processId')
    assert process_id
    # Save process_id for next test
    processes_data = {
        "spawned_processes": [process_id],
        "current_process": process_id
    }
    with open(PROCESSES_FILE, 'w') as f:
        json.dump(processes_data, f, indent=2)

@pytest.mark.skipif(not os.path.exists(WALLET_PATH) or not os.path.exists(PROCESSES_FILE), reason='wallet.json or processes.json not found; run previous tests first.')
def test_send_message():
    wrapper = AOConnectWrapper(WALLET_PATH)
    with open(PROCESSES_FILE) as f:
        processes_data = json.load(f)
        process_id = processes_data["current_process"]
    tags = [
        {"name": "Your-Tag-Name-Here", "value": "your-tag-value"},
        {"name": "Another-Tag", "value": "another-value"},
    ]
    data = "any data"
    result = wrapper.send_message(process_id, data, tags=tags)
    print('Send message result:', result)
    assert result['success']
    assert 'messageId' in result

@pytest.mark.skipif(not os.path.exists(PROCESSES_FILE), reason='processes.json not found; run previous tests first.')
def test_get_results():
    wrapper = AOConnectWrapper()
    with open(PROCESSES_FILE) as f:
        processes_data = json.load(f)
        process_id = processes_data["current_process"]
    result = wrapper.get_results(process_id)
    print('Get results:', result)
    assert result['success']
    assert 'results' in result
    assert 'edges' in result['results']
    assert isinstance(result['results']['edges'], list)

@pytest.mark.skipif(not os.path.exists(WALLET_PATH) or not os.path.exists(PROCESSES_FILE), reason='wallet.json or processes.json not found; run previous tests first.')
def test_send_eval_message():
    wrapper = AOConnectWrapper(WALLET_PATH)
    with open(PROCESSES_FILE) as f:
        processes_data = json.load(f)
        process_id = processes_data["current_process"]
    tags = [
        {"name": "Action", "value": "Eval"},
    ]
    data = "print('hello from eval!')"
    result = wrapper.send_message(process_id, data, tags=tags)
    print('Send eval message result:', result)
    assert result['success']
    assert 'messageId' in result

@pytest.mark.skipif(not os.path.exists(PROCESSES_FILE), reason='processes.json not found; run previous tests first.')
def test_read_results():
    wrapper = AOConnectWrapper()
    with open(PROCESSES_FILE) as f:
        processes_data = json.load(f)
        process_id = processes_data["current_process"]
    
    # Test fetching multiple results
    result = wrapper.get_results(process_id, options={
        "sort": "ASC",
        "limit": 25
    })
    print('Read results:', result)
    assert result['success']
    assert 'results' in result
    assert 'edges' in result['results']
    assert isinstance(result['results']['edges'], list)
    
    # If we have results, test reading a single result
    if result['results']['edges'] and len(result['results']['edges']) > 0:
        first_result = result['results']['edges'][0]['node']
        print('First result node:', first_result)
        assert 'Output' in first_result or 'Messages' in first_result or 'Spawns' in first_result 

@pytest.mark.skipif(not os.path.exists(PROCESSES_FILE), reason='processes.json not found; run previous tests first.')
def test_dryrun():
    wrapper = AOConnectWrapper(WALLET_PATH)
    with open(PROCESSES_FILE) as f:
        processes_data = json.load(f)
        process_id = processes_data["current_process"]
    
    # Test Node.js bridge dryrun
    result = wrapper.dryrun(process_id, "test data", [{"name": "Action", "value": "Balance"}])
    print('Dryrun result:', result)
    assert 'success' in result
    if result.get('success'):
        print('Result keys:', list(result.get('result', {}).keys())) 