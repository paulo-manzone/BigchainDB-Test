# importar driver
from bigchaindb_driver import BigchainDB
bdb_root_url = 'https://test.bigchaindb.com'
bdb = BigchainDB(bdb_root_url)

# gerar keypair
from bigchaindb_driver.crypto import generate_keypair
sementille, humberto = generate_keypair(), generate_keypair()

# criar a estrutura do asset
acao = {
    'data': {
        'acao_da': {
            'Empresa_Nilceu_CIA': {
                'valor': '1/30 do valor da empresa',
                'emissao': '20/11/2018'
            }
        },
        'description': 'Ação da empresa Nilceu CIA ',
    },
}

# Preparando Transação Create
prepared_token_tx = bdb.transactions.prepare(
    operation='CREATE',
    signers=sementille.public_key,
    recipients=[([humberto.public_key], 10)],
    asset=acao)

# assinando e enviando
fulfilled_token_tx = bdb.transactions.fulfill(
    prepared_token_tx,
    private_keys=sementille.private_key)
bdb.transactions.send_commit(fulfilled_token_tx)

print('Humberto:', humberto.public_key)
print('Sementille:', sementille.public_key)
print ('ID da transacao:', fulfilled_token_tx['id'])

# Transferindo ações
# Criando input e output
transfer_asset = {'id': fulfilled_token_tx['id']}
output_index = 0
output = fulfilled_token_tx['outputs'][output_index]
transfer_input = {'fulfillment': output['condition']['details'],
                  'fulfills': {'output_index': output_index,
                               'transaction_id': transfer_asset['id']},
                  'owners_before': output['public_keys']}

# Preparando Transação Transfer
prepared_transfer_tx = bdb.transactions.prepare(
    operation='TRANSFER',
    asset=transfer_asset,
    inputs=transfer_input,
    recipients=[([sementille.public_key], 5), ([humberto.public_key], 5)])

# Assinando e Enviando a Transação
fulfilled_transfer_tx = bdb.transactions.fulfill(
    prepared_transfer_tx,
    private_keys=humberto.private_key)
sent_transfer_tx = bdb.transactions.send_commit(fulfilled_transfer_tx)



print('\nID do Transfer:', sent_transfer_tx['id'])