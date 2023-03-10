from web3 import Web3
from web3.middleware import geth_poa_middleware
import json
from eth_account import Account
import sha3

w3 = Web3(Web3.HTTPProvider(''))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

private_key = ''
print('####################')
print('Private Key : ', private_key)
account = Account.from_key(private_key)
print('Account Address : ', account.address)
print('Account Balance : ', w3.eth.getBalance(account.address))
print('####################')

contractAddress = '0x1781EFc998AFE084c8277dE9914372d57b767830'
with open('./NantoToken.json') as f:
    abi = json.load(f)

nantoTokenCa = w3.eth.contract(address=contractAddress, abi=abi)
print('####################')
print('Contract Address : ', contractAddress)
print('Symbol : ', nantoTokenCa.functions.symbol().call())
print('Owner Balance : ', nantoTokenCa.functions.balanceOf(account.address).call())

# txid = nantoTokenCa.functions.transfer('0x8be81A53955a7E65822C19752cc3ed8fCeEd1a60', 1000000000000).transact({'from': account.address})
# w3.eth.waitForTransactionReceipt(txid, 500)

k256=sha3.keccak_256()
k256.update('transfer(address,uint256)'.encode())
method_id = "0x" + k256.hexdigest()
to_hex = "8be81A53955a7E65822C19752cc3ed8fCeEd1a60".zfill(64)
value_hex = "{:064x}".format(100000000)
data = method_id[:10] + to_hex+ value_hex

print('####################')
print('Input data : ', data)
print('####################')

signedTransaction = w3.eth.account.sign_transaction(dict(
    nonce=w3.eth.getTransactionCount(account.address),
    gas=100000, 
    maxFeePerGas = 3000000000, 
    maxPriorityFeePerGas = 3000000000, 
    to='0x8be81A53955a7E65822C19752cc3ed8fCeEd1a60', 
    value=0, 
    data=data, 
    chainId=5, 
    type=2), 
    private_key)

print('####################')
print(signedTransaction)
print('####################')

w3.eth.sendRawTransaction(signedTransaction.rawTransaction)
print(w3.eth.waitForTransactionReceipt(signedTransaction.hash, 500))