#!/usr/bin/env node

// AO Connect Node.js Bridge Script
// Usage: node ao_connect.js '{"command": "create_wallet"}'
//        node ao_connect.js '{"command": "spawn", "jwkPath": "wallet.json", "source": "..."}'
//        node ao_connect.js '{"command": "message", "jwkPath": "wallet.json", "processId": "...", "message": "..."}'

const fs = require('fs');
const path = require('path');
const aoconnect = require('@permaweb/aoconnect');

// Connect to testnet
const { result, results, message, spawn, monitor, unmonitor, dryrun } = aoconnect.connect({
  MU_URL: "https://mu.ao-testnet.xyz",
  CU_URL: "https://cu.ao-testnet.xyz", 
  GATEWAY_URL: "https://arweave.net",
});

async function main() {
  try {
    const input = process.argv[2];
    if (!input) throw new Error('No input JSON provided');
    const args = JSON.parse(input);
    let result;

    switch (args.command) {
      case 'create_wallet': {
        // Use arweave for JWK keygen
        const Arweave = require('arweave');
        const arweave = Arweave.init({});
        const jwk = await arweave.wallets.generate();
        const address = await arweave.wallets.jwkToAddress(jwk);
        const signer = aoconnect.createSigner(jwk);
        result = { success: true, wallet: { address, jwk } };
        break;
      }
      case 'spawn': {
        if (!args.jwkPath || !args.source) throw new Error('jwkPath and source required');
        const jwk = JSON.parse(fs.readFileSync(args.jwkPath, 'utf8'));
        const signer = aoconnect.createSigner(jwk);

        // Use 'source' as the module hash
        const spawnArgs = {
          module: args.source,
          signer
        };
        
        // Only add scheduler if explicitly provided
        if (args.scheduler) {
          spawnArgs.scheduler = args.scheduler;
        }

        const processId = await spawn(spawnArgs);
        result = { success: true, processId };
        break;
      }
            case 'message': {
        if (!args.jwkPath || !args.processId || !args.message) throw new Error('jwkPath, processId, and message required');
        const jwk = JSON.parse(fs.readFileSync(args.jwkPath, 'utf8'));
        const signer = aoconnect.createDataItemSigner(jwk);
        
        // Normalize tags
        let tags = args.tags || [];
        if (!Array.isArray(tags)) {
          tags = [];
        }
        const normalizedTags = tags.map(tag => {
          if (typeof tag === 'object' && tag !== null && 'name' in tag && 'value' in tag) {
            return { name: String(tag.name), value: String(tag.value) };
          }
          throw new Error('Invalid tag format: ' + JSON.stringify(tag));
        });



        const messageArgs = {
          signer,
          process: args.processId,
          data: args.message
        };
        if (normalizedTags.length > 0) {
          messageArgs.tags = normalizedTags;
        }

        const messageId = await message(messageArgs);
        result = { success: true, messageId };
        break;
      }
      case 'results': {
        if (!args.processId) throw new Error('processId required');
        const resultsArgs = {
          process: args.processId,
          ...args.options
        };
        const processResults = await results(resultsArgs);
        result = { success: true, results: processResults };
        break;
      }
      case 'single_result': {
        if (!args.processId || !args.messageId) throw new Error('processId and messageId required');
        const singleResult = await result({
          process: args.processId,
          message: args.messageId
        });
        result = { success: true, result: singleResult };
        break;
      }
      case 'dryrun': {
        if (!args.processId || !args.data) throw new Error('processId and data required');
        
        // Normalize tags
        let tags = args.tags || [];
        if (!Array.isArray(tags)) {
          tags = [];
        }
        const normalizedTags = tags.map(tag => {
          if (typeof tag === 'object' && tag !== null && 'name' in tag && 'value' in tag) {
            return { name: String(tag.name), value: String(tag.value) };
          }
          throw new Error('Invalid tag format: ' + JSON.stringify(tag));
        });

        const dryrunArgs = {
          process: args.processId,
          data: args.data
        };
        if (normalizedTags.length > 0) {
          dryrunArgs.tags = normalizedTags;
        }

        const dryrunResult = await dryrun(dryrunArgs);
        result = { success: true, result: dryrunResult };
        break;
      }
      default:
        throw new Error('Unknown command: ' + args.command);
    }
    process.stdout.write(JSON.stringify(result));
  } catch (error) {
    process.stdout.write(JSON.stringify({ success: false, error: error.message, stack: error.stack }));
    process.exit(1);
  }
}

main(); 