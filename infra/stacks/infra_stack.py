
from aws_cdk import core as cdk
from aws_cdk.aws_stepfunctions import StateMachine, Pass, Result, JsonPath, Choice, Condition, Wait, WaitTime
from aws_cdk.aws_stepfunctions_tasks import AthenaStartQueryExecution, AthenaGetQueryResults, AthenaGetQueryExecution, LambdaInvoke
from aws_cdk.aws_iam import Role
from aws_cdk.aws_lambda import Function
from aws_cdk.aws_events import Rule, Schedule
from aws_cdk.aws_events_targets import SfnStateMachine
from aws_cdk import aws_dynamodb as dynamodb
from dataclasses import dataclass, asdict 
from typing import Optional
import textwrap

@dataclass
class ScheduleOption:
    day: Optional[str] = ''
    hour: Optional[str] = ''
    minute: Optional[str] = ''
    month: Optional[str] = ''
    week_day: Optional[str] = ''
    year: Optional[str]  = ''

    def get_cron_parameters(self):
            params = {}
            for field in self.__dataclass_fields__:
                value = getattr(self, field)
                if value != '':
                    params[field] = str(value)
            return params

@dataclass
class QueryOptions:
    database: str
    table: str
    select_statement: Optional[str] = ''
    time_stamp_column_name: Optional[str] = ''
    vendor_name: Optional[str] = ''

@dataclass
class AthenaRunnerFunctions:
    wait_timer_backoff: Function
    slack_reporter: Function

@dataclass
class AthenaRunnerStepFunctionOptions:
    refresh_type: str
    role: Role
    query: QueryOptions
    functions: AthenaRunnerFunctions
    schedule: Optional[ScheduleOption] = None

@dataclass
class DynamoDBRunnerFunctions:
    wait_timer_backoff: Function
    slack_reporter: Function # Going to want to update the lambda function
    get_time: Function
    dyanmodb_writer: Function

@dataclass
class DynamoDBRunnerStepFunctionOptions:
    dynamoDB_table: str
    role: Role
    query: QueryOptions
    functions: DynamoDBRunnerFunctions
    schedule: Optional[ScheduleOption] = None

class DynamoDBCreateTableStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        table_creation = dynamodb.Table(self, 
                    f"test-table", 
                    table_name=f"test-table",
                    partition_key=dynamodb.Attribute(name="pbr_id", type=dynamodb.AttributeType.STRING),
                    sort_key=dynamodb.Attribute(name="event_id",type=dynamodb.AttributeType.STRING),
                    billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST, 
                    stream = dynamodb.StreamViewType.NEW_AND_OLD_IMAGES
                )
        

        cdk.CfnOutput(self, "table_test_stream_arn",value=table_creation.table_stream_arn)