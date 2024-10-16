import { Discord, On } from "discordx";
import { Message } from "discord.js";

/**
 * Handles Discord message creation events.
 */
@Discord()
export class MessageCreateEvent {
  /**
   * Event handler for the 'messageCreate' event.
   * 
   * This method processes incoming messages, checking if they mention the bot
   * and are replies to other messages. If both conditions are met, it fetches
   * the replied-to message and sends its content back to the channel.
   * 
   * @param {Message[]} args - An array containing the created message.
   * @returns {Promise<void>} A promise that resolves when the operation is complete.
   */
  @On({ event: "messageCreate" })
  async handleMentions([message]: [Message]): Promise<void> {
    if (!message.mentions.has(message.client.user)) {
      return;
    }
    if (!message.reference || !message.reference.messageId) {
      return;
    }

    try {
      const repliedTo = await message.channel.messages.fetch(message.reference.messageId);
      if (repliedTo) {
        await message.reply(`The original message content is: ${repliedTo.content}`);
      } else {
        await message.reply("Unable to fetch the replied message.");
      }
    } catch (error) {
      console.error("Error fetching replied message:", error);
      await message.reply("An error occurred while trying to read the replied message.");
    }
  }
}
