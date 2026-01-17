-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: relaxdash
-- ------------------------------------------------------
-- Server version	8.0.44

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `menu_items`
--

DROP TABLE IF EXISTS `menu_items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `menu_items` (
  `id` int NOT NULL,
  `restaurant_id` int DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `category` varchar(50) DEFAULT NULL,
  `ingredients` varchar(255) DEFAULT NULL,
  `dietary_type` varchar(20) DEFAULT NULL,
  `restaurant_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `restaurant_id` (`restaurant_id`),
  CONSTRAINT `menu_items_ibfk_1` FOREIGN KEY (`restaurant_id`) REFERENCES `restaurants` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menu_items`
--

LOCK TABLES `menu_items` WRITE;
/*!40000 ALTER TABLE `menu_items` DISABLE KEYS */;
INSERT INTO `menu_items` VALUES (1,101,'Vegan Delight Bowl','A colorful mix of fresh veggies and grains.',9.99,'Bowl','Quinoa, greens, avocado','Vegan','Green Garden'),(2,101,'Grilled Tofu Skewers','Grilled tofu with bold seasoning on skewers.',11.50,'Skewers','Tofu, peppers, spices','Vegan','Green Garden'),(3,101,'Baked Falafel Plate','Baked falafel served with tahini and salad.',10.00,'Plate','Falafel, tahini, salad','Vegan','Green Garden'),(4,101,'Roasted Veggie Wrap','Roasted seasonal veggies in a whole wheat wrap.',8.50,'Wrap','Whole wheat wrap, seasonal veggies','Vegan','Green Garden'),(5,101,'Snack Attack Veggie Chips','Crispy baked vegetable chips, lightly salted.',5.00,'Snack','Veggie chips, sea salt','Vegan','Green Garden'),(6,102,'Fiery Chicken Wrap','Grilled chicken with spicy sauce and fresh veggies.',9.50,'Wrap','Chicken, hot sauce, lettuce','non-veg','Spice Hub'),(7,102,'Chili Paneer Skewers','Spicy paneer cubes grilled on skewers.',12.00,'Skewers','Paneer, chili sauce, peppers','Veg','Spice Hub'),(8,102,'Mild Curry Bowl','Comforting curry with mild spices and rice.',9.00,'Bowl','Curry sauce, rice, veggies','Veg','Spice Hub'),(9,102,'Snack Attack Chicken Nuggets','Crispy chicken nuggets with mild spices.',6.50,'Snack','Chicken, breadcrumbs, mild spice','non-veg','Spice Hub'),(10,102,'Roasted Veggie Curry','Roasted vegetables cooked in rich spices.',10.50,'Bowl','Roasted veggies, curry spices','Vegan','Spice Hub'),(11,103,'Cheesy Veggie Pizza','Loaded with cheese and fresh veggies.',11.00,'Pizza','Cheese, pizza base, veggies','Veg','Cozy Corner'),(12,103,'Spicy Grilled Sandwich','Grilled sandwich with a spicy twist.',8.00,'Sandwich','Bread, spicy mayo, cheese','Veg','Cozy Corner'),(13,103,'Grilled Chicken Salad','Salad with grilled chicken and fresh greens.',10.50,'Salad','Grilled chicken, greens, dressing','non-veg','Cozy Corner'),(14,103,'Baked Sweet Potato Fries','Crispy baked fries with a hint of sweetness.',6.00,'Snack','Sweet potato, paprika','Veg','Cozy Corner'),(15,103,'Roasted Chicken Sandwich','Freshly roasted chicken with pesto on bread.',9.50,'Sandwich','Chicken, pesto, bread','non-veg','Cozy Corner');
/*!40000 ALTER TABLE `menu_items` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `restaurants`
--

DROP TABLE IF EXISTS `restaurants`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `restaurants` (
  `id` int NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `restaurants`
--

LOCK TABLES `restaurants` WRITE;
/*!40000 ALTER TABLE `restaurants` DISABLE KEYS */;
INSERT INTO `restaurants` VALUES (101,'Green Garden','2105, Maple Street, Raleigh'),(102,'Spice Hub','1020, Oak Avenue, Durham'),(103,'Cozy Corner','3021, Pine Road, Chapel Hill');
/*!40000 ALTER TABLE `restaurants` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-01-17  3:55:33
