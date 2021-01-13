#!/usr/bin/env python3
#Version 1.2.1.0
import os
import sys
import argparse
import json
import yaml
import pyodbc
from collections import defaultdict

class AtlasInventory(object):

    def __init__(self):
        server = 'tcp:'+os.getenv('HOSTNAME_DATABASE', 'hostname')
        database = os.getenv('NAME_DATABASE', 'database')
        username = os.getenv('USERNAME_DATABASE', 'user')
        password = os.getenv('PASSWORD_DATABASE', 'pass')
        driver = os.getenv('DRIVER_ODBC', '{ODBC Driver 17 for SQL Server}')
        scriptsql = os.getenv('SCRIPTSQL_FILE', 'inventory.sql')
        if driver == "" or driver is None:
            driver = '{ODBC Driver 17 for SQL Server}'
        if scriptsql == "" or scriptsql is None:
            scriptsql = 'inventory.sql'
        self.script_text = os.getenv('SCRIPT_TEXT', self.read_sqlscript_inventory(scriptsql))
        #self.vars_windows = self.download_yaml(self.read_file('vars/vars_windows.yaml'))
        self.vars = self.list_vars()
        self.inventory = {}
        self.read_cli_args()
        self.cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
        self.cursor = self.cnxn.cursor()
        # Called with `--list`.
        if self.args.list:
            self.inventory = self.atlas_inventory()
        # Called with `--host [hostname]`.
        elif self.args.host:
            # Not implemented, since we return _meta info `--list`.
            self.inventory = self.empty_inventory()
        # If no groups or vars are present, return empty inventory.
        else:
            self.inventory = self.empty_inventory()

        #print(yaml.safe_dump(self.inventory))
        print(json.dumps(self.inventory))

    # Example inventory for testing.
    def atlas_inventory(self):
        self.cursor.execute(self.script_text)
        row = self.cursor.fetchone()
        result_dict = lambda: defaultdict(result_dict)
        results_os = result_dict()
        results_region = result_dict()
        results_complex = result_dict()
        results_subsystem = result_dict()
        results_circuit = result_dict()
        results_segment = result_dict()
        results_domain = result_dict()
        results_role = result_dict()
        self.inventory['_meta'] = {
                 'hostvars': {}
        }
        while row:
            self.inventory['_meta']['hostvars'][row.name] = { 
                'region': row.region,
                'complex': row.complex,
                'subsystem': row.subsystem,
                'circuit': row.circuit,
                'segment': row.segment,
                'domain': row.domain,
                'role': row.role
                }               
            results_os[row.os][row.name] = row.name
            results_region['VAL_REGION_'+row.region.replace(' ','_')][row.name] = row.name
            results_complex['VAL_COMPLEX_'+row.complex.replace(' ','_')][row.name] = row.name
            results_subsystem['VAL_SUBSYSTEM_'+row.subsystem.replace(' ','_')][row.name] = row.name
            results_circuit['VAL_CIRCUIT_'+row.circuit.replace(' ','_')][row.name] = row.name
            results_segment['VAL_SEGMENT_'+row.segment.replace(' ','_')][row.name] = row.name
            results_domain['VAL_DOMAIN_'+row.domain.replace(' ','_')][row.name] = row.name
            results_role['VAL_ROLE_'+row.role.replace(' ','_')][row.name] = row.name
            row = self.cursor.fetchone()
        #Заполнение Inventory
        self.mas_group(results_region)
        self.mas_group(results_complex)
        self.mas_group(results_subsystem)
        self.mas_group(results_circuit)
        self.mas_group(results_segment)
        self.mas_group(results_domain)
        self.mas_group(results_role)
         #Заполнение Inventory для OS
        for os in results_os:
            self.inventory[os] = {
                    'hosts': [],
                    'vars': {}
            }
            for col in results_os[os]:
                self.inventory[os]['hosts'].append(col)
                if os == 'LINUX':
                  self.inventory[os]['vars'] = self.vars['linux']
                elif os == 'WINDOWS':
                  self.inventory[os]['vars'] = self.vars['windows']
                  #inventory[os]['vars']['ansible_connection'] = 'winrm'
                  #inventory[os]['vars']['ansible_winrm_transport'] = 'ntlm'
                  #inventory[os]['vars']['ansible_winrm_scheme'] = 'http'
                  #inventory[os]['vars']['ansible_port'] = '5985'
        return self.inventory

    # Empty inventory for testing.
    def empty_inventory(self):
        return {'_meta': {'hostvars': {}}}
    
    def mas_group(self, mas):
        for val in mas:
            self.inventory[val] = {
                    'hosts': [],
                    'vars': {}
            }
            for col in mas[val]:
                self.inventory[val]['hosts'].append(col)

    def dir_script(self):
        #pathos = os.getcwd()
        pathscript = os.path.dirname(os.path.realpath(__file__))
        return pathscript

    def read_file(self, scriptfile):
        #pathscript = os.path.dirname(os.path.realpath(__file__))
        #filescript = open(os.path.join(pathscript,scriptfile), 'r')
        filescript = open(scriptfile, 'r')
        text = filescript.read()
        filescript.close
        return text

    def download_yaml(self, textfile):
        try:
          return yaml.safe_load(textfile)
        except yaml.YAMLError as exc:
          print(exc)
          return ''

    def list_folder(self,folder):
        path_mas = []
        pathscript = self.dir_script()
        #files = os.listdir(os.path.join(pathscript,folder))
        for d, dirs, files in os.walk(os.path.join(pathscript,folder)):
            dirs=dirs
            for f in files:
                path = os.path.join(d,f)
                path_mas.append(path)
        return path_mas

    def list_vars(self):
        vars_mas = {}
        listfiles = self.list_folder('vars')
        for fileyaml in listfiles:
            masyaml = self.download_yaml(self.read_file(fileyaml))
            if masyaml is None:
                masyaml = {}
            namefile = os.path.basename(fileyaml).rpartition('.')[0].replace('vars_','')
            basename = namefile.split('_')[0]
            vars_mas[basename] = masyaml
        return vars_mas

    def read_sqlscript_inventory(self,scriptsql):
        script_text = self.read_file(os.path.join(self.dir_script(),'sql',scriptsql))
        script_text = script_text.replace("$region",os.getenv('SQL_REGION', 'region'))
        script_text = script_text.replace("$complex",os.getenv('SQL_COMPLEX', 'complex'))
        script_text = script_text.replace("$subsystem",os.getenv('SQL_SUBSYSTEM', 'subsystem'))
        script_text = script_text.replace("$circuit",os.getenv('SQL_CIRCUIT', 'circuit'))
        script_text = script_text.replace("$segment",os.getenv('SQL_SEGMENT', 'segment'))
        script_text = script_text.replace("$domain",os.getenv('SQL_DOMAIN', 'domain'))
        script_text = script_text.replace("$role",os.getenv('SQL_ROLE', 'role'))
        return script_text

    # Read the command line args passed to the script.
    def read_cli_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--list', action = 'store_true')
        parser.add_argument('--host', action = 'store')
        self.args = parser.parse_args()

# Get the inventory.
AtlasInventory()