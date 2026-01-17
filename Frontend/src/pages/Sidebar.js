import React from 'react';

function Sidebar({ currentView, onNavigate, cart, removeFromCart, onCheckout }) {
  // Calculate total
  const total = cart.reduce((sum, item) => sum + item.price, 0).toFixed(2);

  return (
    <div className="sidebar">
      <div className="logo">🍔 Relaxdash</div>
      
      {/* NAVIGATION */}
      <div className="nav-section">
        <button 
          className={`nav-btn ${currentView === 'chat' ? 'active' : ''}`} 
          onClick={() => onNavigate('chat')}
        >
          🤖 AI Assistant
        </button>
        <button 
          className={`nav-btn ${currentView === 'browse' ? 'active' : ''}`} 
          onClick={() => onNavigate('browse')}
        >
          🍽️ Browse Menu
        </button>
      </div>

      {/* SHOPPING CART AREA */}
      <div className="cart-section">
        <h3>Your Cart ({cart.length})</h3>
        <div className="cart-items">
          {cart.length === 0 ? (
            <p className="empty-cart-msg">Cart is empty</p>
          ) : (
            cart.map((item, idx) => (
              <div key={idx} className="cart-item">
                <img 
                  src={`/assets/${item.name}.jpg`} 
                  alt={item.name}
                  onError={(e) => {e.target.style.display='none'}} // Hide if missing
                />
                <div className="cart-info">
                  <div className="cart-name">{item.name}</div>
                  <div className="cart-price">${item.price}</div>
                </div>
                <button className="remove-btn" onClick={() => removeFromCart(idx)}>×</button>
              </div>
            ))
          )}
        </div>
        
        {cart.length > 0 && (
          <div className="cart-footer">
            <div className="total">Total: ${total}</div>
            <button className="checkout-btn" onClick={onCheckout}>
              Proceed to Checkout
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default Sidebar;