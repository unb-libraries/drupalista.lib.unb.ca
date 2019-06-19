"""This is Drupalista herself.

"""
import subprocess
import os
from prettytable import PrettyTable

class Drupalista(object):
    def __init__(self, message, config):
        self.output = ''
        self.servers = {}
        self.site = False
        self.drush_command = False

        self.message = message
        self.config = config
        self.command_data = self.message['text'].split()
        self.kube_command = ['/app/kubectl', '--kubeconfig=/root/.kube/config', '--selector=app=drupal']
        self.commands = ['list_sites', 'clear_cache', 'uli', 'hostfile']

        if self.command_data[1] in self.commands:
            command = self.command_data[1]
            command_method = getattr(self, command)
            command_method()
        else:
            self.output += "Invalid command (" + self.command_data[1]+ "). Valid commands are " + str(self.commands)

    def clear_cache(self):
        uri = self.strip_formatting(self.command_data[2])
        pod_id, pod_env = self.get_pod_id(uri)

        if not pod_id == False:
            cmd = self.kube_command + [
                'exec',
                pod_id,
                '--namespace=' + pod_env,
                '--',
                '/usr/bin/drush',
                '--root=/app/html',
                'cr'
            ]
            cmd.remove('--selector=app=drupal')
            self.output += subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        else:
            self.output += 'A pod with the URI *' + uri + '* was not found. Available pods:'
            self.list_sites()

    def get_pod_id(self, uri):
        cmd = self.kube_command + [
            'get',
            'pods',
            '--all-namespaces',
            '--selector=uri=' + uri,
            '-o',
            'jsonpath={range .items[*]}{.metadata.name}|{.metadata.namespace}\n{end}'
        ]
        kube_output = subprocess.check_output(cmd)

        pods = kube_output.split("\n")
        if len(pods) > 1:
            for pod in pods:
                return pod.split("|")
        return [False, False]

    def hostfile(self):
        cmd = self.kube_command + [
            'get',
            'pods',
            '--all-namespaces',
            '-o',
            'jsonpath={range .items[*]}131.202.38.13     {.metadata.labels.uri}\n{end}'
        ]
        self.output += "```# Start Drupalista Host File List #\n"
        self.output += subprocess.check_output(cmd)
        self.output += '# End Drupalista Host File List #```'

    def list_sites(self):
        cmd = self.kube_command + [
            'get',
            'pods',
            '--all-namespaces',
            '-o',
            'jsonpath={range .items[*]}{.metadata.labels.uri}|{.metadata.name}|{.metadata.namespace}\n{end}'
        ]

        self.output += self.tabulate(
            ['URI', 'ID', 'Env'],
            subprocess.check_output(cmd)
        )

    def strip_formatting(self, text):
        if '<http://' in text:
            tmp_identifier = text.split('|')
            return tmp_identifier[1].replace('>', '')
        return text

    def tabulate(self, header, output):
        table = PrettyTable(header)
        table.padding_width = 1
        table.align = "l"

        for details in output.split("\n") :
            details_list = details.split("|")
            if len(details_list) > 1:
                table.add_row(details_list)

        return '```' + str(table) + '```'

    def uli(self):
        uri = self.strip_formatting(self.command_data[2])
        pod_id, pod_env = self.get_pod_id(uri)
        if not pod_id == False:
            cmd = self.kube_command + [
                'exec',
                pod_id,
                '--namespace=' + pod_env,
                '--',
                '/scripts/drupalUli.sh'
            ]
            try:
                cmd.append(self.strip_formatting(self.command_data[3]))
            except Exception:
                pass
            cmd.remove('--selector=app=drupal')
            self.output += '```' + subprocess.check_output(cmd, stderr=subprocess.STDOUT).replace('http://default', 'http://' + uri) + '```'
        else:
            self.output += 'A pod with the URI *' + uri + '* was not found. Available pods:'
            self.list_sites()
