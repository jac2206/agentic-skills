# AWS4 icon guidance for Draw.io

Use this reference when creating or reviewing an AWS infrastructure diagram in Draw.io. An icon style is a rendering instruction, not evidence that a service is deployed.

## Preferred style

Search the installed diagrams.net AWS libraries for the current AWS4 service icon and check its exact identifier. A common service icon style is:

```text
shape=mxgraph.aws4.resourceIcon;resIcon=mxgraph.aws4.lambda;fillColor=#ED7100;
```

The `resIcon` suffix is the stencil identifier. Use the exact identifier exposed by the installed diagrams.net AWS4 library; names are not guaranteed to remain identical across library versions. Do not substitute a guessed name or an older AWS stencil generation because the result may be a blank tile or dated icon. If the current stencil is absent or stale, search the current official AWS icon package for its SVG.

Use the provider's service color and preserve the native icon proportions. Keep the full service name as editable text next to the icon. A service-specific icon is preferable to a category mark; when only a category icon is available, label the actual service explicitly. If neither an exact service icon nor a truthful category icon is available or verifiable, use the labeled service-card fallback in [Draw.io XML guidance](drawio-xml.md) and record why it was needed. Do not guess a stencil or borrow an icon from Azure or Google Cloud.

## Names used by this Skill's examples

These identifiers appear in the example XML. This table records the XML styles and intended service labels; it does **not** assert that every icon was rendered and visually checked in this environment.

| AWS4 identifier | Example service label | Example color |
| --- | --- | --- |
| `amplify` | AWS Amplify | `#DD344C` |
| `api_gateway` | Amazon API Gateway | `#E7157B` |
| `bedrock` | Amazon Bedrock, including labeled AgentCore or Knowledge Base concepts | `#01A88D` |
| `certificate_manager` | AWS Certificate Manager | `#DD344C` |
| `cloud_development_kit` | AWS CDK | `#C925D1` |
| `cloudformation` | AWS CloudFormation | `#E7157B` |
| `cloudfront` | Amazon CloudFront | `#8C4FFF` |
| `cloudfront_functions` | CloudFront Functions | `#8C4FFF` |
| `cloudwatch_2` | Amazon CloudWatch | `#E7157B` |
| `cognito` | Amazon Cognito | `#DD344C` |
| `dynamodb` | Amazon DynamoDB | `#C925D1` |
| `ecs` | Amazon ECS | `#ED7100` |
| `eks` | Amazon EKS | `#ED7100` |
| `elasticsearch_service` | Amazon OpenSearch Service | `#8C4FFF` |
| `eventbridge` | Amazon EventBridge | `#E7157B` |
| `identity_and_access_management` | AWS IAM | `#DD344C` |
| `key_management_service` | AWS KMS | `#DD344C` |
| `lambda` | AWS Lambda | `#ED7100` |
| `network_load_balancer` | Network Load Balancer | `#8C4FFF` |
| `rds` | Amazon RDS for PostgreSQL | `#C925D1` |
| `rekognition_2` | Amazon Rekognition | `#01A88D` |
| `route_53` | Amazon Route 53 | `#8C4FFF` |
| `s3` | Amazon S3 | `#7AA116` |
| `secrets_manager` | AWS Secrets Manager | `#DD344C` |
| `sqs` | Amazon SQS | `#E7157B` |
| `step_functions` | AWS Step Functions | `#E7157B` |
| `waf` | AWS WAF | `#DD344C` |

Other example XML uses standalone shapes for `mxgraph.aws4.dynamodb_stream`, `mxgraph.aws4.mobile_client`, and `mxgraph.aws4.traditional_server`. These are not `resourceIcon` suffixes.

## Verification workflow

1. Confirm the service name against the AWS architecture icon package and choose a matching AWS4 stencil in the current diagrams.net library.
2. Open the `.drawio` in diagrams.net. Confirm each service glyph appears, has the expected color and proportions, and is not a blank tile. Check labels, connector routes, spacing, and overlaps at normal zoom.
3. If the native stencil is unavailable or stale, use the current official AWS SVG icon and embed it in the Draw.io file as an image object. Keep its label editable and preserve the original proportions and color.
4. If the official AWS catalog has no suitable icon, use a truthful official category icon with the exact service label. If that is not available, use and disclose the labeled service-card fallback defined in [Draw.io XML guidance](drawio-xml.md).
5. Record which sources and checks were used. XML parsing and identifier checks alone do not validate rendering or visual quality.

AWS publishes its official [architecture icon package](https://aws.amazon.com/architecture/icons/) and notes that third-party libraries may contain legacy icon sets. The [Draw.io style reference](https://www.drawio.com/docs/reference/diagram-generation/style-reference/) documents `mxgraph.aws4.*` shape styles. Check those sources when a service identifier is missing or a newer service icon is required; do not treat this short example list as a complete AWS catalog.
