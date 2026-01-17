import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Browse({ addToCart }) {
  const [restaurants, setRestaurants] = useState([]);
  const [selectedRestaurant, setSelectedRestaurant] = useState(null);
  const [menu, setMenu] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:8000/restaurants')
      .then(res => setRestaurants(res.data))
      .catch(err => console.error("Error fetching restaurants:", err));
  }, []);

  const loadMenu = async (restaurant) => {
    setSelectedRestaurant(restaurant);
    try {
      const res = await axios.get(`http://localhost:8000/restaurants/${restaurant.id}/menu`);
      setMenu(res.data);
    } catch (error) {
      console.error("Error loading menu:", error);
    }
  };

  return (
    <div className="browse-container">
      
      {/* 1. RESTAURANT GRID */}
      {!selectedRestaurant && (
        <>
          <h2 className="page-title">Select a Restaurant</h2>
          <div className="restaurant-grid">
            {restaurants.map(rest => (
              <div key={rest.id} className="card restaurant-card" onClick={() => loadMenu(rest)}>
                {/* Image of Restaurant */}
                <img 
                  src={`/assets/${rest.name}.jpg`} 
                  alt={rest.name} 
                  className="card-img"
                  onError={(e) => {e.target.src='https://via.placeholder.com/300x150?text=No+Image'}}
                />
                <div className="card-content">
                  <h3>{rest.name}</h3>
                  <p>📍 {rest.address}</p>
                </div>
              </div>
            ))}
          </div>
        </>
      )}

      {/* 2. MENU LIST */}
      {selectedRestaurant && (
        <div className="menu-view">
          <button className="back-btn" onClick={() => setSelectedRestaurant(null)}>
            ← Back to Restaurants
          </button>
          
          <div className="menu-header">
            <img 
              src={`/assets/${selectedRestaurant.name}.jpg`} 
              alt={selectedRestaurant.name}
              className="header-img"
              onError={(e) => {e.target.style.display='none'}}
            />
            <h2>{selectedRestaurant.name} Menu</h2>
          </div>

          <div className="menu-grid">
            {menu.map((item, idx) => (
              <div key={idx} className="menu-card">
                <img 
                  src={`/assets/${item.name}.jpg`} 
                  alt={item.name} 
                  className="menu-img"
                  onError={(e) => {e.target.src='https://via.placeholder.com/150?text=Food'}}
                />
                <div className="menu-info">
                  <div className="menu-top">
                    <h3>{item.name}</h3>
                    <span className={`badge ${item.dietary_type.toLowerCase()}`}>
                      {item.dietary_type}
                    </span>
                  </div>
                  <p className="desc">{item.description}</p>
                  <div className="menu-footer">
                    <span className="price">${item.price}</span>
                    <button className="add-btn" onClick={() => addToCart(item)}>
                      + Add
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default Browse;