# Made by TheHolyOneZ 
# For more cogs and extensions, visit our official extension portal: https://zygnalbot.com/extension/
#
# ==============================================================================================
# 📢 IMPORTANT INFORMATION REGARDING THE EXTENSION PORTAL 📢
# ==============================================================================================
#
# ACCESS REQUIREMENT: Access to the extension portal requires a FREE ZygnalID, 
# which can only be obtained by joining our Discord server: discord.gg/sgZnXca5ts
#
# ZYGNALID ACTIVATION PROCESS:
# 1. Download and run the ZygnalBot (Main_bot_3.py).
# 2. Open the generated 'zygnalid.txt' file to retrieve your ID. (or run !mp myid)
# 3. Go to our Discord server and open a Support Ticket with the title "ZygnalID Activation".
# 4. Provide the required information (specified within the ticket) and your ZygnalID.
#
# NOTE: Many Cogs from the ZygnalBot extension portal are only allowed to be used 
# within the ZygnalBot ecosystem (e.g., ZygnalBot itself / Main_bot_3.py).
#
# ==============================================================================================


import discord
from discord.ext import commands
from discord import app_commands
from typing import Union, List, Set
import inspect
import traceback
import re

class ZWhatPerms(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_command_type(self, command):
        if isinstance(command, commands.HybridCommand) or isinstance(command, commands.HybridGroup):
            return "Hybrid Command (Prefix & Slash)"
        elif hasattr(command, 'app_command') and command.app_command:
            return "Slash Command"
        else:
            return "Prefix Command"

    def extract_permissions_from_checks(self, checks):
        user_perms = set()
        bot_perms = set()
        special_checks = []
        role_requirements = []

        for check in checks:
            check_name = check.__qualname__ if hasattr(check, '__qualname__') else str(check)
            
            if 'has_permissions' in check_name or 'has_guild_permissions' in check_name:
                perm_type = "Guild Permissions" if 'guild' in check_name else "Channel Permissions"
                if hasattr(check, '__closure__') and check.__closure__:
                    for cell in check.__closure__:
                        if isinstance(cell.cell_contents, dict):
                            perms_dict = cell.cell_contents
                            for perm, value in perms_dict.items():
                                if value:
                                    user_perms.add((perm, perm_type))
                                    if perm == 'administrator':
                                        special_checks.append("⚠️ ADMINISTRATOR (Bypasses all other permissions)")
            
            elif 'bot_has_permissions' in check_name or 'bot_has_guild_permissions' in check_name:
                perm_type = "Guild Permissions" if 'guild' in check_name else "Channel Permissions"
                if hasattr(check, '__closure__') and check.__closure__:
                    for cell in check.__closure__:
                        if isinstance(cell.cell_contents, dict):
                            perms_dict = cell.cell_contents
                            for perm, value in perms_dict.items():
                                if value:
                                    bot_perms.add((perm, perm_type))
            
            elif 'is_owner' in check_name:
                special_checks.append("🔴 Bot Owner Only")
            
            elif 'has_role' in check_name:
                if hasattr(check, '__closure__') and check.__closure__:
                    for cell in check.__closure__:
                        content = cell.cell_contents
                        if isinstance(content, int):
                            role_requirements.append(f"Role ID: `{content}`")
                        elif isinstance(content, str):
                            role_requirements.append(f"Role: `{content}`")
            
            elif 'has_any_role' in check_name:
                if hasattr(check, '__closure__') and check.__closure__:
                    roles = []
                    for cell in check.__closure__:
                        content = cell.cell_contents
                        if isinstance(content, (list, tuple)):
                            for item in content:
                                if isinstance(item, int):
                                    roles.append(f"`{item}`")
                                elif isinstance(item, str):
                                    roles.append(f"`{item}`")
                        elif isinstance(content, int):
                            roles.append(f"`{content}`")
                        elif isinstance(content, str):
                            roles.append(f"`{content}`")
                    if roles:
                        role_requirements.append(f"Any of: {', '.join(roles)}")
            
            elif 'is_nsfw' in check_name:
                special_checks.append("🔞 NSFW Channel Required")
            elif 'dm_only' in check_name:
                special_checks.append("📬 DM Only")
            elif 'guild_only' in check_name:
                special_checks.append("🏛️ Server Only (No DMs)")
            elif 'check_voice_client' in check_name:
                special_checks.append("🔊 Voice Channel Required")
            elif 'is_in_voice' in check_name:
                special_checks.append("🎤 User Must Be In Voice")
            elif 'bot_in_voice' in check_name:
                special_checks.append("🤖 Bot Must Be In Voice")
            elif 'cooldown' not in check_name and 'max_concurrency' not in check_name and 'DynamicCooldownMapping' not in check_name:
                special_checks.append(f"🔧 Custom Check: `{check_name}`")

        return user_perms, bot_perms, special_checks, role_requirements

    def analyze_check_source(self, check_func):
        findings = {
            'user_perms': set(),
            'bot_perms': set(),
            'special_checks': [],
            'role_requirements': [],
            'source_code': None
        }
        
        try:
            source = inspect.getsource(check_func)
            findings['source_code'] = source
            
            if 'administrator' in source.lower():
                findings['user_perms'].add(('administrator', "Source"))
                findings['special_checks'].append("⚠️ ADMINISTRATOR (Found in source)")
            
            perm_patterns = [
                'manage_guild', 'manage_channels', 'manage_roles', 'kick_members', 
                'ban_members', 'moderate_members', 'manage_messages', 'manage_webhooks',
                'manage_nicknames', 'manage_emojis', 'view_audit_log', 'manage_events'
            ]
            
            for perm in perm_patterns:
                if perm in source:
                    findings['user_perms'].add((perm, "Source"))
            
            if 'owner' in source.lower() and ('ctx.guild.owner' in source or 'owner_id' in source):
                findings['special_checks'].append("👑 Server Owner (Found in source)")
            
            role_id_pattern = re.findall(r'\b\d{17,19}\b', source)
            if role_id_pattern:
                for role_id in role_id_pattern[:5]:
                    findings['role_requirements'].append(f"Role ID: `{role_id}`")
            
            if 'get_role' in source or 'has_role' in source:
                findings['role_requirements'].append("🎭 Role Check (Found in source)")
            
            if 'database' in source.lower() or 'db.' in source or '.fetch' in source or 'SELECT' in source:
                findings['special_checks'].append("💾 Database Check (Found in source)")
            
        except Exception as e:
            pass
        
        return findings

    async def simulate_command_checks(self, ctx, command):
        simulated_info = {
            'user_perms': set(),
            'bot_perms': set(),
            'special_checks': [],
            'role_requirements': [],
            'detected_from_simulation': [],
            'raw_error': None
        }

        try:
            can_run_result = await command.can_run(ctx)
            if not can_run_result:
                simulated_info['detected_from_simulation'].append("⚠️ Command check returned False")
        
        except commands.MissingPermissions as e:
            simulated_info['raw_error'] = str(e)
            for perm in e.missing_permissions:
                simulated_info['user_perms'].add((perm, "Required"))
                if perm == 'administrator':
                    simulated_info['special_checks'].append("⚠️ ADMINISTRATOR")
            simulated_info['detected_from_simulation'].append(f"❌ {str(e)}")
        
        except commands.BotMissingPermissions as e:
            simulated_info['raw_error'] = str(e)
            for perm in e.missing_permissions:
                simulated_info['bot_perms'].add((perm, "Required"))
            simulated_info['detected_from_simulation'].append(f"❌ {str(e)}")
        
        except commands.MissingRole as e:
            simulated_info['raw_error'] = str(e)
            role_info = str(e.missing_role)
            if isinstance(e.missing_role, int):
                simulated_info['role_requirements'].append(f"Role ID: `{e.missing_role}`")
            else:
                simulated_info['role_requirements'].append(f"Role: `{e.missing_role}`")
            simulated_info['detected_from_simulation'].append(f"❌ {str(e)}")
        
        except commands.MissingAnyRole as e:
            simulated_info['raw_error'] = str(e)
            roles = [str(r) for r in e.missing_roles]
            simulated_info['role_requirements'].append(f"Any of: {', '.join([f'`{r}`' for r in roles])}")
            simulated_info['detected_from_simulation'].append(f"❌ {str(e)}")
        
        except commands.NotOwner:
            simulated_info['raw_error'] = "Bot Owner Only"
            simulated_info['special_checks'].append("🔴 Bot Owner Only")
            simulated_info['detected_from_simulation'].append("❌ Bot Owner Only")
        
        except commands.NSFWChannelRequired:
            simulated_info['raw_error'] = "NSFW Channel Required"
            simulated_info['special_checks'].append("🔞 NSFW Channel Required")
            simulated_info['detected_from_simulation'].append("❌ NSFW Channel Required")
        
        except commands.PrivateMessageOnly:
            simulated_info['raw_error'] = "DM Only"
            simulated_info['special_checks'].append("📬 DM Only")
            simulated_info['detected_from_simulation'].append("❌ DM Only")
        
        except commands.NoPrivateMessage:
            simulated_info['raw_error'] = "Server Only"
            simulated_info['special_checks'].append("🏛️ Server Only (No DMs)")
            simulated_info['detected_from_simulation'].append("❌ Server Only")
        
        except commands.CheckFailure as e:
            simulated_info['raw_error'] = str(e)
            error_msg = str(e).lower()
            simulated_info['detected_from_simulation'].append(f"❌ Check Failed: {str(e)}")
            
            if 'administrator' in error_msg or 'admin' in error_msg:
                simulated_info['user_perms'].add(('administrator', "Error"))
                simulated_info['special_checks'].append("⚠️ ADMINISTRATOR")
            
            if 'owner' in error_msg:
                simulated_info['special_checks'].append("🔴 Owner Required")
            
            if 'role' in error_msg:
                simulated_info['role_requirements'].append(f"Role Check: {str(e)}")
            
            if 'permission' in error_msg:
                simulated_info['special_checks'].append(f"Permission Check: {str(e)}")
        
        except Exception as e:
            simulated_info['raw_error'] = f"{type(e).__name__}: {str(e)}"
            error_msg = str(e).lower()
            simulated_info['detected_from_simulation'].append(f"❌ {type(e).__name__}: {str(e)}")
            
            if 'administrator' in error_msg or 'admin' in error_msg:
                simulated_info['user_perms'].add(('administrator', "Error"))
            
            if 'permission' in error_msg:
                simulated_info['special_checks'].append(f"Permission Error: {str(e)}")
            
            if 'role' in error_msg:
                simulated_info['role_requirements'].append(f"Role Error: {str(e)}")

        return simulated_info

    def format_permission_name(self, perm, perm_type=None):
        formatted = perm.replace('_', ' ').title()
        if perm_type:
            return f"{formatted} ({perm_type})"
        return formatted

    @commands.hybrid_command(name="zwperms", description="Check what permissions and info a command has")
    async def zwperms(self, ctx: commands.Context, *, cmd: str):
        command = self.bot.get_command(cmd)
        
        if command is None:
            all_commands = [c.qualified_name for c in self.bot.walk_commands()]
            similar = [c for c in all_commands if cmd.lower() in c.lower()]
            
            embed = discord.Embed(
                title="❌ Command Not Found",
                description=f"The command `{cmd}` does not exist in this bot.",
                color=discord.Color.red()
            )
            
            if similar:
                embed.add_field(
                    name="Did you mean?",
                    value="\n".join([f"• `{c}`" for c in similar[:5]]),
                    inline=False
                )
            
            embed.set_footer(text="Made By TheHolyOneZ")
            await ctx.send(embed=embed)
            return

        prefix_used = ctx.prefix if hasattr(ctx, 'prefix') and ctx.prefix else "/"
        command_type = self.get_command_type(command)
        
        embed = discord.Embed(
            title=f"📋 Command Info: `{command.qualified_name}`",
            color=discord.Color.blue()
        )

        info_text = f"**Type:** {command_type}\n"
        info_text += f"**Prefix Used:** `{prefix_used}`\n"
        
        if command.aliases:
            info_text += f"**Aliases:** {', '.join([f'`{alias}`' for alias in command.aliases])}\n"
        
        if command.description:
            info_text += f"**Description:** {command.description}\n"
        elif command.help:
            info_text += f"**Description:** {command.help}\n"
        
        if command.signature:
            info_text += f"**Usage:** `{prefix_used}{command.qualified_name} {command.signature}`\n"
        else:
            info_text += f"**Usage:** `{prefix_used}{command.qualified_name}`\n"
        
        if command.hidden:
            info_text += f"**Hidden:** ✅ Yes\n"
        
        if not command.enabled:
            info_text += f"**Enabled:** ❌ No\n"
        
        if isinstance(command, commands.Group):
            subcommands = [c.name for c in command.commands]
            info_text += f"**Subcommands:** {', '.join([f'`{sc}`' for sc in subcommands])}\n"

        embed.add_field(name="ℹ️ Basic Info", value=info_text, inline=False)

        user_perms = set()
        bot_perms = set()
        special_checks = []
        role_requirements = []
        source_codes = []

        simulated = await self.simulate_command_checks(ctx, command)
        
        user_perms.update(simulated['user_perms'])
        bot_perms.update(simulated['bot_perms'])
        special_checks.extend(simulated['special_checks'])
        role_requirements.extend(simulated['role_requirements'])

        if hasattr(command, 'requires') and command.requires:
            if hasattr(command.requires, 'user_perms') and command.requires.user_perms:
                for perm, value in command.requires.user_perms:
                    if value:
                        user_perms.add((perm, "Guild Permissions"))
                        if perm == 'administrator':
                            if not any('ADMINISTRATOR' in str(check) for check in special_checks):
                                special_checks.append("⚠️ ADMINISTRATOR")
            if hasattr(command.requires, 'bot_perms') and command.requires.bot_perms:
                for perm, value in command.requires.bot_perms:
                    if value:
                        bot_perms.add((perm, "Guild Permissions"))

        if command.checks:
            check_user_perms, check_bot_perms, checks_list, role_reqs = self.extract_permissions_from_checks(command.checks)
            user_perms.update(check_user_perms)
            bot_perms.update(check_bot_perms)
            special_checks.extend(checks_list)
            role_requirements.extend(role_reqs)

        if hasattr(command, 'cog') and command.cog:
            cog_checks = []
            if hasattr(command.cog, 'cog_check'):
                cog_check_func = getattr(command.cog, 'cog_check')
                if callable(cog_check_func):
                    cog_checks.append(cog_check_func)
                    
                    source_findings = self.analyze_check_source(cog_check_func)
                    if source_findings['source_code']:
                        source_codes.append(("Cog Check", source_findings['source_code']))
                    user_perms.update(source_findings['user_perms'])
                    bot_perms.update(source_findings['bot_perms'])
                    special_checks.extend(source_findings['special_checks'])
                    role_requirements.extend(source_findings['role_requirements'])
            
            if hasattr(command.cog, '__cog_commands_checks__'):
                for cog_check in command.cog.__cog_commands_checks__:
                    cog_checks.append(cog_check)
                    source_findings = self.analyze_check_source(cog_check)
                    if source_findings['source_code']:
                        source_codes.append(("Cog Commands Check", source_findings['source_code']))
                    user_perms.update(source_findings['user_perms'])
                    bot_perms.update(source_findings['bot_perms'])
                    special_checks.extend(source_findings['special_checks'])
                    role_requirements.extend(source_findings['role_requirements'])
            
            if cog_checks:
                check_user_perms, check_bot_perms, checks_list, role_reqs = self.extract_permissions_from_checks(cog_checks)
                user_perms.update(check_user_perms)
                bot_perms.update(check_bot_perms)
                for check in checks_list:
                    if check not in special_checks:
                        special_checks.append(f"[Cog] {check}")
                role_requirements.extend(role_reqs)

        callback = command.callback
        if callback:
            source_findings = self.analyze_check_source(callback)
            if source_findings['source_code']:
                source_codes.append(("Command Callback", source_findings['source_code']))
            user_perms.update(source_findings['user_perms'])
            bot_perms.update(source_findings['bot_perms'])
            for check in source_findings['special_checks']:
                if check not in special_checks:
                    special_checks.append(check)
            role_requirements.extend(source_findings['role_requirements'])

        if user_perms:
            perms_text = "\n".join([f"• {self.format_permission_name(perm[0], perm[1])}" for perm in sorted(user_perms, key=lambda x: x[0])])
            embed.add_field(name="👤 User Permissions", value=perms_text, inline=True)
        else:
            embed.add_field(name="👤 User Permissions", value="✅ None Required", inline=True)

        if bot_perms:
            perms_text = "\n".join([f"• {self.format_permission_name(perm[0], perm[1])}" for perm in sorted(bot_perms, key=lambda x: x[0])])
            embed.add_field(name="🤖 Bot Permissions", value=perms_text, inline=True)
        else:
            embed.add_field(name="🤖 Bot Permissions", value="✅ None Required", inline=True)

        if role_requirements:
            roles_text = "\n".join([f"• {req}" for req in role_requirements])
            embed.add_field(name="🎭 Role Requirements", value=roles_text, inline=False)

        if special_checks:
            checks_text = "\n".join([f"• {check}" for check in special_checks])
            embed.add_field(name="🔒 Special Requirements", value=checks_text, inline=False)

        if simulated['detected_from_simulation']:
            detected_text = "\n".join([f"{info}" for info in simulated['detected_from_simulation']])
            embed.add_field(name="🔍 Simulation Result", value=detected_text, inline=False)

        if simulated['raw_error']:
            error_display = simulated['raw_error']
            if len(error_display) > 1000:
                error_display = error_display[:1000] + "..."
            embed.add_field(name="⚠️ Raw Error", value=f"```{error_display}```", inline=False)

        if hasattr(command, '_buckets') and command._buckets:
            cooldown = command._buckets._cooldown
            if cooldown:
                rate = cooldown.rate
                per = cooldown.per
                bucket_type = str(command._buckets.type).split('.')[-1]
                embed.add_field(
                    name="⏱️ Cooldown",
                    value=f"`{rate}` use(s) per `{per}s`\nType: `{bucket_type}`",
                    inline=True
                )

        if hasattr(command, '_max_concurrency') and command._max_concurrency:
            max_conc = command._max_concurrency
            bucket_type = str(max_conc.per).split('.')[-1]
            embed.add_field(
                name="🔄 Max Concurrency",
                value=f"`{max_conc.number}` concurrent use(s)\nType: `{bucket_type}`",
                inline=True
            )

        if command.cog:
            embed.add_field(name="📦 Cog", value=f"`{command.cog.qualified_name}`", inline=True)

        guild_only = any('guild_only' in str(check).lower() or 'Guild Only' in str(check) or 'Server Only' in str(check) for check in special_checks) or any('Server Only' in info for info in simulated['detected_from_simulation'])
        dm_only = any('dm_only' in str(check).lower() or 'DM Only' in str(check) for check in special_checks) or any('DM Only' in info for info in simulated['detected_from_simulation'])
        
        if not guild_only and not dm_only:
            embed.add_field(name="🌐 Availability", value="✅ Works in DMs and Servers", inline=True)
        elif guild_only:
            embed.add_field(name="🌐 Availability", value="🏛️ Server Only", inline=True)
        elif dm_only:
            embed.add_field(name="🌐 Availability", value="📬 DM Only", inline=True)

        embed.set_footer(text="Made By TheHolyOneZ")
        await ctx.send(embed=embed)
        
        if source_codes:
            for check_name, source_code in source_codes:
                lines = source_code.split('\n')
                chunks = []
                current_chunk = []
                current_length = 0
                
                for line in lines:
                    line_length = len(line) + 1
                    if current_length + line_length > 1900:
                        chunks.append('\n'.join(current_chunk))
                        current_chunk = [line]
                        current_length = line_length
                    else:
                        current_chunk.append(line)
                        current_length += line_length
                
                if current_chunk:
                    chunks.append('\n'.join(current_chunk))
                
                for i, chunk in enumerate(chunks):
                    source_embed = discord.Embed(
                        title=f"📜 {check_name} Source Code ({i+1}/{len(chunks)})",
                        description=f"```python\n{chunk}\n```",
                        color=discord.Color.purple()
                    )
                    source_embed.set_footer(text="Made By TheHolyOneZ")
                    await ctx.send(embed=source_embed)

async def setup(bot):
    await bot.add_cog(ZWhatPerms(bot))


# README

"""
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
"""