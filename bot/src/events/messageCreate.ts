import { Discord, On, Client, ArgsOf, ContextMenu } from "discordx";
import { Message, MessageContextMenuCommandInteraction, ApplicationCommandType } from "discord.js";
import { sendDataToBackend } from '../services/backendService.js';

/**
 * Handles Discord message-related events and commands.
 *
 * This class centralizes the logic for processing messages, both from regular
 * chat events and context menu commands. It includes methods for handling new
 * messages and reporting messages via context menus.
 *
 * Events Handled:
 *   - messageCreate: Triggered for every new message in the server.
 *
 * Commands:
 *   - Report a message: Available in the context menu for messages.
 *
 * Methods:
 *   - handleNewMessage: Processes incoming messages.
 *   - reportMessage: Handles the "Report a message" context menu command.
 *   - processData: Internal method to prepare and send message data.
 */
@Discord()
export class MessageHandler {
  /**
   * Prepares and sends message data to the backend.
   * @param message The Discord message object to process.
   */
  private processData(message: Message): void {
    const account = `@${message.author.username}`;
    const content = message.content;
    const social = "discord";
    
    sendDataToBackend(account, content, social);
  }

  /**
   * Event handler for new messages.
   * @param message The newly created message.
   * @param client The Discord client instance.
   */
  @On({ event: "messageCreate" })
  async handleNewMessage([message]: ArgsOf<"messageCreate">, client: Client): Promise<void> {
    if (!message.author || message.author.bot) {
      console.log("Ignoring bot message or message without author");
      return;
    }
    this.processData(message);
  }

  /**
   * Command handler for the "Report a message" context menu action.
   * @param interaction The interaction object for the context menu command.
   */
  @ContextMenu({
    name: "Report a message",
    type: ApplicationCommandType.Message,
  })
  async reportMessage(interaction: MessageContextMenuCommandInteraction): Promise<void> {
    const originalMessage = interaction.targetMessage;

    if (!originalMessage.author || originalMessage.author.bot) {
      await interaction.reply({ content: "Cannot report bot messages or messages without authors.", ephemeral: true });
      return;
    }

    this.processData(originalMessage);

    await interaction.reply({ content: "Message reported successfully.", ephemeral: true });
  }
}
