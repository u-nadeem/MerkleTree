import hashlib
import pandas as pd
import json
import merkletools
import time


#*** Class for coloring the output for better visiuals
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


# *** Reading data from a csv file into dataframes.
data = pd.read_csv('Tweets_500.csv', usecols=['text', 'time', 'hashed_value'])
pd.DataFrame(data)
#*** Adding data from columns to Lists
messageList = data['text'].tolist()
timeList = data['time'].tolist()
HashList = data['hashed_value'].tolist()

# ***   ***     ***     ***     ***     ***     ***
# ***
# *** Our merkle tree implementation.
# ***
# ***   ***     ***     ***     ***     ***     ***


# *** Hashing values of all three columns in the csv file.
def hashing(messageList, timeList, HashList):
    for i, row in data.iterrows():
        # *** Hashes text and date, then store's the hash value in hashed_value column.
        if i == 0:
            val1 = hashlib.sha256(json.dumps(messageList[i]).encode('UTF-8')).hexdigest()
            curr_time = time.ctime()
            #obj = time.gmtime(0)
            #epoch = time.asctime(obj)
            data.loc[i, 'time'] = curr_time
            data.to_csv('Tweets_500.csv')
            val2 = hashlib.sha256(json.dumps(timeList[i]).encode('UTF-8')).hexdigest()
            join_hash = val1 + val2
            double_hash = str(hashlib.sha256(json.dumps(join_hash).encode('UTF-8')).hexdigest())
            data.loc[i, 'hashed_value'] = double_hash
            data.to_csv('Tweets_500.csv')
        # *** Hashes text,date,concatenate the hashes of text, date and the previous hash.
        # *** Then calculates the hash of concatenated string, and store's the hash value in hashed_value column.
        if i != 0:
            val1 = hashlib.sha256(json.dumps(messageList[i]).encode('UTF-8')).hexdigest()
            curr_time = time.ctime()
            #obj = time.gmtime(0)
            #epoch = time.asctime(obj)
            data.loc[i, 'time'] = curr_time
            data.to_csv('Tweets_500.csv')
            val2 = hashlib.sha256(json.dumps(timeList[i]).encode('UTF-8')).hexdigest()
            val3 = str(HashList[i - 1])
            join_hash = val1 + val2
            double_hash = str(hashlib.sha256(json.dumps(join_hash).encode('UTF-8')).hexdigest())
            data.loc[i, 'hashed_value'] = double_hash
            data.to_csv('Tweets_500.csv')

    return HashList


# *** creates a copy of the hashed list.
def copyHashString ( HashList ):
    HashList_copy = []
    HashList_copy = HashList.copy()
    return HashList_copy


# *** creates a merkle tree.
def merkleTree( HashList):
    leaves = len(HashList)
    if leaves == 1:
        return HashList[0]
    if leaves % 2 == 1:
        HashList.append(HashList[-1])
        leaves += 1
    parent_hashes = []
    for i in range(0, leaves, 2):
        combined_hash = HashList[i] + HashList[i + 1]
        parent_hash = hashlib.sha256(json.dumps(combined_hash).encode('UTF-8')).hexdigest()
        parent_hashes.append(parent_hash)
    if len(parent_hashes) == 1:
        return parent_hashes[0]
    else:
        return merkleTree(parent_hashes)

# *** checking if the tree is valid or not.
def validation(m_root,HashList):
    RM = merkleTree(HashList)
    if RM == m_root:
        print(color.BOLD + '\033[93m' + "Merkle Tree is valid." + color.END)
        print('\033[95m' + "Merkle Tree recalculated root:" + color.END, RM)
    else:
        print(color.BOLD + '\033[91m' + "Merkle Tree is in invalid." + color.END)
        print('\033[95m' + "Merkle Tree recalculated root:" + color.END, RM)
    return RM

def My_Algo(messageList, timeList, HashList):
    start_time = time.time()
    h = hashing(messageList, timeList, HashList)
    m = merkleTree(h)
    print(color.BOLD + '\033[96m ' + "Total execution of Proposed MT: --- %s seconds ---" % (time.time() - start_time) + color.END)
    print(color.BOLD + '\033[94m' + "Merkle tree root: " + color.END, m)
    validation(m, h)
    print(color.BOLD + '\033[93m' + "-----------------------------------------" + color.END)
    print(data)




# ***   ***     ***     ***     ***     ***     ***
# ***
# *** Using Python's Builtin Merkle tree function.
# ***
# ***   ***     ***     ***     ***     ***     ***

def Python_MT (HashList_copy):
    start_time = time.time()
    mTree = merkletools.MerkleTools(hash_type='sha256')
    # Adding the hashed input from the file to the tree.
    for j, row in data.iterrows():
        mTree.add_leaf(str(HashList_copy[j]), True)
    mTree.make_tree()
    Tree_there = mTree.is_ready
    if Tree_there == True:
        mt_root = mTree.get_merkle_root()
        print("Merkle Tree Root:", mt_root)
    else:
        proof = mTree.get_proof(1)
        print(proof)
    # Prove and verify tree
    check_valid = mTree.validate_proof(mTree.get_proof(1), mTree.get_leaf(1), mt_root)
    print("Verification: ", check_valid)
    print(color.BOLD + '\033[96m ' + "Total execution time of Python's MT: --- %s seconds ---" % (time.time() - start_time) + color.END)


def main():
    print(color.BOLD + '\033[93m' + "*** ----------------------------------------- ***" + color.END)
    print(color.BOLD + '\033[94m' + "*** Our merkle tree implementation. ***" + color.END)
    print(color.BOLD + '\033[93m' + "*** ----------------------------------------- ***" + color.END)
    My_Algo(messageList, timeList, HashList)
    print(color.BOLD + '\033[93m' + "*** ----------------------------------------- ***" + color.END)
    print(color.BOLD + '\033[94m' + "*** Using Python's Builtin Merkle tree function. ***" + color.END)
    print(color.BOLD + '\033[93m' + "*** ----------------------------------------- ***" + color.END)
    Python_MT(HashList)


if __name__ == "__main__":
    main()