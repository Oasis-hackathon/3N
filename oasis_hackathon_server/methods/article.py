from uuid import UUID

import constants.messages
from connector import MySQL
from constants import messages


def if_article_exist(article_id: int):
    sql = MySQL()
    if sql.query('SELECT COUNT(*) FROM article WHERE id=%s', (article_id, ))[0][0] == 1:
        return True
    else:
        return False


def get_articles(user_uuid: UUID, address: str, article_type: str, article_category: str, start_idx: int, end_idx: int):
    sql = MySQL(dict_cursor=True)

    if article_type != 'None' and article_category != 'None':
        pre_result = list(sql.query("SELECT id, title, cost, image, submitter, reg_date, is_visible "
                                    "FROM article WHERE address=%s AND article_type=%s "
                                    "AND article_category=%s ORDER BY reg_date asc LIMIT %s, %s",
                                    (address, article_type, article_category, int(start_idx), int(end_idx))))
    else:
        pre_result = list(sql.query("SELECT id, title, cost, image, submitter, reg_date, is_visible "
                                    "FROM article WHERE address=%s ORDER BY reg_date asc LIMIT %s, %s",
                                    (address, int(start_idx), int(end_idx))))
    result = list()

    for i in pre_result:
        if bool(i['is_visible']):
            if i['image'] is None or i['image'] == "":
                i['image'] = "no image"
            i['submitter'] = sql.query('SELECT nickname FROM account WHERE uuid=%s',
                                       (UUID(bytes=i['submitter']).bytes, ))[0]['nickname']
            if sql.query('SELECT COUNT(*) FROM fork WHERE uuid=%s AND article_id=%s', (user_uuid.bytes, i['id']))[0]['COUNT(*)']:
                i['fork'] = 'active'
            else:
                i['fork'] = 'unactive'

            result.append(i)

    return True, result


def get_article(article_id: int):
    sql = MySQL(dict_cursor=True)

    result = sql.query('SELECT id, title, submitter, address, image, cost, content, '
                       'remain_time, max_num, article_type, article_category, reg_date, is_visible, views '
                       'FROM article WHERE id=%s', (article_id, ))

    if len(result) == 0:
        return False, None

    result = result[0]

    seller_info = sql.query('SELECT nickname, image, rate FROM account WHERE uuid=%s',
                            (UUID(bytes=result['submitter']).bytes,))[0]
    result['submitter_image'] = seller_info['image']
    result['submitter'] = seller_info['nickname']
    result['submitter_result'] = seller_info['rate']

    if result['image'] is None or result['image'] == "":
        result['image'] = "no image"

    if result['submitter_image'] is None or result['submitter_image'] == "":
        result['submitter_image'] = "no image"

    if not bool(result['is_visible']):
        return False, None

    else:
        sql.transaction.start()
        try:
            sql.query('UPDATE article SET views = views + 1 WHERE id=%s', (article_id, ))
        except Exception as e:
            print(e)
        else:
            sql.transaction.commit()
            return True, result


def get_articles_with_search(keyword: str, start_idx: int, end_idx: int):
    sql = MySQL(dict_cursor=True)

    return {'success': True}, list(sql.query(f"SELECT id, title, HEX(submitter) submitter, reg_date, last_modified, is_notify, views FROM article "
                                             f"WHERE is_visible=1 AND title regexp '{keyword}' "
                                             f"ORDER BY reg_date asc LIMIT {start_idx}, {end_idx}"))


def delete_article(article_id: int):
    sql = MySQL()

    result = sql.query('SELECT submitter FROM article WHERE id=%s', (article_id, ))

    if len(result) == 0:
        return False, constants.messages.article_no_exists, 404

    sql.transaction.start()
    try:
        sql.query('DELETE FROM article WHERE id=%s', (article_id, ))
    except:
        sql.transaction.rollback()
        return False, constants.messages.exception_occurred, 403
    else:
        sql.transaction.commit()
        return True, None, 200


def create_article(title=None, submitter: UUID = None, address=None, image=None, cost=None,
                   content=None, remain_time=None, max_num=None, article_type=None, article_category=None):
    sql = MySQL()

    if title is None or submitter is None or address is None or cost is None:
        return False, messages.no_required_args, 400
    if remain_time is None or max_num is None or article_type is None or article_category is None:
        return False, messages.no_required_args, 400

    if image is None:
        image = ''
    if content is None:
        content = ''

    sql.transaction.start()
    try:
        sql.query('INSERT INTO article '
                  '(title, submitter, address, image, cost, content, remain_time, '
                  'max_num, article_type, article_category) '
                  'VALUE (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                  (title, submitter.bytes, address, image, cost, content, remain_time,
                   max_num, article_type, article_category))
    except:
        sql.transaction.rollback()
        return False, messages.exception_occurred, 500
    else:
        inserted = sql.query('SELECT LAST_INSERT_ID()')[0][0]
        sql.transaction.commit()
        return True, inserted, 200


def make_fork(user_uuid: UUID, article_id: int):
    sql = MySQL()

    sql.transaction.start()
    try:
        sql.query('INSERT INTO fork (uuid, article_id) VALUE (%s, %s)', (user_uuid.bytes, article_id, ))
    except Exception as e:
        print(e)
        return False, {'message': "fork_fail"}, 500
    else:
        sql.transaction.commit()
        return True, None, 200
