# Description
An API that authenticates the user in github and retreives the user’s access token by the “code”.
Tutorial how it’s implemented is https://docs.github.com/en/apps/creating-github-apps/writing-code-for-a-github-app/building-a-login-with-github-button-with-a-github-app#add-code-to-generate-a-user-access-token
Using the code, retrieve the user’s access token from github, retreive the user’s id, name and avatar url. 
If user does not exist in the API database, register the user.

Generate the encrypted hash of access token using a salt. Store the salt in the database too.