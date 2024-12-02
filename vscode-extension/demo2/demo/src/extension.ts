import * as vscode from 'vscode';

// This method is called when your extension is activated
// Your extension is activated the very first time the command is executed
export function activate(context: vscode.ExtensionContext) {
    console.log('Congratulations, your extension "demo" is now active!');

    let disposable = vscode.commands.registerCommand('demo.helloWorld', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showErrorMessage('No active editor found.');
            return;
        }

        const document = editor.document;
        const userQuery = document.getText();
        
        try {
            const chatModels = await vscode.lm.selectChatModels({
                vendor: 'copilot',
                family: 'gpt-4o'
            });

            const messages = [
                vscode.LanguageModelChatMessage.User(userQuery)
            ];

            const chatRequest = await chatModels[0].sendRequest(messages, undefined, undefined);
            for await (const token of chatRequest.text) {
                vscode.window.showInformationMessage(token);
            }
        } catch (error) {
            if (error instanceof Error) {
                vscode.window.showErrorMessage(`An error occurred: ${error.message}`);
            } else {
                vscode.window.showErrorMessage('An unknown error occurred.');
            }
        }
    });

    context.subscriptions.push(disposable);
}

// This method is called when your extension is deactivated
export function deactivate() {}
