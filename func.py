import threading
import requests
import time
import yeelight
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope
import dictionaries
from twitchAPI.pubsub import PubSub
from uuid import UUID
from datetime import datetime

threads_donate = []
threads_follow = []
threads_loop_list = []


def start_monitoring():
    """
    Запускается при нажатии кнопки Start в GUI.
    Нужна для инициализации нужных переменных и запуска потоков для каждой из отслеживаемых переменных для запуска
    уведомления.

    :return:
    """

    initialize_bulbs()
    initialize_link()
    twitch_app = twitch_auth_app()
    twitch_user = twitch_auth_user()
    broadcaster_id = get_broadcaster_id(twitch_app)
    for bulb in dictionaries.bulbs:  #У ламп и РГБ лент сейчас есть баг, что они не могут вернуть текущее состояние, в обход этого при старте всегда запускается 1 цвет
        bulb.set_rgb(int(dictionaries.previous_rgb[0]), int(dictionaries.previous_rgb[1]), int(dictionaries.previous_rgb[2]))
    if not threads_loop_list:
        t = threading.Thread(target=thread_loop, args=(twitch_app, broadcaster_id), daemon=True)
        t.start()
        threads_loop_list.append(t)
        print(threading.enumerate())
    wait_for_new_sub(twitch_user, broadcaster_id)


def wait_for_donate_alert():
    """
    Каждую секунду делает GET запрос. Если выявляется новое пожертвование, то запускается уведомление

    :return:
    """
    r = requests.get(dictionaries.donation_link_full[0])
    json_past = float(r.json()['response']['data'][0]['sum'])
    while True:
        r = requests.get(dictionaries.donation_link_full[0])
        json_current = float(r.json()['response']['data'][0]['sum'])
        if json_past != json_current:
            json_past = json_current
            donation_switch_lights(json_current)
        time.sleep(1)


def wait_for_new_follower(twitch, broadcaster_id):
    """
    Каждую секунду делает GET запрос к Twitch. При новом фолловере запускается уведомление

    :return:
    """
    r = Twitch.get_users_follows(twitch, first=1, to_id=broadcaster_id)
    previous_follower = int(r['data'][0]['from_id'])
    while True:
        r = Twitch.get_users_follows(twitch, first=1, to_id=broadcaster_id)
        current_follower = int(r['data'][0]['from_id'])
        if previous_follower != current_follower:
            previous_follower = current_follower
            follow_switch_lights()
        ts = time.time()
        ts = datetime.fromtimestamp(ts)
        with open('Logs.txt', 'a+') as outfile:
            outfile.write(str(ts) + str(r)+"\n")
        time.sleep(1)


def wait_for_new_sub(twitch, broadcaster_id):
    """
    Попытка сделать ту же операцию, что и в wait_for_new_follower, но по средствам Twitch API
    Создается подписка на действие "Subscribe". И если это действие происходит, вызывается запуск уведомления

    :return:
    """
    pubsub = PubSub(twitch)
    pubsub.start()
    pubsub.listen_channel_subscriptions(broadcaster_id, sub_switch_lights)


def follow_switch_lights():
    """
    Функция для запуска уведомления для нового фолловера.

    :return:
    """
    start_stop_flow(selected_flow=dictionaries.effects[dictionaries.saved_effects['follow_effect'][0]][0],
                    duration=int(dictionaries.saved_effects['follow_duration'][0]))


def sub_switch_lights(uuid: UUID, data: dict) -> None:
    """
    Функция для запуска уведомления для нового подписчика.

    :param uuid: uuid нового подписчика
    :param data: данные по новому подписчику
    :return:
    """
    start_stop_flow(selected_flow=dictionaries.effects[dictionaries.saved_effects['sub_effect'][0]][0],
                    duration=int(dictionaries.saved_effects['sub_duration'][0]))
    ts = time.time()
    ts = datetime.fromtimestamp(ts)
    with open('Logs_subs.txt', 'a+') as outfile:
        outfile.write(str(ts) + str(uuid) + "\t" + str(data) + "\n")


def donation_switch_lights(amount):
    """
    Функция для запуска уведомления для нового пожертвования

    :param amount: сумма доната
    :return:
    """
    found_bracket = None
    for bracket in dictionaries.brackets_classes:
        if bracket.min <= amount <= bracket.max:
            found_bracket = bracket
    if found_bracket:
        if str(found_bracket.effect) == 'RGB':
            for bulb in dictionaries.bulbs:
                try:
                    bulb.set_rgb(int(found_bracket.color[0]), int(found_bracket.color[1]),
                                 int(found_bracket.color[2]))
                except:
                    pass
            dictionaries.previous_rgb = found_bracket.color
        else:
            start_stop_flow(selected_flow=dictionaries.effects[str(found_bracket.effect)][0],
                            duration=int(found_bracket.duration))


def twitch_auth_app():
    """
    Функция авторизации приложения на стороне Twitch для использования API

    :return:
    """
    twitch = Twitch('v2m6lpsgrw410cdfqqqgr29uc7m7jx', 'oezl30gj5cs7ll80axb8qhothxzunh')
    twitch.authenticate_app([])
    return twitch


def twitch_auth_user():
    """
    Функция авторизации пользователя на стороне Twitch для использования API.

    :return:
    """
    twitch = Twitch('52i4tirzld6gfnoelunofmoz0l43ai', 'hnlxaqfjskcicw2vtl3uhz2fkkasl2')
    target_scope = [AuthScope.CHANNEL_READ_SUBSCRIPTIONS]
    auth = UserAuthenticator(twitch, target_scope, force_verify=False)
    token, refresh_token = auth.authenticate()
    twitch.set_user_authentication(token, target_scope, refresh_token)
    return twitch


def get_broadcaster_id(twitch):
    """
    Получение id, с которого запущена трансляция

    :param twitch: объект twitch API
    :return:
    """
    r = twitch.get_users(logins=dictionaries.twitch[0])
    return(r['data'][0]['id'])


def initialize_bulbs():
    """
    Инициализация словаря bulb.

    :return:
    """
    for p in dictionaries.lights['bulb']:
        bulb = yeelight.Bulb(p)
        dictionaries.bulbs.append(bulb)


def initialize_link():
    """
    Инициализация ссылки для сайта donate.stream

    :return:
    """
    dictionaries.donation_link_full.append('https://donate.stream/api/v1/donateAlert.paginate?app=31eec3f14e45ed242b78e6374724ade8&token='
                                           + str(dictionaries.donation_link[0]))


def test_follow_effect():
    """
    Фунция для тестирования уведомления для нового фолловера

    :return:
    """
    #initialize_bulbs()
    start_stop_flow(selected_flow=dictionaries.effects[dictionaries.saved_effects['follow_effect'][0]][0],
                    duration=int(dictionaries.saved_effects['follow_duration'][0]))


def test_sub_effect():
    """
    Фунция для тестирования уведомления для нового подписчика

    :return:
    """
    #initialize_bulbs()
    start_stop_flow(selected_flow=dictionaries.effects[dictionaries.saved_effects['sub_effect'][0]][0],
                    duration=int(dictionaries.saved_effects['sub_duration'][0]))


def print_threads():
    """
    Функция используемая для отладки, чтобы можно было мониторить запущенные потоки

    :return:
    """
    while True:
        print(threading.enumerate())
        time.sleep(1)


def thread_loop(twitch_app, broadcaster_id):
    """
    Запуск потоков для отслеживания новых пожертвований и фолловеров. Подписчики сделаны по другой системе

    :param twitch_app: Объект twitch приложения
    :param broadcaster_id: ID пользователя, который проводит трансляцию
    :return:
    """
    if not threads_donate:
        t = threading.Thread(target=wait_for_donate_alert, daemon=True)
        t.start()
        threads_donate.append(t)
        print(threading.enumerate())

    if not threads_follow:
        d = threading.Thread(target=wait_for_new_follower, args=(twitch_app, broadcaster_id), daemon=True)
        d.start()
        threads_follow.append(d)
        print(threading.enumerate())


def start_stop_flow(selected_flow, duration):
    '''
    Фунция для запуска и остановки уведомления

    :param selected_flow: выбранный эффект
    :param duration: длительность эффекта
    :return:
    '''
    for bulb in dictionaries.bulbs:
        try:
            bulb.start_flow(selected_flow)
        except:
            pass
    time.sleep(int(duration))
    for bulb in dictionaries.bulbs:
        try:
            bulb.stop_flow()
        except:
            pass
    for bulb in dictionaries.bulbs:
        try:
            bulb.set_rgb(int(dictionaries.previous_rgb[0]), int(dictionaries.previous_rgb[1]),
                         int(dictionaries.previous_rgb[2]))
        except:
            pass
