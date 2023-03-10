from web3 import Web3
from web3.middleware import geth_poa_middleware
import json
from eth_account import Account

w3 = Web3(Web3.HTTPProvider(''))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

private_key = ''
print('####################')
print('Private Key : ', private_key)
account = Account.from_key(private_key)
print('Account Address : ', account.address)
print('Account Balance : ', w3.eth.getBalance(account.address))
print('####################')

signedTransaction = w3.eth.account.sign_transaction(dict(nonce=w3.eth.getTransactionCount(account.address), gas=100000, maxFeePerGas = 3000000000, maxPriorityFeePerGas = 3000000000, to='0x8be81A53955a7E65822C19752cc3ed8fCeEd1a60', value=w3.toWei(0.001, 'ether'), data=b'first Transaction From Web3py', chainId=5, type=1), private_key)

print('####################')
print(signedTransaction)
print('####################')

w3.eth.sendRawTransaction(signedTransaction.rawTransaction)
print(w3.eth.waitForTransactionReceipt(signedTransaction.hash, 500))
