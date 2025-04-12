-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: cookiemania
-- ------------------------------------------------------
-- Server version	8.0.34

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `compra`
--

DROP TABLE IF EXISTS `compra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `compra` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fecha_compra` datetime NOT NULL,
  `usuario_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `compra_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `compra`
--

LOCK TABLES `compra` WRITE;
/*!40000 ALTER TABLE `compra` DISABLE KEYS */;
INSERT INTO `compra` VALUES (1,'2025-04-11 14:21:12',1),(2,'2025-04-11 14:22:12',1),(3,'2025-04-11 14:22:55',1),(4,'2025-04-11 14:24:21',1),(5,'2025-04-11 14:26:30',1),(6,'2025-04-11 14:27:33',1),(7,'2025-04-11 14:29:44',1),(8,'2025-04-11 14:30:38',1),(9,'2025-04-11 14:31:44',1),(10,'2025-04-11 14:32:40',1),(11,'2025-04-11 14:34:24',1),(12,'2025-04-11 14:35:19',1),(13,'2025-04-11 14:35:54',1),(14,'2025-04-11 14:36:33',1),(15,'2025-04-11 14:37:15',1),(16,'2025-04-11 14:37:59',1),(17,'2025-04-11 14:39:27',1),(18,'2025-04-11 14:40:51',1),(19,'2025-04-11 14:41:47',1),(20,'2025-04-11 14:42:42',1),(21,'2025-04-11 14:44:20',1),(22,'2025-04-11 14:46:01',1),(23,'2025-04-11 00:00:00',1),(24,'2025-04-11 00:00:00',1),(25,'2025-04-11 00:00:00',1),(26,'2025-04-11 00:00:00',1),(27,'2025-04-11 00:00:00',1),(28,'2025-04-11 00:00:00',1);
/*!40000 ALTER TABLE `compra` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `corteventa`
--

DROP TABLE IF EXISTS `corteventa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `corteventa` (
  `id` int NOT NULL AUTO_INCREMENT,
  `total_ventas` decimal(12,2) NOT NULL,
  `total_egresos` decimal(12,2) NOT NULL,
  `total_mermas_insumos` decimal(12,2) NOT NULL,
  `total_mermas_productos` decimal(12,2) NOT NULL,
  `total_neto` decimal(12,2) NOT NULL,
  `monto_inicial` decimal(12,2) NOT NULL,
  `total_caja` decimal(12,2) NOT NULL,
  `diferencia` decimal(12,2) NOT NULL,
  `fecha_corte` datetime NOT NULL,
  `usuario_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `usuario_id` (`usuario_id`),
  CONSTRAINT `corteventa_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `corteventa`
--

LOCK TABLES `corteventa` WRITE;
/*!40000 ALTER TABLE `corteventa` DISABLE KEYS */;
INSERT INTO `corteventa` VALUES (1,877.18,57360.00,500.00,68.41,-55914.41,500.00,500.00,56414.41,'2025-04-11 18:59:39',1);
/*!40000 ALTER TABLE `corteventa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detallereceta`
--

DROP TABLE IF EXISTS `detallereceta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detallereceta` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cantidad_insumo` decimal(10,2) NOT NULL,
  `receta_id` int NOT NULL,
  `insumo_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `receta_id` (`receta_id`),
  KEY `insumo_id` (`insumo_id`),
  CONSTRAINT `detallereceta_ibfk_1` FOREIGN KEY (`receta_id`) REFERENCES `receta` (`id`),
  CONSTRAINT `detallereceta_ibfk_2` FOREIGN KEY (`insumo_id`) REFERENCES `insumo` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=95 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detallereceta`
--

LOCK TABLES `detallereceta` WRITE;
/*!40000 ALTER TABLE `detallereceta` DISABLE KEYS */;
INSERT INTO `detallereceta` VALUES (43,1.25,1,1),(44,1.00,1,2),(45,10.00,1,3),(46,2.00,1,4),(47,0.03,1,5),(48,0.03,1,6),(49,0.03,1,7),(50,1.00,2,1),(51,0.90,2,2),(52,5.00,2,3),(53,0.03,2,7),(54,1.40,2,4),(55,0.15,2,8),(56,0.03,2,5),(57,0.03,2,6),(58,0.25,2,9),(59,0.63,3,1),(60,0.75,3,10),(61,5.00,3,3),(62,0.01,3,7),(63,0.50,3,4),(64,0.75,3,11),(65,0.02,3,12),(66,0.01,3,13),(67,0.03,3,6),(68,0.40,3,14),(69,0.50,4,1),(70,0.50,4,10),(71,5.00,4,3),(72,1.50,4,4),(73,0.03,4,15),(74,0.02,4,12),(75,0.10,4,13),(76,0.03,4,6),(83,0.75,5,1),(84,0.60,5,2),(85,5.00,5,3),(86,0.50,5,16),(87,0.01,5,5),(88,0.03,5,6),(89,1.00,5,4),(90,0.50,6,1),(91,1.00,6,17),(92,0.75,6,2),(93,5.00,6,3),(94,0.75,6,4);
/*!40000 ALTER TABLE `detallereceta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalleventa`
--

DROP TABLE IF EXISTS `detalleventa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalleventa` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cantidad_unidades` int NOT NULL,
  `cantidad_presentacion` int NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  `tipo_venta` enum('GRAMAJE','UNIDAD','PAQUETE1','PAQUETE2') NOT NULL,
  `venta_id` int NOT NULL,
  `galleta_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `venta_id` (`venta_id`),
  KEY `galleta_id` (`galleta_id`),
  CONSTRAINT `detalleventa_ibfk_1` FOREIGN KEY (`venta_id`) REFERENCES `venta` (`id`),
  CONSTRAINT `detalleventa_ibfk_2` FOREIGN KEY (`galleta_id`) REFERENCES `galleta` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalleventa`
--

LOCK TABLES `detalleventa` WRITE;
/*!40000 ALTER TABLE `detalleventa` DISABLE KEYS */;
INSERT INTO `detalleventa` VALUES (1,11,11,10.50,'UNIDAD',1,1),(2,50,1,8.92,'PAQUETE1',1,3),(3,5,5,10.13,'UNIDAD',2,2),(4,1,1,8.92,'UNIDAD',2,3),(5,1,1,7.72,'UNIDAD',2,4),(6,1,1,10.13,'UNIDAD',3,2),(7,5,5,10.50,'UNIDAD',3,1),(8,10,10,10.50,'UNIDAD',4,1),(9,10,10,10.26,'UNIDAD',5,1),(10,50,1,9.95,'PAQUETE1',5,2),(11,11,11,9.95,'UNIDAD',6,2);
/*!40000 ALTER TABLE `detalleventa` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `galleta`
--

DROP TABLE IF EXISTS `galleta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `galleta` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `peso` float NOT NULL,
  `precio` decimal(10,2) NOT NULL,
  `descripcion` varchar(255) NOT NULL,
  `estado_disponibilidad` enum('SUFICIENTE','POR_TERMINAR','BAJO_INVENTARIO') NOT NULL,
  `imagen` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `galleta`
--

LOCK TABLES `galleta` WRITE;
/*!40000 ALTER TABLE `galleta` DISABLE KEYS */;
INSERT INTO `galleta` VALUES (1,'Galleta de mantequilla',20,10.26,'Galleta de mantequilla','SUFICIENTE','mantequillla.png'),(2,'Galletas de Chocolate',20,9.95,'Galletas de Chocolate','SUFICIENTE','Chocolate.png'),(3,'Galletas de Avena y Pasas',20,8.80,'Galletas de Avena y Pasas','SUFICIENTE','Avena_y_pasas.png'),(4,'Galletas de Jengibre',20,7.61,'Galleta de jengibre','SUFICIENTE','Jenjibre.png'),(5,'Galletas de Coco ',20,9.01,'galleta de coco','SUFICIENTE','Coco.png'),(6,' Galletas de Crema de Cacahuate ',20,9.61,'Galleta de crema de cacahuate','SUFICIENTE','Crema_cacahuate.png');
/*!40000 ALTER TABLE `galleta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `insumo`
--

DROP TABLE IF EXISTS `insumo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `insumo` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `unidad_medida` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `insumo`
--

LOCK TABLES `insumo` WRITE;
/*!40000 ALTER TABLE `insumo` DISABLE KEYS */;
INSERT INTO `insumo` VALUES (1,'Matequilla','KILOGRAMOS'),(2,'Azucar granulada','KILOGRAMOS'),(3,'Huevo','UNIDADES'),(4,'Harina de trigo','KILOGRAMOS'),(5,'Polvo para hornear','KILOGRAMOS'),(6,'Sal','KILOGRAMOS'),(7,'Extracto de vainilla','LITROS'),(8,'Cacao en polvo sin azúcar','KILOGRAMOS'),(9,'Chispas de chocolate','KILOGRAMOS'),(10,'Azúcar moreno','KILOGRAMOS'),(11,'Copos de avena','KILOGRAMOS'),(12,'Canela en polvo','KILOGRAMOS'),(13,'Bicarbonato de sodio','KILOGRAMOS'),(14,'Pasas','KILOGRAMOS'),(15,'Jengibre en polvo','KILOGRAMOS'),(16,'Coco rallado','KILOGRAMOS'),(17,'Crema de cacahuate','KILOGRAMOS'),(18,'Jugo de limón','LITROS'),(19,'Ralladura de limón','KILOGRAMOS'),(20,'Almendras molidas','KILOGRAMOS'),(21,'Jugo de naranja','LITROS'),(22,'Nutella','KILOGRAMOS');
/*!40000 ALTER TABLE `insumo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `loteinsumo`
--

DROP TABLE IF EXISTS `loteinsumo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `loteinsumo` (
  `id` int NOT NULL AUTO_INCREMENT,
  `precio_unitario` decimal(10,2) NOT NULL,
  `cantidad` decimal(10,2) NOT NULL,
  `cantidad_disponible` decimal(10,2) NOT NULL,
  `fecha_caducidad` datetime DEFAULT NULL,
  `compra_id` int NOT NULL,
  `insumo_id` int NOT NULL,
  `presentacion_id` int NOT NULL,
  `proveedor_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `compra_id` (`compra_id`),
  KEY `insumo_id` (`insumo_id`),
  KEY `presentacion_id` (`presentacion_id`),
  KEY `proveedor_id` (`proveedor_id`),
  CONSTRAINT `loteinsumo_ibfk_1` FOREIGN KEY (`compra_id`) REFERENCES `compra` (`id`),
  CONSTRAINT `loteinsumo_ibfk_2` FOREIGN KEY (`insumo_id`) REFERENCES `insumo` (`id`),
  CONSTRAINT `loteinsumo_ibfk_3` FOREIGN KEY (`presentacion_id`) REFERENCES `presentacioninsumo` (`id`),
  CONSTRAINT `loteinsumo_ibfk_4` FOREIGN KEY (`proveedor_id`) REFERENCES `proveedor` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `loteinsumo`
--

LOCK TABLES `loteinsumo` WRITE;
/*!40000 ALTER TABLE `loteinsumo` DISABLE KEYS */;
INSERT INTO `loteinsumo` VALUES (1,0.00,0.00,0.00,NULL,1,1,1,1),(2,0.00,0.00,0.00,NULL,2,2,2,1),(3,0.00,0.00,0.00,NULL,3,3,3,1),(4,0.00,0.00,0.00,NULL,4,4,4,1),(5,0.00,0.00,0.00,NULL,5,5,5,1),(6,0.00,0.00,0.00,NULL,6,6,6,1),(7,0.00,0.00,0.00,NULL,7,7,7,1),(8,0.00,0.00,0.00,NULL,8,8,8,1),(9,0.00,0.00,0.00,NULL,9,9,9,1),(10,0.00,0.00,0.00,NULL,10,10,10,1),(11,0.00,0.00,0.00,NULL,11,11,11,1),(12,0.00,0.00,0.00,NULL,12,12,12,1),(13,0.00,0.00,0.00,NULL,13,13,13,1),(14,0.00,0.00,0.00,NULL,14,14,14,1),(15,0.00,0.00,0.00,NULL,15,15,15,1),(16,0.00,0.00,0.00,NULL,16,16,16,1),(17,0.00,0.00,0.00,NULL,17,17,17,1),(18,0.00,0.00,0.00,NULL,18,18,18,1),(19,0.00,0.00,0.00,NULL,19,19,19,1),(20,0.00,0.00,0.00,NULL,20,20,20,1),(21,0.00,0.00,0.00,NULL,21,21,21,1),(22,0.00,0.00,0.00,NULL,22,22,22,1),(23,270.00,20.00,15.37,'2025-06-10 00:00:00',23,1,1,1),(24,40.00,10.00,5.75,'2025-06-06 00:00:00',23,2,2,1),(25,1100.00,1.00,315.00,'2025-04-30 00:00:00',23,3,3,1),(26,350.00,4.00,90.85,'2025-06-13 00:00:00',23,4,4,1),(27,25.00,10.00,0.90,'2026-01-20 00:00:00',23,5,5,1),(28,25.00,20.00,19.82,'2025-06-30 00:00:00',23,6,6,1),(29,450.00,5.00,4.90,'2025-12-10 00:00:00',23,7,7,1),(30,80.00,30.00,29.85,'2026-05-07 00:00:00',24,8,8,1),(31,200.00,30.00,29.75,'2025-10-06 00:00:00',24,9,9,1),(32,35.00,50.00,48.75,'2026-03-20 00:00:00',24,10,10,1),(33,50.00,20.00,19.25,'2026-10-21 00:00:00',24,11,11,1),(34,150.00,25.00,24.96,'2028-11-16 00:00:00',24,12,12,1),(35,45.00,10.00,9.89,'2026-10-02 00:00:00',24,13,13,1),(36,120.00,15.00,14.60,'2027-10-31 00:00:00',24,14,14,1),(37,90.00,20.00,20.00,'2025-08-14 00:00:00',25,21,21,1),(38,150.00,25.00,24.97,'2025-08-15 00:00:00',25,15,15,1),(39,150.00,20.00,19.50,'2025-08-13 00:00:00',25,16,16,1),(40,200.00,20.00,19.00,'2025-08-25 00:00:00',25,17,17,1),(41,30.00,20.00,20.00,'2025-07-29 00:00:00',25,18,18,1),(42,160.00,20.00,20.00,'2025-06-05 00:00:00',25,19,19,1),(43,250.00,15.00,15.00,'2025-07-28 00:00:00',25,20,20,1),(44,200.00,30.00,30.00,'2025-07-20 00:00:00',25,22,22,1),(45,250.00,1.00,0.00,'2025-05-02 00:00:00',26,1,1,1),(46,250.00,10.00,7.75,'2025-05-26 00:00:00',27,1,1,1),(47,30.00,2.00,2.00,'2025-06-26 00:00:00',28,2,2,1);
/*!40000 ALTER TABLE `loteinsumo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `loteproduccion`
--

DROP TABLE IF EXISTS `loteproduccion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `loteproduccion` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fecha_produccion` datetime NOT NULL,
  `fecha_caducidad` datetime NOT NULL,
  `cantidad_disponible` int NOT NULL,
  `estado_lote` enum('SOLICITADO','MEZCLANDO','HORNEANDO','ENFRIANDO','TERMINADO','CANCELADO') NOT NULL,
  `receta_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `receta_id` (`receta_id`),
  CONSTRAINT `loteproduccion_ibfk_1` FOREIGN KEY (`receta_id`) REFERENCES `receta` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `loteproduccion`
--

LOCK TABLES `loteproduccion` WRITE;
/*!40000 ALTER TABLE `loteproduccion` DISABLE KEYS */;
INSERT INTO `loteproduccion` VALUES (1,'2025-04-11 16:30:58','2025-04-26 16:30:58',64,'TERMINADO',1),(2,'2025-04-11 16:30:58','2025-04-26 16:30:58',100,'TERMINADO',1),(3,'2025-04-11 16:33:08','2025-04-26 16:33:08',83,'TERMINADO',2),(4,'2025-04-11 16:33:15','2025-04-26 16:33:15',49,'TERMINADO',3),(5,'2025-04-11 16:33:24','2025-04-26 16:33:24',99,'TERMINADO',4),(6,'2025-04-11 18:53:03','2025-04-26 18:53:03',93,'TERMINADO',6),(7,'2025-04-11 18:55:08','2025-04-26 18:55:08',100,'TERMINADO',5);
/*!40000 ALTER TABLE `loteproduccion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mermainsumo`
--

DROP TABLE IF EXISTS `mermainsumo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mermainsumo` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cantidad_merma` decimal(10,2) NOT NULL,
  `fecha` datetime NOT NULL,
  `tipo` enum('CADUCIDAD','DESPERDICIO') NOT NULL,
  `insumo_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `insumo_id` (`insumo_id`),
  CONSTRAINT `mermainsumo_ibfk_1` FOREIGN KEY (`insumo_id`) REFERENCES `insumo` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mermainsumo`
--

LOCK TABLES `mermainsumo` WRITE;
/*!40000 ALTER TABLE `mermainsumo` DISABLE KEYS */;
INSERT INTO `mermainsumo` VALUES (1,0.00,'2025-04-11 17:50:49','DESPERDICIO',1),(2,1.00,'2025-04-11 17:51:13','DESPERDICIO',1),(3,1.00,'2025-04-11 17:51:24','DESPERDICIO',1);
/*!40000 ALTER TABLE `mermainsumo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mermaproducto`
--

DROP TABLE IF EXISTS `mermaproducto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `mermaproducto` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cantidad_merma` int NOT NULL,
  `fecha` datetime NOT NULL,
  `tipo` enum('CADUCIDAD','DESPERDICIO') NOT NULL,
  `lote_produccion_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `lote_produccion_id` (`lote_produccion_id`),
  CONSTRAINT `mermaproducto_ibfk_1` FOREIGN KEY (`lote_produccion_id`) REFERENCES `loteproduccion` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mermaproducto`
--

LOCK TABLES `mermaproducto` WRITE;
/*!40000 ALTER TABLE `mermaproducto` DISABLE KEYS */;
INSERT INTO `mermaproducto` VALUES (1,10,'2025-04-11 16:32:42','DESPERDICIO',1),(2,7,'2025-04-11 18:54:40','DESPERDICIO',6);
/*!40000 ALTER TABLE `mermaproducto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pagoproveedor`
--

DROP TABLE IF EXISTS `pagoproveedor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pagoproveedor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fecha` datetime NOT NULL,
  `monto` decimal(10,2) NOT NULL,
  `proveedor_id` int NOT NULL,
  `lote_insumo_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `proveedor_id` (`proveedor_id`),
  KEY `lote_insumo_id` (`lote_insumo_id`),
  CONSTRAINT `pagoproveedor_ibfk_1` FOREIGN KEY (`proveedor_id`) REFERENCES `proveedor` (`id`),
  CONSTRAINT `pagoproveedor_ibfk_2` FOREIGN KEY (`lote_insumo_id`) REFERENCES `loteinsumo` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=48 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pagoproveedor`
--

LOCK TABLES `pagoproveedor` WRITE;
/*!40000 ALTER TABLE `pagoproveedor` DISABLE KEYS */;
INSERT INTO `pagoproveedor` VALUES (1,'2025-04-11 14:21:12',0.00,1,1),(2,'2025-04-11 14:22:12',0.00,1,2),(3,'2025-04-11 14:22:55',0.00,1,3),(4,'2025-04-11 14:24:21',0.00,1,4),(5,'2025-04-11 14:26:30',0.00,1,5),(6,'2025-04-11 14:27:33',0.00,1,6),(7,'2025-04-11 14:29:44',0.00,1,7),(8,'2025-04-11 14:30:38',0.00,1,8),(9,'2025-04-11 14:31:44',0.00,1,9),(10,'2025-04-11 14:32:40',0.00,1,10),(11,'2025-04-11 14:34:24',0.00,1,11),(12,'2025-04-11 14:35:19',0.00,1,12),(13,'2025-04-11 14:35:54',0.00,1,13),(14,'2025-04-11 14:36:33',0.00,1,14),(15,'2025-04-11 14:37:15',0.00,1,15),(16,'2025-04-11 14:37:59',0.00,1,16),(17,'2025-04-11 14:39:27',0.00,1,17),(18,'2025-04-11 14:40:51',0.00,1,18),(19,'2025-04-11 14:41:47',0.00,1,19),(20,'2025-04-11 14:42:42',0.00,1,20),(21,'2025-04-11 14:44:20',0.00,1,21),(22,'2025-04-11 14:46:01',0.00,1,22),(23,'2025-04-11 00:00:00',5400.00,1,23),(24,'2025-04-11 00:00:00',400.00,1,24),(25,'2025-04-11 00:00:00',1100.00,1,25),(26,'2025-04-11 00:00:00',1400.00,1,26),(27,'2025-04-11 00:00:00',250.00,1,27),(28,'2025-04-11 00:00:00',500.00,1,28),(29,'2025-04-11 00:00:00',2250.00,1,29),(30,'2025-04-11 00:00:00',2400.00,1,30),(31,'2025-04-11 00:00:00',6000.00,1,31),(32,'2025-04-11 00:00:00',1750.00,1,32),(33,'2025-04-11 00:00:00',1000.00,1,33),(34,'2025-04-11 00:00:00',3750.00,1,34),(35,'2025-04-11 00:00:00',450.00,1,35),(36,'2025-04-11 00:00:00',1800.00,1,36),(37,'2025-04-11 00:00:00',1800.00,1,37),(38,'2025-04-11 00:00:00',3750.00,1,38),(39,'2025-04-11 00:00:00',3000.00,1,39),(40,'2025-04-11 00:00:00',4000.00,1,40),(41,'2025-04-11 00:00:00',600.00,1,41),(42,'2025-04-11 00:00:00',3200.00,1,42),(43,'2025-04-11 00:00:00',3750.00,1,43),(44,'2025-04-11 00:00:00',6000.00,1,44),(45,'2025-04-11 00:00:00',250.00,1,45),(46,'2025-04-11 00:00:00',2500.00,1,46),(47,'2025-04-11 00:00:00',60.00,1,47);
/*!40000 ALTER TABLE `pagoproveedor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `presentacioninsumo`
--

DROP TABLE IF EXISTS `presentacioninsumo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `presentacioninsumo` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `cantidad_base` decimal(10,5) NOT NULL,
  `unidad_base` enum('LITROS','KILOGRAMOS','UNIDADES') DEFAULT NULL,
  `insumo_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `insumo_id` (`insumo_id`),
  CONSTRAINT `presentacioninsumo_ibfk_1` FOREIGN KEY (`insumo_id`) REFERENCES `insumo` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `presentacioninsumo`
--

LOCK TABLES `presentacioninsumo` WRITE;
/*!40000 ALTER TABLE `presentacioninsumo` DISABLE KEYS */;
INSERT INTO `presentacioninsumo` VALUES (1,'Barra 1 kg mantequilla',1.00000,'KILOGRAMOS',1),(2,'Bolsa 1kg azucar granulada',1.00000,'KILOGRAMOS',2),(3,'Caja 360 unidades huevos',360.00000,'UNIDADES',3),(4,'Costal de 25 kg de harina de trigo',25.00000,'KILOGRAMOS',4),(5,'Recipiente de 100 gramos de polvo para hornear',0.10000,'KILOGRAMOS',5),(6,'Bolsa 1kg sal',1.00000,'KILOGRAMOS',6),(7,'Recipiente de 1 lt extracto de vainilla',1.00000,'LITROS',7),(8,'Bolsa 1kg de cacao en polvo sin azúcar',1.00000,'KILOGRAMOS',8),(9,'Bolsa 1kg de chispas de chocolate',1.00000,'KILOGRAMOS',9),(10,'Bolsa 1kg Azúcar moreno',1.00000,'KILOGRAMOS',10),(11,'Bolsa 1kg Copos de avena',1.00000,'KILOGRAMOS',11),(12,'Bolsa 1kg Canela en polvo',1.00000,'KILOGRAMOS',12),(13,'Bolsa 1kg Bicarbonato de sodio',1.00000,'KILOGRAMOS',13),(14,'Bolsa 1kg Pasas',1.00000,'KILOGRAMOS',14),(15,'Bolsa 1kg',1.00000,'KILOGRAMOS',15),(16,'Bolsa 1kg Coco rallado',1.00000,'KILOGRAMOS',16),(17,'Recipiente de 1kg de Crema de cacahuate',1.00000,'KILOGRAMOS',17),(18,'Recipiente de 1 L de Jugo de limón',1.00000,'LITROS',18),(19,'Bolsa 1kg de Ralladura de limón',1.00000,'KILOGRAMOS',19),(20,'Bolsa 1kg de Almendras molidas',1.00000,'KILOGRAMOS',20),(21,'Envase de 1 litro de jugo de naranja',1.00000,'LITROS',21),(22,'Recipiente de 1 kg de Nutella',1.00000,'KILOGRAMOS',22);
/*!40000 ALTER TABLE `presentacioninsumo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `produccioninsumo`
--

DROP TABLE IF EXISTS `produccioninsumo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `produccioninsumo` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cantidad_usada` decimal(10,2) NOT NULL,
  `lote_produccion_id` int NOT NULL,
  `lote_insumo_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `lote_produccion_id` (`lote_produccion_id`),
  KEY `lote_insumo_id` (`lote_insumo_id`),
  CONSTRAINT `produccioninsumo_ibfk_1` FOREIGN KEY (`lote_produccion_id`) REFERENCES `loteproduccion` (`id`),
  CONSTRAINT `produccioninsumo_ibfk_2` FOREIGN KEY (`lote_insumo_id`) REFERENCES `loteinsumo` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `produccioninsumo`
--

LOCK TABLES `produccioninsumo` WRITE;
/*!40000 ALTER TABLE `produccioninsumo` DISABLE KEYS */;
INSERT INTO `produccioninsumo` VALUES (1,1.25,1,23),(2,1.00,1,24),(3,10.00,1,25),(4,2.00,1,26),(5,0.03,1,27),(6,0.03,1,28),(7,0.03,1,29),(8,1.25,2,23),(9,1.00,2,24),(10,10.00,2,25),(11,2.00,2,26),(12,0.03,2,27),(13,0.03,2,28),(14,0.03,2,29),(15,1.00,3,23),(16,0.90,3,24),(17,5.00,3,25),(18,0.03,3,29),(19,1.40,3,26),(20,0.15,3,30),(21,0.03,3,27),(22,0.03,3,28),(23,0.25,3,31),(24,0.63,4,23),(25,0.75,4,32),(26,5.00,4,25),(27,0.01,4,29),(28,0.50,4,26),(29,0.75,4,33),(30,0.02,4,34),(31,0.01,4,35),(32,0.03,4,28),(33,0.40,4,36),(34,0.50,5,23),(35,0.50,5,32),(36,5.00,5,25),(37,1.50,5,26),(38,0.03,5,38),(39,0.02,5,34),(40,0.10,5,35),(41,0.03,5,28),(42,0.50,6,46),(43,1.00,6,40),(44,0.75,6,24),(45,5.00,6,25),(46,0.75,6,26),(47,0.75,7,46),(48,0.60,7,24),(49,5.00,7,25),(50,0.50,7,39),(51,0.01,7,27),(52,0.03,7,28),(53,1.00,7,26);
/*!40000 ALTER TABLE `produccioninsumo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `proveedor`
--

DROP TABLE IF EXISTS `proveedor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `proveedor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `numero_telefonico` varchar(20) NOT NULL,
  `correo` varchar(100) NOT NULL,
  `direccion` varchar(255) NOT NULL,
  `fecha_registro` datetime NOT NULL,
  `estado` enum('ACTIVO','INACTIVO') NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proveedor`
--

LOCK TABLES `proveedor` WRITE;
/*!40000 ALTER TABLE `proveedor` DISABLE KEYS */;
INSERT INTO `proveedor` VALUES (1,'Abarrotes Juana','4776017502','abarrotesjuana@gmail.com','Reforma #303','2025-04-11 14:19:48','ACTIVO');
/*!40000 ALTER TABLE `proveedor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `receta`
--

DROP TABLE IF EXISTS `receta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `receta` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cantidad_lote` int NOT NULL,
  `descripcion` text NOT NULL,
  `galleta_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `galleta_id` (`galleta_id`),
  CONSTRAINT `receta_ibfk_1` FOREIGN KEY (`galleta_id`) REFERENCES `galleta` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `receta`
--

LOCK TABLES `receta` WRITE;
/*!40000 ALTER TABLE `receta` DISABLE KEYS */;
INSERT INTO `receta` VALUES (1,100,'100 galletas',1),(2,100,'100 galletas',2),(3,100,'100 galletas',3),(4,100,'Receta para 100 galletas',4),(5,100,'100 galletas',5),(6,100,'Receta para 100 galletas',6);
/*!40000 ALTER TABLE `receta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(255) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL,
  `rol` varchar(50) NOT NULL,
  `estado` varchar(50) NOT NULL,
  `fecha_registro` datetime DEFAULT NULL,
  `ultimo_inicio_sesion` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (1,'Galleto','Galleto','scrypt:32768:8:1$XZGBk0n9CqHdsr6G$a356b672e0b849e7fc5f6dde318d9a1cca4c86cc4b6f64fc3c6e79ebc18fb70954c8aa7e3da8f8d857c6e1252791b2de8e7d0a1008feeb11ffe86f3fc0fb0624','maniacookie10@gmail.com','ADMIN','ACTIVO','2025-04-11 14:16:52','2025-04-11 18:29:18'),(2,'Luis','betillo','scrypt:32768:8:1$SFogEyBMLCIrQh3Q$bb0a43e626eeefabc2a17c97c879d3116634ec7ed2e43bf663ce12606774841e8ffc0d16a1b65aab9ce0ee10e9de01507c93e9da6dd032569b23dcf14642d29c','81542@alumnos.utleon.edu.mx','CLIENTE','ACTIVO','2025-04-11 17:08:55','2025-04-11 18:45:03');
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `venta`
--

DROP TABLE IF EXISTS `venta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `venta` (
  `id` int NOT NULL AUTO_INCREMENT,
  `fecha_registro` datetime NOT NULL,
  `fecha_entrega` datetime NOT NULL,
  `fecha_atencion` datetime DEFAULT NULL,
  `estado` enum('PENDIENTE','CANCELADO','LISTO','ENTREGADO') DEFAULT NULL,
  `vendedor_id` int DEFAULT NULL,
  `cliente_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `vendedor_id` (`vendedor_id`),
  KEY `cliente_id` (`cliente_id`),
  CONSTRAINT `venta_ibfk_1` FOREIGN KEY (`vendedor_id`) REFERENCES `usuario` (`id`),
  CONSTRAINT `venta_ibfk_2` FOREIGN KEY (`cliente_id`) REFERENCES `usuario` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `venta`
--

LOCK TABLES `venta` WRITE;
/*!40000 ALTER TABLE `venta` DISABLE KEYS */;
INSERT INTO `venta` VALUES (1,'2025-04-09 16:37:37','2025-04-11 16:37:37',NULL,'ENTREGADO',1,NULL),(2,'2025-04-10 16:39:29','2025-04-11 16:39:29',NULL,'ENTREGADO',1,NULL),(3,'2025-04-11 16:39:46','2025-04-11 16:39:46',NULL,'ENTREGADO',1,NULL),(4,'2025-04-11 17:10:30','2025-04-12 00:00:00','2025-04-11 19:00:23','ENTREGADO',1,2),(5,'2025-04-11 18:44:51','2025-04-16 00:00:00',NULL,'PENDIENTE',NULL,2),(6,'2025-04-11 18:58:20','2025-04-11 18:58:20',NULL,'ENTREGADO',1,NULL);
/*!40000 ALTER TABLE `venta` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-11 20:44:10
