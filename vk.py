# -*- coding: utf-8 -*-
import vk_api
import credentials

location_name = 'vladimir'


def main():
    """ Пример получения последнего сообщения со стены """

    login, password = credentials.login(), credentials.password()
    vk_session = vk_api.VkApi(login, password)

    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()

    """ VkApi.method позволяет выполнять запросы к API. В этом примере
        используется метод wall.get (https://vk.com/dev/wall.get) с параметром
        count = 1, т.е. мы получаем один последний пост со стены текущего
        пользователя.
    """

    items = set()

    with open(f'events_{location_name}.txt', 'r') as fp:
        num_lines = sum(1 for ln in fp)
        events_count = 0
        fp.seek(0)
        for event in fp:
            events_count += 1
            print(f'{events_count}/{num_lines}')
            print(f'Event {event}')
            offset = 0
            while True:
                try:
                    q = vk.groups.getMembers(group_id=event, offset=offset)
                    items.update(q['items'])
                    if len(q['items']) < 1000:
                        break
                    offset += 1000
                except vk_api.exceptions.ApiError as e:
                    print(e)
                    break
                except:
                    break

            offset = 0
            while True:
                try:
                    q = vk.groups.getMembers(group_id=event, offset=offset, filter='unsure')
                    items.update(q['items'])
                    if len(q['items']) < 1000:
                        break
                    offset += 1000
                except vk_api.exceptions.ApiError as e:
                    print(e)
                    break
                except:
                    break

            print(len(items))
            pass

    with open(f'events_members_{location_name}.txt', 'w') as f:
        for item in items:
            f.write("%s\n" % item)


if __name__ == '__main__':
    main()
