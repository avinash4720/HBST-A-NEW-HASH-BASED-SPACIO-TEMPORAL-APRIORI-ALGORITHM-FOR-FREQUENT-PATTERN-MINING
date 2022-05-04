#!/usr/bin/env python
# coding: utf-8

# In[584]:


import csv


# In[585]:


filename = 'Big_Dataset.csv'


# In[586]:


import datetime


# In[587]:


filename


# In[588]:


t1 = datetime.datetime.now()


# In[589]:


def get_quantized_list(rows):
  so2_list = []
  no2_list = []
  pmt_list = []
  print(len(rows))
  for row in rows:
    try:
      x = float(row[9])
      so2_list.append(x)
    except ValueError:
      so2_list.append(0)
    try:
      x = float(row[5])
      no2_list.append(x)
    except ValueError:
      no2_list.append(0)
    try:
      x = float(row[2])
      pmt_list.append(x)
    except ValueError:
      pmt_list.append(0)
  
  for i in range(len(so2_list)):
    if so2_list[i]==0:
      if not (so2_list[i+1]==0):
        so2_list[i]=(so2_list[i-1]+so2_list[i+1])/2
      else:
        so2_list[i]=so2_list[i-1]
  
  """
  for i in so2_list:
    print(i)
    
  """
  for i in range(len(no2_list)):
    if no2_list[i]==0:
      if not (no2_list[i+1]==0):
        no2_list[i]=(no2_list[i-1]+no2_list[i+1])/2
      else:
        no2_list[i]=no2_list[i-1]
        
  """"
  for i in no2_list:
    print(i)
    
  """
  mean=0
  count=0
  for i in pmt_list:
    if not(i==0):
        mean=mean+i
        count=count+1
  mean=int(mean/count)
  
  #print('\n')
  #print(mean,count)
    
  for i in range(len(pmt_list)):
    if pmt_list[i]==0:
      if not (pmt_list[i+1]==0):
        pmt_list[i]=(pmt_list[i-1]+pmt_list[i+1])/2
      elif pmt_list[0]==0:
        pmt_list[i]=mean
      else:
        pmt_list[i]=pmt_list[i-1]
        
  """"
  for i in pmt_list:
    print(i)
    
  """
  
  #print(so2_list)
  #print(no2_list)
  #print(pmt_list)

  so2_max, so2_min = max(so2_list), min(so2_list)
  no2_max, no2_min = max(no2_list), min(no2_list)
  pmt_max, pmt_min = max(pmt_list), min(pmt_list)
    
  so2_part = (so2_max-so2_min)/3
  so2_lim1 = so2_min + so2_part
  so2_lim2 = so2_min + 2*so2_part

  """"
  print('\n')
  print(so2_max)
  print(so2_min)
  print(so2_part)
  print(so2_lim1)
  print(so2_lim2)
  
  """

  for i in range(len(so2_list)):
    so2 = so2_list[i]
    if so2 >= so2_min and so2 < so2_lim1:
      so2_list[i] = 'so21'
    elif so2 >= so2_lim1 and so2 < so2_lim2:
      so2_list[i] = 'so22'
    else:
      so2_list[i] = 'so23'

  no2_part = (no2_max-no2_min)/3
  no2_lim1 = no2_min + no2_part
  no2_lim2 = no2_min + 2*no2_part  
  
  for i in range(len(no2_list)):
    no2 = no2_list[i]
    if no2 >= no2_min and no2 < no2_lim1:
      no2_list[i] = 'no21'
    elif no2 >= no2_lim1 and no2 < no2_lim2:
      no2_list[i] = 'no22'
    else:
      no2_list[i] = 'no23'
    
  """"
  print('\n')
  print(no2_max)
  print(no2_min)
  print(no2_part)
  print(no2_lim1)
  print(no2_lim2)
  
  """

  pmt_part = (pmt_max-pmt_min)/3
  pmt_lim1 = pmt_min + pmt_part
  pmt_lim2 = pmt_min + 2*pmt_part

  for i in range(len(pmt_list)):
    pmt = pmt_list[i]
    if pmt >= pmt_min and pmt < pmt_lim1:
      pmt_list[i] = 'pmt1'
    elif pmt >= pmt_lim1 and pmt < pmt_lim2:
      pmt_list[i] = 'pmt2'
    else:
      pmt_list[i] = 'pmt3'
    
  """"
  print('\n')
  print(pmt_max)
  print(pmt_min)
  print(pmt_part)
  print(pmt_lim1)
  print(pmt_lim2)
  
  """

  compound_list = []

  """"
  so21_count=0
  so22_count=0
  so23_count=0
  for i in so2_list:
    if i=="so21":
      so21_count=so21_count+1
    elif i=="so22":
      so22_count=so22_count+1
    else:
      so23_count=so23_count+1
  print(so21_count,so22_count,so23_count)
  
  """
    
  for i in range(len(so2_list)):
    compound_list.append([so2_list[i], no2_list[i], pmt_list[i]])
  return compound_list


# In[590]:


def get_spatial_list(rows):
  location = []
  for row in rows:
    location.append(row[0])
  return location


# In[591]:


def get_temporal_list(rows):
  months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'Semptember', 'October', 'November', 'December']
  return [months[int(row[1].split('-')[1])-1] for row in rows]


# In[592]:


def preprocessing(filename):
  file_ptr = open(filename, 'r')
  csvread = csv.reader(file_ptr)
  rows = []
  for row in csvread:
    rows.append(row)
  rows = rows[1:]
  quantized_list = get_quantized_list(rows)
  spatial_list = get_spatial_list(rows)
  temporal_list = get_temporal_list(rows)
  test_data = []
  for i in range(len(quantized_list)):
    test_data.append([quantized_list[i], spatial_list[i], temporal_list[i]])
  return test_data


# In[593]:


transactions = preprocessing(filename)


# In[594]:


t2 = datetime.datetime.now()


# In[595]:


transactions


# In[596]:


def CMS_Generation(transactions):
  location = {}
  time = {}
  time_location = {}
  for row in transactions:
    city = row[1]
    month = row[2]
    if city in location:
      location[city].add(month)
    else:
      new_set = set()
      new_set.add(month)
      location[city] = new_set
    if month in time:
      time[month].add(city)
    else:
      new_set = set()
      new_set.add(city)
      time[month] = new_set
    if not (city, month) in time_location:
      time_location[(city, month)] = True
  location = [city for city in location if len(location[city]) > 1]
  time = [month for month in time if len(time[month]) > 1]
  time_location = [key for key in time_location]
  return [location, time, time_location]


# In[597]:


CMS = CMS_Generation(transactions)


# In[598]:


CMS


# In[599]:





# In[600]:


def get_hash_ids(CMS):
  one_star_location = CMS[0]
  one_star_time = CMS[1]
  zero_star_time_location = CMS[2]
  hash_ids = {}
  start_id = 1
  for time_location in zero_star_time_location:
    hash_ids[time_location] = '1' +  str(start_id)
    start_id += 1
  start_id = 1
  for location in one_star_location:
    hash_ids[(location, '*')] = '2' + str(start_id)
    start_id += 1
  for time in one_star_time:
    hash_ids[('*', time)] = '2' + str(start_id)
    start_id += 1
  start_id = 1
  hash_ids[('*', '*')] = '3' + str(start_id)
  return hash_ids


# In[601]:


hash_ids = get_hash_ids(CMS)


# In[602]:


hash_ids


# In[603]:


def get_rev_hash_ids(hash_ids):
  rev_hash_ids = {}
  for time_location, id in hash_ids.items():
    rev_hash_ids[id] = time_location
  return rev_hash_ids


# In[604]:


rev_hash_ids = get_rev_hash_ids(hash_ids)


# In[605]:


rev_hash_ids


# In[606]:


def get_itemsets_by_hash_id(transactions, hash_ids):
  itemsets_by_hash_id = {}
  for row in transactions:
    location_time = (row[1], row[2])
    itemset = row[0]
    if hash_ids[location_time] in itemsets_by_hash_id:
      itemsets_by_hash_id[hash_ids[location_time]].append(set(itemset))
    else:
      itemsets = [set(itemset)]
      itemsets_by_hash_id[hash_ids[location_time]] = itemsets
  return itemsets_by_hash_id


# In[607]:


itemsets_by_hash_id = get_itemsets_by_hash_id(transactions, hash_ids)


# In[608]:


itemsets_by_hash_id


# In[609]:


MIN_SUPPORT_VALUE=3




# In[610]:


def get_two_items_itemsets_by_hash_id(itemsets_by_hash_id):
  two_items_itemsets_by_hash_id = {}
  for id, itemsets in itemsets_by_hash_id.items():
    unique_two_itemset = set()
    #print(itemsets)
    #print('\n')
    for itemset in itemsets:
      #print(itemset)
      #print('\n')
      two_itemsets = combinations(list(itemset), 2)
      for two_itemset in two_itemsets:
        #print(two_itemset)
        #print('\n')
        two_itemset = sorted(list(two_itemset), key=lambda item: int(item[3:]))
        itemset_freq_in_transaction = get_itemset_freq_in_transaction(two_itemset, itemsets_by_hash_id, id)
        if itemset_freq_in_transaction >= MIN_SUPPORT_VALUE:
          unique_two_itemset.add((tuple(two_itemset), itemset_freq_in_transaction))
    if len(unique_two_itemset) > 0:
      two_items_itemsets_by_hash_id[id] = list(unique_two_itemset)
  return two_items_itemsets_by_hash_id


# In[611]:





# In[612]:


from itertools import combinations, chain


# In[613]:


def get_itemset_freq_in_transaction(items, itemsets_by_hash_id, id):
  count = 0
  for itemset in itemsets_by_hash_id[id]:
    is_subset = True
    for item in items:
      if not item in itemset:
        is_subset = False
        break
    if is_subset:
      count += 1
  return count


# In[614]:


two_items_itemsets_by_hash_id = get_two_items_itemsets_by_hash_id(itemsets_by_hash_id)


# In[615]:


two_items_itemsets_by_hash_id


# In[616]:


two_items_itemsets_by_hash_id


# In[ ]:





# In[ ]:

t3 = datetime.datetime.now()



# In[617]:


def get_final_itemsets_by_hash_id(base_itemset, itemsets_by_hash_id):
  next_itemset_size = 3
  terminate = False
  final_itemsets_by_hash_id = {}
  # apriori algorithm on hashed spatio-temporal itemsets
  while(not terminate):
    terminate = True
    for id, itemsets in base_itemset.items():
      next_itemsets = set()
      if len(itemsets) > 0:
        if id in final_itemsets_by_hash_id:
          final_itemsets_by_hash_id[id].append(itemsets)
        else:
          final_itemsets_by_hash_id[id] = [itemsets]
      for i in range(len(itemsets)):
        for j in range(i+1, len(itemsets)):
          new_itemset = list(set(itemsets[i][0] + itemsets[j][0]))
          new_itemset = sorted(new_itemset, key=lambda item: int(item[3:]))
          if len(new_itemset) == next_itemset_size:
            itemset_freq_in_transaction = get_itemset_freq_in_transaction(new_itemset, itemsets_by_hash_id, id)
            if(itemset_freq_in_transaction >= MIN_SUPPORT_VALUE):
              next_itemsets.add((tuple(new_itemset), itemset_freq_in_transaction))
      if len(next_itemsets) > 0:
        terminate = False
      base_itemset[id] = list(next_itemsets)
    next_itemset_size += 1
 
  for id, itemsets in final_itemsets_by_hash_id.items():
    final_itemsets_by_hash_id[id] = list(chain.from_iterable(final_itemsets_by_hash_id[id]))
  return final_itemsets_by_hash_id


# In[618]:


final_itemsets_by_hash_id = get_final_itemsets_by_hash_id(two_items_itemsets_by_hash_id, itemsets_by_hash_id)


# In[619]:


final_itemsets_by_hash_id

t4 = datetime.datetime.now()


# In[620]:


def get_star_itemsets_by_hash_id(final_itemsets_by_hash_id, location_time_star_items, hash_ids, rev_hash_ids):
  one_star_location = location_time_star_items[0]
  one_star_time = location_time_star_items[1]
  one_star_itemsets = {}
  two_star_itemsets = {}
  for location in one_star_location:
    for id, itemsets in final_itemsets_by_hash_id.items():
      if location == rev_hash_ids[id][0]:
        new_id = hash_ids[(location, '*')]
        if new_id in one_star_itemsets:
          one_star_itemsets[new_id].append(itemsets)
        else:
          one_star_itemsets[new_id] = [itemsets]
  for time in one_star_time:
    for id, itemsets in final_itemsets_by_hash_id.items():
      if time == rev_hash_ids[id][1]:
        new_id = hash_ids[('*', time)]
        if new_id in one_star_itemsets:
          one_star_itemsets[new_id].append(itemsets)
        else:
          one_star_itemsets[new_id] = [itemsets]
  # concatenate the list of list to form single list of itemsets
  for id, itemsets in one_star_itemsets.items():
    one_star_itemsets[id] = list(chain.from_iterable(one_star_itemsets[id]))
  two_star_id = hash_ids[('*', '*')]
  two_star_itemsets[two_star_id] = []
  for id, itemsets in final_itemsets_by_hash_id.items():
    two_star_itemsets[two_star_id].append(itemsets)
  two_star_itemsets[two_star_id] = list(chain.from_iterable(two_star_itemsets[two_star_id]))
  for id, itemsets in one_star_itemsets.items():
    one_star_itemsets[id] = combine_same_itemsets_count(itemsets)
  for id, itemsets in two_star_itemsets.items():
    two_star_itemsets[id] = combine_same_itemsets_count(itemsets)
  return [one_star_itemsets, two_star_itemsets]


# In[ ]:





# In[621]:


def combine_same_itemsets_count(itemsets):
  itemset_freq = {}
  for itemset in itemsets:
    curr_itemset = tuple(sorted(itemset[0], key=lambda x: ord(x[0])))
    if curr_itemset in itemset_freq:
      itemset_freq[curr_itemset] += itemset[1]
    else:
      itemset_freq[curr_itemset] = itemset[1]
  itemsets = []
  for itemset, count in itemset_freq.items():
    itemsets.append((itemset, count))
  return itemsets


# In[622]:


star_itemsets_by_hash_id = get_star_itemsets_by_hash_id(final_itemsets_by_hash_id, CMS, hash_ids, rev_hash_ids)


# In[623]:


star_itemsets_by_hash_id

t5 = datetime.datetime.now()


# In[624]:


one_star_itemsets_by_hash_id = star_itemsets_by_hash_id[0]


# In[625]:


one_star_itemsets_by_hash_id


# In[626]:


two_star_itemsets_by_hash_id = star_itemsets_by_hash_id[1]


# In[ ]:





# In[627]:


final_itemsets_by_hash_id


# In[628]:


rev_hash_ids


# In[629]:


def Max_Pollutant(final_itemsets_by_hash_id):
    Pollutant_List={}
    for id,itemset in final_itemsets_by_hash_id.items():
        #print(itemset)
        #print('\n')
        max=0
        sum=0
        for (items,frequency) in itemset:
            #print(items)
            #print('\n')
            if frequency > max:
                max = frequency
                max_pollutants=items
            sum = sum + frequency
        Pollutant_List[id]=(rev_hash_ids[id],max_pollutants,(max))      
    return Pollutant_List        
            
    
            
        
    


# In[630]:


MAX_FREQ_final_itemsets=Max_Pollutant(final_itemsets_by_hash_id)


# In[631]:


MAX_FREQ_final_itemsets


# In[ ]:





# In[632]:


star_itemsets_by_hash_id


# In[633]:


MAX_FREQ_one_star_itemsets=Max_Pollutant(one_star_itemsets_by_hash_id)


# In[634]:


MAX_FREQ_one_star_itemsets


# In[635]:


MAX_FREQ_two_star_itemsets=Max_Pollutant(two_star_itemsets_by_hash_id)


# In[636]:


MAX_FREQ_two_star_itemsets


# In[637]:


two_star_itemsets_by_hash_id


# In[638]:





# In[639]:


preprocess_time_HBST = t2-t1


# In[640]:


CMS_Generation_time_HBST = t3-t2


# In[641]:


two_Item_set_time_HBST = t4-t3


# In[642]:


Star_Item_set_time_HBST = t5-t4


# In[643]:


total_time_HBST = t5-t1


# In[644]:


transactions


# In[645]:


def Co_Pollutants(transactions,Pollutant_Max_Freq):
    for id,itemset in Pollutant_Max_Freq.items():
        total_count = 0
        location = itemset[0][0]
        time = itemset[0][1]
        co_pollutants = itemset[1]
        for row in transactions:
            if (row[1] == location) & (row[2] == time):
                pollutants_list = row[0]
                if (pollutants_list[0] == co_pollutants[0]) | (pollutants_list[0] == co_pollutants[1]) | (pollutants_list[1] == co_pollutants[0]) | (pollutants_list[1] == co_pollutants[1]) | (pollutants_list[2] == co_pollutants[0]) | (pollutants_list[2] == co_pollutants[1]):
                    total_count = total_count + 1
        Pollutant_Max_Freq[hash_ids[(location,time)]]=[Pollutant_Max_Freq[hash_ids[(location,time)]],total_count]
        #print(Pollutant_Max_Freq[hash_ids[(location,time)]])
                    
    
    


# In[ ]:





# In[ ]:





# In[ ]:





# In[646]:


Pollutant_Max_Freq={}
Pollutant_Max_Freq.update(MAX_FREQ_final_itemsets)
Pollutant_Max_Freq.update(MAX_FREQ_one_star_itemsets)
Pollutant_Max_Freq.update(MAX_FREQ_two_star_itemsets)
#print(MAX_FREQ_final_itemsets)



# In[647]:


Co_Pollutants(transactions,Pollutant_Max_Freq)


# In[648]:


Pollutant_Max_Freq


# In[649]:


'''def find_Co_Pollutants_Percentage(Pollutant_Max_Freq):
    for id,itemset in Pollutant_Max_Freq.items():
        co_pollutant_count = itemset[0][2]
        #print(co_pollutant_count)
        total_pollutant_count = itemset[1]
        #print(total_pollutant_count)
        #print('\n')
        percentage = (co_pollutant_count*100)/total_pollutant_count
        Pollutant_Max_Freq[id] = [Pollutant_Max_Freq[id],percentage]'''


# In[650]:


#find_Co_Pollutants_Percentage(Pollutant_Max_Freq)


# In[651]:


#Pollutant_Max_Freq


# In[ ]:


from prettytable import PrettyTable


# In[ ]:


def print_table(final_itemsets, title):
  print(title)
  table = PrettyTable(['ID', 'Itemsets', 'Count', 'Location', 'Time'])
  for index, (id, itemsets) in enumerate(final_itemsets.items()):
    items = [itemset[0] for itemset in itemsets]
    items_freq = [itemset[1] for itemset in itemsets]
    row = [index+1, items, items_freq, id[0], id[1]]
    table.add_row(row)
  table._max_width = {'Itemsets': 70, 'Count': 30}
  print(table)


# In[ ]:


print(20*'*')
print('Total time taken for preprocessing in (microseconds) by Hash Based Spatio-Temporal(HBST) algorithm:', preprocess_time_HBST.microseconds)
print('Total time taken for CMS Generation in (microseconds) by Hash Based Spatio-Temporal(HBST) algorithm:', CMS_Generation_time_HBST.microseconds)
print('Total time taken for 2-Item-set in (microseconds) by Hash Based Spatio-Temporal(HBST) algorithm:', two_Item_set_time_HBST.microseconds)
print('Total time taken for star_Item-set in (microseconds) by Hash Based Spatio-Temporal(HBST) algorithm:', Star_Item_set_time_HBST.microseconds)
#print('Total time taken in (microseconds) by Hash Based Spatio-Temporal(HBST) algorithm:', total_time_HBST.microseconds)
print('Min support value:', MIN_SUPPORT_VALUE)
print(20*'*')
print_table(final_itemsets_by_hash_id,'Itemsets for CMB')
print_table(one_star_itemsets_by_hash_id,'Itemsets for 1 star CMP')
print_table(two_star_itemsets_by_hash_id,'Itemsets for 2 star')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




