from semantic_router import Route, SemanticRouter
from semantic_router.encoders import HuggingFaceEncoder

# Initialize the encoder
encoder = HuggingFaceEncoder(
    name="sentence-transformers/all-MiniLM-L6-v2"
)

# 1. FAQ Route (Generic questions from your CSV)
faq = Route(
    name='faq',
    utterances=[
        "How do I place an order?",
        "Can I cancel my order?",
        "How do I track my delivery?",
        "What payment methods are accepted?",
        "My order is late. What should I do?",
        "I received the wrong items.",
        "Can I schedule an order for later?",
        "Is there a minimum order value?",
        "Do you offer contactless delivery?",
        "My payment failed but money was deducted.",
        "Can I order from multiple restaurants at once?",
        "Do you deliver 24/7?",
        "Can I rate my delivery driver?",
        "Can I tip the driver?",
        "My food arrived cold or damaged.",
        "Is my payment information safe?",
        "Do you charge a delivery fee?",
        "What happens if I am not home?",
        "How are refunds processed?",
        "Can I add special cooking instructions?",
        "Why was my order cancelled by the restaurant?",
        "Do you provide cutlery?",
        "Can I order food for someone else?",
        "Are menu prices different from dine-in?",
        "How do I handle food allergies?",
        "Can I get a tax invoice?",
        "Do you have a referral program?",
        "What if no drivers are available?",
        "Is there a limit on order size?",
        "Can I reorder a previous meal?"
    ],
    score_threshold=0.3
)

# 2. SQL Route (Specific to your 15 Menu Items)
sql = Route(
    name='sql',
    utterances=[
        # Direct Item Requests
        "I want to order the Vegan Delight Bowl",
        "Add Grilled Tofu Skewers to my cart",
        "One Cheesy Veggie Pizza please",
        "I'm craving a Fiery Chicken Wrap",
        "Order the Baked Falafel Plate",
        "Get me the Spicy Grilled Sandwich",
        "I want Snack Attack Veggie Chips",
        "Send me a Roasted Chicken Sandwich",
        
        # Category Searches (Bowl, Skewers, Wrap, Pizza, Snack, Salad)
        "Show me all the bowls",
        "Do you have any wraps?",
        "I want something on skewers",
        "List all the snacks available",
        "Are there any salads on the menu?",
        "I want a pizza",
        
        # Ingredient & Attribute Searches (Based on your data)
        "Show me dishes with paneer",
        "I want something with sweet potato",
        "Do you have any chicken nuggets?",
        "I want a meal with falafel",
        "Show me items with grilled tofu",
        "Do you have any curry dishes?",
        
        # Dietary & Flavor Profile (Vegan, Spicy, Roasted, Baked)
        "Show me spicy food",
        "I want a vegan option",
        "List all roasted vegetable dishes",
        "Do you have any baked items?",
        "I want a healthy low calorie option",
        
        # Price Queries (Relevant to your $5 - $12 range)
        "Show me food under $10",
        "What is the cheapest snack?",
        "List items between $8 and $12"
    ],
    score_threshold=0.3
)

# Initialize Router
router = SemanticRouter(encoder=encoder)
router.add([faq, sql]) 

# Testing
if __name__ == "__main__":
    # Test 1: Specific Dish (Should be 'sql')
    query1 = "I want that tofu skewer dish"
    print(f"Query: '{query1}' -> Route: {router(query1).name}")
    
    # Test 2: Ingredient Search (Should be 'sql')
    query2 = "Do you have anything with paneer?"
    print(f"Query: '{query2}' -> Route: {router(query2).name}")

    # Test 3: FAQ (Should be 'faq')
    query3 = "Can I pay with cash?"
    print(f"Query: '{query3}' -> Route: {router(query3).name}")