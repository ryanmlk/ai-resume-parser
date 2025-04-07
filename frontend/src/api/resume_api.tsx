const API_URL = import.meta.env.VITE_API_URL;

export async function parseResume(file: File): Promise<any> {
    const formData = new FormData();
    formData.append("file", file);
    
    const response = await fetch(`${API_URL}/parse`, {
      method: "POST",
      body: formData,
    });
  
    if (!response.ok) {
      throw new Error("Failed to upload resume");
    }
  
    const text = await response.json();
    return text;
  }
  