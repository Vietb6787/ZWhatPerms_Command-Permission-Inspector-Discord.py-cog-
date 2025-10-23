# ZWhatPerms - Command Permission Inspector 🔍

A powerful Discord bot cog that reveals detailed information about any command, including permissions, requirements, and restrictions.

## What is ZWhatPerms?

Ever wondered what permissions you need to run a specific bot command? Or what permissions the bot needs? ZWhatPerms analyzes any command in your Discord bot and displays comprehensive information about its requirements, restrictions, and behavior.

## Features ✨

### 📋 **Comprehensive Command Analysis**
- **Command Type Detection** - Identifies if it's a prefix command, slash command, or hybrid command
- **Basic Information** - Shows description, aliases, usage syntax, and whether it's hidden or disabled
- **Subcommands** - Lists all subcommands if the command is a command group

### 👤 **Permission Detection**
- **User Permissions** - Shows what permissions the user needs to run the command
- **Bot Permissions** - Displays what permissions the bot needs to execute the command
- **Permission Types** - Distinguishes between channel and guild permissions

### 🎭 **Role & Special Requirements**
- **Role Requirements** - Detects specific roles or role IDs needed to use the command
- **Special Checks** - Identifies unique requirements like:
  - 🔴 Bot Owner Only
  - ⚠️ Administrator permissions
  - 🔞 NSFW Channel Required
  - 🏛️ Server Only (No DMs)
  - 📬 DM Only
  - 🔊 Voice Channel requirements
  - 💾 Database checks
  - 🔧 Custom checks

### 🔬 **Advanced Analysis**
- **Check Simulation** - Actually runs the command checks to detect requirements
- **Source Code Analysis** - Inspects the command's source code to find hidden requirements
- **Cog-Level Checks** - Detects permissions and requirements set at the cog level
- **Error Detection** - Shows what errors you'd get if you tried to run the command without proper permissions

### ⏱️ **Rate Limiting Info**
- **Cooldowns** - Shows how often the command can be used and cooldown type (per user, channel, guild, etc.)
- **Concurrency Limits** - Displays how many times the command can run simultaneously

### 🌍 **Availability Information**
- Shows whether the command works in DMs, servers, or both

## Commands

### `/zwperms <command_name>`
**Aliases:** None  
**Usage:** `/zwperms help` or `!zwperms moderation kick`

Analyzes the specified command and displays all its requirements, permissions, and information.

**Examples:**
- `/zwperms ban` - Check what permissions are needed for the ban command
- `/zwperms music play` - Analyze a subcommand
- `/zwperms help` - See what the help command requires

## What You'll See 📊

When you run `zwperms`, you'll get an embedded message with sections like:

1. **ℹ️ Basic Info** - Command type, usage, description, aliases
2. **👤 User Permissions** - What permissions you need
3. **🤖 Bot Permissions** - What permissions the bot needs
4. **🎭 Role Requirements** - Specific roles needed (if any)
5. **🔒 Special Requirements** - Owner-only, NSFW, voice checks, etc.
6. **🔍 Simulation Result** - Live check results
7. **⚠️ Raw Error** - Actual error message you'd receive
8. **⏱️ Cooldown** - Rate limiting information
9. **🔄 Max Concurrency** - Concurrent usage limits
10. **📦 Cog** - Which cog the command belongs to
11. **🌍 Availability** - Where the command works

## Use Cases 💡

- **Server Admins**: Quickly check what permissions to assign for specific commands
- **Bot Developers**: Debug why commands aren't working for certain users
- **Users**: Understand why you can't use a specific command
- **Documentation**: Generate accurate permission requirements for your commands

## Smart Features 🧠

- **Fuzzy Search**: If you mistype a command name, it suggests similar commands
- **Deep Analysis**: Checks multiple layers - decorators, cog checks, source code, and runtime simulation
- **Source Code Display**: Optionally shows the actual source code of checks for transparency
- **Error Simulation**: Runs the command checks to see exactly what error would occur

## Made By

**TheHolyOneZ**  
Part of the ZygnalBot ecosystem

---

*This cog works with any Discord.py bot and provides instant insights into command requirements!*


* For more cogs and extensions, visit our official extension portal: https://zygnalbot.com/extension/
*
* ===================================
* 📢 IMPORTANT INFORMATION REGARDING THE EXTENSION PORTAL 📢
* ===================================
*
* ACCESS REQUIREMENT: Access to the extension portal requires a FREE ZygnalID, 
* which can only be obtained by joining our Discord server: discord.gg/sgZnXca5ts
*
* ZYGNALID ACTIVATION PROCESS:
* 1. Download and run the ZygnalBot (Main_bot_3.py).
* 2. Open the generated 'zygnalid.txt' file to retrieve your ID. (or run !mp myid)
* 3. Go to our Discord server and open a Support Ticket with the title "ZygnalID Activation".
* 4. Provide the required information (specified within the ticket) and your ZygnalID.
*
* NOTE: Many Cogs from the ZygnalBot extension portal are only allowed to be used 
* within the ZygnalBot ecosystem (e.g., ZygnalBot itself / Main_bot_3.py).
*



