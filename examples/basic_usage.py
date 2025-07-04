from aopy_connect.ao_connect_wrapper import AOConnectWrapper

def main():
    ao = AOConnectWrapper()
    wallet = ao.generate_wallet()
    print("Wallet:", wallet)

    # Replace with your process source
    process_id = ao.spawn_process(source="your_process_hash", tags=["MyApp"], scheduler="", data="")
    print("Process ID:", process_id)

    result = ao.send_message(process_id, "Hello AO!")
    print("Message result:", result)

    eval_result = ao.send_eval(process_id, "print('Hello from backend!')")
    print("Eval result:", eval_result)

    results = ao.read_results(process_id)
    print("Results:", results)

    dry_run_result = ao.dry_run(process_id, "print('Test!')")
    print("Dry run:", dry_run_result)

if __name__ == "__main__":
    main() 