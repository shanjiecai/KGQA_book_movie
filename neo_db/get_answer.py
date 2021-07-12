from py2neo import *
from neo_db.config import graph, CA_LIST, similar_words

class Get_answer():
    def __init__(self):
        self.graph = graph

    def get_data(self, index, params):
        query = ''
        if index == 0:
            query = "MATCH (n:ns0__movie_info) WHERE n.ns0__movie_info_name='{}' RETURN  n.ns0__movie_info_rating,n.ns0__movie_info_name,{},n.ns0__movie_info_review_count,n.ns0__movie_info_image_url;".format(params[0],'-1')  # 评分
        elif index == 1:
            query = "MATCH (n:ns0__movie_info) WHERE n.ns0__movie_info_name='{}' RETURN  n.ns0__movie_info_pubdate,n.ns0__movie_info_name,n.ns0__movie_info_rating,n.ns0__movie_info_review_count,n.ns0__movie_info_image_url;".format(params[0])  # 上映时间
        elif index == 2:
            query = "MATCH (n:ns0__movie_info) WHERE n.ns0__movie_info_name='{}' RETURN  n.ns0__movie_info_duration,n.ns0__movie_info_name,n.ns0__movie_info_rating,n.ns0__movie_info_review_count,n.ns0__movie_info_image_url;".format(params[0])  # 时长
        elif index == 3:
            query = "MATCH (n:ns0__movie_info) WHERE n.ns0__movie_info_name='{}' RETURN  n.ns0__movie_info_summary,n.ns0__movie_info_name,n.ns0__movie_info_rating,n.ns0__movie_info_review_count,n.ns0__movie_info_image_url;".format(params[0])  # 简介
        elif index == 4:
            query = "MATCH (p)-[r:ns0__has_acted_in]->(n) WHERE n.ns0__movie_info_name='{}' RETURN  p.ns0__movie_person_name,{},p.ns0__movie_person_birthday,p.ns0__movie_person_introduction,p.ns0__movie_person_image_url LIMIT 25;".format(params[0],'-1')  # 演员列表,限制最多25个
        elif index == 5:
            query = "MATCH (n:ns0__movie_person) WHERE n.ns0__movie_person_name='{}' RETURN  n.ns0__movie_person_introduction,p,ns0__movie_person_name,p.ns0__movie_person_birthplace,p.ns0__movie_person_birthday,p.ns0__movie_person_image_url;".format(params[0])  # 演员介绍
        elif index == 6:
            query = "MATCH (n:ns0__movie_info) WHERE n.ns0__movie_info_name='{}' RETURN  n.ns0__movie_info_country,n.ns0__movie_info_name,n.ns0__movie_info_rating,n.ns0__movie_info_review_count,n.ns0__movie_info_image_url".format(params[0], params[
                1])  # 电影国家
        elif index == 7:
            query = "MATCH (p)-[r:ns0__has_acted_in]->(n) WHERE p.ns0__movie_person_name='{}' RETURN  n.ns0__movie_info_name,{},n.ns0__movie_info_rating,n.ns0__movie_info_review_count,n.ns0__movie_info_image_url LIMIT 25;".format(
                params[0],'-1')  # 某演员演过什么电影，限制最多25个
        elif index == 8:
            query = "MATCH (n:ns0__movie_person) WHERE n.ns0__movie_person_name='{}' RETURN n.ns0__movie_person_birthday,n.ns0__movie_person_name,{},n.ns0__movie_person_birthday,n.ns0__movie_person_image_url".format(
                params[0], params[1])  # 演员出生日期
        elif index == 9:
            query = "MATCH (n:ns0__book_info) WHERE n.ns0__book_info_name='{}' RETURN n.ns0__book_info_content_abstract,n.ns0__book_info_name,n.ns0__book_info_rating,n.ns0__book_info_review_count,n.ns0__book_info_image_url;".format(
                params[0])  # 某本书的简介
        elif index == 10:
            query = "MATCH (p)-[r:ns0__has_authored_in]->(n) WHERE p.ns0__book_person_name='{}' RETURN n.ns0__book_info_name,{},n.ns0__book_info_rating,n.ns0__book_info_review_count,n.ns0__book_info_image_url LIMIT 25;".format(params[0],'-1')  # 作家写了哪些书
        elif index == 11:
            query = "MATCH (p)-[r:ns0__has_directed_in]->(n) WHERE p.ns0__movie_person_name='{}' RETURN  n.ns0__movie_info_name,{},n.ns0__movie_info_rating,n.ns0__movie_info_review_count,n.ns0__movie_info_image_url LIMIT 25;".format(params[0],'-1')  # 某导演导演了哪些电影

        result= self.graph.run(query)

        return result



if __name__ == "__main__":
    ga = Get_answer()
    answers = ga.get_data(3, ['英雄'])
    for answer in answers:
        print(answer[0])
