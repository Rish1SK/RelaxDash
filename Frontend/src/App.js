/* src/App.js */
import React, { useState } from 'react';
import './App.css';
import Sidebar from './pages/Sidebar';
import ChatBot from './pages/ChatBot';
import Browse from './pages/Browse';
import Checkout from './pages/Checkout';

function App() {
  const [currentView, setCurrentView] = useState('chat');
  const [cart, setCart] = useState([]);

  // --- CART ACTIONS ---
  const addToCart = (item) => {
    // Check if item already exists to avoid duplicates (optional logic)
    // For now, we allow multiples
    setCart([...cart, item]);
  };

  const removeFromCart = (indexToRemove) => {
    setCart(cart.filter((_, index) => index !== indexToRemove));
  };

  const clearCart = () => {
    setCart([]);
  };

  return (
    <div className="app-container">
      {/* Sidebar gets cart data to display it */}
      <Sidebar 
        currentView={currentView} 
        onNavigate={setCurrentView} 
        cart={cart}
        removeFromCart={removeFromCart}
        onCheckout={() => setCurrentView('checkout')}
      />

      <div className="main-content">
        {currentView === 'chat' && (
          <ChatBot addToCart={addToCart} />
        )}
        
        {currentView === 'browse' && (
          <Browse addToCart={addToCart} />
        )}

        {currentView === 'checkout' && (
          <Checkout 
            cart={cart} 
            clearCart={clearCart} 
            removeFromCart={removeFromCart}
          />
        )}
      </div>
    </div>
  );
}

export default App;