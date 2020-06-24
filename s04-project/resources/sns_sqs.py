import json
from aws_cdk import core, aws_sns as _sns, aws_sns_subscriptions as _subs, aws_sqs as _sqs


class SnsSqs(core.Stack):
    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # create sns topic and subscription
        mytopic = _sns.Topic(self, "mytopic", display_name="latest topics", topic_name="mytopic")
        mytopic.add_subscription(_subs.EmailSubscription("example@email.com"))

        # create sqs
        myqueue = _sqs.Queue(
            self,
            "myqueue",
            queue_name="myqueue.fifo",
            fifo=True,
            encryption=_sqs.QueueEncryption.KMS_MANAGED,
            retention_period=core.Duration.days(4),
            visibility_timeout=core.Duration.seconds(45),
        )

