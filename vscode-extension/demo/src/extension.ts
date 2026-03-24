import * as vscode from 'vscode';

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {
	console.log('Extension "demo" is now active!');

	vscode.chat.createChatParticipant("demo.helloWorld", async (request, context, response, token) => {
		const userQuery = request.prompt;
		const chatModels = await vscode.lm.selectChatModels({
			vendor: 'copilot',
			family: 'gpt-4o'
		  });
		const messages = [
			vscode.LanguageModelChatMessage.User(userQuery)
		];
		const chatRequest = await chatModels[0].sendRequest(messages, undefined, token);
		for await( const token of chatRequest.text) {
			response.markdown(token);
		}
	});
	
}

// This method is called when your extension is deactivated
export function deactivate() {}
