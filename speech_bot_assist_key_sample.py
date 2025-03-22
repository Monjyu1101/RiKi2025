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

    # assist チャットボット
    if (api == 'assist'):
        print('speech_bot_assist_key.py')
        print('set your key!')
        if (key == 'assist_api_type'):
            return 'use assist api type'
        if (key == 'assist_default_gpt'):
            return 'use assist default gpt'
        if (key == 'assist_default_class'):
            return 'use chat default class'
        if (key == 'assist_auto_continue'):
            return 'use chat auto continue'
        if (key == 'assist_max_step'):
            return 'chat max step'
        if (key == 'assist_max_session'):
            return 'use max session'
        if (key == 'assist_max_wait_sec'):
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

        if (key == 'assist_a_nick_name'):
            return 'your assist (a) nick name'
        if (key == 'assist_a_model'):
            return 'your assist (a) model'
        if (key == 'assist_a_token'):
            return 'your assist (a) token'
        if (key == 'assist_a_use_tools'):
            return 'your assist (a) use tools'

        if (key == 'assist_b_nick_name'):
            return 'your assist (b) nick name'
        if (key == 'assist_b_model'):
            return 'your assist (b) model'
        if (key == 'assist_b_token'):
            return 'your assist (b) token'
        if (key == 'assist_b_use_tools'):
            return 'your assist (b) use tools'

        if (key == 'assist_v_nick_name'):
            return 'your assist (v) nick name'
        if (key == 'assist_v_model'):
            return 'your assist (v) model'
        if (key == 'assist_v_token'):
            return 'your assist (v) token'
        if (key == 'assist_v_use_tools'):
            return 'your assist (v) use tools'

        if (key == 'assist_x_nick_name'):
            return 'your assist (x) nick name'
        if (key == 'assist_x_model'):
            return 'your assist (x) model'
        if (key == 'assist_x_token'):
            return 'your assist (x) token'
        if (key == 'assist_x_use_tools'):
            return 'your assist (x) use tools'

    return False


