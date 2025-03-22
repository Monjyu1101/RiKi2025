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

    # groq チャットボット
    if (api == 'groq'):
        print('speech_bot_groq_key.py')
        print('set your key!')
        if (key == 'groq_api_type'):
            return 'use groq api type'
        if (key == 'groq_default_gpt'):
            return 'use groq default gpt'
        if (key == 'groq_default_class'):
            return 'use chat default class'
        if (key == 'groq_auto_continue'):
            return 'use chat auto continue'
        if (key == 'groq_max_step'):
            return 'chat max step'
        if (key == 'groq_max_session'):
            return 'use max session'
        if (key == 'groq_max_wait_sec'):
            return 'chat max wait(sec)'

        if (key == 'groq_key_id'):
            return 'your groq key'

        if (key == 'groq_a_nick_name'):
            return 'your groq (a) nick name'
        if (key == 'groq_a_model'):
            return 'your groq (a) model'
        if (key == 'groq_a_token'):
            return 'your groq (a) token'
        if (key == 'groq_a_use_tools'):
            return 'your groq (a) use tools'

        if (key == 'groq_b_nick_name'):
            return 'your groq (b) nick name'
        if (key == 'groq_b_model'):
            return 'your groq (b) model'
        if (key == 'groq_b_token'):
            return 'your groq (b) token'
        if (key == 'groq_b_use_tools'):
            return 'your groq (b) use tools'

        if (key == 'groq_v_nick_name'):
            return 'your groq (v) nick name'
        if (key == 'groq_v_model'):
            return 'your groq (v) model'
        if (key == 'groq_v_token'):
            return 'your groq (v) token'
        if (key == 'groq_v_use_tools'):
            return 'your groq (v) use tools'

        if (key == 'groq_x_nick_name'):
            return 'your groq (x) nick name'
        if (key == 'groq_x_model'):
            return 'your groq (x) model'
        if (key == 'groq_x_token'):
            return 'your groq (x) token'
        if (key == 'groq_x_use_tools'):
            return 'your groq (x) use tools'

    return False


