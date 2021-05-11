from database.tools import *
import exceptions


class Content:
    SORT_BY_CREATED_TIME = 'created_time'

    def __init__(self, d):
        self.d = d
        self.col: pymongo.collection.Collection = self.d.content
        self.tree: pymongo.collection.Collection = self.d.content_tree
        insert_id_if_not_exist(self.d.content_cid, "cnt_cid", 0)
        auto_time_update(self.tree, {'anchor': {"$exists": True}}, {
            'anchor': True,
            '/': {}
        })

    def get_tree_root(self) -> dict:
        tree = find_one(self.tree, {'anchor': {"$exists": True}})
        root = tree['/']
        return root

    def update_tree_path(self, path: str):
        root = self.get_tree_root()
        root = tree_update_path(root, path=path)
        auto_time_update(self.tree, {'anchor': {"$exists": True}}, {'/': root})

    def delete_tree_path(self, path: str):
        root = self.get_tree_root()
        root = tree_delete_path(root, path=path)
        auto_time_update(self.tree, {'anchor': {"$exists": True}}, {'/': root})

    def get_next_cid(self):
        ret = self.d.content_cid.find_one_and_update({"_id": "cnt_cid"},
                                                     {"$inc": {"sequence_value": 1}},
                                                     new=True)
        new_cid = ret["sequence_value"]
        return new_cid

    def insert(self, content: dict) -> int:
        cid = self.get_next_cid()
        content['cid'] = cid
        if 'path' not in content:
            content['path'] = '/'
        elif not str.startswith(content['path'], '/'):
            content['path'] = '/'
        # 和浏览器的 path 兼容
        content['path'].replace('\\', '/')
        self.update_tree_path(content['path'])
        auto_time_update(self.col, {'cid': cid}, content)
        return cid

    def find(self, filter_dict: dict,
             sort_by: str = "cid",
             reverse: bool = True,
             limit: int = Constants.FIND_LIMIT,
             offset: int = 0,
             path_prefix: str = None) -> list:
        if sort_by is None:
            sort_by = Content.SORT_BY_CREATED_TIME
        if 'password' not in filter_dict:
            filter_dict['password'] = {'$exists': False}
        result = find_many(self.col, filter_dict, limit=limit, offset=offset, sort_by=sort_by, reverse=reverse)
        return result

    def update_one(self, content: dict) -> bool:
        cid = content.get('cid')
        content_data = self.get_by_cid(cid)
        if content_data is None:
            return False
        print('content_data', json_dumps_format(content_data))
        print('content', json_dumps_format(content))
        if 'created_at' in content_data:
            del content_data['created_at']
        dict_update(content_data, content)
        auto_time_update(self.col, {'cid': cid}, content_data)
        return True

    def get_by_cid(self, cid: int) -> dict or None:
        return find_one(self.col, {'cid': cid})

    def find_by_title(self, title: str) -> dict or None:
        return find_one(self.col, {'title': title})

    def delete_one(self, cid: int):
        content = self.get_by_cid(cid)
        self.delete_tree_path(path=content.get('path'))
        self.col.delete_one({'cid': cid})
