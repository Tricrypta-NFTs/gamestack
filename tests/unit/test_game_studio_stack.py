import aws_cdk as core
import aws_cdk.assertions as assertions

from game_studio.game_studio_stack import GameStudioStack

# example tests. To run these tests, uncomment this file along with the example
# resource in game_studio/game_studio_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = GameStudioStack(app, "gamestack")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
