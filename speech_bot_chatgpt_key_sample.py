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

    # chatgpt チャットボット
    if (api == 'chatgpt'):
        print('speech_bot_chatgpt_key.py')
        print('set your key!')
        if (key == 'chatgpt_api_type'):
            return 'use chatgpt api type'
        if (key == 'chatgpt_default_gpt'):
            return 'use chatgpt default gpt'
        if (key == 'chatgpt_default_class'):
            return 'use chat default class'
        if (key == 'chatgpt_auto_continue'):
            return 'use chat auto continue'
        if (key == 'chatgpt_max_step'):
            return 'chat max step'
        if (key == 'chatgpt_max_session'):
            return 'use max session'
        if (key == 'chatgpt_max_wait_sec'):
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

        if (key == 'chatgpt_a_nick_name'):
            return 'your chatgpt (a) nick name'
        if (key == 'chatgpt_a_model'):
            return 'your chatgpt (a) model'
        if (key == 'chatgpt_a_token'):
            return 'your chatgpt (a) token'
        if (key == 'chatgpt_a_use_tools'):
            return 'your chatgpt (a) use tools'

        if (key == 'chatgpt_b_nick_name'):
            return 'your chatgpt (b) nick name'
        if (key == 'chatgpt_b_model'):
            return 'your chatgpt (b) model'
        if (key == 'chatgpt_b_token'):
            return 'your chatgpt (b) token'
        if (key == 'chatgpt_b_use_tools'):
            return 'your chatgpt (b) use tools'

        if (key == 'chatgpt_v_nick_name'):
            return 'your chatgpt (v) nick name'
        if (key == 'chatgpt_v_model'):
            return 'your chatgpt (v) model'
        if (key == 'chatgpt_v_token'):
            return 'your chatgpt (v) token'
        if (key == 'chatgpt_v_use_tools'):
            return 'your chatgpt (v) use tools'

        if (key == 'chatgpt_x_nick_name'):
            return 'your chatgpt (x) nick name'
        if (key == 'chatgpt_x_model'):
            return 'your chatgpt (x) model'
        if (key == 'chatgpt_x_token'):
            return 'your chatgpt (x) token'
        if (key == 'chatgpt_x_use_tools'):
            return 'your chatgpt (x) use tools'

    return False


