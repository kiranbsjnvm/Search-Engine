import time
import urllib

def get_page(url):
    try:
        return urllib.urlopen(url).read()
    except:
        return ""

#********************************************   HASHING     ******************************************************

def make_hash_table(nbuckets):
    table = []
    for x in range(0,nbuckets):
        table.append([])
    return table

def hash_string(keyword,nbucket):               
    sum=0
    for c in keyword:
        sum = sum + ord(c)
    value = sum % nbucket
    return value

def hashtable_get_bucket(htable, key):
    hv = hash_string(key, len(htable))
    return htable[hv]

def hashtable_update(htable,key,value):
    bucket = hashtable_get_bucket(htable,key)
    for entry in bucket:
        if entry[0] == key:
            entry[1] = value    #Overwritting by new url
            #entry[1].append(value)
            return
    bucket.append([key,value])

def hashtable_lookup(htable,key):
    bucket = hashtable_get_bucket(htable,key)
    for entry in bucket:
        if entry[0] == key:
            return entry[1]
    return None


#*****************************  INDEX CODE  ***************************************************#
    
#def add_to_index(index,keyword,url):
#    for entry in index:
#        if entry[0] == keyword:                 #checking weather keyword is alredy present or not
#            if url not in entry[1]:                 #checking weather url is alredy added or not 
#                entry[1].append(url)
#            return
#    index.append([keyword,[url]])


#Add to index using dictionarie
def add_to_index(index,keyword,url):
    if keyword in index:
        if url not in index[keyword]:
            index[keyword].append(url)
    else:
        index[keyword]=[url]


#def lookup(index,keyword):
#    for entry in index:
#        if entry[0] == keyword:
#            return entry[1]
#    return []

#lookup in dictionarie 
def lookup(index,keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None

table = make_hash_table(100)

def add_page_to_index(index,url,content):
    words = content.split()
    for value in words:
        add_to_index(index,value,url)
        hashtable_update(table,value,url)

#***********************************    CRAWLER     *******************************************#

def get_next_target(page):
    start_link = page.find('a href=')
    if start_link==-1:
        return None,0
    else:
        start_qute = page.find('"',start_link)
        end_qute = page.find('"',start_qute+1)
        url = page[start_qute+1:end_qute]
        if '?' in url:
            end_pos = page.find('?',start_qute+1)
            url = page[start_qute+1:end_pos]
        return url, end_qute

def get_all_links(page):
    links = []                                                  #initializing list to empty
    while True:
        url,endpos = get_next_target(page)
        if url:
            links.append(url)
            page=page[endpos:]
        else:
            break
    return links


def union(a,b):                            # union of a and b
    flag=1
    for x in b:
        if x not in a:
            a.append(x)
    return a


def crawl_web(seed_url):
    to_crawl = [seed_url]
    crawled = []
    index = {}
    graph = {}          #To store the structure of all links , graph = { {url0: {url1,url2,....}, url1:{ } , .....}
    while to_crawl:
        url = to_crawl.pop()
        if url not in crawled and url != '#':
            content = get_page(url)
            add_page_to_index(index,url,content)
            outgoing_links = get_all_links(content)
            graph[url] = outgoing_links
            to_crawl = union(to_crawl,outgoing_links)  
            crawled.append(url)
    return index,crawled,graph

index_list,crawled_links , graph = crawl_web('index.php')
print crawled_links


#**************************************  RANK   ******************************************************

def compute_rank(graph):
    d = 0.8
    numloops = 100
    ranks = {}
    npages = len(graph)

    for page in graph:
        ranks[page] = 1.0/npages
    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1-d)/npages
            for node in graph:
                if page in graph[node]:
                    newrank = newrank + d * (ranks[node] / len(graph[node]))                    
            newranks[page] = newrank
        ranks = newranks
    return ranks

#**************************************************************************************************


start = time.clock()
print lookup(index_list,'my')
end = time.clock()
print end-start

start = time.clock()
print hashtable_lookup(table,'my')
end = time.clock()
print end-start


#print 'runtime for seraching keyword is ' + `end - start`
#print graph['primary.php']

#counting no of keywords in index
#count =0
#for item in index_list:
#    count = count+1

#print count

#ranks = compute_rank(graph)
#print ranks
