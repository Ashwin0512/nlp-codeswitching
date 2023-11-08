import pandas as pd

def is_hindi(character):
    maxchar = max(character)
    if u'\u0900' <= maxchar <= u'\u097f':
        return True
    else:
      return False

def Iindex(df):
    for ind in df.index:
        count=0
        lan=-1
        s=0
        for word in df['ENHI-CS'][ind].split():
                if word not in ["!", ".", "?"]:
                    count+=1
                    if lan==-1:
                        lan=is_hindi(word[0])
                    elif lan!=is_hindi(word[0]):
                        s+=1
                        lan=is_hindi(word[0])
                        
        print(ind, s)