#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import sys
import time
import signal
from pprint import pprint
import argparse
import json
import os
import os.path
import re
import jinja2
import codecs

try:
    from zapv2 import ZAPv2
except ImportError:
    print('You need to install zapv2 python module - pip install python-owasp-zap-v2.4')
    sys.exit(1)


__author__ = 'ale'
__package__ = 'zapit'
__doc__ = """
ZapIt is a python script that used the ZAP python API to interact with a headless Zed Attack Proxy.
Mainly useful to automate runs.
"""


def signal_handler(signal, frame):
    print('\n')
    sys.exit(0)


def fix_encoding(alerts):

    _alerts = []

    for a in alerts:
        _a = {}
        for k, v in a.iteritems():
            k = ''.join([i if ord(i) < 128 else ' ' for i in k])
            v = ''.join([i if ord(i) < 128 else ' ' for i in v])
            _a[k] = v
        assert isinstance(_a, dict)
        _alerts.append(_a)
    assert isinstance(_alerts, list)
    return _alerts


def run_spider(zap, target, api_key):
    """
    spider the target

    only spiders the target, it will not automatically kick off a active scan
    """
    print('Spidering target {0}'.format(target))
    zap.spider.set_option_scope_string(target, apikey=api_key)
    zap.spider.set_option_max_depth(10, apikey=api_key)
    zap.spider.set_option_thread_count(3)
    z = zap.spider.scan(target, apikey=api_key)
    # Give the Spider a chance to start
    time.sleep(2)
    while (int(zap.spider.status()) < 100):
        print('Spider progress %: ' + zap.spider.status())
        time.sleep(2)

    print('Spider completed')

def run_active_scan(zap, target, api_key):
    """
    run a active scan against target using the initialized zap object

    a active scan will run through all available plugins like SQLi, Path Traversal, etc. just like when you would
    use the UI and start an attack against TARGET
    """
    print('Scanning target {0}'.format(target))
    zap.ascan.scan(target, True, apikey=api_key)

    while (int(zap.ascan.status()) < 100):
        print('Scan progress %: ' + zap.ascan.status())
        time.sleep(5)
    print('Scan completed')


def main(args=None):
    """
    main function
    """
    if args is not None:
        target = args.target
        api_key = args.api_key
        spider = args.spider
        active_scan = args.active_scan
        html_report = args.html_report
        force = args.force
    else:
        print('No arguments supplied. Exiting')
        sys.exit(1)

    zap = ZAPv2()
    # Use the line below if ZAP is not listening on 8090
    # zap = ZAPv2(proxies={'http': 'http://127.0.0.1:8090', 'https': 'http://127.0.0.1:8090'})
    print('Accessing target {0}'.format(target))
    zap.urlopen(target)
    time.sleep(2)

    zap.core.delete_all_alerts(apikey=api_key)
    zap.core.new_session(target, True, apikey=api_key)

    if spider:
        run_spider(zap, target, api_key)
        time.sleep(5)

    if active_scan:
        run_active_scan(zap, target, api_key)
        time.sleep(5)

    print('Hosts: ' + ', '.join(zap.core.hosts))

    alerts = zap.core.alerts()
    alerts = fix_encoding(alerts)

    #pprint(alerts, indent=4)

    if html_report:
        # zap.core.htmlreport seems to be broken so we're using json2html for a very basic report in html
        # report = zap.core.htmlreport()
        report_file = html_report
        try:

            if os.path.isfile(report_file) and force is True:
                try:
                    os.remove(report_file)
                except IOError as e:
                    print('Unable to remove {0}'.format(report_file))
            else:
                print ('File {0} exists and --html-force was not used. '
                       'Please remove file manually and re-run. Exiting.'.format(report_file))
                sys.exit(1)

            with open(report_file, 'a') as f:
                templateLoader = jinja2.FileSystemLoader(searchpath=os.path.dirname(os.path.realpath(__file__)))
                templateEnv = jinja2.Environment(loader=templateLoader)
                TEMPLATE_FILE = "report.html.j2"
                template = templateEnv.get_template(TEMPLATE_FILE)
                templateVars = { "alerts": alerts }

                html_alerts = template.render(templateVars)
                f.write(html_alerts)

            print ('Success: HTML report saved at {0}'.format(report_file))
        except Exception as e:
            print('Error: Unable to save HTML report: {0}'.format(e))


if __name__ == '__main__':

    signal.signal(signal.SIGINT, signal_handler)

    parser = argparse.ArgumentParser()

    parser.add_argument('-t', '--target', '-u', '--url',
                        help="The target / url to scan (https://scanme.domain.com)",
                        required=True)

    parser.add_argument('-k', '--api-key',
                        help="The api key to connect to ZAP",
                        required=False)

    parser.add_argument('-s', '--spider', action='store_true',
                        help="Run spider against TARGET",
                        required=False)

    parser.add_argument('-a', '--active-scan', action='store_true',
                        help="Run a active-scan against TARGET",
                        required=False)

    parser.add_argument('--html-report',
                        help="Create a html report in /data/report.html",
                        required=False)

    parser.add_argument('--force', action='store_true',
                        help="Overwrite /data/report.html if it exists",
                        required=False)

    args = parser.parse_args()
    main(args)
