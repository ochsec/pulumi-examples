import * as pulumi from "@pulumi/pulumi";
import * as aws from "@pulumi/aws";


// Lambda exec role
const lambdaRole = new aws.iam.Role("lambdaRole", {
    assumeRolePolicy: {
        Version: "2012-10-17",
        Statement: [{
            Action: "sts:AssumeRole",
            Effect: "Allow",
            Principal: {
                Service: "lambda.amazonaws.com",
            },
        }],
    },
});

// Lambda function
const lambda = new aws.lambda.Function("echoLambda", {
    runtime: aws.lambda.Go1dxRuntime,
    handler: "main",
    code: new pulumi.asset.FileArchive("./lambda/deployment.zip"),
    role: lambdaRole.arn,
});

// Attach exec role to lambda
new aws.iam.RolePolicyAttachment("lambdaExecPolicy", {
    role: lambdaRole,
    policyArn: aws.iam.ManagedPolicy.AWSLambdaBasicExecutionRole,
});

// API Gateway
const api = new aws.apigatewayv2.Api("httpApi", {
    protocolType: "HTTP",
});

// Integration endpoint
const integration = new aws.apigatewayv2.Integration("lambdaIntegration", {
    apiId: api.id,
    integrationType: "AWS_PROXY",
    integrationUri: lambda.arn,
    payloadFormatVersion: "2.0"
});

// Setup the route for the '/echo' endpoint
const route = new aws.apigatewayv2.Route("echoRoute", {
    apiId: api.id,
    routeKey: "ANY /echo",
    target: pulumi.interpolate`integrations/${integration.id}`,
});

// Deploy API
const deployment = new aws.apigatewayv2.Deployment("apiDeployment", {
    apiId: api.id,
    triggers: {
        redeployment: pulumi.all([integration.id, route.id])
            .apply((ids: string[]) => JSON.stringify(ids)),
    }
}, { dependsOn: [route] });

// Stage for deployment
new aws.apigatewayv2.Stage("apiStage", {
    apiId: api.id,
    name: "prod",
    deploymentId: deployment.id,
    autoDeploy: true,
});

export const endpointUrl = api.apiEndpoint;
