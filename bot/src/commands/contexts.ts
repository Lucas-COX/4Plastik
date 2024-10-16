import type { MessageContextMenuCommandInteraction } from "discord.js";
import { ApplicationCommandType } from "discord.js";
import { ContextMenu, Discord } from "discordx";

@Discord()
export class Example {
  /**
   * Handles the "Send DM to Author" context menu command.
   * 
   * Sends a DM to the author of the selected message.
   * 
   * @param interaction - The interaction object containing information about
   *                      the context menu command invocation.
   * @returns A Promise that resolves when the operation is complete.
   */
  @ContextMenu({
    name: "Send DM to Author",
    type: ApplicationCommandType.Message,
  })
  async sendDMToAuthor(
    interaction: MessageContextMenuCommandInteraction
  ): Promise<void> {
    const author = interaction.targetMessage.author;
    const successMessage = "DM sent successfully to the author.";

    try {
      await author.send("zbi tkt ça va bien se passer");
      console.log(successMessage)
      await interaction.reply({
        content: successMessage,
        ephemeral: true,
      });
    } catch (error) {
      console.error("Error sending DM:", error);
      await interaction.reply({
        content: "Failed to send DM. The user might have DMs disabled.",
        ephemeral: true,
      });
    }
  }

  /**
   * Handles the "Echo Message" context menu command.
   * 
   * Retrieves the content of the selected message and sends it back as an ephemeral reply.
   * 
   * @param interaction - The interaction object containing information about
   *                      the context menu command invocation.
   * @returns A Promise that resolves when the operation is complete.
   */
  @ContextMenu({ name: "Echo Message", type: ApplicationCommandType.Message })
  async echoMessage(
    interaction: MessageContextMenuCommandInteraction
  ): Promise<void> {
    const originalMessage = interaction.targetMessage;

    if (originalMessage.content) {
      await interaction.reply({
        content: `Original message: ${originalMessage.content}`,
        ephemeral: true,
      });
    } else {
      await interaction.reply({
        content: "The original message doesn't contain any text.",
        ephemeral: true,
      });
    }
  }
}