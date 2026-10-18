from app.repositories.base import ArticleRepository
from app.schemas.news import ArticleRequest
import json


class FileArticleRepository(ArticleRepository):

    '''
    File interface implementation
    Check dupe using a set instead of DB
    '''

    # TODO : FileNotFoundError raise in custom error class
    # Json load error on empty file

    async def save_articles_to_db(self, articles:list[ArticleRequest]):

        '''
        Save articles to file.
        '''
        articles_list = [a.model_dump(mode='json') for a in articles]
        url_set = set()

        try:
            with open('db.txt','r') as f:
                content = json.load(f)
                for c in content:
                    url_set.add(c['url'])
        except FileNotFoundError:
            content = []
            
        for a in articles_list:
            if a['url'] not in url_set:
                url_set.add(a['url'])
                content.append(a)

        with open('db.txt','w') as f:
            json.dump(content,f)

