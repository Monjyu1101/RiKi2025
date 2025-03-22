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

    # grok チャットボット
    if (api == 'grok'):
        print('speech_bot_grok_key.py')
        print('set your key!')
        if (key == 'grok_api_type'):
            return 'use grok api type'
        if (key == 'grok_default_gpt'):
            return 'use grok default gpt'
        if (key == 'grok_default_class'):
            return 'use chat default class'
        if (key == 'grok_auto_continue'):
            return 'use chat auto continue'
        if (key == 'grok_max_step'):
            return 'chat max step'
        if (key == 'grok_max_session'):
            return 'use max session'
        if (key == 'grok_max_wait_sec'):
            return 'chat max wait(sec)'

        if (key == 'grok_key_id'):
            return 'your grok key'

        if (key == 'grok_a_nick_name'):
            return 'your grok (a) nick name'
        if (key == 'grok_a_model'):
            return 'your grok (a) model'
        if (key == 'grok_a_token'):
            return 'your grok (a) token'
        if (key == 'grok_a_use_tools'):
            return 'your grok (a) use tools'

        if (key == 'grok_b_nick_name'):
            return 'your grok (b) nick name'
        if (key == 'grok_b_model'):
            return 'your grok (b) model'
        if (key == 'grok_b_token'):
            return 'your grok (b) token'
        if (key == 'grok_b_use_tools'):
            return 'your grok (b) use tools'

        if (key == 'grok_v_nick_name'):
            return 'your grok (v) nick name'
        if (key == 'grok_v_model'):
            return 'your grok (v) model'
        if (key == 'grok_v_token'):
            return 'your grok (v) token'
        if (key == 'grok_v_use_tools'):
            return 'your grok (v) use tools'

        if (key == 'grok_x_nick_name'):
            return 'your grok (x) nick name'
        if (key == 'grok_x_model'):
            return 'your grok (x) model'
        if (key == 'grok_x_token'):
            return 'your grok (x) token'
        if (key == 'grok_x_use_tools'):
            return 'your grok (x) use tools'

    return False


