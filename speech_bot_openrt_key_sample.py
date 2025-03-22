#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------
# COPYRIGHT (C) 2014-2025 Mitsuo KONDOU.
# This software is released under the not MIT License.
# Permission from the right holder is required for use.
# https://github.com/konsan1101
# Thank you for keeping the rules.
# ------------------------------------------------

def getkey(api, key):

    # openrt チャットボット
    if (api == 'openrt'):
        print('speech_bot_openrt_key.py')
        print('set your key!')
        if (key == 'openrt_api_type'):
            return 'use openrt api type'
        if (key == 'openrt_default_gpt'):
            return 'use openrt default gpt'
        if (key == 'openrt_default_class'):
            return 'use chat default class'
        if (key == 'openrt_auto_continue'):
            return 'use chat auto continue'
        if (key == 'openrt_max_step'):
            return 'chat max step'
        if (key == 'openrt_max_session'):
            return 'use max session'
        if (key == 'openrt_max_wait_sec'):
            return 'chat max wait(sec)'

        if (key == 'openrt_key_id'):
            return 'your openrt key'

        if (key == 'openrt_a_nick_name'):
            return 'your openrt (a) nick name'
        if (key == 'openrt_a_model'):
            return 'your openrt (a) model'
        if (key == 'openrt_a_token'):
            return 'your openrt (a) token'
        if (key == 'openrt_a_use_tools'):
            return 'your openrt (a) use tools'

        if (key == 'openrt_b_nick_name'):
            return 'your openrt (b) nick name'
        if (key == 'openrt_b_model'):
            return 'your openrt (b) model'
        if (key == 'openrt_b_token'):
            return 'your openrt (b) token'
        if (key == 'openrt_b_use_tools'):
            return 'your openrt (b) use tools'

        if (key == 'openrt_v_nick_name'):
            return 'your openrt (v) nick name'
        if (key == 'openrt_v_model'):
            return 'your openrt (v) model'
        if (key == 'openrt_v_token'):
            return 'your openrt (v) token'
        if (key == 'openrt_v_use_tools'):
            return 'your openrt (v) use tools'

        if (key == 'openrt_x_nick_name'):
            return 'your openrt (x) nick name'
        if (key == 'openrt_x_model'):
            return 'your openrt (x) model'
        if (key == 'openrt_x_token'):
            return 'your openrt (x) token'
        if (key == 'openrt_x_use_tools'):
            return 'your openrt (x) use tools'

    return False


