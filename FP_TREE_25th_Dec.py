#!/usr/bin/env python
# coding: utf-8

# In[1]:


import itertools
import pandas as pd
import numpy as np
import functools
import csv
import datetime
#from preprocess import get_preprocessed_data
from prettytable import PrettyTable
from utils import print_table, get_location_time_star_items, combine_same_itemsets_count, get_config_info


# In[ ]:





# In[2]:


class FPNode(object):
    def __init__(self, value, count, parent):
        self.value = value
        self.count = count
        self.parent = parent
        self.link = None
        self.children = []

    def has_child(self, value):

        for node in self.children:
            if node.value == value:
                return True

        return False

    def get_child(self, value):
  
        for node in self.children:
            if node.value == value:
                return node

        return None

    def add_child(self, value):
        child = FPNode(value, 1, self)
        self.children.append(child)
        return child


class FPTree(object):
    def __init__(self, transactions, threshold, root_value, root_count):
        self.frequent = self.find_frequent_items(transactions, threshold)
        self.headers = self.build_header_table(self.frequent)
        self.root = self.build_fptree(
            transactions, root_value,
            root_count, self.frequent, self.headers)

    @staticmethod
    def find_frequent_items(transactions, threshold):
        items = {}

        for transaction in transactions:
            for item in transaction:
                if item in items:
                    items[item] += 1
                else:
                    items[item] = 1

        for key in list(items.keys()):
            if items[key] < threshold:
                del items[key]

        return items

    @staticmethod
    def build_header_table(frequent):
        headers = {}
        for key in frequent.keys():
            headers[key] = None

        return headers

    def build_fptree(self, transactions, root_value,
                     root_count, frequent, headers):
        root = FPNode(root_value, root_count, None)

        for transaction in transactions:
            sorted_items = [x for x in transaction if x in frequent]
            sorted_items.sort(key=lambda x: frequent[x], reverse=True)
            if len(sorted_items) > 0:
                self.insert_tree(sorted_items, root, headers)

        return root

    def insert_tree(self, items, node, headers):
        first = items[0]
        child = node.get_child(first)
        if child is not None:
            child.count += 1
        else:
            # Add new child.
            child = node.add_child(first)

            # Link it to header structure.
            if headers[first] is None:
                headers[first] = child
            else:
                current = headers[first]
                while current.link is not None:
                    current = current.link
                current.link = child

        # Call function recursively.
        remaining_items = items[1:]
        if len(remaining_items) > 0:
            self.insert_tree(remaining_items, child, headers)

    def tree_has_single_path(self, node):
        num_children = len(node.children)
        if num_children > 1:
            return False
        elif num_children == 0:
            return True
        else:
            return True and self.tree_has_single_path(node.children[0])

    def mine_patterns(self, threshold):
        if self.tree_has_single_path(self.root):
            return self.generate_pattern_list()
        else:
            return self.zip_patterns(self.mine_sub_trees(threshold))

    def zip_patterns(self, patterns):
        """
        Append suffix to patterns in dictionary if
        we are in a conditional FP tree.
        """
        suffix = self.root.value

        if suffix is not None:
            # We are in a conditional tree.
            new_patterns = {}
            for key in patterns.keys():
                new_patterns[tuple(sorted(list(key) + [suffix]))] = patterns[key]

            return new_patterns

        return patterns

    def generate_pattern_list(self):
        patterns = {}
        items = self.frequent.keys()
        if self.root.value is None:
            suffix_value = []
        else:
            suffix_value = [self.root.value]
            patterns[tuple(suffix_value)] = self.root.count

        for i in range(1, len(items) + 1):
            for subset in itertools.combinations(items, i):
                pattern = tuple(sorted(list(subset) + suffix_value))
                patterns[pattern] =                     min([self.frequent[x] for x in subset])

        return patterns

    def mine_sub_trees(self, threshold):
        """
        Generate subtrees and mine them for patterns.
        """
        patterns = {}
        mining_order = sorted(self.frequent.keys(),
                              key=lambda x: self.frequent[x])

        # Get items in tree in reverse order of occurrences.
        for item in mining_order:
            suffixes = []
            conditional_tree_input = []
            node = self.headers[item]

            # Follow node links to get a list of
            # all occurrences of a certain item.
            while node is not None:
                suffixes.append(node)
                node = node.link

            # For each occurrence of the item, 
            # trace the path back to the root node.
            for suffix in suffixes:
                frequency = suffix.count
                path = []
                parent = suffix.parent

                while parent.parent is not None:
                    path.append(parent.value)
                    parent = parent.parent

                for i in range(frequency):
                    conditional_tree_input.append(path)

            # Now we have the input for a subtree,
            # so construct it and grab the patterns.
            subtree = FPTree(conditional_tree_input, threshold,
                             item, self.frequent[item])
            subtree_patterns = subtree.mine_patterns(threshold)

            # Insert subtree patterns into main patterns dictionary.
            for pattern in subtree_patterns.keys():
                if pattern in patterns:
                    patterns[pattern] += subtree_patterns[pattern]
                else:
                    patterns[pattern] = subtree_patterns[pattern]

        return patterns


def find_frequent_patterns(transactions, support_threshold):
    tree = FPTree(transactions, support_threshold, None, None)
    return tree.mine_patterns(support_threshold)


def generate_association_rules(patterns, confidence_threshold):
    """
    Given a set of frequent itemsets, return a dict
    of association rules in the form
    {(left): ((right), confidence)}
    """
    rules = {}
    for itemset in patterns.keys():
        upper_support = patterns[itemset]

        for i in range(1, len(itemset)):
            for antecedent in itertools.combinations(itemset, i):
                antecedent = tuple(sorted(antecedent))
                consequent = tuple(sorted(set(itemset) - set(antecedent)))

                if antecedent in patterns:
                    lower_support = patterns[antecedent]
                    confidence = float(upper_support) / lower_support

                    if confidence >= confidence_threshold:
                        rules[antecedent] = (consequent, confidence)

    return rules



def get_transaction_from_file(num):
	file_name = ["retail_dataset.csv", "test_dataset_1.csv"]
	transaction = []
	with open(file_name[num]) as csvfile:
		datareader = csv.reader(csvfile)
		for row in datareader:
			curr_item_list = []
			for item_num in row:
				if item_num == '':
					continue
				if num == 1:
					item_num = int(item_num[1:])
				else:
					item_num = int(item_num)
				if item_num in curr_item_list:
					continue
				curr_item_list.append(item_num)
				
			curr_item_list.sort()
			transaction.append(curr_item_list)

	return transaction


# In[3]:


def find_frequent_patterns_by_location_time(transactions, support_value):
    transactions_by_location_time = {}
    for transaction in transactions:
        id = (transaction[1], transaction[2])
        if id in transactions_by_location_time:
            transactions_by_location_time[id].append(transaction[0])
        else:
            transactions_by_location_time[id] = [transaction[0]]
    final_itemsets = []
    for location_time, transactions in transactions_by_location_time.items():
        frequent_itemsets = find_frequent_patterns(transactions, support_value)
        frequent_itemsets = [(id, count, location_time) for id, count in frequent_itemsets.items() if len(id) > 1]
        if len(frequent_itemsets) > 0:
            final_itemsets.append(frequent_itemsets)
    final_itemsets = list(itertools.chain.from_iterable(final_itemsets))
    return final_itemsets


# In[4]:


def get_star_itemsets(final_itemsets, location_time_star_items):
  one_star_location = location_time_star_items[0]
  one_star_time = location_time_star_items[1]
  zero_star_itemsets = {}
  one_star_itemsets = {}
  two_star_itemsets = {}
  for itemset in final_itemsets:
    if itemset[2] in zero_star_itemsets:
      zero_star_itemsets[itemset[2]].append(itemset)
    else:
      zero_star_itemsets[itemset[2]] = [itemset]
  for location in one_star_location:
    for id, itemsets in zero_star_itemsets.items():
      if location == id[0]:
        new_id = (location, '*')
        if new_id in one_star_itemsets:
          one_star_itemsets[new_id].append(itemsets)
        else:
          one_star_itemsets[new_id] = [itemsets]
  for time in one_star_time:
    for id, itemsets in zero_star_itemsets.items():
      if time == id[1]:
        new_id = ('*', time)
        if new_id in one_star_itemsets:
          one_star_itemsets[new_id].append(itemsets)
        else:
          one_star_itemsets[new_id] = [itemsets]
  # concatenate the list of list to form single list of itemsets
  for id, itemsets in one_star_itemsets.items():
    one_star_itemsets[id] = list(itertools.chain.from_iterable(one_star_itemsets[id]))
  two_star_id = ('*', '*')
  two_star_itemsets[two_star_id] = []
  for id, itemsets in zero_star_itemsets.items():
    two_star_itemsets[two_star_id].append(itemsets)
  two_star_itemsets[two_star_id] = list(itertools.chain.from_iterable(two_star_itemsets[two_star_id]))
  for id, itemsets in one_star_itemsets.items():
    one_star_itemsets[id] = combine_same_itemsets_count(itemsets)
  for id, itemsets in two_star_itemsets.items():
    two_star_itemsets[id] = combine_same_itemsets_count(itemsets)
  return [zero_star_itemsets, one_star_itemsets, two_star_itemsets]


# In[5]:


config_data = get_config_info()
MIN_SUPPORT_VALUE = int(config_data['min_support'])
filename = config_data['filename']


# In[6]:


def get_quantized_list(rows):
  so2_list = []
  no2_list = []
  pmt_list = []

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


# In[7]:


def get_spatial_list(rows):
  location = []
  for row in rows:
    location.append(row[0])
  return location


# In[8]:


def get_temporal_list(rows):
  months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'Semptember', 'October', 'November', 'December']
  return [months[int(row[1].split('-')[1])-1] for row in rows]


# In[9]:


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


# In[10]:


t1 = datetime.datetime.now()


# In[11]:


transactions = preprocessing('./Big_Dataset.csv')


# In[12]:


t2 = datetime.datetime.now()


# In[13]:


transactions


# In[14]:


location_time_star_items = get_location_time_star_items(transactions)


# In[15]:


final_itemsets = find_frequent_patterns_by_location_time(transactions, MIN_SUPPORT_VALUE)


# In[16]:


t3 = datetime.datetime.now()


# In[17]:


star_itemsets = get_star_itemsets(final_itemsets, location_time_star_items)


# In[18]:


t4 = datetime.datetime.now()


# In[19]:


zero_star_itemsets = star_itemsets[0]


# In[20]:


one_star_itemsets = star_itemsets[1]


# In[21]:


two_star_itemsets = star_itemsets[2]


# In[ ]:





# In[ ]:





# In[22]:


t5 = datetime.datetime.now()


# In[25]:


preprocess_time = t2-t1

two_Item_set_time = t3-t2

Star_Item_set_time = t4-t2

total_time = t5-t1


# In[27]:


print(20*'*')
print('Min support value:', MIN_SUPPORT_VALUE)
print(20*'*')
print_table(zero_star_itemsets, 'Itemsets for CMB')
print_table(one_star_itemsets, 'Itemsets for 1 star CMP')
print_table(two_star_itemsets, 'Itemsets for 2 star')
print('Total time taken for preprocessing in (microseconds) by FP-Tree algorithm:', preprocess_time.microseconds)
print('Total time taken for 2-Item-set in (microseconds) by FP-Tree algorithm:', two_Item_set_time.microseconds)
print('Total time taken for star_Item-set in (microseconds) by FP-Tree algorithm:', Star_Item_set_time.microseconds)
#print('Total time taken in (microseconds) by FP-Tree algorithm:', total_time.microseconds)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




