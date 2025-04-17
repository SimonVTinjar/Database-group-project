-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: 17. Apr, 2025 20:18 PM
-- Tjener-versjon: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `food_delivery`
--

-- --------------------------------------------------------

--
-- Tabellstruktur for tabell `menu`
--

CREATE TABLE `menu` (
  `menuID` varchar(10) NOT NULL,
  `menuName` varchar(100) DEFAULT NULL,
  `restaurantID` int(11) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dataark for tabell `menu`
--

INSERT INTO `menu` (`menuID`, `menuName`, `restaurantID`, `price`, `description`) VALUES
('m1', 'Pizza Deal', 1, 199.00, 'Pizza + drikke'),
('m2', 'Burger Combo', 2, 149.00, 'Burger + fries + drikke');

-- --------------------------------------------------------

--
-- Tabellstruktur for tabell `menuitem`
--

CREATE TABLE `menuitem` (
  `menuID` varchar(10) NOT NULL,
  `productID` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dataark for tabell `menuitem`
--

INSERT INTO `menuitem` (`menuID`, `productID`) VALUES
('m1', 'p1'),
('m1', 'p2'),
('m2', 'p1'),
('m2', 'p2'),
('m2', 'p3'),
('m2', 'p4');

-- --------------------------------------------------------

--
-- Tabellstruktur for tabell `product`
--

CREATE TABLE `product` (
  `productID` varchar(10) NOT NULL,
  `name` varchar(100) NOT NULL,
  `type` varchar(50) DEFAULT NULL,
  `description` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dataark for tabell `product`
--

INSERT INTO `product` (`productID`, `name`, `type`, `description`) VALUES
('p1', 'Ham Pizza', 'Mat', 'Pizza med ost og skinke'),
('p2', 'Coca-Cola', 'Drikke', 'Brus'),
('p3', 'Cheeseburger', 'Mat', 'Burger med ost'),
('p4', 'Pommes frites', 'Mat', 'Sprø poteter');

-- --------------------------------------------------------

--
-- Tabellstruktur for tabell `restaurant`
--

CREATE TABLE `restaurant` (
  `restaurantID` int(11) NOT NULL,
  `rName` varchar(100) NOT NULL,
  `address` varchar(200) DEFAULT NULL,
  `phoneNr` varchar(20) DEFAULT NULL,
  `openingTime` time DEFAULT NULL,
  `closingTime` time DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dataark for tabell `restaurant`
--

INSERT INTO `restaurant` (`restaurantID`, `rName`, `address`, `phoneNr`, `openingTime`, `closingTime`) VALUES
(1, 'PizzaHuset', 'Pizzaveien 1', '12345678', '10:00:00', '22:00:00'),
(2, 'BurgerKing', 'Burgergata 2', '87654321', '11:00:00', '23:00:00'),
(3, '1', 'da', 'sda', '10:00:00', '22:00:00');

-- --------------------------------------------------------

--
-- Tabellstruktur for tabell `restaurant_admins`
--

CREATE TABLE `restaurant_admins` (
  `restaurantID` int(11) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dataark for tabell `restaurant_admins`
--

INSERT INTO `restaurant_admins` (`restaurantID`, `user_id`) VALUES
(1, 1),
(1, 2),
(2, 1),
(2, 3),
(3, 1);

-- --------------------------------------------------------

--
-- Tabellstruktur for tabell `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `username` varchar(100) DEFAULT NULL,
  `fname` varchar(100) DEFAULT NULL,
  `lname` varchar(100) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `phoneNr` varchar(12) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dataark for tabell `users`
--

INSERT INTO `users` (`user_id`, `username`, `fname`, `lname`, `address`, `phoneNr`, `email`, `password`) VALUES
(1, 'admin', 'Simon', 'Tinjar', 'Gate 1', '12345678', 'simon@ntnu.no', 'pass123'),
(2, 'pb', 'Lise', 'Pizza', 'Ostepalasset 1', '11111111', 'lise@pizza.no', '1'),
(3, 'bb', 'Jonas', 'Burger', 'Burgerveien 5', '22222222', 'jonas@burger.no', '1');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `menu`
--
ALTER TABLE `menu`
  ADD PRIMARY KEY (`menuID`),
  ADD KEY `restaurantID` (`restaurantID`);

--
-- Indexes for table `menuitem`
--
ALTER TABLE `menuitem`
  ADD PRIMARY KEY (`menuID`,`productID`),
  ADD KEY `productID` (`productID`);

--
-- Indexes for table `product`
--
ALTER TABLE `product`
  ADD PRIMARY KEY (`productID`);

--
-- Indexes for table `restaurant`
--
ALTER TABLE `restaurant`
  ADD PRIMARY KEY (`restaurantID`);

--
-- Indexes for table `restaurant_admins`
--
ALTER TABLE `restaurant_admins`
  ADD PRIMARY KEY (`restaurantID`,`user_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `restaurant`
--
ALTER TABLE `restaurant`
  MODIFY `restaurantID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Begrensninger for dumpede tabeller
--

--
-- Begrensninger for tabell `menu`
--
ALTER TABLE `menu`
  ADD CONSTRAINT `menu_ibfk_1` FOREIGN KEY (`restaurantID`) REFERENCES `restaurant` (`restaurantID`) ON DELETE CASCADE;

--
-- Begrensninger for tabell `menuitem`
--
ALTER TABLE `menuitem`
  ADD CONSTRAINT `menuitem_ibfk_1` FOREIGN KEY (`menuID`) REFERENCES `menu` (`menuID`) ON DELETE CASCADE,
  ADD CONSTRAINT `menuitem_ibfk_2` FOREIGN KEY (`productID`) REFERENCES `product` (`productID`) ON DELETE CASCADE;

--
-- Begrensninger for tabell `restaurant_admins`
--
ALTER TABLE `restaurant_admins`
  ADD CONSTRAINT `restaurant_admins_ibfk_1` FOREIGN KEY (`restaurantID`) REFERENCES `restaurant` (`restaurantID`) ON DELETE CASCADE,
  ADD CONSTRAINT `restaurant_admins_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
