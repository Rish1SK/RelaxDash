/* src/pages/Checkout.js */
import React, { useState } from 'react';

function Checkout({ cart, clearCart, removeFromCart }) {
  const [isFinished, setIsFinished] = useState(false);
  const [paymentMethod, setPaymentMethod] = useState('card'); // Default to card
  
  const total = cart.reduce((sum, item) => sum + item.price, 0).toFixed(2);

  const handlePayment = (e) => {
    e.preventDefault();
    setIsFinished(true);
    setTimeout(() => {
      clearCart(); 
    }, 1000);
  };

  if (isFinished) {
    return (
      <div className="checkout-success">
        <div className="success-card">
          <h1>🎉 Order Placed!</h1>
          <p>Your delicious food is on the way.</p>
          <p>Total Paid: <strong>${total}</strong></p>
        </div>
      </div>
    );
  }

  return (
    <div className="checkout-container">
      <h2 className="page-title">Checkout</h2>
      
      <div className="checkout-layout">
        {/* LEFT: ORDER SUMMARY */}
        <div className="order-summary">
          <h3>Order Summary</h3>
          {cart.length === 0 ? <p>Your cart is empty.</p> : (
            <div className="summary-list">
              {cart.map((item, idx) => (
                <div key={idx} className="summary-item">
                  <img 
                    src={`/assets/${item.name}.jpg`} 
                    alt={item.name} 
                    onError={(e) => {e.target.style.display='none'}}
                  />
                  <div className="info">
                    <h4>{item.name}</h4>
                    <p>${item.price}</p>
                  </div>
                  {/* Added specific class for styling */}
                  <button className="checkout-remove-btn" onClick={() => removeFromCart(idx)}>
                    Remove
                  </button>
                </div>
              ))}
            </div>
          )}
          <div className="summary-total">
            <span>Total to Pay:</span>
            <span>${total}</span>
          </div>
        </div>

        {/* RIGHT: PAYMENT FORM */}
        <div className="payment-form">
          <h3>Payment Details</h3>
          <form onSubmit={handlePayment}>
            <label>Payment Method</label>
            <select 
              required 
              value={paymentMethod}
              onChange={(e) => setPaymentMethod(e.target.value)}
            >
              <option value="card">Credit / Debit Card</option>
              <option value="wallet">Digital Wallet (GPay, Apple Pay)</option>
              <option value="netbanking">Net Banking</option>
              <option value="cod">Cash on Delivery</option>
            </select>

            {/* CONDITIONAL RENDERING: Only show Card Number for Card payments */}
            {paymentMethod === 'card' && (
              <div className="card-input-section">
                <label>Card Number</label>
                <input 
                  type="text" 
                  placeholder="0000 0000 0000 0000" 
                  maxLength="19"
                  required
                />
                <div style={{display:'flex', gap:'10px', marginTop:'10px'}}>
                   <input type="text" placeholder="MM/YY" style={{width:'50%'}} required/>
                   <input type="text" placeholder="CVC" style={{width:'50%'}} required/>
                </div>
              </div>
            )}

            <button type="submit" className="pay-btn" disabled={cart.length === 0}>
              {paymentMethod === 'cod' ? 'Place Order' : `Pay $${total}`}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default Checkout;