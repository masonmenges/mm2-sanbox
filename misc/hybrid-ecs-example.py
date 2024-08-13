{
  "variables": {
    "type": "object",
    "$defs": {
      "AwsCredentials": {
        "type": "object",
        "title": "AwsCredentials",
        "properties": {
          "region_name": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ],
            "title": "Region Name",
            "default": null,
            "description": "The AWS Region where you want to create new connections."
          },
          "profile_name": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ],
            "title": "Profile Name",
            "default": null,
            "description": "The profile to use when creating your session."
          },
          "aws_access_key_id": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ],
            "title": "AWS Access Key ID",
            "default": null,
            "description": "A specific AWS access key ID."
          },
          "aws_session_token": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ],
            "title": "AWS Session Token",
            "default": null,
            "description": "The session key for your AWS account. This is only needed when you are using temporary credentials."
          },
          "aws_client_parameters": {
            "allOf": [
              {
                "$ref": "#/$defs/AwsClientParameters"
              }
            ],
            "title": "AWS Client Parameters",
            "description": "Extra parameters to initialize the Client."
          },
          "aws_secret_access_key": {
            "anyOf": [
              {
                "type": "string",
                "format": "password",
                "writeOnly": true
              },
              {
                "type": "null"
              }
            ],
            "title": "AWS Access Key Secret",
            "default": null,
            "description": "A specific AWS secret access key."
          }
        },
        "description": "Block used to manage authentication with AWS. AWS authentication is\nhandled via the `boto3` module. Refer to the\n[boto3 docs](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html)\nfor more info about the possible credential configurations.",
        "secret_fields": [
          "aws_secret_access_key"
        ],
        "block_type_slug": "aws-credentials",
        "additionalProperties": true,
        "block_schema_references": {}
      },
      "CapacityProvider": {
        "type": "object",
        "title": "CapacityProvider",
        "required": [
          "capacityProvider",
          "weight",
          "base"
        ],
        "properties": {
          "base": {
            "type": "integer",
            "title": "Base"
          },
          "weight": {
            "type": "integer",
            "title": "Weight"
          },
          "capacityProvider": {
            "type": "string",
            "title": "Capacityprovider"
          }
        },
        "description": "The capacity provider strategy to use when running the task."
      },
      "AwsClientParameters": {
        "type": "object",
        "title": "AwsClientParameters",
        "properties": {
          "config": {
            "anyOf": [
              {
                "type": "object"
              },
              {
                "type": "null"
              }
            ],
            "title": "Botocore Config",
            "default": null,
            "description": "Advanced configuration for Botocore clients."
          },
          "verify": {
            "anyOf": [
              {
                "type": "boolean"
              },
              {
                "type": "string",
                "format": "file-path"
              }
            ],
            "title": "Verify",
            "default": true,
            "description": "Whether or not to verify SSL certificates."
          },
          "use_ssl": {
            "type": "boolean",
            "title": "Use SSL",
            "default": true,
            "description": "Whether or not to use SSL."
          },
          "api_version": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ],
            "title": "API Version",
            "default": null,
            "description": "The API version to use."
          },
          "endpoint_url": {
            "anyOf": [
              {
                "type": "string"
              },
              {
                "type": "null"
              }
            ],
            "title": "Endpoint URL",
            "default": null,
            "description": "The complete URL to use for the constructed client."
          },
          "verify_cert_path": {
            "anyOf": [
              {
                "type": "string",
                "format": "file-path"
              },
              {
                "type": "null"
              }
            ],
            "title": "Certificate Authority Bundle File Path",
            "default": null,
            "description": "Path to the CA cert bundle to use."
          }
        },
        "description": "Model used to manage extra parameters that you can pass when you initialize\nthe Client. If you want to find more information, see\n[boto3 docs](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/core/session.html)\nfor more info about the possible client configurations.\n\nAttributes:\n    api_version: The API version to use. By default, botocore will\n        use the latest API version when creating a client. You only need\n        to specify this parameter if you want to use a previous API version\n        of the client.\n    use_ssl: Whether or not to use SSL. By default, SSL is used.\n        Note that not all services support non-ssl connections.\n    verify: Whether or not to verify SSL certificates. By default\n        SSL certificates are verified. If False, SSL will still be used\n        (unless use_ssl is False), but SSL certificates\n        will not be verified. Passing a file path to this is deprecated.\n    verify_cert_path: A filename of the CA cert bundle to\n        use. You can specify this argument if you want to use a\n        different CA cert bundle than the one used by botocore.\n    endpoint_url: The complete URL to use for the constructed\n        client. Normally, botocore will automatically construct the\n        appropriate URL to use when communicating with a service. You\n        can specify a complete URL (including the \"http/https\" scheme)\n        to override this behavior. If this value is provided,\n        then ``use_ssl`` is ignored.\n    config: Advanced configuration for Botocore clients. See\n        [botocore docs](https://botocore.amazonaws.com/v1/documentation/api/latest/reference/config.html)\n        for more details."
      }
    },
    "properties": {
      "cpu": {
        "anyOf": [
          {
            "type": "integer"
          },
          {
            "type": "null"
          }
        ],
        "title": "CPU",
        "description": "The amount of CPU to provide to the ECS task. Valid amounts are specified in the AWS documentation. If not provided, a default value of 1024 will be used unless present on the task definition."
      },
      "env": {
        "type": "object",
        "title": "Environment Variables",
        "description": "Environment variables to provide to the task run. These variables are set on the Prefect container at task runtime. These will not be set on the task definition.",
        "additionalProperties": {
          "anyOf": [
            {
              "type": "string"
            },
            {
              "type": "null"
            }
          ]
        }
      },
      "name": {
        "anyOf": [
          {
            "type": "string"
          },
          {
            "type": "null"
          }
        ],
        "title": "Name",
        "description": "Name given to infrastructure created by a worker."
      },
      "image": {
        "anyOf": [
          {
            "type": "string"
          },
          {
            "type": "null"
          }
        ],
        "title": "Image",
        "description": "The image to use for the Prefect container in the task. If this value is not null, it will override the value in the task definition. This value defaults to a Prefect base image matching your local versions."
      },
      "family": {
        "anyOf": [
          {
            "type": "string"
          },
          {
            "type": "null"
          }
        ],
        "title": "Family",
        "description": "A family for the task definition. If not provided, it will be inferred from the task definition. If the task definition does not have a family, the name will be generated. When flow and deployment metadata is available, the generated name will include their names. Values for this field will be slugified to match AWS character requirements."
      },
      "labels": {
        "type": "object",
        "title": "Labels",
        "description": "Labels applied to infrastructure created by a worker.",
        "additionalProperties": {
          "type": "string"
        }
      },
      "memory": {
        "anyOf": [
          {
            "type": "integer"
          },
          {
            "type": "null"
          }
        ],
        "title": "Memory",
        "description": "The amount of memory to provide to the ECS task. Valid amounts are specified in the AWS documentation. If not provided, a default value of 2048 will be used unless present on the task definition."
      },
      "vpc_id": {
        "anyOf": [
          {
            "type": "string"
          },
          {
            "type": "null"
          }
        ],
        "title": "VPC ID",
        "default": "vpc-0c58432a0c76215e3",
        "description": "The AWS VPC to link the task run to. This is only applicable when using the 'awsvpc' network mode for your task. FARGATE tasks require this network  mode, but for EC2 tasks the default network mode is 'bridge'. If using the 'awsvpc' network mode and this field is null, your default VPC will be used. If no default VPC can be found, the task run will fail."
      },
      "cluster": {
        "anyOf": [
          {
            "type": "string"
          },
          {
            "type": "null"
          }
        ],
        "title": "Cluster",
        "default": "kevin-sandbox",
        "description": "The ECS cluster to run the task in. An ARN or name may be provided. If not provided, the default cluster will be used."
      },
      "command": {
        "anyOf": [
          {
            "type": "string"
          },
          {
            "type": "null"
          }
        ],
        "title": "Command",
        "description": "The command to use when starting a flow run. In most cases, this should be left blank and the command will be automatically generated by the worker."
      },
      "launch_type": {
        "anyOf": [
          {
            "enum": [
              "FARGATE",
              "EC2",
              "EXTERNAL",
              "FARGATE_SPOT"
            ],
            "type": "string"
          },
          {
            "type": "null"
          }
        ],
        "title": "Launch Type",
        "default": "EC2",
        "description": "The type of ECS task run infrastructure that should be used. Note that 'FARGATE_SPOT' is not a formal ECS launch type, but we will configure the proper capacity provider strategy if set here."
      },
      "stream_output": {
        "anyOf": [
          {
            "type": "boolean"
          },
          {
            "type": "null"
          }
        ],
        "title": "Stream Output",
        "description": "If enabled, logs will be streamed from the Prefect container to the local console. Unless you have configured AWS CloudWatch logs manually on your task definition, this requires the same prerequisites outlined in `configure_cloudwatch_logs`."
      },
      "task_role_arn": {
        "anyOf": [
          {
            "type": "string"
          },
          {
            "type": "null"
          }
        ],
        "title": "Task Role ARN",
        "default": "arn:aws:iam::455346737763:role/ecsTaskExecutionWithS3",
        "description": "A role to attach to the task run. This controls the permissions of the task while it is running."
      },
      "container_name": {
        "anyOf": [
          {
            "type": "string"
          },
          {
            "type": "null"
          }
        ],
        "title": "Container Name",
        "description": "The name of the container flow run orchestration will occur in. If not specified, a default value of prefect will be used and if that is not found in the task definition the first container will be used."
      },
      "aws_credentials": {
        "allOf": [
          {
            "$ref": "#/definitions/AwsCredentials"
          }
        ],
        "title": "AWS Credentials",
        "description": "The AWS credentials to use to connect to ECS. If not provided, credentials will be inferred from the local environment following AWS's boto client's rules."
      },
      "execution_role_arn": {
        "anyOf": [
          {
            "type": "string"
          },
          {
            "type": "null"
          }
        ],
        "title": "Execution Role ARN",
        "default": "arn:aws:iam::455346737763:role/ecsTaskExecutionRole",
        "description": "An execution role to use for the task. This controls the permissions of the task when it is launching. If this value is not null, it will override the value in the task definition. An execution role must be provided to capture logs from the container."
      },
      "task_definition_arn": {
        "anyOf": [
          {
            "type": "string"
          },
          {
            "type": "null"
          }
        ],
        "title": "Task Definition Arn",
        "description": "An identifier for an existing task definition to use. If set, options that require changes to the task definition will be ignored. All contents of the task definition in the job configuration will be ignored."
      },
      "network_configuration": {
        "type": "object",
        "title": "Network Configuration",
        "description": "When `network_configuration` is supplied it will override ECS Worker'sawsvpcConfiguration that defined in the ECS task executing your workload. See the [AWS documentation](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ecs-service-awsvpcconfiguration.html) for available options."
      },
      "cloudwatch_logs_prefix": {
        "anyOf": [
          {
            "type": "string"
          },
          {
            "type": "null"
          }
        ],
        "title": "Cloudwatch Logs Prefix",
        "description": "When `configure_cloudwatch_logs` is enabled, this setting may be used to set a prefix for the log group. If not provided, the default prefix will be `prefect-logs_<work_pool_name>_<deployment_id>`. If `awslogs-stream-prefix` is present in `Cloudwatch logs options` this setting will be ignored."
      },
      "cloudwatch_logs_options": {
        "type": "object",
        "title": "Cloudwatch Logs Options",
        "default": {
          "awslogs-stream-prefix": "my-hello-flow"
        },
        "description": "When `configure_cloudwatch_logs` is enabled, this setting may be used to pass additional options to the CloudWatch logs configuration or override the default options. See the [AWS documentation](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/using_awslogs.html#create_awslogs_logdriver_options) for available options. ",
        "additionalProperties": {
          "type": "string"
        }
      },
      "task_watch_poll_interval": {
        "type": "number",
        "title": "Task Watch Poll Interval",
        "default": 5,
        "description": "The amount of time to wait between AWS API calls while monitoring the state of an ECS task."
      },
      "configure_cloudwatch_logs": {
        "anyOf": [
          {
            "type": "boolean"
          },
          {
            "type": "null"
          }
        ],
        "title": "Configure Cloudwatch Logs",
        "default": true,
        "description": "If enabled, the Prefect container will be configured to send its output to the AWS CloudWatch logs service. This functionality requires an execution role with logs:CreateLogStream, logs:CreateLogGroup, and logs:PutLogEvents permissions. The default for this field is `False` unless `stream_output` is set."
      },
      "capacity_provider_strategy": {
        "type": "array",
        "items": {
          "$ref": "#/$defs/CapacityProvider"
        },
        "title": "Capacity Provider Strategy",
        "default": [
          {
            "base": 1,
            "weight": 1,
            "capacityProvider": "FARGATE"
          }
        ],
        "description": "The capacity provider strategy to use when running the task. If a capacity provider strategy is specified, the selected launch type will be ignored."
      },
      "task_start_timeout_seconds": {
        "type": "integer",
        "title": "Task Start Timeout Seconds",
        "default": 300,
        "description": "The amount of time to watch for the start of the ECS task before marking it as failed. The task must enter a RUNNING state to be considered started."
      },
      "auto_deregister_task_definition": {
        "type": "boolean",
        "title": "Auto Deregister Task Definition",
        "default": false,
        "description": "If enabled, any task definitions that are created by this block will be deregistered. Existing task definitions linked by ARN will never be deregistered. Deregistering a task definition does not remove it from your AWS account, instead it will be marked as INACTIVE."
      },
      "match_latest_revision_in_family": {
        "type": "boolean",
        "title": "Match Latest Revision In Family",
        "default": false,
        "description": "If enabled, the most recent active revision in the task definition family will be compared against the desired ECS task configuration. If they are equal, the existing task definition will be used instead of registering a new one. If no family is specified the default family \"prefect\" will be used."
      }
    },
    "description": "Variables for templating an ECS job."
  },
  "job_configuration": {
    "env": "{{ env }}",
    "name": "{{ name }}",
    "labels": "{{ labels }}",
    "vpc_id": "{{ vpc_id }}",
    "cluster": "{{ cluster }}",
    "command": "{{ command }}",
    "stream_output": "{{ stream_output }}",
    "container_name": "{{ container_name }}",
    "aws_credentials": "{{ aws_credentials }}",
    "task_definition": {
      "cpu": "{{ cpu }}",
      "family": "{{ family }}",
      "memory": "{{ memory }}",
      "executionRoleArn": "{{ execution_role_arn }}",
      "containerDefinitions": [
        {
          "name": "{{ container_name }}",
          "image": "{{ image }}"
        }
      ]
    },
    "task_run_request": {
      "tags": "{{ labels }}",
      "cluster": "{{ cluster }}",
      "overrides": {
        "cpu": "{{ cpu }}",
        "memory": "{{ memory }}",
        "taskRoleArn": "{{ task_role_arn }}",
        "containerOverrides": [
          {
            "cpu": "{{ cpu }}",
            "name": "{{ container_name }}",
            "memory": "{{ memory }}",
            "command": "{{ command }}",
            "environment": "{{ env }}"
          }
        ]
      },
      "launchType": "{{ launch_type }}",
      "taskDefinition": "{{ task_definition_arn }}",
      "capacityProviderStrategy": "{{ capacity_provider_strategy }}"
    },
    "execution_role_arn": "{{ execution_role_arn }}",
    "network_configuration": "{{ network_configuration }}",
    "cloudwatch_logs_prefix": "{{ cloudwatch_logs_prefix }}",
    "cloudwatch_logs_options": "{{ cloudwatch_logs_options }}",
    "task_watch_poll_interval": "{{ task_watch_poll_interval }}",
    "configure_cloudwatch_logs": "{{ configure_cloudwatch_logs }}",
    "task_start_timeout_seconds": "{{ task_start_timeout_seconds }}",
    "auto_deregister_task_definition": "{{ auto_deregister_task_definition }}",
    "match_latest_revision_in_family": "{{ match_latest_revision_in_family }}"
  }
}