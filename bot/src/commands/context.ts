import type {
  MessageContextMenuCommandInteraction,
  UserContextMenuCommandInteraction,
} from "discord.js";
import { ApplicationCommandType } from "discord.js";
import { ContextMenu, Discord } from "discordx";

@Discord()
export class Example {
  @ContextMenu({
    name: "message context",
    type: ApplicationCommandType.Message,
  })
  async messageHandler(
    interaction: MessageContextMenuCommandInteraction
  ): Promise<void> {
    await interaction.reply("I am message context handler");
  }

  @ContextMenu({
    name: "user context",
    type: ApplicationCommandType.User,
  })
  async userHandler(
    interaction: UserContextMenuCommandInteraction
  ): Promise<void> {
    await interaction.reply("I am user context handler");
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
  @ContextMenu({
    name: "Echo Message",
    type: ApplicationCommandType.Message,
  })
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
