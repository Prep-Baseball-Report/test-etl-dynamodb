#!/usr/bin/env python
from inspect import stack
import os
import yaml
from aws_cdk import core as cdk

from stacks.infra_stack import DynamoDBCreateTableStack
from stacks.core_stack import DynamoDBTableCreationCoreStack 


# def read_yml(manifest_file: str):
#     with open(manifest_file) as file:
#         return yaml.load(file, Loader=yaml.FullLoader)
# def get_manifest_file(manifest: str) -> str:
#     root_dir = f"{os.path.abspath(os.path.join(os.curdir, '..'))}/manifests"
#     manifest_file = f"{root_dir}/{manifest}"
#     if not os.path.isfile(manifest_file):
#        raise FileNotFoundError(manifest_file)
#     return manifest_file

app = cdk.App()
# Get context variables
app_name =  'test-pbr-dynamodb-table-creation'
environment = 'dev'#app.node.try_get_context("environment")
#manifest = app.node.try_get_context("manifest")
# if not manifest:
#     raise Exception("Please provide a manifest yaml file, or * to update all manifests.")
# elif manifest == '*':
#     print()
#     manifest_files = [
#         get_manifest_file(manifest) 
#         for manifest in os.listdir(f"{os.path.abspath(os.path.join(os.curdir, '..'))}/manifests/")
#     ]
# else:
#     manifest_files = [get_manifest_file(manifest)]

core_stack = DynamoDBTableCreationCoreStack(app, f"{environment}-{app_name}-CoreStack", environment)
DynamoDBCreateTableStack(app)
# for manifest_file in manifest_files:
#     manifest_yml = read_yml(manifest_file)
#     stack_id = f"{environment}-{app_name}-{manifest_file.split('/')[-1].replace('.yml','').replace('_','-')}-Stack"
#     athena_runner_options =  AthenaRunnerStepFunctionOptions(
#         query=QueryOptions(
#             database=f"{manifest_yml['database']}_{environment}", 
#             table=manifest_yml['table'], 
#             select_statement=manifest_yml['select_statement']
#         ),
#         functions=AthenaRunnerFunctions(
#             core_stack.wait_timer_backoff_lambda,
#             core_stack.slack_reporter_lambda
#         ),
#         schedule= ScheduleOption(**manifest_yml.get('schedule', {})),
#         role=core_stack.role,
#         refresh_type=manifest_yml.get('refresh_type')
#     )
    
#     AthenaRunnerStepFunctionStack(
#         app, 
#         stack_id, 
#         environment, 
#         options=athena_runner_options, 
#         description=f"Athena runner for {manifest_yml['database']}.{manifest_yml['table']}"
#     )
app.synth()

