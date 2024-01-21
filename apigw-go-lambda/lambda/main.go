package main

import (
	"context"
	"encoding/json"
	"fmt"

	"github.com/aws/aws-lambda-go/events"
	"github.com/aws/aws-lambda-go/lambda"
)

type InputEvent struct {
	Name    string `json:"name"`
	Message string `json:"message"`
}

type Response struct {
	Response string `json:"response"`
}

func handler(ctx context.Context, event events.APIGatewayProxyRequest) (events.APIGatewayProxyResponse, error) {
	// Parse the input event
	var inputEvent InputEvent
	err := json.Unmarshal([]byte(event.Body), &inputEvent)
	if err != nil {
		return events.APIGatewayProxyResponse{StatusCode: 400, Body: "Bad Request"}, err
	}

	// Create the response
	response := Response{
		Response: fmt.Sprintf("%s says %s", inputEvent.Name, inputEvent.Message),
	}

	// Serialize the response
	responseJSON, err := json.Marshal(response)
	if err != nil {
		return events.APIGatewayProxyResponse{StatusCode: 500, Body: "Internal Server Error"}, err
	}

	return events.APIGatewayProxyResponse{
		StatusCode: 200,
		Headers:    map[string]string{"Content-Type": "application/json"},
		Body:       string(responseJSON),
	}, nil
}

func main() {
	lambda.Start(handler)
}
