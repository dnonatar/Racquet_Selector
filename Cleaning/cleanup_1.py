import pandas as pd
import os

os.chdir('/home/ratanond/Desktop/DataScience/Projects/Racquet_Selector/Cleaning/scraped_data')

babolat = pd.read_csv('babolat.csv')
wilson = pd.read_csv('wilson.csv')
head = pd.read_csv('head.csv')
yonex = pd.read_csv('yonex.csv')

babolat.name = 'babolat'
wilson.name = 'wilson'
head.name = 'head'
yonex.name = 'yonex'

cols_drop = ['Tension','Grip_Type', 'Composition','Weight','Beam_Width']

def exclude_junior(df):
    df = df[~df.Racket_Name.str.contains('Junior')]
    return df

## remove the word 'Tennis Racquet'
def fix_racket_name(df):
    for i in range(0,df.shape[0]):
         df['Racket_Name'][i] = df['Racket_Name'][i].replace(" Tennis Racquet","")
    return df
    


racket_brands = [babolat,wilson,head,yonex]      
for brand in racket_brands:
    file_name = brand.name
    brand = brand.drop(cols_drop,axis=1)
    brand = fix_racket_name(brand)
    brand = exclude_junior(brand)
    brand.to_csv('./cleaned_output/'+file_name+'.csv',index=False)
    
# Question..
# If put file_name just before to_csv, it wouldn't work
# If drop and exclude_junior first, also doesn't work
    
