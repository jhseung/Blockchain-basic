import hashlib
import json
from time import time
from urllib.parse import urlparse

class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.nodes = set()

        #Create Genesis Block
        self.new_block(previous_hash=1, proof=100)

    def register_node(self, address):
        """
        Add a new node to this Blockchain

        :param address: <str> address of node
        :return: None
        """
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def new_block(self, proof, previous_hash=None):
        #create a new Block and add it to chain

        """
        Create a new Block in the Blockchain

        :param proof: <int> proof given by PoW algorithm
        :param previous_hash: (optional) <str> hash of previous Block
        :return: <dict> New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.chain.append(block)

        return block

    def new_transaction(self, sender, recipient, amount):
        #Add new transaction to list of transactions

        """
        new transaction to go into next mined Block

        :param sender: <str> address of the sender
        :param recipient: <str> address of the recipient
        :param amount: <int> amount
        :return: <int> the index of the block that will hold this transaction
        """

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1


    @staticmethod
    def hash(block):
        """
        Create a SHA-256 hash of a Block

        :param block: <dict> Block
        :return: <str>
        """
        #Order dictionary, or we'll have inconsistent hashes
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()


    @property
    def last_block(self):
        #returns the last block in the chain
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        """
        Does the necessary work to mine a block.
        :param previous_proof: <int> proof of previous block
        :return: <int> proof of current block
        """
        proof = 0

        while not self.is_valid_proof(previous_proof, proof):
            proof += 1

        return proof

    def resolve_conflict(self):
        """
        Consense Algorithm for determining correct chain
        :return: <bool> True if our chain replaced, False if not
        """
        

    def is_valid_chain(self, chain):
        """
        Determines if given blockchain is valid
        :param chain: <list> a blockchain
        :return: <bool> True if valid, False if not
        """

        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            if block["previous_hash"] != self.hash(last_block):
                return False

            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True

    def is_valid_proof(self, previous_proof, proof):
        """
        Validates whether the proof is valid or not.
        :param previous_proof: <int> proof of previous block
        :param proof: <int> proposed proof of current block
        :return: <bool> true if valid, false if not
        """

        guess = '{}{}'.format(previous_proof, proof).encode()
        hashed_guess = hashlib.sha256(guess).hexdigest()

        return hashed_guess[:4] == "0000"
