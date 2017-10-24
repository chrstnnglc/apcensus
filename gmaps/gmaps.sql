-- phpMyAdmin SQL Dump
-- version 4.6.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 07, 2017 at 09:05 AM
-- Server version: 5.7.14
-- PHP Version: 5.6.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `gmaps`
--

-- --------------------------------------------------------

--
-- Table structure for table `aps`
--

CREATE TABLE `aps` (
  `id` int(11) NOT NULL,
  `ssid` varchar(60) NOT NULL,
  `mac` varchar(80) NOT NULL,
  `isp` varchar(60) NOT NULL,
  `lat` float(10,6) NOT NULL,
  `lng` float(10,6) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `aps`
--

INSERT INTO `aps` (`id`, `ssid`, `mac`, `isp`, `lat`, `lng`) VALUES
(1, 'test1', '00-01-02-03-04-05', 'glowb', 14.676908, 121.043861),
(2, 'hulaan_mo_password', '1A-2B-3C-4D-5E-6F', 'pldc', 14.676308, 121.044861),
(3, 'test2', '00-00-00-00-00-01', 'pldc', 14.676728, 121.043869),
(4, 'test3', '00-00-00-00-00-02', 'pldc', 14.676428, 121.043869),
(5, 'test3', '00-00-00-00-00-02', 'pldc', 14.676748, 121.043671),
(7, 'test3', '00-00-00-00-00-02', 'pldc', 14.676428, 121.043968),
(8, 'test3', '00-00-00-00-00-02', 'pldc', 14.676638, 121.043648),
(9, 'test3', '00-00-00-00-00-02', 'pldc', 14.676518, 121.043877),
(10, 'test', '00-00-00-00-00-00', 'pldc', 14.675143, 121.041916),
(11, 'test', '00-00-00-00-00-00', 'pldc', 14.675309, 121.042046),
(12, 'test', '00-00-00-00-00-00', 'pldc', 14.674671, 121.041901),
(13, 'test', '00-00-00-00-00-00', 'pldc', 14.674723, 121.041992),
(14, 'test', '00-00-00-00-00-00', 'pldc', 14.675081, 121.041466),
(15, 'test', '00-00-00-00-00-00', 'glowb', 14.674910, 121.041466),
(16, 'test', '00-00-00-00-00-00', 'glowb', 14.675024, 121.041649),
(17, 'test', '00-00-00-00-00-00', 'glowb', 14.674754, 121.041618),
(18, 'test', '00-00-00-00-00-00', 'glowb', 14.675044, 121.041992);

-- --------------------------------------------------------

--
-- Table structure for table `markers`
--

CREATE TABLE `markers` (
  `id` int(11) NOT NULL,
  `name` varchar(60) NOT NULL,
  `address` varchar(80) NOT NULL,
  `lat` float(10,6) NOT NULL,
  `lng` float(10,6) NOT NULL,
  `type` varchar(30) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `markers`
--

INSERT INTO `markers` (`id`, `name`, `address`, `lat`, `lng`, `type`) VALUES
(1, 'Love.Fish', '580 Darling Street, Rozelle, NSW', -33.861034, 151.171936, 'restaurant'),
(2, 'Young Henrys', '76 Wilford Street, Newtown, NSW', -33.898113, 151.174469, 'bar'),
(3, 'Hunter Gatherer', 'Greenwood Plaza, 36 Blue St, North Sydney NSW', -33.840282, 151.207474, 'bar'),
(4, 'The Potting Shed', '7A, 2 Huntley Street, Alexandria, NSW', -33.910751, 151.194168, 'bar'),
(5, 'Nomad', '16 Foster Street, Surry Hills, NSW', -33.879917, 151.210449, 'bar'),
(6, 'Three Blue Ducks', '43 Macpherson Street, Bronte, NSW', -33.906357, 151.263763, 'restaurant'),
(7, 'Single Origin Roasters', '60-64 Reservoir Street, Surry Hills, NSW', -33.881123, 151.209656, 'restaurant'),
(8, 'Red Lantern', '60 Riley Street, Darlinghurst, NSW', -33.874737, 151.215530, 'restaurant'),
(9, 'Test', 'QC', 14.676208, 121.043861, 'bar'),
(10, 'Test 2', 'QC', 14.676908, 121.043861, 'restaurant');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `aps`
--
ALTER TABLE `aps`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `markers`
--
ALTER TABLE `markers`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `aps`
--
ALTER TABLE `aps`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;
--
-- AUTO_INCREMENT for table `markers`
--
ALTER TABLE `markers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
