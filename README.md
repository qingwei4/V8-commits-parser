# V8-commits-parser

### note 
The bot is under testing. If issues arise, please open an issue.


### What is it?
A simple discord bot that will parse V8 commits and notify you.

### How to use:
1. Clone the repo
2. add your discord token to the `discord_token` file
3. add you github access token to the `github_token` file
4. Run `docker build -t v8-commits-parser .`
5. Run `docker run -d --name v8-commits-parser v8-commits-parser`
6. Invite the bot to your server using the token in `discord_token`
7. Use `!> subscribe <keywords>` to subscribe to commits with the given keywords
8. Use `!> unsubscribe` to unsubscribe from commits
