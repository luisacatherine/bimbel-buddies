-- MySQL dump 10.13  Distrib 5.7.25, for Linux (x86_64)
--
-- Host: localhost    Database: dbbimbel
-- ------------------------------------------------------
-- Server version	5.7.25-0ubuntu0.18.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `blocked`
--

DROP TABLE IF EXISTS `blocked`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `blocked` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `client_id` int(11) DEFAULT NULL,
  `blocked_tentor` varchar(100) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blocked`
--

LOCK TABLES `blocked` WRITE;
/*!40000 ALTER TABLE `blocked` DISABLE KEYS */;
/*!40000 ALTER TABLE `blocked` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `booking`
--

DROP TABLE IF EXISTS `booking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `booking` (
  `id_booking` int(11) NOT NULL AUTO_INCREMENT,
  `id_murid` int(11) NOT NULL,
  `id_tentor` int(11) DEFAULT NULL,
  `jenis` varchar(10) NOT NULL,
  `tanggal` datetime DEFAULT NULL,
  `mapel` varchar(50) DEFAULT NULL,
  `harga_booking` int(11) DEFAULT NULL,
  `harga_bensin` int(11) DEFAULT NULL,
  `saldo_tentor` int(11) DEFAULT NULL,
  `saldo_admin` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `jarak` float DEFAULT NULL,
  `status` varchar(12) NOT NULL,
  `jumlah_murid` int(11) NOT NULL,
  PRIMARY KEY (`id_booking`),
  UNIQUE KEY `id_booking` (`id_booking`),
  KEY `ix_booking_updated_at` (`updated_at`),
  KEY `ix_booking_created_at` (`created_at`)
) ENGINE=InnoDB AUTO_INCREMENT=78 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `booking`
--

LOCK TABLES `booking` WRITE;
/*!40000 ALTER TABLE `booking` DISABLE KEYS */;
INSERT INTO `booking` VALUES (1,11,1,'insidentil','2019-04-04 05:01:00','fis',40000,0,0,0,'2019-04-01 15:32:02','2019-04-01 15:32:02',0,'done',1),(2,11,3,'insidentil','2019-04-04 05:01:00','fis',40000,5068,37068,8000,'2019-04-01 20:07:27','2019-04-01 20:07:27',0,'done',1),(11,11,3,'insidentil','2019-04-05 18:00:00','fis',40000,0,0,0,'2019-04-02 21:34:52','2019-04-02 21:34:52',0,'done',1),(12,11,0,'insidentil','2019-04-05 16:00:00','fis',40000,0,0,0,'2019-04-02 21:35:19','2019-04-06 15:32:45',0,'expired',1),(13,11,0,'insidentil','2019-04-05 16:00:00','fis',40000,0,0,0,'2019-04-02 21:35:52','2019-04-06 15:32:45',0,'expired',1),(14,11,3,'insidentil','2019-04-06 14:00:00','fis',0,0,37068,-37068,'2019-04-02 21:37:28','2019-04-02 21:37:28',0,'cancelled',1),(15,11,3,'insidentil','2019-04-05 16:00:00','fis',40000,0,0,0,'2019-04-03 10:10:26','2019-04-06 15:32:45',0,'expired',1),(16,11,3,'insidentil','2019-04-06 14:00:00','fis',0,0,-20000,65068,'2019-04-03 10:12:10','2019-04-03 10:12:10',0,'cancelled',1),(22,11,3,'insidentil','2019-04-04 14:00:00','mat',0,0,17068,78136,'2019-04-03 11:44:33','2019-04-03 11:44:33',0,'cancelled',1),(32,11,0,'insidentil','2019-04-06 14:00:00','kim',40000,10136,0,95204,'2019-04-04 00:45:37','2019-04-06 15:32:45',0,'expired',1),(33,11,3,'insidentil','2019-04-06 14:00:00','fis',0,0,-20000,65068,'2019-04-04 00:46:13','2019-04-04 00:46:13',0,'cancelled',1),(34,11,3,'insidentil','2019-04-05 14:00:00','fis',40000,5068,0,45068,'2019-04-04 00:56:24','2019-04-06 15:32:45',0,'expired',1),(35,11,3,'insidentil','2019-04-05 16:00:00','fis',40000,0,0,0,'2019-04-04 00:57:18','2019-04-06 15:32:45',0,'expired',1),(36,11,3,'insidentil','2019-04-05 16:00:00','fis',40000,0,0,0,'2019-04-04 00:58:25','2019-04-06 15:32:45',0,'expired',1),(37,11,3,'insidentil','2019-04-08 16:00:00','fis',0,0,0,0,'2019-04-04 10:42:06','2019-04-04 10:42:06',0,'cancelled',1),(38,11,0,'insidentil','2019-04-07 16:00:00','fis',40000,0,0,0,'2019-04-04 15:42:20','2019-04-07 11:05:57',0,'expired',1),(39,11,0,'insidentil','2019-04-05 14:00:00','fis',40000,0,0,0,'2019-04-04 15:43:50','2019-04-06 15:32:45',0,'expired',1),(40,11,0,'insidentil','2019-04-05 14:00:00','fis',40000,5068,0,45068,'2019-04-04 15:44:23','2019-04-06 15:32:45',0,'expired',1),(41,11,3,'insidentil','2019-04-08 16:00:00','fis',40000,5068,0,45068,'2019-04-04 15:44:42','2019-04-04 15:44:42',0,'accepted',1),(42,11,0,'insidentil','2019-04-09 12:00:00','fis',40000,0,0,0,'2019-04-04 15:47:19','2019-04-04 15:47:19',0,'waiting',1),(43,11,0,'insidentil','2019-04-05 05:01:00','fis',40000,0,0,0,'2019-04-04 18:11:18','2019-04-06 15:32:45',0,'expired',1),(44,11,0,'insidentil','2019-04-07 14:00:00','fis',40000,0,0,0,'2019-04-06 16:01:59','2019-04-07 11:05:57',0,'expired',1),(45,11,0,'insidentil','2019-04-08 14:00:00','fis',40000,0,0,0,'2019-04-06 16:05:10','2019-04-06 16:05:10',0,'waiting',1),(46,11,3,'insidentil','2019-04-09 12:00:00','fis',0,0,0,0,'2019-04-06 16:07:58','2019-04-06 16:09:06',0,'cancelled',1),(47,11,0,'insidentil','2019-04-09 14:00:00','fis',40000,0,0,0,'2019-04-06 16:09:41','2019-04-06 16:09:41',0,'waiting',1),(48,11,0,'insidentil','2019-04-09 16:00:00','fis',40000,0,0,0,'2019-04-06 16:10:00','2019-04-06 16:10:00',0,'waiting',1),(49,11,0,'insidentil','2019-04-10 12:00:00','fis',40000,0,0,0,'2019-04-06 17:07:53','2019-04-06 17:07:53',0,'waiting',1),(50,11,0,'rutin','2019-04-12 12:00:00','fis',40000,0,0,0,'2019-04-06 17:10:20','2019-04-06 17:10:20',0,'waiting',1),(51,11,0,'rutin','2019-04-19 12:00:00','fis',40000,0,0,0,'2019-04-06 17:10:20','2019-04-06 17:10:20',0,'waiting',1),(52,11,0,'rutin','2019-04-26 12:00:00','fis',40000,0,0,0,'2019-04-06 17:10:20','2019-04-06 17:10:20',0,'waiting',1),(53,11,0,'rutin','2019-05-03 12:00:00','fis',40000,0,0,0,'2019-04-06 17:10:20','2019-04-06 17:10:20',0,'waiting',1),(66,11,0,'rutin','2019-04-13 18:00:00','mat',160000,0,0,0,'2019-04-06 17:30:56','2019-04-06 17:30:56',0,'waiting',4),(67,11,0,'rutin','2019-04-20 18:00:00','mat',160000,0,0,0,'2019-04-06 17:30:56','2019-04-06 17:30:56',0,'waiting',4),(68,11,0,'rutin','2019-04-27 18:00:00','mat',160000,0,0,0,'2019-04-06 17:30:56','2019-04-06 17:30:56',0,'waiting',4),(69,11,0,'rutin','2019-05-04 18:00:00','mat',160000,0,0,0,'2019-04-06 17:30:56','2019-04-06 17:30:56',0,'waiting',4),(70,11,0,'rutin','2019-04-13 18:00:00','mat',136000,0,0,0,'2019-04-06 17:44:19','2019-04-06 17:44:19',0,'waiting',4),(71,11,0,'rutin','2019-04-20 18:00:00','mat',136000,0,0,0,'2019-04-06 17:44:19','2019-04-06 17:44:19',0,'waiting',4),(72,11,0,'rutin','2019-04-27 18:00:00','mat',136000,0,0,0,'2019-04-06 17:44:19','2019-04-06 17:44:19',0,'waiting',4),(73,11,0,'rutin','2019-05-04 18:00:00','mat',136000,0,0,0,'2019-04-06 17:44:19','2019-04-06 17:44:19',0,'waiting',4),(74,11,0,'rutin','2019-04-13 16:00:00','mat',76000,0,0,0,'2019-04-06 17:47:51','2019-04-06 17:47:51',0,'waiting',2),(75,11,0,'rutin','2019-04-20 16:00:00','mat',76000,0,0,0,'2019-04-06 17:47:51','2019-04-06 17:47:51',0,'waiting',2),(76,11,0,'rutin','2019-04-27 16:00:00','mat',76000,0,0,0,'2019-04-06 17:47:51','2019-04-06 17:47:51',0,'waiting',2),(77,11,0,'rutin','2019-05-04 16:00:00','mat',76000,0,0,0,'2019-04-06 17:47:51','2019-04-06 17:47:51',0,'waiting',2);
/*!40000 ALTER TABLE `booking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clients`
--

DROP TABLE IF EXISTS `clients`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `clients` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `nama` varchar(100) DEFAULT NULL,
  `address` text,
  `phone` varchar(30) DEFAULT NULL,
  `image` text,
  `tgl_lahir` datetime DEFAULT NULL,
  `gender` varchar(20) DEFAULT NULL,
  `tingkat` varchar(20) DEFAULT NULL,
  `gender_tentor` varchar(20) DEFAULT NULL,
  `ortu` varchar(100) DEFAULT NULL,
  `saldo` int(11) DEFAULT NULL,
  `lat` float DEFAULT NULL,
  `lon` float DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `ix_clients_updated_at` (`updated_at`),
  KEY `ix_clients_created_at` (`created_at`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clients`
--

LOCK TABLES `clients` WRITE;
/*!40000 ALTER TABLE `clients` DISABLE KEYS */;
INSERT INTO `clients` VALUES (11,11,'Aswin','Jalan Tidar Karang Besuki Kota Malang','085329465870','https://firebasestorage.googleapis.com/v0/b/bismillah-68cc8.appspot.com/o/4a8f9c99-3453-4e5d-a85b-f14824feb184?alt=media&token=a21c319b-22b2-41c8-bb38-3d333af18d3b','2019-03-05 00:00:00','Male','SD','Male','Kaka',21859184,-7.9662,112.608,'2019-03-31 19:57:39','2019-03-31 19:57:39'),(12,12,'Aswin','Jalan Tidar Karang Besuki Kota Malang','02039438129','okok','2011-02-02 00:00:00','Male','SD','Male','Kaka',0,-7.9662,112.608,'2019-03-31 20:01:54','2019-03-31 20:01:54'),(13,14,'Test','Jalan Tidar Karang Besuki Kota Malang','085449596765','Tes','2019-04-16 00:00:00','Male','SMP','Male','Ortu',0,-7.9662,112.608,'2019-04-01 16:06:36','2019-04-01 16:06:36'),(14,16,'Aswin','Jl. Tidar Malang','02039438129','okok','2011-02-02 00:00:00','Male','SD','Male','Kaka',0,-7.96624,112.61,'2019-04-01 18:42:31','2019-04-01 18:42:31');
/*!40000 ALTER TABLE `clients` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `harga`
--

DROP TABLE IF EXISTS `harga`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `harga` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tingkat` varchar(5) NOT NULL,
  `harga` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `ix_harga_updated_at` (`updated_at`),
  KEY `ix_harga_created_at` (`created_at`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `harga`
--

LOCK TABLES `harga` WRITE;
/*!40000 ALTER TABLE `harga` DISABLE KEYS */;
INSERT INTO `harga` VALUES (1,'SD',40000,'2019-04-01 15:28:51','2019-04-05 15:20:51'),(2,'SMP',50000,'2019-04-01 15:28:58','2019-04-01 15:28:58'),(3,'SMA',60000,'2019-04-01 15:29:04','2019-04-01 15:29:04');
/*!40000 ALTER TABLE `harga` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `jadwalclient`
--

DROP TABLE IF EXISTS `jadwalclient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jadwalclient` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `client_id` int(11) DEFAULT NULL,
  `tentor_id` int(11) DEFAULT NULL,
  `booking_id` int(11) DEFAULT NULL,
  `schedule_start` datetime DEFAULT NULL,
  `schedule_end` datetime DEFAULT NULL,
  `status` varchar(30) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `booking_id` (`booking_id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jadwalclient`
--

LOCK TABLES `jadwalclient` WRITE;
/*!40000 ALTER TABLE `jadwalclient` DISABLE KEYS */;
INSERT INTO `jadwalclient` VALUES (1,11,0,44,'2019-04-07 14:00:00','2019-04-07 15:30:00','waiting','2019-04-06 16:01:59','2019-04-06 16:01:59'),(2,11,0,45,'2019-04-08 14:00:00','2019-04-08 15:30:00','waiting','2019-04-06 16:05:10','2019-04-06 16:05:10'),(3,11,0,46,'2019-04-09 12:00:00','2019-04-09 13:30:00','waiting','2019-04-06 16:07:58','2019-04-06 16:07:58'),(4,11,0,47,'2019-04-09 14:00:00','2019-04-09 15:30:00','waiting','2019-04-06 16:09:41','2019-04-06 16:09:41'),(5,11,0,48,'2019-04-09 16:00:00','2019-04-09 17:30:00','waiting','2019-04-06 16:10:00','2019-04-06 16:10:00'),(6,11,0,49,'2019-04-10 12:00:00','2019-04-10 13:30:00','waiting','2019-04-06 17:07:53','2019-04-06 17:07:53'),(7,11,0,50,'2019-04-12 12:00:00','2019-04-12 13:30:00','waiting','2019-04-06 17:10:20','2019-04-06 17:10:20'),(8,11,0,51,'2019-04-19 12:00:00','2019-04-19 13:30:00','waiting','2019-04-06 17:10:20','2019-04-06 17:10:20'),(9,11,0,52,'2019-04-26 12:00:00','2019-04-26 13:30:00','waiting','2019-04-06 17:10:20','2019-04-06 17:10:20'),(10,11,0,53,'2019-05-03 12:00:00','2019-05-03 13:30:00','waiting','2019-04-06 17:10:20','2019-04-06 17:10:20'),(11,11,0,54,'2019-04-13 12:00:00','2019-04-13 13:30:00','waiting','2019-04-06 17:10:47','2019-04-06 17:10:47'),(12,11,0,55,'2019-04-20 12:00:00','2019-04-20 13:30:00','waiting','2019-04-06 17:10:47','2019-04-06 17:10:47'),(13,11,0,56,'2019-04-27 12:00:00','2019-04-27 13:30:00','waiting','2019-04-06 17:10:47','2019-04-06 17:10:47'),(14,11,0,57,'2019-05-04 12:00:00','2019-05-04 13:30:00','waiting','2019-04-06 17:10:47','2019-04-06 17:10:47'),(27,11,0,70,'2019-04-13 18:00:00','2019-04-13 19:30:00','waiting','2019-04-06 17:44:19','2019-04-06 17:44:19'),(28,11,0,71,'2019-04-20 18:00:00','2019-04-20 19:30:00','waiting','2019-04-06 17:44:19','2019-04-06 17:44:19'),(29,11,0,72,'2019-04-27 18:00:00','2019-04-27 19:30:00','waiting','2019-04-06 17:44:19','2019-04-06 17:44:19'),(30,11,0,73,'2019-05-04 18:00:00','2019-05-04 19:30:00','waiting','2019-04-06 17:44:19','2019-04-06 17:44:19'),(31,11,0,74,'2019-04-13 16:00:00','2019-04-13 17:30:00','waiting','2019-04-06 17:47:51','2019-04-06 17:47:51'),(32,11,0,75,'2019-04-20 16:00:00','2019-04-20 17:30:00','waiting','2019-04-06 17:47:51','2019-04-06 17:47:51'),(33,11,0,76,'2019-04-27 16:00:00','2019-04-27 17:30:00','waiting','2019-04-06 17:47:51','2019-04-06 17:47:51'),(34,11,0,77,'2019-05-04 16:00:00','2019-05-04 17:30:00','waiting','2019-04-06 17:47:51','2019-04-06 17:47:51');
/*!40000 ALTER TABLE `jadwalclient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `jadwaltentor`
--

DROP TABLE IF EXISTS `jadwaltentor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `jadwaltentor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `client_id` int(11) DEFAULT NULL,
  `tentor_id` int(11) DEFAULT NULL,
  `booking_id` int(11) DEFAULT NULL,
  `schedule_start` datetime DEFAULT NULL,
  `schedule_end` datetime DEFAULT NULL,
  `status` varchar(30) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `booking_id` (`booking_id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `jadwaltentor`
--

LOCK TABLES `jadwaltentor` WRITE;
/*!40000 ALTER TABLE `jadwaltentor` DISABLE KEYS */;
INSERT INTO `jadwaltentor` VALUES (11,11,3,32,'2019-04-06 14:00:00','2019-04-06 15:30:00','waiting','2019-04-04 10:08:17','2019-04-04 10:08:17'),(13,11,3,34,'2019-04-05 14:00:00','2019-04-05 15:30:00','waiting','2019-04-04 10:08:23','2019-04-04 10:08:23');
/*!40000 ALTER TABLE `jadwaltentor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments`
--

DROP TABLE IF EXISTS `payments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `payments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_booking` int(11) DEFAULT NULL,
  `nominal` int(11) DEFAULT NULL,
  `total_nominal` int(11) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `ix_payments_updated_at` (`updated_at`),
  KEY `ix_payments_created_at` (`created_at`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments`
--

LOCK TABLES `payments` WRITE;
/*!40000 ALTER TABLE `payments` DISABLE KEYS */;
/*!40000 ALTER TABLE `payments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reviews` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_murid` int(11) DEFAULT NULL,
  `id_tentor` int(11) DEFAULT NULL,
  `id_booking` int(11) DEFAULT NULL,
  `rating` int(11) DEFAULT NULL,
  `deskripsi` text,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `id_booking` (`id_booking`),
  KEY `ix_reviews_created_at` (`created_at`),
  KEY `ix_reviews_updated_at` (`updated_at`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews`
--

LOCK TABLES `reviews` WRITE;
/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
INSERT INTO `reviews` VALUES (3,11,1,1,5,'Hebat','2019-04-01 16:05:13','2019-04-01 16:05:13');
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tentors`
--

DROP TABLE IF EXISTS `tentors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tentors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `nama` varchar(100) DEFAULT NULL,
  `address` text,
  `ktp` varchar(16) DEFAULT NULL,
  `phone` varchar(30) DEFAULT NULL,
  `image` text,
  `tgl_lahir` datetime DEFAULT NULL,
  `gender` varchar(20) DEFAULT NULL,
  `fokus` varchar(20) DEFAULT NULL,
  `tingkat` varchar(20) DEFAULT NULL,
  `pendidikan` varchar(20) DEFAULT NULL,
  `rekening` varchar(30) DEFAULT NULL,
  `pemilik_nasabah` varchar(100) DEFAULT NULL,
  `saldo` int(11) DEFAULT NULL,
  `rating` float DEFAULT NULL,
  `qty_rating` int(11) DEFAULT NULL,
  `lat` float DEFAULT NULL,
  `lon` float DEFAULT NULL,
  `status` varchar(30) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `ket` varchar(400) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `ix_tentors_created_at` (`created_at`),
  KEY `ix_tentors_updated_at` (`updated_at`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tentors`
--

LOCK TABLES `tentors` WRITE;
/*!40000 ALTER TABLE `tentors` DISABLE KEYS */;
INSERT INTO `tentors` VALUES (1,13,'Aswin','Jalan Tidar Karang Besuki Kota Malang','162537485967485','082947392748','Kaka','2019-03-07 00:00:00','Female','Matematika','SMP','S1','6183629','Aswin',0,4.33333,3,-7.9662,112.608,'active','2019-03-31 20:32:39','2019-03-31 20:32:39',NULL),(2,17,'Aswin','Jl. Tidar Malang','123457685930029','02039438129','okok','2011-02-02 00:00:00','Male','fis','SMP','S2','112833729','Aswin',0,3,6,-7.96624,112.61,'active','2019-04-01 20:07:14','2019-04-01 20:07:14',NULL),(3,18,'Aswin','Jl. Sawojajar Malang','123457685930029','02039438129','okok','2011-02-02 00:00:00','Male','fis','SMP','S3','112833729','Aswin',88272,5,2,-7.9735,112.656,'active','2019-04-01 21:01:44','2019-04-01 21:01:44',NULL),(4,26,'Kakak','Jl. Sawojajar Malang','9784546484349455','085649758649','','1991-04-05 00:00:00','Male','fis','SMP','S2','6797848754648','Kakak',0,0,0,-7.9735,112.656,'active','2019-04-04 22:16:48','2019-04-04 22:16:48','Saya sangat menyenangi petualangan'),(5,27,'Kakak','Jl. Sengkaling Malang','8497685784649584','085467958468','','1995-04-06 00:00:00','Male','mat','SMP','S2','649784648468','Kaka',0,0,0,-7.9159,112.587,'active','2019-04-04 22:19:09','2019-04-04 22:19:09','Saya suka makan');
/*!40000 ALTER TABLE `tentors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `token`
--

DROP TABLE IF EXISTS `token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `token` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `expo_token` varchar(100) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  KEY `ix_token_created_at` (`created_at`),
  KEY `ix_token_updated_at` (`updated_at`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `token`
--

LOCK TABLES `token` WRITE;
/*!40000 ALTER TABLE `token` DISABLE KEYS */;
/*!40000 ALTER TABLE `token` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `topups`
--

DROP TABLE IF EXISTS `topups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `topups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_murid` int(11) DEFAULT NULL,
  `nominal` int(11) DEFAULT NULL,
  `metode_pembayaran` varchar(50) DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `ix_topups_created_at` (`created_at`),
  KEY `ix_topups_updated_at` (`updated_at`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `topups`
--

LOCK TABLES `topups` WRITE;
/*!40000 ALTER TABLE `topups` DISABLE KEYS */;
INSERT INTO `topups` VALUES (1,11,200000,'transfer','ok','2019-04-01 12:05:02','2019-04-04 22:24:30'),(2,11,100000,'cash','ok','2019-04-01 12:35:48','2019-04-04 22:24:33'),(3,11,100000,'cash','ok','2019-04-01 12:40:09','2019-04-02 11:43:16'),(4,11,200000,'transfer','ok','2019-04-01 15:03:50','2019-04-02 11:44:01'),(5,11,200000,'transfer','ok','2019-04-01 15:29:39','2019-04-02 11:44:06'),(6,11,200000,'transfer','ok','2019-04-01 15:29:47','2019-04-05 15:23:22'),(7,11,100000,'credit','ok','2019-04-01 16:08:43','2019-04-05 15:24:01'),(8,11,500000,'cash','waiting','2019-04-04 00:17:11','2019-04-04 00:17:11');
/*!40000 ALTER TABLE `topups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) DEFAULT NULL,
  `password` varchar(50) DEFAULT NULL,
  `tipe` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (11,'Aswindanu','75dcb017b161160a193f9a38dbbc6edb','client'),(12,'Aswinda','75dcb017b161160a193f9a38dbbc6edb','bank'),(13,'Blabla','75dcb017b161160a193f9a38dbbc6edb','tentor'),(14,'Test','6428310f1de8a7c760664a8b110c3160','client'),(15,'Aswind','75dcb017b161160a193f9a38dbbc6edb','admin'),(16,'Aswindasaaasasnupsdsad','75dcb017b161160a193f9a38dbbc6edb','client'),(17,'Aswindaas','75dcb017b161160a193f9a38dbbc6edb','tentor'),(18,'Aswin','75dcb017b161160a193f9a38dbbc6edb','tentor'),(19,'Luisa','2ac9cb7dc02b3c0083eb70898e549b63','client'),(20,'Kaki','75dcb017b161160a193f9a38dbbc6edb','client'),(21,'Kakik','75dcb017b161160a193f9a38dbbc6edb','client'),(22,'Kakiku','75dcb017b161160a193f9a38dbbc6edb','tentor'),(23,'Kakika','75dcb017b161160a193f9a38dbbc6edb','tentor'),(24,'Kakikak','75dcb017b161160a193f9a38dbbc6edb','tentor'),(25,'Kakikaku','75dcb017b161160a193f9a38dbbc6edb','tentor'),(26,'Kakikuka','75dcb017b161160a193f9a38dbbc6edb','tentor'),(27,'Kakiki','75dcb017b161160a193f9a38dbbc6edb','tentor');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-04-07 13:33:11
