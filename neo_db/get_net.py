from neo_db.config import graph, CA_LIST, similar_words
import codecs
import os
import json
import base64
from py2neo.data import Node, Relationship
import re

def query_book(name):
    data = graph.run(
    "MATCH (p)-[r]->(n) where n.ns0__book_info_name='%s' RETURN p,r,n union MATCH (p)-[r]->(n) where p.ns0__book_info_name='%s' RETURN p,r,n" % (name,name)
    ).data()

    data = list(data)
    return get_json_data(data)


def query_movie(name):
    data = graph.run(
    "MATCH (p)-[r]->(n) where n.ns0__movie_info_name='%s' RETURN p,r,n union MATCH (p)-[r]->(n) where p.ns0__movie_info_name='%s' RETURN p,r,n" % (name,name)
    ).data()

    data = list(data)

    return get_json_data(data)


def query_cooperate(name1,name2):
    data = graph.run(
    "MATCH (p:ns0__movie_person{ns0__movie_person_name: '%s'}) - [r*..3] - (n:ns0__movie_person{ns0__movie_person_name: '%s'})RETURN p,r,n" % (name1,name2)
    )

    data = list(data)
    return get_cooperate_json_data(data)



def get_json_data(data):

    json_data = {'data': [], "links": []}
    d = []
    d_categery_dict = {}
    for i in data:
        r = str(i['r'])
        if 'ns0__has_acted_in' in r:
            d.append(i['p']['ns0__movie_person_name'])
            d.append(i['n']['ns0__movie_info_name'])
            d_categery_dict[i['p']['ns0__movie_person_name']] = 'person'
            d_categery_dict[i['n']['ns0__movie_info_name']] = 'movie'
            d = list(set(d))
        if 'ns0__has_authored_in' in r:
            d.append(i['p']['ns0__book_person_name'])
            d.append(i['n']['ns0__book_info_name'])
            d_categery_dict[i['p']['ns0__book_person_name']] = 'person'
            d_categery_dict[i['n']['ns0__book_info_name']] = 'book'
            d = list(set(d))
        if 'ns0__has_book_genre' in r:
            d.append(i['p']['ns0__book_genre_name'])
            d.append(i['n']['ns0__book_info_name'])
            d_categery_dict[i['p']['ns0__book_genre_name']] = 'genre'
            d_categery_dict[i['n']['ns0__book_info_name']] = 'book'
            d = list(set(d))
        if 'ns0__has_directed_in' in r:
            d.append(i['p']['ns0__movie_person_name'])
            d.append(i['n']['ns0__movie_info_name'])
            d_categery_dict[i['p']['ns0__movie_person_name']] = 'person'
            d_categery_dict[i['n']['ns0__movie_info_name']] = 'movie'
            d = list(set(d))
        if 'ns0__has_movie_genre' in r:
            d.append(i['p']['ns0__movie_genre_name'])
            d.append(i['n']['ns0__movie_info_name'])
            d_categery_dict[i['p']['ns0__movie_genre_name']] = 'genre'
            d_categery_dict[i['n']['ns0__movie_info_name']] = 'book'
            d = list(set(d))
        if 'ns0__has_translated_in' in r:
            d.append(i['p']['ns0__book_info_name'])
            d.append(i['n']['ns0__book_person_name'])
            d_categery_dict[i['p']['ns0__book_info_name']] = 'book'
            d_categery_dict[i['n']['ns0__book_person_name']] = 'person'
            d = list(set(d))
        if 'ns0__has_writed_in' in r:
            d.append(i['p']['ns0__movie_person_name'])
            d.append(i['n']['ns0__movie_info_name'])
            d_categery_dict[i['p']['ns0__movie_person_name']] = 'person'
            d_categery_dict[i['n']['ns0__movie_info_name']] = 'movie'
            d = list(set(d))
    name_dict = {}
    count = 0
    for j in d:
        data_item = {}
        name_dict[j] = count
        count += 1
        data_item['name'] = j
        data_item['category'] = d_categery_dict[j]
        json_data['data'].append(data_item)

    for i in data:
        r = str(i['r'])
        link_item = {}
        if 'ns0__has_acted_in' in r:
            link_item['source'] = name_dict[i['p']['ns0__movie_person_name']]
            link_item['target'] = name_dict[i['n']['ns0__movie_info_name']]
            link_item['value'] = 'has_acted_in'
            json_data['links'].append(link_item)
        if 'ns0__has_authored_in' in r:
            link_item['source'] = name_dict[i['p']['ns0__book_person_name']]
            link_item['target'] = name_dict[i['n']['ns0__book_info_name']]
            link_item['value'] = 'has_authored_in'
            json_data['links'].append(link_item)
        if 'ns0__has_book_genre' in r:
            link_item['source'] = name_dict[i['p']['ns0__book_genre_name']]
            link_item['target'] = name_dict[i['n']['ns0__book_info_name']]
            link_item['value'] = 'has_book_genre'
            json_data['links'].append(link_item)
        if 'ns0__has_directed_in' in r:
            link_item['source'] = name_dict[i['p']['ns0__movie_person_name']]
            link_item['target'] = name_dict[i['n']['ns0__movie_info_name']]
            link_item['value'] = 'has_directed_in'
            json_data['links'].append(link_item)
        if 'ns0__has_movie_genre' in r:
            link_item['source'] = name_dict[i['p']['ns0__movie_genre_name']]
            link_item['target'] = name_dict[i['n']['ns0__movie_info_name']]
            link_item['value'] = 'has_movie_genre'
            json_data['links'].append(link_item)
        if 'ns0__has_translated_in' in r:
            link_item['source'] = name_dict[i['p']['ns0__book_info_name']]
            link_item['target'] = name_dict[i['n']['ns0__book_person_name']]
            link_item['value'] = 'has_translated_in'
            json_data['links'].append(link_item)
        if 'ns0__has_writed_in' in r:
            link_item['source'] = name_dict[i['p']['ns0__movie_person_name']]
            link_item['target'] = name_dict[i['n']['ns0__movie_info_name']]
            link_item['value'] = 'has_writed_in'
            json_data['links'].append(link_item)
    return json_data
# f = codecs.open('./static/test_data.json','w','utf-8')
# f.write(json.dumps(json_data,  ensure_ascii=False))

def get_cooperate_json_data(data):
    json_data = {'data': [], "links": []}
    data_item = {}
    data_item['name'] = data[0]['p']['ns0__movie_person_name']
    data_item['category'] = 'person'
    json_data['data'].append(data_item)
    data_item1 = {}
    data_item1['name'] = data[0]['n']['ns0__movie_person_name']
    data_item1['category'] = 'person'
    json_data['data'].append(data_item1)
    count = 2
    for i in data:
        print(i['r'])
        r = str(i['r'])
        movie = re.findall("ns0__movie_info_name=\'(.*?)\'", r)[0]
        data_item = {}
        data_item['name'] = movie
        data_item['category'] = 'movie'
        json_data['data'].append(data_item)
        link_item1 = {}
        link_item1['source'] = 0
        link_item1['target'] = count
        link_item1['value'] = 'has_acted_in'
        link_item2 = {}
        link_item2['source'] = 1
        link_item2['target'] = count
        link_item2['value'] = 'has_acted_in'
        json_data['links'].append(link_item1)
        json_data['links'].append(link_item2)
        count+=1
    return json_data






#print(query_book('极品殿下（全2册）'))
#print(query_cooperate('李连杰','章子怡'))