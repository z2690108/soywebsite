# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

import sys
sys.path.append('/data/')
from ms2mml.ms2mmlMaker import Ms2mmlMaker

import json  
from django.http import HttpResponse  

page_info = {
                    'title':'冒险岛2乐谱制作器',
                    'toggle':'ms2mml_maker',
                }

def home(request):
    context = {}
    context['page_info'] = page_info
    
    context['words'] = 'Inoue Marina'

    return render(request, 'ms2mmlMaker/main.html', context)

def upload_file(request):
    if request.method == 'POST':
        res = {}

        html_file = 'ms2mmlMaker/main.html'
        if request.method == 'POST':
            mmn_file = request.FILES.get("mmn_file", None)
            if not mmn_file or not mmn_file.name.endswith('.mmn'):
                res['res_code'] = 100
                res['error'] = '请检查文格式及后缀!Σ(っ °Д °;)っ '
                return HttpResponse(json.dumps(res), content_type="application/json")
                # return render(request, html_file, { 'res': json.dumps(res), 'test': '123' })

            if mmn_file.size > 1048576:
                res['res_code'] = 101
                res['error'] = '文件太大啦!Σ(っ °Д °;)っ '
                return HttpResponse(json.dumps(res), content_type="application/json")
                # return render(request, html_file, { 'res': json.dumps(res), 'test': '123' })
            
            m_ms2mmlMaker = Ms2mmlMaker(mmn_file.read())
            res['ms2mml_output'] = m_ms2mmlMaker.getMs2mml()
            if not res['ms2mml_output']:
                res['res_code'] = 102
                res['error'] = '文件格式不对，再确认一下吧! :('
            else:
                res['res_code'] = 200
                res['file_name'] = mmn_file.name

        else:
            res['res_code'] = 103
            res['error'] = 'Wrong Method:('
        return HttpResponse(json.dumps(res), content_type="application/json")
        # return render(request, html_file, { 'res': json.dumps(res), 'test': '123' })
