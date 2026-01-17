import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';

function ChatBot({ addToCart }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const extractFoodItems = (text) => {
    const items = [];
    
    // Regex Logic: Matches the standard SQL chain output format:
    // "1. Name, Restaurant, Description, Dietary, Price dollars"
    // Capture Groups:
    // Group 2: Name
    // Group 3: Restaurant (Ignored for now)
    // Group 4: Description
    // Group 6: Price
    const listRegex = /(\d+\.)\s*([^,]+),\s*([^,]+),\s*(.+?),\s*([^,]+),\s*(\d+\.?\d*)\s*dollars/gi;
    
    let match;
    while ((match = listRegex.exec(text)) !== null) {
      const rawName = match[2].trim();
      const rawDesc = match[4].trim();
      const price = parseFloat(match[6]);
      
      items.push({
        name: rawName,
        description: rawDesc, // We now have the description
        price: price,
        image: `/assets/${rawName}.jpg`
      });
    }
    
    // Fallback: If strict regex fails but looks like a single item response
    // Try to salvage just the name and price if possible
    if (items.length === 0 && (text.includes("$") || text.toLowerCase().includes("dollars"))) {
       // This fallback is less accurate for description, so we might skip description or try simple split
       const parts = text.split(',');
       if (parts.length >= 2) {
         const rawName = parts[0].replace(/^\d+\.\s*/, '').trim();
         const priceMatch = text.match(/(\d+\.?\d*)\s*(dollars|USD|\$)/i);
         if (priceMatch) {
            items.push({
              name: rawName,
              description: parts[2] || "Delicious food item", // Try to grab 3rd part as desc
              price: parseFloat(priceMatch[1]),
              image: `/assets/${rawName}.jpg`
            });
         }
       }
    }

    return items;
  };

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMsg = { role: 'user', content: input };
    const updatedHistory = [...messages, newMsg];
    setMessages(updatedHistory);
    setInput("");
    setIsLoading(true);

    try {
      const res = await axios.post('http://localhost:8000/chat', {
        query: input,
        history: messages 
      });

      const responseText = res.data.response;
      const detectedFoods = extractFoodItems(responseText);

      const botMsg = { 
        role: 'assistant', 
        content: responseText,
        foodItems: detectedFoods 
      };
      
      setMessages([...updatedHistory, botMsg]);

    } catch (error) {
      setMessages([...updatedHistory, { role: 'assistant', content: "⚠️ Connection Error." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="messages-area">
        {messages.map((msg, index) => (
          <div key={index} className={`message-row ${msg.role}`}>
            {msg.role === 'assistant' && <div className="avatar">🤖</div>}
            
            <div className={`message-bubble ${msg.role}`} style={{background: msg.foodItems?.length > 0 ? 'transparent' : '', padding: msg.foodItems?.length > 0 ? '0' : ''}}>
              
              {/* LOGIC: If items exist, ONLY show cards. If no items, show text. */}
              {msg.foodItems && msg.foodItems.length > 0 ? (
                <div className="chat-cards-container">
                  {msg.foodItems.map((item, idx) => (
                    <div key={idx} className="chat-food-card large">
                      <img 
                        src={item.image} 
                        onError={(e) => {e.target.src='https://via.placeholder.com/80?text=Food'}} 
                        alt={item.name}
                      />
                      <div className="chat-food-info">
                        <h4>{item.name}</h4>
                        <p className="chat-desc">{item.description}</p>
                        <span>${item.price.toFixed(2)}</span>
                      </div>
                      <button 
                        className="chat-add-btn" 
                        onClick={() => addToCart(item)}
                        title="Add to Cart"
                      >
                        +
                      </button>
                    </div>
                  ))}
                </div>
              ) : (
                // Normal Text Message
                <div>{msg.content}</div>
              )}
              
            </div>
          </div>
        ))}
        {isLoading && <div className="message-row assistant"><div className="avatar">...</div></div>}
        <div ref={messagesEndRef} />
      </div>

      <div className="input-area">
        <input 
          className="chat-input"
          value={input} 
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="I want a chicken sandwich..."
        />
        <button className="send-btn" onClick={sendMessage}>➤</button>
      </div>
    </div>
  );
}

export default ChatBot;