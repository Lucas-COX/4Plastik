import type { MessageContextMenuCommandInteraction } from "discord.js";
import { ApplicationCommandType } from "discord.js";
import { ContextMenu, Discord } from "discordx";

@Discord()
export class Example {
  /**
   * Handles the "Send Data to Backend" context menu command.
   * 
   * This method is triggered when a user selects the "Send Data to Backend" option
   * from the context menu of a message. It collects information about the
   * selected message and sends it to the backend server without any visible
   * response to the user.
   * 
   * @param interaction - The interaction object containing information about
   *                      the context menu command invocation.
   * @returns A Promise that resolves when the operation is complete.
   */
  @ContextMenu({
    name: "Send Data to Backend",
    type: ApplicationCommandType.Message,
  })
  async sendDataToBackend(
    interaction: MessageContextMenuCommandInteraction
  ): Promise<void> {
    const originalMessage = interaction.targetMessage;
  
    const account = `@${originalMessage.author.username}`;
    const content = originalMessage.content;
    const social = "discord";
  
    const data = {
      account,
      content,
      social
    };
  
    try {
      console.log(JSON.stringify(data));
      const response = await fetch('YOUR_BACKEND_URL/add-message', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });
  
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
  
      console.log("Data sent successfully to the backend.");
    } catch (error) {
      console.error("Error sending data:", error);
    }
  } 
}