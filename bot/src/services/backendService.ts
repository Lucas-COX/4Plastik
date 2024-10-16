/**
 * Sends a message to the backend server.
 *
 * Constructs a JSON object from the provided account, content, and social parameters,
 * and sends it via a POST request to the backend endpoint. Logs success or error messages
 * based on the response.
 *
 * @param {string} account - The account identifier for the message.
 * @param {string} content - The content of the message.
 * @param {string} social - The associated social platform.
 * 
 * @returns {Promise<void>} Resolves when data is sent successfully, rejects on error.
 *
 * @throws {Error} If the server response is not OK or if the fetch operation fails.
 *
 * @example
 * sendDataToBackend('user123', 'Hello, World!', 'Discord');
 */

export async function sendDataToBackend(account: string, content: string, social: string): Promise<void> {
  const data = {
    account,
    content,
    social,
  };

  try {
    const response = await fetch(`${process.env.API_URL}/add-message`, {
      mode: 'no-cors',
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${process.env["API_KEY"]}`,
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
  
