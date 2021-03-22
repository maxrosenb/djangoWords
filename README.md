# djangoWords

djangoWords, a django API service.

Features:

- Allows users to sign up/register and create a "game"
- A game has a series of user-generated words or phrases associated with it
- The game master is able to create 4 words or phrases for the game
- The game master is able to share a link to friends (who have not created an account) to create 4 words or phrases for the game and submit them along with their name
- The game master is be able to see a list of names who have submitted words or phrases for the game
- The game master is able to "start" the game after which, the submission of words or phrases will not work and new users cannot join
- Upon the start api call, all the words and phrases are returned to the game master in a randomized order
