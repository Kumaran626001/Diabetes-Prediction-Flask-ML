-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Jan 08, 2025 at 02:55 PM
-- Server version: 8.0.31
-- PHP Version: 8.0.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `disease_diagonsis`
--

-- --------------------------------------------------------

--
-- Table structure for table `registration`
--

DROP TABLE IF EXISTS `registration`;
CREATE TABLE IF NOT EXISTS `registration` (
  `name` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `dob` varchar(10) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `blood_group` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `phone_no` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `username` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`username`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `registration`
--

INSERT INTO `registration` (`name`, `dob`, `blood_group`, `phone_no`, `username`, `password`) VALUES
('jdh', '2025-01-31', 'o+', '7262726282', 'admin', 'admin'),
('mars', '2005-02-04', 'o+', '8608661287', 'mars', '1234'),
('Kumaran', '16-12-2004', 'O+ve', '8300299793', 'kumar', '1234'),
('Kumaran.M', '2020-10-09', 'AB+', '8300299793', 'kumaran', '8555');

-- --------------------------------------------------------

--
-- Table structure for table `result`
--

DROP TABLE IF EXISTS `result`;
CREATE TABLE IF NOT EXISTS `result` (
  `name` varchar(50) COLLATE utf8mb4_general_ci NOT NULL,
  `gender` varchar(20) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `age` int DEFAULT NULL,
  `hypertension` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `heart_disease` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `smoking` varchar(50) COLLATE utf8mb4_general_ci DEFAULT NULL,
  `bmi` double DEFAULT NULL,
  `haemoglobin` double DEFAULT NULL,
  `glucose` double DEFAULT NULL,
  `result` varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `result`
--

INSERT INTO `result` (`name`, `gender`, `age`, `hypertension`, `heart_disease`, `smoking`, `bmi`, `haemoglobin`, `glucose`, `result`) VALUES
('kumar', 'male', 11, 'no', 'yes', 'no info', 23, 3, 333, 'Negative'),
('Kumaran', 'male', 58, 'no', 'no', 'never', 100, 5, 200, 'Negative'),
('Mani', 'male', 11, 'yes', 'no', 'no info', 12, 13, 14, 'Negative'),
('mars', 'female', 20, 'yes', 'no', 'never', 40, 20, 56, 'Positive'),
('Kumaran.M', 'male', 19, 'no', 'yes', 'never', 16, 8, 100, 'Positive'),
('jdh', 'male', 23, 'no', 'no', 'not current', 345, 234, 122, 'Positive');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
