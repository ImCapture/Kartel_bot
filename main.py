import telebot
import random
import re

# ключ к боту находится в файле token.txt
bot_token = open('token.txt', 'r')
bot = telebot.TeleBot(f'5643944530:{bot_token.read()}')

# словарь номера за столом => username
quorum = {}

# словарь username => id
username_id = {}

judge = None

roles_list = []
player_username = []
player_number = []
# /start идентичен /help и не появляется в списке команд, а вызывается единожды при первом входе


@bot.message_handler(commands=['start', 'help'])
def comm_help(message):
    with open('comm_help.txt', 'r') as f:
        comm_help_file = f.read()
    bot.send_message(message.chat.id, comm_help_file)


@bot.message_handler(commands=['addme'])
def comm_addme(message):
    quorum[message.chat.username] = 'Слот неизвестен'
    username_id[message.chat.username] = message.chat.id
    bot.send_message(message.chat.id,
                     'Вы добавлены в кворум. '
                     'Если вы этого еще не сделали, '
                     'напишите номер своего слота одним числом')


@bot.message_handler(commands=['removeme'])
def comm_removeme(message):
    if message.chat.username in quorum:
        del (quorum[message.chat.username])
        bot.send_message(message.chat.id,
                         'Вы были удалены из кворума. Для повторной записи напишите /addme')
    else:
        bot.send_message(message.chat.id, 'Вы еще не находитесь в кворуме')


@bot.message_handler(commands=['judge'])
def comm_judge(message):
    global judge
    global judge_id
    if judge == message.chat.username:
        bot.send_message(message.chat.id, 'Вы уже судья')
    else:
        judge = message.chat.username
        judge_id = message.chat.id
        bot.send_message(message.chat.id,
                         'Вы стали судьей. ' +
                         'Чтобы перестать быть судьей, введите /unjudge ' +
                         'или подождите, пока другой игрок станет судьей')


@bot.message_handler(commands=['unjudge'])
def comm_unjudge(message):
    global judge
    global judge_id
    if judge == message.chat.username:
        judge = None
        judge_id = None
        bot.send_message(message.chat.id, 'Теперь вы больше не судья. ' +
                         'Чтобы снова стать судьей, введите команду  /judge')
    else:
        bot.send_message(message.chat.id, 'Вы и так не судья')


@bot.message_handler(commands=['quorum', 'q'])
def comm_quorum(message):
    bot.send_message(message.chat.id, f'Количество игроков: {len(quorum)}\nСудья: @{judge}')
    for k, v in quorum.items():
        if type(v) == int:
            bot.send_message(message.chat.id, f'@{k} - {v} номер')
        else:
            bot.send_message(message.chat.id, f'@{k} - {v}')


@bot.message_handler(commands=['removeall'])
def comm_removeall(message):
    global quorum
    if quorum == {}:
        bot.send_message(message.chat.id, 'Кворум и так пуст.')
    else:
        quorum = {}
        bot.send_message(message.chat.id, 'Кворум был очищен.')


@bot.message_handler(commands=['create', 'c'])
def comm_create(message):

    if judge is None:
        bot.send_message(message.chat.id,
                         text='Невозможно начать игру без наличия судьи. ' +
                         'Для того, чтобы стать судьей, введите /judge')
        return

    # для экономии места и времени мирные жители добавляются через функцию
    def add_red(n):
        for i in range(n):
            roles_list.append('Мирный житель')

    # == 2 оставлено для теста
    if 10 <= len(quorum) <= 15 or len(quorum) == 2:

        # создаем сбалансированный список ролей в зависимости от кол-ва игроков
        if len(quorum) == 2:
            roles_list.append('Комиссар')
            roles_list.append('Дон мафии')
        elif len(quorum) == 10:
            roles_list.append('Комиссар')
            roles_list.append('Дон мафии')
            roles_list.append('Мафия')
            roles_list.append('Мафия')
            add_red(6)
        elif len(quorum) == 11:
            roles_list.append('Комиссар')
            roles_list.append('Дон мафии')
            roles_list.append('Мафия')
            roles_list.append('Мафия')
            add_red(7)
        elif len(quorum) == 12:
            roles_list.append('Комиссар')
            roles_list.append('Дон мафии')
            roles_list.append('Мафия')
            roles_list.append('Мафия')
            roles_list.append('Путана')
            roles_list.append('Маньяк')
            roles_list.append('Доктор')
            add_red(5)
        elif len(quorum) == 13:
            roles_list.append('Комиссар')
            roles_list.append('Дон мафии')
            roles_list.append('Мафия')
            roles_list.append('Мафия')
            roles_list.append('Путана')
            roles_list.append('Маньяк')
            roles_list.append('Доктор')
            add_red(6)
        elif len(quorum) == 14:
            roles_list.append('Комиссар')
            roles_list.append('Дон мафии')
            roles_list.append('Мафия')
            roles_list.append('Мафия')
            roles_list.append('Мафия')
            roles_list.append('Путана')
            roles_list.append('Маньяк')
            roles_list.append('Доктор')
            add_red(6)
        elif len(quorum) == 15:
            roles_list.append('Комиссар')
            roles_list.append('Дон мафии')
            roles_list.append('Мафия')
            roles_list.append('Мафия')
            roles_list.append('Мафия')
            roles_list.append('Путана')
            roles_list.append('Маньяк')
            roles_list.append('Доктор')
            add_red(7)

        if 15 > len(roles_list) > 0 or len(roles_list) == 2:
            random.shuffle(roles_list)

            # заполняем списки из начала кода
            for k in quorum.keys():
                player_username.append(k)
            for v in quorum.values():
                player_number.append(v)

            # отправляем ведущему роли на каждого игрока
            for i in range(len(quorum)):
                bot.send_message(judge_id, text= str(player_number[i])
                                      + '. ' + '@' + str(player_username[i]
                                      + ' - ' + str(roles_list[i])))

            # корректируем баланс в зависимости от кол-ва игроков
            # отправляем при необходимости доп. правила ведущему и каждому игроку
            if len(quorum) == 11:
                bot.send_message(judge_id, text='У дона 2 проверки в первую ночь')
                for i in range(len(quorum)):
                    bot.send_message(username_id[player_username[i]],
                                     text='У дона 2 проверки в первую ночь')

            if len(quorum) == 13:
                bot.send_message(judge_id, text='Маньяк обязан резать в первую ночь')
                for i in range(len(quorum)):
                    bot.send_message(username_id[player_username[i]],
                                     text='Маньяк обязан резать в первую ночь')

            if len(quorum) == 14:
                bot.send_message(judge_id, text='Мафия не стреляет в первую ночь')
                for i in range(len(quorum)):
                    bot.send_message(username_id[player_username[i]],
                                     text='Мафия не стреляет в первую ночь')

            for i in range(len(quorum)):
                bot.send_message(username_id[player_username[i]],
                                 text='Игра начинается. Ваша роль: '
                                 + roles_list[i])

    else:
        bot.send_message(message.chat.id,
                         'Возможной диапазон игроков: от 10 до 15(включительно)')


@bot.message_handler(content_types=['text'])
def send_something(message):
    try:
        # если пользователь отправит число от 1 до 15 включительно
        # записывает в словарь игрок => его место за столом
        if 1 <= int(message.text.lower()) <= 15:
            bot.send_message(message.chat.id, f"Ваш номер за столом: {message.text}")
            quorum[message.chat.username] = message.text
    except ValueError:
        valueError_mistake = 1
    with open('admin_key.txt', 'r') as f:
        admin_key = f.read()
    if message.text.lower() == admin_key and roles_list != []:
        for i in range(len(roles_list)):
            bot.send_message(message.chat.id,
                             f'{player_number[i]}. @{player_username[i]} - {roles_list[i]}')


    @bot.message_handler(content_types=['text'])
    def remove_comm(message):
        try:
            remove_user = re.split('remove @', message.text.lower())
            if remove_user[0] == '':
                if remove_user[1] in quorum:
                    del (quorum[remove_user[1]])
                    bot.send_message(message.chat.id, 'Пользователь @'
                                     + remove_user[1] + ' удален из кворума.')
                else:
                    bot.send_message(message.chat.id, 'Пользователь @'
                                     + remove_user[1] + ' не находится в кворуме.')

        except IndexError:
            indexError_mistake = 1

    remove_comm(message)


bot.polling(none_stop=True)
