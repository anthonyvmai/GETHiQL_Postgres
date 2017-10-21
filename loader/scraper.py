import json
import cache
import requests
import binascii
import ethereum.abi
from web3 import Web3
from web3 import HTTPProvider
from datetime import datetime

""" Web3 instance  """
web3 = Web3(HTTPProvider('https://mainnet.infura.io/ca7IawBlNfcOgnr7nRpy'))

""" Loads information about block with the given number """
def load_block(block_number):
    block = web3.eth.getBlock(block_number)
    return {
        "block_number": block["number"],
        "block_time": datetime.utcfromtimestamp(block["timestamp"]),
        "gas_limit": block["gasLimit"],
        "gas_used": block["gasUsed"],
        "difficulty": block["difficulty"],
        "total_difficulty": block["totalDifficulty"],
        "block_hash": block["hash"],
        "parent_block_hash": block["parentHash"],
        "miner": block["miner"],
        "size": block["size"],
        "nonce": block["nonce"],
        "transactions_root": block["transactionsRoot"],
        "state_root": block["stateRoot"],
        "receipts_root": block["receiptsRoot"],
        "transactions": block["transactions"],
        "transactions_count": len(block["transactions"]),
        "uncles_count": len(block["uncles"])
    }

""" Loads information about transaction with the given hash """
def load_transaction(tx_hash):
    tx = web3.eth.getTransaction(tx_hash)
    tx_r = web3.eth.getTransactionReceipt(tx_hash)
    return {
        "block_number": tx_r["blockNumber"],
        "transaction_hash": tx_hash,
        "transaction_index": tx["transactionIndex"],
        "from_addr": tx["from"],
        "to_addr": tx["to"],
        "value": tx["value"],
        "input": tx["input"],
        "gas_limit": tx["gas"],
        "gas_used": tx_r["gasUsed"],
        "gas_price": tx["gasPrice"],
        "nonce": tx["nonce"],
        "cumulative_gas_used": tx_r["cumulativeGasUsed"],
        "created_contract_address": tx_r["contractAddress"],
        "logs_count": len(tx_r["logs"]),
        "logs": list(_format_logs(tx_r["logs"], tx_hash))
        # "logs": tx_r["logs"]
    }

""" Loads and caches the ABI for the given address (if exists) """
def load_abi(address):
    res = requests.get(
        "http://api.etherscan.io/api"
        + "?module=contract"
        + "&action=getabi"
        + "&address={}".format(address)
    )
    abi = res.json().get("result", None)
    if (abi is None) or (len(abi) < 2):
        return None
    return json.loads(abi)

""" Makes a ContractTranslator object at the given address """
def get_contract_translator(address):
    key = "ct:{}".format(address)
    if cache.has_key(key):
        ct = cache.get(key)
    else:
        abi = load_abi(address)
        if (abi is not None) and (len(abi) > 1):
            ct = ethereum.abi.ContractTranslator(abi)
        else:
            ct = None
        cache.set(key, ct)
    return ct

""" Maps logs from transaction receipt into nice format """
def _format_logs(tx_logs, tx_hash):
    for log in tx_logs:
        address = log["address"]
        ct = get_contract_translator(address)
        if ct is not None:
            log_topics = [int(t, 0) for t in log["topics"]]
            log_data   = binascii.unhexlify(log["data"][2:])
            try:
                decoded = ct.decode_event(log_topics, log_data)
                yield {
                    "tx_hash": tx_hash,
                    "contract_address": address,
                    "log_index": log["logIndex"],
                    "name": decoded["_event_type"].decode(),
                    "json": json.dumps({k: _map_bin(v) for k, v in decoded.items() if k != "_event_type"})
                }
            except:
                print("Couldn't decode event at index <{}> in tx <{}>".format(log["logIndex"], tx_hash))

def _map_bin(val):
    if type(val) is bytes:
        return "0x" + binascii.hexlify(val).decode()
    return val
