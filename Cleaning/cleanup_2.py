# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 13:15:02 2018

@author: ratanond
"""
### After cleanup_1 and some manual filling steps

import pandas as pd
import os

os.chdir('/home/ratanond/Desktop/DataScience/Projects/Racquet_Selector/Cleaning')

wilson = pd.read_csv('./cleaned_output_1/wilson_fixed.csv')
babolat = pd.read_csv('./cleaned_output_1/babolat_fixed.csv')
head = pd.read_csv('./cleaned_output_1/head_fixed.csv')
yonex = pd.read_csv('./cleaned_output_1/yonex_fixed.csv')

## Replace Even Balance with 0
def replace_even(df):
    for i in range(0,df.shape[0]):
        if (df['Balance'][i] == 'Even Balance'):
            df['Balance'][i] = '0 Pts Head Even'
    return df 
    
## Separate HH/HL from Pts numbers
def separate_pts(df):
    df['Balance_Points'] = df.apply(lambda row: row['Balance'].split()[0],axis=1)
    df['Balance_Type'] = df.apply(lambda row: row['Balance'].split()[3],axis=1)
    return df

## replace Heavy/Light with HH and HL
def change_balance_type(df):
    for i in range(0,df.shape[0]):
        if (df['Balance_Type'][i] == 'Light'):
            df['Balance_Type'][i] = 'HL'
        elif (df['Balance_Type'][i] == 'Heavy'):
            df['Balance_Type'][i] = 'HH'
    return df 
        
## change some column names to include units
def change_col(df):
    df.rename(columns={'Head_Size':'Head_Size (in.^2)','Length':'Length (in.)','Swingweight':'Swingweight (g.)'}, inplace=True)
    return df
    
### get rid of units for head size
def get_head_size(df):
    df['Head_Size'] = df.apply(lambda row: row['Head_Size'][0:3],axis=1)
    return df

## Extract string pattern
def get_string_pattern(df):
    df['String_Pattern'] = df.apply(lambda row: row['String_Pattern'][6:27],axis=1)
    return df
    
## Discard length unit from the 'Length' column
def get_length(df):
    df['Length'] = df.apply(lambda row: row['Length'].replace(' inches',''),axis=1)
    return df
    
## Discard the word 'Swing' from the 'Swing_speed' column
def get_swing(df):
    df['Swing_speed'] = df.apply(lambda row: row['Swing_speed'].replace(' Swing',''),axis=1)    
    return df
    
    ## remove the word 'Tennis Racquet'
def fix_racket_name(df):
    df['Racket_Name']= df.apply(lambda row: row['Racket_Name'].replace(" Tennis Racquet",""),axis=1)
    return df

""" Since I decided later that I want to include the prices, I will have to 
    join them with the current data in order to avoid redoing the manual 
    filling steps. For next time, it can be scraped together with everything 
    else.  
"""
wilson_price = pd.read_csv('./Price/wilson_price.csv').fillna('')
babolat_price = pd.read_csv('./Price/babolat_price.csv').fillna('')
head_price = pd.read_csv('./Price/head_price.csv').fillna('')
yonex_price = pd.read_csv('./Price/yonex_price.csv').fillna('')

wilson_price = fix_racket_name(wilson_price)
babolat_price = fix_racket_name(babolat_price)
head_price = fix_racket_name(head_price)
yonex_price = fix_racket_name(yonex_price)

def get_price(df):
    df['Price($)'] = df['Sale_Price']+df['Price']
    df['Price($)'] = df.apply(lambda row: row['Price($)'].split('$')[1],axis=1)
    df = df[['Racket_Name','Price($)']]
    return(df)

wilson_price = get_price(wilson_price)
babolat_price = get_price(babolat_price)
head_price = get_price(head_price)
yonex_price = get_price(yonex_price)

## merge the price tables with the main tables
wilson = wilson.merge(wilson_price,on='Racket_Name',how='inner',indicator=False)
babolat = babolat.merge(babolat_price,on='Racket_Name',how='inner',indicator=False)
head = head.merge(head_price,on='Racket_Name',how='inner',indicator=False)
yonex = yonex.merge(yonex_price,on='Racket_Name',how='inner',indicator=False)

racket_brands = [babolat,wilson,head,yonex] 
for brand in racket_brands:
    brand = replace_even(brand)
    brand = separate_pts(brand)
    brand = change_balance_type(brand)
    brand = get_head_size(brand)
    brand = get_string_pattern(brand)
    brand = get_length(brand)
    brand = get_swing(brand) 
    brand = change_col(brand)
    brand = brand.drop('Balance',axis='columns',inplace=True)

## Add brands' names in front of the racket names
wilson['Racket_Name'] = 'Wilson '+wilson['Racket_Name']
babolat['Racket_Name'] = 'Babolat '+babolat['Racket_Name']
head['Racket_Name'] = 'Head '+head['Racket_Name']
yonex['Racket_Name'] = 'Yonex '+yonex['Racket_Name']
    
babolat.name = 'babolat'
wilson.name = 'wilson'
head.name = 'head'
yonex.name = 'yonex'

for brand in racket_brands:    
    file_name = brand.name
    brand.to_csv('./final_data/'+file_name+'_final.csv',index=False)    
