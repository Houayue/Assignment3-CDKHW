import aws_cdk as core
import aws_cdk.assertions as assertions

from assignment3_cdk.assignment3_cdk_stack import Assignment3CdkStack

# example tests. To run these tests, uncomment this file along with the example
# resource in assignment3_cdk/assignment3_cdk_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = Assignment3CdkStack(app, "assignment3-cdk")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
