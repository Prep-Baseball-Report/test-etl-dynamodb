
from typing_extensions import runtime
from aws_cdk import core as cdk
from aws_cdk.aws_iam import Role, ServicePrincipal, PolicyDocument, PolicyStatement, Effect
from aws_cdk.aws_lambda import Function, Runtime, Code


class DynamoDBTableCreationCoreStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, environment: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.role = Role(self, "ExecutionRole", 
            assumed_by=ServicePrincipal("states.amazonaws.com"),
            description=f"{environment}-dynamodb-table-creation service execution role",
            inline_policies=[
                PolicyDocument(statements=[
                    PolicyStatement(
                        actions=[
                            "dynamodb:CreateTable"
                        ],
                        effect=Effect.ALLOW,
                        resources=["*"]
                    ),  
                ])
            ]
        )
       

        
        