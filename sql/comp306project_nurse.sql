-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: comp306project
-- ------------------------------------------------------
-- Server version	8.0.35

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
-- Table structure for table `nurse`
--

DROP TABLE IF EXISTS `nurse`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `nurse` (
  `EmployeeId` int NOT NULL,
  PRIMARY KEY (`EmployeeId`),
  CONSTRAINT `nurse_ibfk_1` FOREIGN KEY (`EmployeeId`) REFERENCES `employee` (`EmployeeId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `nurse`
--

LOCK TABLES `nurse` WRITE;
/*!40000 ALTER TABLE `nurse` DISABLE KEYS */;
INSERT INTO `nurse` VALUES (10477),(11270),(11746),(12365),(12372),(13003),(13936),(17369),(23266),(23541),(25938),(30363),(31292),(34745),(36821),(38279),(41960),(43194),(45508),(47260),(48096),(49025),(50551),(52577),(54001),(54408),(54677),(57363),(58254),(62806),(63527),(78363),(80815),(81522),(81844),(81976),(84099),(86042),(88744),(93076),(93440),(95228),(96253),(97752),(97855),(98171),(98686),(106524),(111951),(114572),(115090),(116652),(116867),(117034),(118546),(119298),(125673),(130631),(132013),(132620),(133333),(138897),(139509),(141072),(149793),(150768),(152243),(154494),(156607),(158707),(160980),(165816),(166931),(169913),(171268),(175553),(177993),(178312),(179274),(180069),(180146),(180247),(183077),(183514),(184416),(186347),(189078),(192653),(196770),(198083),(199086),(200913),(200932),(202537),(203597),(204592),(215203),(220180),(225329),(228601),(229035),(229329),(230512),(232724),(236587),(236750),(247384),(247891),(252042),(254596),(254755),(257279),(257366),(261728),(266347),(270334),(272099),(272589),(279743),(281091),(286961),(290125),(290406),(292111),(293116),(293210),(295420),(296757),(299392),(302481),(306779),(307659),(309796),(309868),(310854),(311559),(311671),(312409),(314625),(318683),(320563),(321338),(322795),(330135),(334296),(334977),(335331),(338170),(338484),(342014),(342015),(345702),(346120),(346142),(346519),(347207),(348134),(348457),(349082),(350484),(350780),(351432),(353127),(355300),(356277),(357399),(359297),(359428),(362416),(366904),(368693),(370064),(373196),(379410),(379642),(382617),(387219),(391714),(395891),(398276),(398772),(402583),(402740),(406967),(407162),(407492),(416250),(416407),(419316),(422277),(427839),(430023),(430395),(431642),(432191),(432240),(433340),(435582),(435738),(436869),(437130),(437733),(438507),(439523),(442413),(445216),(446395),(449990),(450245),(450748),(454470),(455600),(455797),(455902),(458867),(459151),(462625),(465310),(470844),(471273),(471794),(472535),(472878),(479714),(484174),(484467),(484909),(488718),(501404),(502022),(505360),(506641),(510756),(512351),(512567),(512856),(512954),(513289),(513630),(515153),(515219),(520540),(522168),(522810),(524716),(525275),(527285),(528501),(530379),(531311),(531800),(532005),(532277),(533706),(535209),(536357),(539484),(542519),(547926),(548347),(550707),(551446),(552286),(553253),(554801),(559465),(561337),(563030),(566015),(568328),(571375),(582261),(582299),(582322),(586932),(587827),(597194),(600032),(600788),(603473),(604578),(605182),(608000),(611849),(613872),(615997),(616755),(619110),(620559),(621924),(623065),(628746),(634337),(638223),(645177),(645809),(646787),(652949),(660224),(664203),(667225),(671272),(673020),(677353),(677935),(678907),(680118),(685022),(688271),(689733),(693746),(693750),(694366),(694842),(696543),(696584),(698412),(699209),(705152),(709808),(712936),(713428),(714098),(716328),(724856),(726590),(729295),(730747),(731119),(733250),(734020),(736509),(740528),(741177),(741282),(742408),(744413),(747254),(747798),(748073),(749696),(750377),(752911),(753487),(755279),(756919),(757375),(759270),(759517),(760943),(762794),(764266),(767267),(767745),(773250),(773542),(776371),(781613),(783697),(783730),(785139),(786310),(788017),(792504),(794938),(795853),(797971),(798656),(800685),(804707),(806614),(808613),(811673),(814440),(821142),(825976),(827305),(827733),(833839),(841524),(844131),(846342),(847323),(848535),(852509),(854983),(856058),(860015),(861454),(864896),(865706),(866039),(868802),(870981),(871014),(878652),(879070),(879476),(880163),(880328),(880472),(882880),(884090),(891652),(891677),(897415),(903270),(904260),(908496),(912992),(915355),(918745),(923794),(931347),(931816),(935913),(938196),(942493),(942532),(944129),(944716),(945544),(946393),(947333),(947461),(950169),(950782),(955575),(955599),(961324),(962525),(965919),(966277),(966927),(969833),(975393),(976349),(980203),(984321),(986644),(987783),(990009),(995237),(995529);
/*!40000 ALTER TABLE `nurse` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-01-20  1:16:34
