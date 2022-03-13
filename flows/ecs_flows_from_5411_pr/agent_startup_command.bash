prefect agent ecs start \
--name ECS-Local \
--cluster arn:aws:ecs:us-east-1:338306982838:cluster/PrefectECS \
--task-role-arn arn:aws:iam::338306982838:role/prefectTaskRole \
--execution-role-arn arn:aws:iam::338306982838:role/prefectECSAgentTaskExecutionRole \
--log-level DEBUG \
--label ecs-agent-local \
--run-task-kwargs agent_capacity_provider.yaml