import pandas as pd
import hashlib
import time
start_time = time.time()

# *** Reading data from a csv file into dataframes.
data = pd.read_csv('sample_txt.csv', usecols=['text', 'date', 'hashed_value'])
pd.DataFrame(data)
# data to List
messageList = data['text'].tolist()
dateList = data['date'].tolist()
HashList = data['hashed_value'].tolist()


# *** Hash Function
def my_hash(val):
    calculatedHash = hashlib.sha256(repr(val).encode('UTF-8')).hexdigest()
    return calculatedHash


# *** Concatinating the hashes
def dataHash(messageList, dateList, HashList):
    for i, row in data.iterrows():
        if len(HashList) == ' ':
            hashVal1 = my_hash(messageList[i])
            hashVal2 = my_hash(dateList[i])
            join_hash = hashVal1 + hashVal2
            #HashList[i].append(join_hash)
            data.loc[HashList[i], 'hashed_value'] = join_hash
            data.to_csv('sample_txt.csv')
        else:
            hashVal1 = my_hash(messageList[i])
            hashVal2 = my_hash(dateList[i])
            hashVal3 = str(my_hash(HashList[i - 1]))
            join_hash = hashVal1 + hashVal2 + hashVal3
            #HashList[i].append(join_hash)
            data.loc[HashList[i], 'hashed_value'] = join_hash
            data.to_csv('sample_txt.csv')
    return HashList





def PrintHashList(HashList):
    print("-------------------------------------")
    print(len(HashList))
    for j in range(0, len(HashList)):
        print("Concatenated Hashed List Values: ", HashList[j])
        print("\n")
    print("-------------------------------------")
    for g in range(len(messageList)):
        print("Actual CSV list values: ", messageList[g])
        print(dateList[g])


def main():
    dataHash(messageList, dateList, HashList)
    PrintHashList(HashList)
    print("--- %s seconds ---" % (time.time() - start_time))
    print(data)



if __name__ == "__main__":
    main()
