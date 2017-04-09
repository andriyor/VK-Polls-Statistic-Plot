import vk_api
import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.font_manager as font_manager

path = 'Roboto.ttf'
prop = font_manager.FontProperties(fname=path)


def main():
    login, password = os.environ.get('LOGIN'), os.environ.get('PASSWORD')
    vk_session = vk_api.VkApi(login, password)

    try:
        vk_session.auth()
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return

    vk = vk_session.get_api()

    # by_id = vk.polls.getById(owner_id=-64525872, is_board=0, poll_id=202047674)
    by_id = vk.polls.getById(owner_id=-60535091, is_board=0, poll_id=237645103)
    print(by_id)
    text = []
    votes = []
    answer_ids = []
    for i in by_id['answers']:
        text.append(i['text'])
        votes.append(i['votes'])
        answer_ids.append(i['id'])

    answer_ids = (', '.join([str(i) for i in answer_ids]))
    # voters = vk.polls.getVoters(owner_id=-64525872, poll_id=202047674, answer_ids=answer_ids)
    voters = vk.polls.getVoters(owner_id=-60535091, poll_id=237645103, answer_ids=answer_ids)
    print(voters)

    fv, mv, gv, f_in_f = [], [], [], []
    for voter in voters:
        voters = voter['users']['items']
        voters_str = (', '.join([str(i) for i in voters]))
        users = vk.users.get(user_ids=voters_str, fields='sex')
        w, m, g = [], [], []
        for user in users:
            if user['sex'] == 1:
                w.append(user['id'])
            elif user['sex'] == 2:
                m.append(user['id'])
            elif user['sex'] == 0:
                g.append(user['id'])

        fv.append(len(w))
        mv.append(len(m))
        gv.append(len(g))
        print(m)
        wom_in_friends_in_element = []
        for ids in m:
            wom_in_friends = 0
            print(ids)
            try:
                friends = vk.friends.get(user_id=ids, fields='sex')
                for friend in friends['items']:
                    if friend['sex'] == 1:
                        wom_in_friends += 1
                print(wom_in_friends)
            except Exception:
                continue
            wom_in_friends_in_element.append(wom_in_friends)
        print(wom_in_friends_in_element)
        f_in_f.append(sum(wom_in_friends_in_element))

    print(f_in_f)
    print(mv)
    print(fv)
    x = np.array(list(range(len(votes))))
    plt.xticks(x, text, fontproperties=prop, size=9)
    plt.plot(x, mv)
    plt.plot(x, fv)
    plt.savefig('a.png')
    plt.savefig('a.pdf')
    plt.show()

    a = np.array(f_in_f)
    b = np.array(mv)
    ab = a / b
    plt.xticks(x, text, fontproperties=prop, size=9)
    plt.plot(x, ab)
    plt.savefig('b.png')
    plt.savefig('b.pdf')
    plt.show()


if __name__ == '__main__':
    main()
