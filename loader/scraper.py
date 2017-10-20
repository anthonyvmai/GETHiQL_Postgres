import cache
import requests
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
        "logs": tx_r["logs"] #  _format_logs(tx_r["logs"])
    }

""" Loads and caches the ABI for the given address (if exists) """
def load_abi(address):
    key = "abi:{}".format(address)
    abi = cache.get(key)
    if abi is None:
        res = requests.get(
            "http://api.etherscan.io/api"
            + "?module=contract"
            + "&action=getabi"
            + "&address={}".format(address)
        )
        abi = res.json().get("result", None)
        cache.set(key, abi)
    return abi

""" Makes a web3 contract object at the given address """
def make_contract(address):
    return web3.eth.contract(
        abi=load_abi(address),
        address=address
    )

""" Maps logs from transaction receipt into nice format """
def _format_logs(tx_logs):
    safe_get = lambda xs, i: xs[i] if i < len(xs) else None
    return [{
        "address": l["address"],
        "log_index": l["logIndex"],
        "data": l["data"],
        "topic_one": safe_get(l["topics"], 0),
        "topic_two": safe_get(l["topics"], 1),
        "topic_three": safe_get(l["topics"], 2),
        "topic_four": safe_get(l["topics"], 3)
    } for l in tx_logs]
