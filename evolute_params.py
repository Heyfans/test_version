# -*- coding: utf-8 -*-
import argparse
import json
import yaml
import os
import os.path
import shutil

parser = argparse.ArgumentParser(description='customize system args')
parser.add_argument('--domain', '-d', help='set domain')
parser.add_argument('--login', '-l', help='set login')
parser.add_argument('--evertest_port', '-ep', help='set evertest_port')
parser.add_argument('--studio_port', '-sp', help='set studio_port')
parser.add_argument('--wiki_port', '-wp', help='set wiki_port')
parser.add_argument('--board_port', '-bp', help='set board_port')
parser.add_argument('--run', '-r', help='run system', const=True, nargs='?')
parser.add_argument('--kill', '-k', help='kill system', const=True, nargs='?')
parser.add_argument('--check', '-c', help='check system', const=True, nargs='?')
parser.add_argument('--websocket_domain', '-wd', help='set websocket_domain')
parser.add_argument('--websocket_port', '-op', help='set websocket_port')
parser.add_argument('--gunicorn_worker','-gw', help='set gunicoren worker')
parser.add_argument('--celery_worker','-cw', help='set celery worker')
success_path = './docker/qawiki/volume/logs/success.txt'

#
sample_settings_path = './sample_customize_settings.json'
sample_yml_path = './sample_docker-compose.yml'
sample_nginx_path = './sample_nginx_demo.conf'

settings_path = './customize_settings.json'
yml_path = './docker-compose.yml'
nginx_path = './evolute_nginx.conf'
success_path = './docker/qawiki/volume/logs/success.txt'


def set_domain(domain):
    with open(settings_path, 'r', encoding='utf8') as o_settings:
        old_settings = json.load(o_settings)
    with open(settings_path, 'w', encoding='utf8') as new_settings:
        old_settings['EVOLUTE_EVERTEST_DOMAIN'] = domain
        json.dump(old_settings, new_settings)


def set_login(login):
    with open(settings_path, 'r', encoding='utf8') as o_settings:
        old_settings = json.load(o_settings)
    with open(settings_path, 'w', encoding='utf8') as new_settings:
        old_settings['EVOLUTE_LOGIN_URL'] = login
        json.dump(old_settings, new_settings)


def set_sp(sp):
    with open(settings_path, 'r', encoding='utf8') as o_settings:
        old_settings = json.load(o_settings)
    with open(settings_path, 'w', encoding='utf8') as new_settings:
        old_settings['EVOLUTE_STUDIO_PORT'] = sp
        json.dump(old_settings, new_settings)


def set_wd(wd):
    with open(settings_path, 'r', encoding='utf8') as o_settings:
        old_settings = json.load(o_settings)
    with open(settings_path, 'w', encoding='utf8') as new_settings:
        old_settings['EVOLUTE_WEBSOCKET_DOMAIN'] = wd
        json.dump(old_settings, new_settings)


def set_ep(ep):
    with open(settings_path, 'r', encoding='utf8') as o_settings:
        old_settings = json.load(o_settings)
    with open(settings_path, 'w', encoding='utf8') as new_settings:
        old_settings['EVOLUTE_EVERTEST_PORT'] = ep
        json.dump(old_settings, new_settings)


def set_bp(bp):
    with open(settings_path, 'r', encoding='utf8') as o_settings:
        old_settings = json.load(o_settings)
    with open(settings_path, 'w', encoding='utf8') as new_settings:
        old_settings['EVOLUTE_BOARD_PORT'] = bp
        json.dump(old_settings, new_settings)


def set_wp(wp):
    with open(settings_path, 'r', encoding='utf8') as o_settings:
        old_settings = json.load(o_settings)
    with open(settings_path, 'w', encoding='utf8') as new_settings:
        old_settings['EVOLUTE_WIKI_PORT'] = wp
        json.dump(old_settings, new_settings)


def set_op(op):
    with open(settings_path, 'r', encoding='utf8') as o_settings:
        old_settings = json.load(o_settings)
    with open(settings_path, 'w', encoding='utf8') as new_settings:
        old_settings['EVOLUTE_WEBSOCKET_PORT'] = op
        json.dump(old_settings, new_settings)

def set_gw(gw):
    with open(settings_path, 'r', encoding='utf8') as o_settings:
        old_settings = json.load(o_settings)
    with open(settings_path, 'w', encoding='utf8') as new_settings:
        #old_settings['GUNICORN_WORKER'] = gw
        old_settings.update({'GUNICORN_WORKER': gw})
        json.dump(old_settings, new_settings)

def set_cw(cw):
    with open(settings_path, 'r', encoding='utf8') as o_settings:
        old_settings = json.load(o_settings)
    with open(settings_path, 'w', encoding='utf8') as new_settings:
        old_settings.update({'CELERY_WORKER':cw})
        json.dump(old_settings, new_settings)

def replace_params():
    with open(settings_path, 'r', encoding='utf8') as settings_content:
        settings = json.load(settings_content)
    check_field = ['EVOLUTE_EVERTEST_DOMAIN', 'EVOLUTE_LOGIN_URL', 'EVOLUTE_EVERTEST_PORT', 'EVOLUTE_STUDIO_PORT',
                   'EVOLUTE_WIKI_PORT', 'EVOLUTE_BOARD_PORT', 'EVOLUTE_WEBSOCKET_PORT', 'EVOLUTE_WEBSOCKET_DOMAIN']
    remain_settings = []
    for cf in check_field:
        if not settings.get(cf, ''):
            remain_settings.append(cf)
    if remain_settings:
        res = 'some settings should be seted:'
        for rs in remain_settings:
            res = res + f' {rs},'

        print(res)
        return False

    # ???????????????????????????????????????yml??????
    with open(sample_yml_path, 'r', encoding='utf-8') as yml_settings_content:
        yml_settings = yaml.full_load(yml_settings_content)
        print(yml_settings)

    with open(yml_path, 'w', encoding='utf-8') as yml_settings_content:
        # ???????????????????????????
        yml_settings['services']['celery-board']['environment']['SUFFIX'] = settings['EVOLUTE_EVERTEST_DOMAIN']
        yml_settings['services']['celery-board-beat']['environment']['SUFFIX'] = settings['EVOLUTE_EVERTEST_DOMAIN']
        yml_settings['services']['celery-wiki']['environment']['SUFFIX'] = settings['EVOLUTE_EVERTEST_DOMAIN']
        yml_settings['services']['evolute-wiki']['environment']['WS_DOMAIN'] = settings['EVOLUTE_EVERTEST_DOMAIN']
        yml_settings['services']['evolute-wiki-ws']['environment']['WS_DOMAIN'] = settings['EVOLUTE_EVERTEST_DOMAIN']
        # yml_settings['services']['celery-wiki-beat']['environment']['SUFFIX'] = settings['EVOLUTE_EVERTEST_DOMAIN']
        yml_settings['services']['evolute']['environment']['SUFFIX'] = settings['EVOLUTE_EVERTEST_DOMAIN']
        yml_settings['services']['evolute-board']['environment']['SUFFIX'] = settings['EVOLUTE_EVERTEST_DOMAIN']
        yml_settings['services']['evolute-studio']['environment']['SUFFIX'] = settings['EVOLUTE_EVERTEST_DOMAIN']
        yml_settings['services']['evolute-wiki']['environment']['SUFFIX'] = settings['EVOLUTE_EVERTEST_DOMAIN']
        yml_settings['services']['evolute-wiki-ws']['environment']['SUFFIX'] = settings['EVOLUTE_EVERTEST_DOMAIN']
        # yml_settings['services']['db']['environment']['DOMAIN'] = settings['EVOLUTE_EVERTEST_DOMAIN']
        yml_settings['services']['evolute']['ports'] = [f'{settings["EVOLUTE_EVERTEST_PORT"]}:8000']
        yml_settings['services']['evolute-board']['ports'] = [f'{settings["EVOLUTE_BOARD_PORT"]}:8002']
        yml_settings['services']['evolute-studio']['ports'] = [f'{settings["EVOLUTE_STUDIO_PORT"]}:8001']
        yml_settings['services']['evolute-wiki']['ports'] = [f'{settings["EVOLUTE_WIKI_PORT"]}:8003']
        yml_settings['services']['evolute-wiki-ws']['ports'] = [f'{settings["EVOLUTE_WEBSOCKET_PORT"]}:8000']

        # ????????????celery???worker???
        worker_amount = settings['CELERY_WORKER']
        board_command = yml_settings['services']['celery-board']['command'].split('info')[
                            0] + f'info --concurrency={worker_amount}"'
        yml_settings['services']['celery-board']['command'] = board_command

        wiki_command = yml_settings['services']['celery-wiki']['command'].split('info')[
                           0] + f'info --concurrency={worker_amount}"'
        yml_settings['services']['celery-wiki']['command'] = wiki_command

        # ??????gunicorn???worker??????
        gunicorn_worker = settings['GUNICORN_WORKER']
        yml_settings['services']['evolute-board']['environment']['SERVER_WORKER'] = gunicorn_worker
        yml_settings['services']['evolute-wiki']['environment']['SERVER_WORKER'] = gunicorn_worker

        try:
            # replace_tag
            replace_tag = 'need_replace_evolute_login_url'
            login_url = f'http://{settings["EVOLUTE_EVERTEST_DOMAIN"]}/auth/login_complete/'
            LOGIN_URL = settings["EVOLUTE_LOGIN_URL"]
            yml_settings['services']['evolute']['environment']['LOGIN_URL'] = LOGIN_URL
        except:
            print('set login_url error')
            return False

        yaml.dump(yml_settings, yml_settings_content)

    with open(sample_nginx_path, 'r', encoding='utf-8') as nginx_content:
        nginx_settings = nginx_content.read()
    with open(nginx_path, 'w', encoding='utf-8') as nginx_content:
        nginx_settings = nginx_settings.replace('EVOLUTE_EVERTEST_PORT', str(settings['EVOLUTE_EVERTEST_PORT']))
        nginx_settings = nginx_settings.replace('EVOLUTE_BOARD_PORT', str(settings['EVOLUTE_BOARD_PORT']))
        nginx_settings = nginx_settings.replace('EVOLUTE_WIKI_PORT', str(settings['EVOLUTE_WIKI_PORT']))
        nginx_settings = nginx_settings.replace('EVOLUTE_STUDIO_PORT', str(settings['EVOLUTE_STUDIO_PORT']))
        nginx_settings = nginx_settings.replace('EVOLUTE_DOMAIN', str(settings['EVOLUTE_EVERTEST_DOMAIN']))
        nginx_settings = nginx_settings.replace('EVOLUTE_WEBSOCKET_PORT', str(settings['EVOLUTE_WEBSOCKET_PORT']))
        nginx_content.write(nginx_settings)
    return True

if __name__ == '__main__':
    # ????????????????????????????????????

    sample_settings_path = './sample_customize_settings.json'
    sample_yml_path = './sample_docker-compose.yml'
    sample_nginx_path = './sample_nginx_demo.conf'

    settings_path = './customize_settings.json'
    yml_path = './docker-compose.yml'
    nginx_path = './evolute_nginx.conf'
    try:
        if os.path.exists(settings_path):
            pass
        else:
            shutil.copy(sample_settings_path, settings_path)

        if os.path.exists(yml_path):
            pass
        else:
            shutil.copy(sample_yml_path, yml_path)

        if os.path.exists(nginx_path):
            pass
        else:
            shutil.copy(sample_nginx_path, nginx_path)
    except:
        pass
    args = parser.parse_args()
    if args.domain:
        set_domain(args.domain)
    if args.login:
        set_login(args.login)
    if args.evertest_port:
        set_ep(args.evertest_port)
    if args.studio_port:
        set_sp(args.studio_port)
    if args.wiki_port:
        set_wp(args.wiki_port)
    if args.board_port:
        set_bp(args.board_port)
    if args.websocket_domain:
        set_wd(args.websocket_domain)

    if args.websocket_port:
        set_op(args.websocket_port)
    if args.gunicorn_worker:
        set_gw(args.gunicorn_worker)
    if args.celery_worker:
        set_cw(args.celery_worker)
