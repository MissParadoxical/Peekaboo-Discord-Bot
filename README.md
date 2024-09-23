![Peekaboo Bot Logo](https://files.catbox.moe/a8mvtz.png)

# Peekaboo Discord Bot

Peekaboo is a fun and interactive Discord bot that plays a game of "Peekaboo" with server members. The bot sends random "Peekaboo!" messages to channels, and users can earn points by reacting to these messages before they disapear.

## Features

- Sends a "Peekaboo!" message to a random channels
- Users earn a point by reacting to the bot's message beofre it's gone
- Leaderboard to track user scores
- Admin commands for managing the game
- Sleek, minimalist embed design for bot responses

## Commands

- `p!start` - Start the Peekaboo game (Admin only)
- `p!stop` - Stop the Peekaboo game (Admin only)
- `p!leaderboard` - Show the Peekaboo leaderboard
- `p!adminboard` - Show detailed Peekaboo leaderboard (Admin only)
- `p!reset` - Reset the Peekaboo leaderboard (Admin only)
- `p!help` - Show the help menu

## Permissions

The bot requires the following permissions in the channels where it will operate:

- Read Messages
- Send Messages
- Manage Messages (to delete its own messages)
- Read Message History

The bot will only send messages in channels where it has permission to send messages and which are not marked as NSFW.

Note: While the bot doesn't need administrator rights for its core functionality, some commands (start, stop, reset) are restricted to users with administrator permissions on the server.

## Setup and Installation

1. Make sure you have Python 3.8 or higher installed on your system.

2. Install the required dependencies:
   ```
   pip install discord.py python-dotenv
   ```

3. Create a file named `.env` in the same directory as `main.py` and add your Discord bot token:
   ```
   DISCORD_TOKEN=your_bot_token_here
   ```
   Replace `your_bot_token_here` with your actual Discord bot token.

4. Run the bot:
   ```
   python main.py
   ```

## Configuration

You can modify the following variables in `main.py` to customize the bot's behavior:

- `command_prefix`: Change the prefix for bot commands (default is 'p!')
- `peekaboo_loop.change_interval(minutes=2)`: Change the interval between Peekaboo messages

## Contributing

Contributions are welcome! <3

## License

This project is licensed under the MIT License - see the [LICENSE] file for details.
