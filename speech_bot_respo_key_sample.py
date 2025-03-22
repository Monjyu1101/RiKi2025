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

    # respo チャットボット
    if (api == 'respo'):
        print('speech_bot_respo_key.py')
        print('set your key!')
        if (key == 'respo_api_type'):
            return 'use respo api type'
        if (key == 'respo_default_gpt'):
            return 'use respo default gpt'
        if (key == 'respo_default_class'):
            return 'use chat default class'
        if (key == 'respo_auto_continue'):
            return 'use chat auto continue'
        if (key == 'respo_max_step'):
            return 'chat max step'
        if (key == 'respo_max_session'):
            return 'use max session'
        if (key == 'respo_max_wait_sec'):
            return 'chat max wait(sec)'

        if (key == 'openai_organization'):
            return 'your openai organization'
        if (key == 'openai_key_id'):
            return 'your openai key'

        if (key == 'azure_endpoint'):
            return 'your azure endpoint'
        if (key == 'azure_version'):
            return 'your azure version'
        if (key == 'azure_key_id'):
            return 'your azure key'

        if (key == 'respo_a_nick_name'):
            return 'your respo (a) nick name'
        if (key == 'respo_a_model'):
            return 'your respo (a) model'
        if (key == 'respo_a_token'):
            return 'your respo (a) token'
        if (key == 'respo_a_use_tools'):
            return 'your respo (a) use tools'

        if (key == 'respo_b_nick_name'):
            return 'your respo (b) nick name'
        if (key == 'respo_b_model'):
            return 'your respo (b) model'
        if (key == 'respo_b_token'):
            return 'your respo (b) token'
        if (key == 'respo_b_use_tools'):
            return 'your respo (b) use tools'

        if (key == 'respo_v_nick_name'):
            return 'your respo (v) nick name'
        if (key == 'respo_v_model'):
            return 'your respo (v) model'
        if (key == 'respo_v_token'):
            return 'your respo (v) token'
        if (key == 'respo_v_use_tools'):
            return 'your respo (v) use tools'

        if (key == 'respo_x_nick_name'):
            return 'your respo (x) nick name'
        if (key == 'respo_x_model'):
            return 'your respo (x) model'
        if (key == 'respo_x_token'):
            return 'your respo (x) token'
        if (key == 'respo_x_use_tools'):
            return 'your respo (x) use tools'

    return False


