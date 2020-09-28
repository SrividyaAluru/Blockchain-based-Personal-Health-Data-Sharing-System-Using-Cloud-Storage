import datetime
import sys
import time
import boto3
from Block import Block
from Transaction import Transaction
from User import User


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 5
        self.pending_transactions = []

    @staticmethod
    def create_genesis_block():
        return Block(datetime.datetime.now(), "Genesis Block", "0")

    def mine_pending_transactions(self, miner):
        latest_block = self.chain[-1]
        new_block = Block(datetime.datetime.now(), self.pending_transactions, latest_block.hash)
        new_block.mine_block(self.difficulty, miner)

        for trans in self.pending_transactions:
            new_block.transactions.append(trans)
        self.chain.append(new_block)
        self.pending_transactions = []

    def verify_chain(self):
        for i in range(1, len(self.chain)):
            curr_block = self.chain[i]
            prev_block = self.chain[i - 1]

            if curr_block.calculate_hash() != curr_block.hash or curr_block.prev_hash != prev_block.hash:
                # 1st cond : Checks current block's integrity
                # 2nd cond : If a user changes data of a block and calls calculate_hash(), the previous condn cannot
                print("\n********Blockchain corrupted.*************")
                return False

        print("\n********Blockchain secure and verified.*************")
        return True
        # catch it , but this condition catches it
        
    def add_data(self,description, cost, user):
        trans_obj = Transaction(description, cost, user)
        if trans_obj.verify_transaction():
            self.pending_transactions.append(trans_obj)
        else:
            print("Error")

    def print_details(self):
        for block in self.chain[1:]:
            print("\n")
            print(block)
            print("\nTransactions in block:")
            for trans in block.transactions:
                print(trans.description)
                #table = dynamodb.Table(trans.table_name)
                #print(table.scan())
                #print("\n")

    def purchase_data(self, user):
        print(
            "***************************************************************************************************************************************************************************************")
        print("\nID \t\t   Cost \t\t Description")
        data_cost = {}
        for block in self.chain:
            for transaction in block.transactions:
                data_cost[transaction.transaction_id] = transaction.data_cost
                print("Transaction ID : "+transaction.transaction_id)
                print("Cost : $" + str(transaction.data_cost))
                print(transaction.description)
                print("\n")
        print("\nEnter ID of the data you would like to buy: ")
        #option = input().strip()
        option = raw_input()
        while option not in data_cost.keys():
            print("Please enter from the available options only.")
            #option = input().strip()
            option = raw_input()
        print("Please wait while the transaction is completed")
        for _ in range(10):
            print("*")
            sys.stdout.flush()
            time.sleep(0.5)
        print("\nTransaction success!!")

        for block in self.chain:
            for transaction in block.transactions:
                if transaction.transaction_id == option:
                    user.purchases.append(transaction)
                    break


if __name__ == "__main__":
    #dynamodb = boto3.resource('dynamodb', 'us-east-2')

    blockchain = Blockchain()


    user1 = User()
    user2 = User()

    print("Adding Transaction 1 ........")
    blockchain.add_data("MRI reports of 3rd grade ankle sprains.", 60, user1)
    print("***************************************************************************")
    print("Mining block....")
    blockchain.mine_pending_transactions(user1)
    print("Finished mining.")
    print("***************************************************************************")
    print("Adding transaction 2 ........")
    blockchain.add_data("MRI reports of meniscus tears.", 60, user1)
    print("***************************************************************************")
    print("Mining block Please wait....")
    blockchain.mine_pending_transactions(user1)
    print("Finished mining.")
    print("***************************************************************************")
    print("Adding transaction 3 ........")
    blockchain.add_data("MRI reports of ACL tears.", 70, user1)
    print("***************************************************************************")
    print("Mining block Please wait....")
    blockchain.mine_pending_transactions(user1)
    print("Finished mining.")
    print("***************************************************************************")
    print("Adding transaction 4 ........")
    blockchain.add_data("MRI reports of ATFL tears.", 80, user1)
    print("***************************************************************************")
    print("Mining block Please wait....")
    blockchain.mine_pending_transactions(user1)
    print("Finished mining.")
    print("***************************************************************************")

    print("Blockchain details: ")
    blockchain.print_details()
    blockchain.verify_chain()
    blockchain.purchase_data(user2)
    blockchain.purchase_data(user2)
    print(
        "*********************************************************************************************************************************")
    print("_______________________________________________________________________________________________________________________________")
    print("User1's details:")
    user1.view_user(blockchain)
    print("_______________________________________________________________________________________________________________________________")
    print("User2's details:")
    user2.view_user(blockchain)
