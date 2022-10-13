import numpy as np
import pandas as pd
import pathlib
import re


# Here, I'm replicating the same code that the challenge winners [made available here](https://github.com/salilkanitkar/responsible_ai_hackathon/blob/master/dataset/ADS_Dataset_generator_2.ipynb).

# Global constants
g_userPart1PathPrefix = "../../data/ads16-dataset/ADS16_Benchmark_part1/ADS16_Benchmark_part1/Corpus/Corpus/"
g_userPart2PathPrefix = "../../data/ads16-dataset/ADS16_Benchmark_part2/ADS16_Benchmark_part2/Corpus/Corpus/"
g_userIdPrefix = "U0"

g_adsPart1PathPrefix = "../../data/ads16-dataset/ADS16_Benchmark_part1/ADS16_Benchmark_part1/Ads/Ads/"
g_adsPart2PathPrefix = "../../data/ads16-dataset/ADS16_Benchmark_part2/ADS16_Benchmark_part2/Ads/Ads/"


def generate_data_User( pathPrefix, userId ):
    completePath = pathPrefix + userId + "/"
    
    # INF
    infFile = userId + "-INF.csv"
    userInf_df = pd.read_csv(completePath + infFile, delimiter=";")
    
    # Pref
    prefFile = userId + "-PREF.csv"
    userPref_df = pd.read_csv(completePath + prefFile, delimiter=";")
    
    user_df = pd.concat([userInf_df, userPref_df], axis=1)
    
    # Pos
    posFile = userId + "-IM-POS.csv"
    userPos_df = pd.read_csv(completePath + posFile, delimiter=";")
    userPos_df = userPos_df.iloc[1:]
    userPos_df.reset_index(drop=True, inplace=True)
    user_df = pd.concat([user_df, userPos_df], axis=1)

    # Neg
    negFile = userId + "-IM-NEG.csv"
    userNeg_df = pd.read_csv(completePath + negFile, delimiter=";")
    userNeg_df = userNeg_df.iloc[1:]
    userNeg_df.reset_index(drop=True, inplace=True)
    user_df = pd.concat([user_df, userNeg_df], axis=1)

    user_df.insert(0, "UserId", userId, True)
    # user_df = user_df.set_index('UserId')
    # user_df.info()
    
    return user_df


def generate_data_partUsers( usersPartPathPrefix, startRange, endRange ):
    partUsers_df = pd.DataFrame()
    
    for i in range(startRange, endRange):
        thisUserIdNum = str(i)
        thisUserId = g_userIdPrefix + thisUserIdNum.zfill(3)
        # print(thisUserId)
        thisUser_df = generate_data_User(usersPartPathPrefix, thisUserId)
        partUsers_df = partUsers_df.append(thisUser_df, sort=True)
        partUsers_df.set_index('UserId')
        
    return partUsers_df


def generate_data_allUsers():
    allUsers_df = pd.DataFrame()

    part1Users_df = generate_data_partUsers(g_userPart1PathPrefix, 1, 61)
    allUsers_df = allUsers_df.append(part1Users_df, sort=True)

    part2Users_df = generate_data_partUsers(g_userPart2PathPrefix, 61, 121)
    allUsers_df = allUsers_df.append(part2Users_df, sort=True)

    return allUsers_df


def generate_data_adCats():
    adCatsLst = [['01', "Clothing & Shoes", 16],
                 ['02', "Automotive", 15],
                 ['03', "Baby Products", 15],
                 ['04', "Health & Beauty", 15],
                 ['05', "Media (BMVD)", 15],
                 ['06', "Consumer Electronics", 15],
                 ['07', "Console & Video Games", 15],
                 ['08', "DIY & Tools", 15],
                 ['09', "Garden & Outdoor living", 15],
                 ['10', "Grocery", 15],
                 ['11', "Kitchen & Home", 15],
                 ['12', "Betting", 15],
                 ['13', "Jewellery & Watches", 15],
                 ['14', "Musical Instruments", 15],
                 ['15', "Office Products", 15],
                 ['16', "Pet Supplies", 15],
                 ['17', "Computer Software", 15],
                 ['18', "Sports & Outdoors", 15],
                 ['19', "Toys & Games", 15],
                 ['20', "Dating Sites", 15]
                ] 
    adCats_df = pd.DataFrame(adCatsLst, columns =['AdCatId', 'AdCatName', 'AdCatNumAds'])
    return adCats_df


def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    return [ atoi(c) for c in re.split(r'(\d+)',text.split('/')[-1].split('.')[0]) ]

def generate_data_partAds( adsPartPathPrefix, startRange, endRange ):
    partAds_df = pd.DataFrame()
    partAdsRows = []
    
    for i in range(startRange, endRange):
        iStr = str(i)
        adsFiles = pathlib.Path(adsPartPathPrefix + iStr + "/").glob("*.png")
        adsFileStrLst = []
        for adsFile in adsFiles:
            adsFileStr = str(adsFile)
            adsFileStrLst.append(adsFileStr)
        adsFileStrLst.sort(key=natural_keys)
    
        for adsFileStr in adsFileStrLst:
            adId = adsFileStr.split('/')[-1].split('.')[0]
            adId = "A" +  iStr.zfill(2) + "_" + adId.zfill(2)
        #    print(adId, adsFileStr)
            partAdsRows.append([adId, adsFileStr])
        
    partAds_df = pd.DataFrame(partAdsRows, columns =['AdId', 'AdFilePath'])
    partAds_df.set_index('AdId')
        
    return partAds_df


def generate_data_allAds():
    allAds_df = pd.DataFrame()
    
    part1Ads_df = generate_data_partAds(g_adsPart1PathPrefix, 1, 11)
    allAds_df = allAds_df.append(part1Ads_df, sort=True)

    part2Ads_df = generate_data_partAds(g_adsPart2PathPrefix, 11, 21)
    allAds_df = allAds_df.append(part2Ads_df, sort=True)

    allAds_df = allAds_df.set_index('AdId')
    return allAds_df


def df_crossjoin(df1, df2):
    df1['_tmpkey'] = 1
    df2['_tmpkey'] = 1

    res = pd.merge(df1, df2, on='_tmpkey').drop('_tmpkey', axis=1)
    res.index = pd.MultiIndex.from_product((df1.index, df2.index))

    df1.drop('_tmpkey', axis=1, inplace=True)
    df2.drop('_tmpkey', axis=1, inplace=True)

    return res


def generate_data_RatingsPerUser( pathPrefix, userId ):
    completePath = pathPrefix + userId + "/"

    data = ""
    rtFile = userId + "-RT.csv"
    rtNewFile = userId + "-RT-NEW.csv"
    
    with open(completePath + rtFile) as file:
        data = file.read().replace("\"", "")

    with open(completePath + rtNewFile,"w") as file:
        file.write(data)

    my_cols = [str(i) for i in range(300)]
    data3 = pd.read_csv(completePath + rtNewFile, sep=";|,", names=my_cols, header=None, engine="python")
    data3 = data3.iloc[2:]
    data3.reset_index(drop = True, inplace = True)
    
    for i in range(20):
        index = str(i)
        data3[index] = data3[index].astype('float64')
    
    data3 = data3.transpose()
        
    return data3


def generate_data_RatingsPartUsers( usersPartPathPrefix, startRange, endRange ):
    partUsers_df = pd.DataFrame()
    
    for i in range(startRange, endRange):
        thisUserIdNum = str(i)
        thisUserId = g_userIdPrefix + thisUserIdNum.zfill(3)
        # print(thisUserId)
        thisUser_df = generate_data_RatingsPerUser(usersPartPathPrefix, thisUserId)
        partUsers_df = partUsers_df.append(thisUser_df, sort=True)
        # partUsers_df.set_index('UserId')
        
    return partUsers_df


def generate_data_RatingsAllUsers():
    allUsers_df = pd.DataFrame()

    part1Users_df = generate_data_RatingsPartUsers(g_userPart1PathPrefix, 1, 61)
    allUsers_df = allUsers_df.append(part1Users_df, sort=True)

    part2Users_df = generate_data_RatingsPartUsers(g_userPart2PathPrefix, 61, 121)
    allUsers_df = allUsers_df.append(part2Users_df, sort=True)

    return allUsers_df
